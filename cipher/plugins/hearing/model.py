from collections import deque

# Contains chat history.
# Used to keep track of a conversion even if user leaves the chat page.
chat_queue = deque(maxlen=30)
