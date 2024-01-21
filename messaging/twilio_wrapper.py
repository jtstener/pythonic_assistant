"""
File: twilio_wrapper.py
Author: Julius Stener
"""

# imports
from twilio.rest import Client

# load the environment variables
from dotenv import load_dotenv
load_dotenv()

# import the log
from _log.log import Log
log = Log(log_name=__name__)

class TwilioWrapper():
    """
    Twilio API Wrapper
    """

    def __init__(self, **kwargs):
        """
        __init__ for the Twillio class
        """
        self.client = Client()

    def send_message(self, msg):

        message = self.client.messages.create(
        from_='+12144756041',
        body=msg,
        to='+12144756041'
        )


