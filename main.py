# imports
from pythonic_assistant.pythonic_assistant import PythonicAssistant
import json
import inspect
# from messaging.twilio_wrapper import TwilioWrapper

name = "General Assistant"
description = "You are a general assistant. Use the functions provided to follow the directions of the user."
instructions = "Please address the user as Jane Doe. The user has a premium account."


assistant = PythonicAssistant(
    name = name,
    description = description,
    instructions = instructions
)


# @assistant.tool
def addition(a, b=3):
  """
  addition adds two numbers together.

  Parameters
  ----------
  a : int
      The first number
  b : int, optional
      The second number

  Returns
  -------
  int
      the int addition of 'a' and 'b'

  Raises
  ------
  """
  return a + b

@assistant.tool
def get_weather():
  """
  Provides the most recent weather forecast.

  Parameters
  ----------

  Returns
  -------
  string
      the current weather

  Raises
  ------
  """
  return "High 81, Low of 72, Sunny with a whispy clouds"

messages = [
    {
      'role': 'user',
      'content': 'What is the weather today?'
    }
  ]

response = assistant.execute(messages, as_list=True)

def pretty_print(response):
  for msg in response:
    print(f"{msg['role']}: {msg['content']}")

pretty_print(response)