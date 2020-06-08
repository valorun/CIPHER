import logging
from flask_socketio import SocketIO
from cipher import socketio
from .actions import Action, DEFAULT_ACTIONS
from .action_parameters import IntegerParameter

class PauseAction(Action):
    """
    Pause the executed sequence
    """
    display_name = 'Pause'

    @staticmethod
    def get_parameters():
        return [IntegerParameter('time', 'Temps(ms)')]

    @staticmethod
    def check_parameters(time: int):
        if not isinstance(time, int):
            return False, "The pause time must be an integer."
        return True, None

    @staticmethod
    def execute(time: int):
        socketio.sleep(time / 1000)

DEFAULT_ACTIONS['pause'] = PauseAction

class Node:
    def __init__(self, action: Action, action_parameters: dict, children=[]):
        self.action = action
        self.action_parameters = action_parameters
        self.children = children
        self.in_execution = False

    def execute(self):
        self.in_execution = True
        result = self.action.execute(**self.action_parameters)
        if result is False:
            # if conditions aren't achieved, or the code is incorrect
            return
        for c in self.children:
            socketio.start_background_task(c.execute)
        self.in_execution = False

    def is_in_execution(self):
        """
        Check if the sequence is currently in execution.
        """
        return any([(self.in_execution or c.is_in_execution()) for c in self.children])


class Sequence:
    def __init__(self, start_nodes: list):
        self.start_nodes = start_nodes

    def execute(self):
        """
        Launch the sequence execution, place each new branch in another thread.
        """
        for n in self.start_nodes:
            n.execute()

    def is_in_execution(self):
        """
        Check if the sequence is currently in execution.
        """
        return any([n.is_in_execution() for n in self.start_nodes])
