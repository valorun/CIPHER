from collections import deque
from cipher.model import db

# Contains chat history.
# Used to keep track of a conversion even if the leave the chat page.
chat_queue = deque(maxlen=30)
