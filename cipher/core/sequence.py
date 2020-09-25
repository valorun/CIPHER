from flask_socketio import SocketIO
from cipher import socketio
from .actions import Action

class Node:
    def __init__(self, action: Action, action_parameters: dict, transitions: list = []):
        self.action = action
        self.action_parameters = action_parameters
        self.transitions = transitions
        self.in_execution = False

    def execute(self):
        self.in_execution = True
        if self.action is not None:
            result = self.action.execute(**self.action_parameters)
            if result is False:
                # if conditions aren't achieved, or the code is incorrect
                return
        for t in self.transitions:
            socketio.start_background_task(t.execute)
        self.in_execution = False

    def is_in_execution(self):
        """
        Check if the sequence is currently in execution.
        """
        return self.in_execution or any([t.is_in_execution() for t in self.transitions])


class Transition:
    def __init__(self, target: Node, time: int):
        self.target = target
        self.time = time
        self.in_execution = False

    def execute(self):
        self.in_execution = True
        socketio.sleep(self.time / 1000)
        self.target.execute()
        self.in_execution = False
    
    def is_in_execution(self):
        """
        Check if the sequence is currently in execution.
        """
        return self.in_execution or self.target.is_in_execution()

class Sequence:
    def __init__(self, start_transitions: list):
        self.start_transitions = start_transitions

    def execute(self):
        """
        Launch the sequence execution, place each new branch in another thread.
        """
        for t in self.start_transitions:
            socketio.start_background_task(t.execute)

    def is_in_execution(self):
        """
        Check if the sequence is currently in execution.
        """
        return any([t.is_in_execution() for t in self.start_transitions])
