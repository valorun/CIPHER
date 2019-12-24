import logging
from flask_socketio import SocketIO
from cipher import socketio
from .actions import Action


class PauseAction(Action):
    """
    Pause the executed sequence
    """
    def __init__(self, time: int):
        self.time = time

    def execute(self, **kwargs):
        socketio.sleep(self.time / 1000)


class Node:
    def __init__(self, action: Action, children=[]):
        self.action = action
        self.children = children
        self.inExecution = False

    def execute(self, **kwargs):
        self.inExecution = True
        result = self.action.execute(**kwargs)
        if result is False:
            # if conditions aren't achieved, or the code is incorrect
            return
        for c in self.children:
            socketio.start_background_task(c.execute, **kwargs)
        self.inExecution = False

    def isInExecution(self):
        """
        Check if the sequence is currently in execution.
        """
        return any([(self.inExecution or c.isInExecution()) for c in self.children])


class Sequence:
    def __init__(self, startNodes: list):
        self.startNodes = startNodes

    def execute(self, **kwargs):
        """
        Launch the sequence execution, place each new branch in another thread.
        """
        for n in self.startNodes:
            n.execute(**kwargs)

    def inExecution(self):
        """
        Check if the sequence is currently in execution.
        """
        return any([n.isInExecution() for n in self.startNodes])

