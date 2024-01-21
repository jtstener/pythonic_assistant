# imports
from openai import OpenAI
import json
import inspect

# load the environment variables
from dotenv import load_dotenv
load_dotenv()

# constants
FC_EXAMPLES = [
  'function_calling_examples/fc_example_1.json',
  'function_calling_examples/fc_example_2.json'
  ]

# @assistant.tool
def foo():
  """Get today's date"""
  return 0

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


def list_assistants():
  client = OpenAI()
  my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
  )
  print(my_assistants)

def delete_assistants():
  client = OpenAI()
  my_assistants = client.beta.assistants.list(
    order="desc",
  )
  for assistant in my_assistants.data:
    client.beta.assistants.delete(assistant.id)

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

delete_assistants()
list_assistants()
