import json
import ollama
from . import hearing
from .model import chat_queue
from .tools import AVAILABLE_TOOLS
from flask_socketio import SocketIO, emit
from datetime import datetime as dt
from cipher import socketio, mqtt, config
from cipher.core.sequence_reader import sequence_reader
from cipher.model import Sequence, db
from cipher.core.actions import DEFAULT_ACTIONS, CUSTOM_ACTIONS

def call_llm(messages: list, tools: list):
    response = ollama.chat(
        model=config.core_config.LLM_MODEL, 
        messages=messages, 
        tools=tools
    )
    return response.message

@hearing.startup()
def on_startup():
    mqtt.subscribe('client/speech/speak')

@mqtt.on_topic('client/speech/speak')
def on_speak(client, userdata, message):
    msg_obj = {'message': json.loads(message.payload.decode('utf-8'))['text'], 'source': 'robot', 'time': dt.now().strftime('%H:%M')}
    chat_queue.append(msg_obj)
    socketio.emit('chat', msg_obj, namespace='/client')

@mqtt.on_topic('server/hearing/transcription')
def handle_transcription(client, userdata, message):
    global chat_queue
    transcript = message.payload.decode('utf-8')
    hearing.log.info("Received transcription: '%s'", transcript)

    msg_obj = {'message': transcript, 'source': 'user', 'time': dt.now().strftime('%H:%M')}
    chat_queue.append(msg_obj)
    socketio.emit('chat', msg_obj, namespace='/client')

    with mqtt.app.app_context():
        sequences = Sequence.query.filter_by(enabled=True).all()
        
        # Call LLM
        robot_name = config.core_config.get_robot_name()
        system_prompt = config.core_config.get_llm_system_prompt().format(robot_name=robot_name)
        
        llm_messages = [{"role": "system", "content": system_prompt}]
        for msg in chat_queue:
            role = "user" if msg["source"] == "user" else "assistant"
            llm_messages.append({"role": role, "content": msg["message"]})
            
        tools = []
        sequence_map = {}
        for s in sequences:
            # Create a safe name for the tool (alphanumeric and underscores only)
            safe_name = "sequence_" + "".join(c if c.isalnum() else "_" for c in str(s.id))
            sequence_map[safe_name] = s.id
            desc = s.description.strip() if s.description else f"Execute sequence {s.id}"
            
            tools.append({
                "type": "function",
                "function": {
                    "name": safe_name,
                    "description": desc,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            })

        # Add tools directly using Ollama's native support
        tools.extend(AVAILABLE_TOOLS)
        
        response = call_llm(llm_messages, tools)
        print(tools)
        
        # Determine if we need to call LLM again with tool results
        needs_second_call = False
        
        if response.tool_calls:
            print(response)
            for call in response.tool_calls:
                if call.function.name == "speech":
                    text = call.function.arguments.get("text")
                    if text:
                        # Handle speech
                        mqtt.publish('client/speech/speak', json.dumps({'text': text}).encode('utf-8'))
                elif call.function.name in sequence_map:
                    original_id = sequence_map[call.function.name]
                    hearing.log.info("LLM requested sequence execution: %s", original_id)
                    sequence_reader.launch_sequence(original_id)
                else:
                    # Check if it's a python tool
                    tool_func = next((f for f in AVAILABLE_TOOLS if f.__name__ == call.function.name), None)
                    if tool_func:
                        # Extract arguments safely
                        kwargs = call.function.arguments or {}
                        try:
                            result = tool_func(**kwargs)
                        except Exception as e:
                            hearing.log.error("Error executing tool %s: %s", call.function.name, str(e))
                            result = f"Erreur lors de l'exécution: {str(e)}"
                            
                        # Format the tool calls list as expected by ollama (list of dicts)
                        formatted_tool_calls = []
                        for tc in response.tool_calls:
                            formatted_tool_calls.append({
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            })
                            
                        llm_messages.append({"role": "assistant", "content": "", "tool_calls": formatted_tool_calls})
                        llm_messages.append({"role": "tool", "content": str(result)})
                        needs_second_call = True
                    else:
                        hearing.log.warning("LLM tried to call unknown tool: %s", call.function.name)
        elif response.content:
             # Handle conversational response
             text = response.content
             mqtt.publish('client/speech/speak', json.dumps({'text': text}).encode('utf-8'))
             
        # Second call to LLM if tools provided results
        if needs_second_call:
            final_response = call_llm(llm_messages, tools)
            if final_response.content:
                mqtt.publish('client/speech/speak', json.dumps({'text': final_response.content}).encode('utf-8'))

@socketio.on('start_speech_recognition', namespace='/client')
def start_speech_recognition():
    hearing.log.info("Started speech recognition")
    mqtt.publish('client/hearing/start')

@socketio.on('stop_speech_recognition', namespace='/client')
def stop_speech_recognition():
    hearing.log.info("Stopped speech recognition")
    mqtt.publish('client/hearing/stop')
