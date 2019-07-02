from flask_socketio import SocketIO
from cipher import socketio
from .actions import speech, relay, motion, servo, servo_sequence, sound, script

class Sequence:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        #number of actions in progress, to wait before executing another sequence.
        self.threads = 0

    def _getChildren(self, id):
        """
        Return the list of the child nodes.
        """
        children=[]
        for e in self.edges:
            if e['from'] == id:
                children.append(e['to'])
        return children

    def _getNodeActionData(self, id):
        """
        Return the action of the node with the given id.
        """
        for n in self.nodes:
            if n['id'] == id:
                if 'action' in n:
                    return n['action']
        return None
    
    def isValid(self):
        """
        Check if the sequence is valid.
        """
        #check if all nodes have at least one parent node
        nonStartNodes = [n for n in self.nodes if n['id'] != 'start']
        for n in nonStartNodes:
            if not any([True for e in self.edges if e['to'] == n['id']]) > 0:
                return False
        #check if all nodes have no edge that is both "to" and "from"
        if len([False for e in self.edges if e['to'] == e['from']]) > 0:
            return False
        #check if the sequence has no cycle
        return not self.containsCycle()

    def _containsCycle(self, nodeId, visited, recStack):
        #mark current node as visited and adds to recursion stack
        visited.append(nodeId)
        recStack.append(nodeId)

        #recur for all neighbours if any neighbour is visited and in recStack then graph is cyclic 
        for neighbour in self._getChildren(nodeId): 
            if neighbour not in visited: 
                if self._containsCycle(neighbour, visited, recStack) == True: 
                    return True
            elif neighbour in recStack: 
                return True

        #the node needs to be poped from recursion stack before function ends 
        recStack.remove(nodeId)
        return False

    def containsCycle(self):
        """
        Check if the sequence contains a cycle.
        """
        visited = []
        recStack = []
        for n in self.nodes: 
            if n['id'] not in visited: 
                if self._containsCycle(n['id'], visited, recStack) == True: 
                    return True
        return False

    def execute(self, startNodeId, **kwargs):
        """
        Launch the sequence execution, place each new branch in another thread.
        """
        self.threads += 1
        result = self.executeNode(startNodeId, **kwargs)
        if result == False:
            # if conditions aren't achieved, or the code is incorrect
            return
        for c in self._getChildren(startNodeId):
            socketio.start_background_task(self.execute, c, **kwargs)
        self.threads -= 1

    def executeNode(self, nodeId, **kwargs):
        """
        Execute an action based on an action data, for exemple 'sleep'.
        """
        actionData = self._getNodeActionData(nodeId)
        if actionData is None:
            return True

        action = actionData['type']

        if action == 'pause':
            #if it's a pause, the executed script is paused
            socketio.sleep( actionData['time']/1000 )
        elif action == 'speech':
            speech(actionData['speech'])
        elif action == 'relay':
            relay(actionData['relay'], actionData['state'])
        elif action == 'script':
            #pass the kwargs to the script (can be altered)
            kwargs = script(actionData['script'], **kwargs)
        elif action == 'sound':
            sound(actionData['sound'])
        elif action == 'motion':
            motion(actionData['direction'], actionData['speed'])
        elif action == 'servo':
            servo(actionData['servo'], actionData['position'], actionData['speed'])
        elif action == 'servo_sequence': #COMPATIBILITY REASON
            servo_sequence(actionData['sequence'])
        elif action == 'condition':
            if 'flags' not in kwargs or actionData['flag'] not in kwargs['flags']:
                #if there is no flag, or the specified flag is missing, stop the execution
                return False
        return True

    
    def inExecution(self):
        """
        Check if the sequence is currently in execution.
        """
        return self.threads > 0