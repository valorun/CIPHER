import json
import uuid
import os
import threading
import queue
import pyaudio
import numpy as np
from . import speech
from .config import voice_config, VOICES_DIR
from cipher import mqtt
from cipher.config import core_config
from cipher.model import resources
from cipher.core.actions import SoundAction
from cipher.core.signals import speech_synthesized

# Lazy loading of TTS
tts = None

def get_tts():
    global tts
    if tts is None:
        from .neutts_lite import NeuTTSLite
        speech.log.info("Loading NeuTTS...")
        tts = NeuTTSLite()
        speech.log.info("NeuTTS loaded.")
    return tts

def _read_if_path(value: str) -> str:
    return open(value, "r", encoding="utf-8").read().strip() if os.path.exists(value) else value

def audio_player_thread(audio_queue, stream, prefill_chunks=0):
    PLAYBACK_CHUNK_BYTES = 2048
    buffer = []

    for _ in range(prefill_chunks):
        chunk = audio_queue.get()
        if chunk is None:
            buffer.append(None)
            break
        buffer.append(chunk)

    for chunk in buffer:
        if chunk is None:
            audio_queue.task_done()
            return
        for i in range(0, len(chunk), PLAYBACK_CHUNK_BYTES):
            stream.write(
                chunk[i : i + PLAYBACK_CHUNK_BYTES], exception_on_underflow=False
            )
        audio_queue.task_done()

    while True:
        audio_bytes = audio_queue.get()
        if audio_bytes is None:
            audio_queue.task_done()
            break

        for i in range(0, len(audio_bytes), PLAYBACK_CHUNK_BYTES):
            slice_bytes = audio_bytes[i : i + PLAYBACK_CHUNK_BYTES]
            stream.write(slice_bytes, exception_on_underflow=False)

        audio_queue.task_done()


@speech.startup()
def on_startup():
    """
    Function called when the server connects to the broker.
    """
    mqtt.subscribe('client/speech/speak')

@speech_synthesized.connect
def on_speak(sender, **kwargs):
    text = kwargs.get('text')
    if not text:
        return
    """
    Function called when the robot needs to speak.
    """
    if voice_config.get_voice() is None:
        speech.log.debug("Trying to speak but, no voice is set")
        return
        
    voice_name = voice_config.get_voice()
    
    ref_audio_path = os.path.join(VOICES_DIR, f"{voice_name}.npy")
    ref_text_path = os.path.join(VOICES_DIR, f"{voice_name}.txt")
    
    if not os.path.exists(ref_audio_path) or not os.path.exists(ref_text_path):
        speech.log.warning(f"Voice files for {voice_name} are missing.")
        return

    try:
        ref_codes = np.load(ref_audio_path, mmap_mode='r')
        ref_text = _read_if_path(ref_text_path)
    except Exception as e:
        speech.log.error(f"Failed to load reference voice {voice_name}: {str(e)}")
        return

    current_tts = get_tts()

    # Streaming is used only when the audio is played locally on the server
    # If it is meant to be sent to a web client, we might want to group it.
    if core_config.get_audio_on_server():
        speech.log.info("Streaming speech generation...")
        
        # Audio setup
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16, channels=1, rate=current_tts.sample_rate, output=True
        )

        audio_queue = queue.Queue()
        player = threading.Thread(target=audio_player_thread, args=(audio_queue, stream))
        player.start()
        
        try:
            for chunk in current_tts.infer_stream(text, ref_codes, ref_text):
                audio = (chunk * 32767).astype(np.int16)
                audio_queue.put(audio.tobytes())

            # Add tail pad
            tail_pad = np.zeros(int(0.25 * current_tts.sample_rate), dtype=np.int16)
            audio_queue.put(tail_pad.tobytes())
            
        except Exception as e:
            speech.log.error(f"Error during TTS generation: {e}")
        finally:
            audio_queue.put(None)
            player.join()
            stream.stop_stream()
            stream.close()
            p.terminate()
            speech.log.info("Finished speaking.")
            
    else:
        # Fallback to generating the full wav to send over socket
        speech.log.info("Generating full speech for client...")
        import soundfile as sf
        
        chunks = []
        try:
            for chunk in current_tts.infer_stream(text, ref_codes, ref_text):
                chunks.append(chunk)
            
            if chunks:
                full_audio = np.concatenate(chunks)
                temp_sound = '.' + str(uuid.uuid4().hex) + '.wav'
                # write wav file for client
                sf.write(resources.get_sound_path(temp_sound), full_audio, current_tts.sample_rate)
                SoundAction.execute(temp_sound)
                # Cleanup would be nice, but SoundAction doesn't provide a hook yet. 
                # Leaving it like this follows previous design or could be improved later.
                
        except Exception as e:
            speech.log.error(f"Error during TTS generation: {e}")

