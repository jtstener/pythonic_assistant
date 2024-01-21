"""
Author: Julius Stener
Date: 12/23/23
Description: This file should be thought of as a wrapper for the OpenAI API.
    This file does not contain any execution.
"""

# imports


# import the log
from _log.log import Log
log = Log(log_name=__name__)

class ThreadsWrapper():
    """
    ThreadsWrapper serves as a clean way to interact with the OpenAI Threads API.
    """

    def __init__(self, client, **kwargs):
        """
        Initializes the ThreadsWrapper class
        """
        self.client = client

        self.thread = client.beta.threads.create()
        log.info(f"Initialized Thread: {self.thread.id}")
        self.latest_msg_id = None
        
    def handle_kwargs(self, **kwargs):
        """
        Manage all the kwargs for the Threads and Messages APIs in one function
        """

    def get_id(self):
        """
        Returns the thread id
        """
        return self.thread.id

    def add_message(self, message: dict):
        """
        Add a message to the thread. 'message' argument should be in the format:
            {
            'role': str,
            'content': str
            }
        """
        thread_msg = self.client.beta.threads.messages.create(
            self.thread.id,
            role = message['role'],
            content = message['content']
        )
        log.info(f"Added Message <{thread_msg.id}> to Thread: {self.thread.id}")

    def add_messages(self, messages: list):
        """
        Add multiple messages, in sequential order.
        """
        for msg in messages:
            self.add_message(msg)

    def remove_message(self):
        """
        Remove a message from the thread
        """
        pass

    def list_messages(self, as_list=False):
        """
        List all the messages in the thread
        """
        messages = self.client.beta.threads.messages.list(self.thread.id)
        if as_list:
            msg_list = []
            for msg in messages.data:
                msg_list.append({'role': msg.role, 'content': msg.content[0].text.value})
            msg_list.reverse()
            return msg_list
        return messages.data

    def retrieve_new_messages(self, record=True):
        """
        Retrieve the latest messages that have not been seen yet
        """
        pass
