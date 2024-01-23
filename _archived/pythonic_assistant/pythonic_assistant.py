"""
Author: Julius Stener
Created: 12/3/23
Description: This file handles the execution of an assistants functions.
"""

# imports
import time
from pythonic_assistant.openai_wrappers.assistants_wrapper import AssistantsWrapper
from pythonic_assistant.openai_wrappers.threads_wrapper import ThreadsWrapper
from pythonic_assistant.openai_wrappers.runs_wrapper import RunsWrapper
from openai import OpenAI

# load the environment variables
from dotenv import load_dotenv
load_dotenv()

# import the log
from _log.log import Log
log = Log(log_name=__name__)

# establish the client
client = OpenAI()

TERMINAL_STATUS = ['expired', 'completed', 'failed', 'cancelled']
WORKING_STATUS = ['queued', 'in_progress', 'cancelling']
ACTION_STATUS = ['requires_action']

class PythonicAssistant():
  """
  PythonicAssistant contains the execution management for an Assistant.
  """

  def __init__(self, **kwargs):
    """
    Initialize the PythonicAssistant class
    """
    self.assistant = AssistantsWrapper(client, **kwargs)
    self.thread = ThreadsWrapper(client, **kwargs)

    # self.tool(self.create_tool)

  def handle_kwargs(self, **kwargs):
    """
    Manage all the kwargs for the PythonicAssistant in one function
    """

  def execute(self, 
              messages: list, 
              wait: int = 1,
              as_list=False,
              **kwargs
              ):
    """
    Run the assistant
    """
    
    self.thread.add_messages(messages)
    self.run = RunsWrapper(
      self.assistant.get_id(),
      self.thread.get_id(),
      client, 
      **kwargs)

    while (status := self.run.get_status()) not in TERMINAL_STATUS:
      log.debug(f"STATUS UPDATE\n\t- Run: {self.run.get_id()}\n\t- Status: {status}")
      if status in WORKING_STATUS:
        pass # do_nothing -> continue waiting
      elif status in ACTION_STATUS:
        self.function_calling()
      else:
        log.error(f"Returned Status Incorrect: {status}")

      time.sleep(wait)
      
    log.debug(f"STATUS UPDATE\n\t- Run: {self.run.get_id}\n\t- Status: {status}")
    response = self.thread.list_messages(as_list=as_list)
    
    return response

  def function_calling(self, **kwargs):
    """
    Call the required functions and return their answer 
    """
    # get all the functions that need to be run from runs_wrapper
    tools = self.run.get_required_tools()

    # match the associated funcs from assistants_wrapper
    for tool in tools:
      tool['func'] = self.assistant.get_tool(tool['func_name'])
      self.run.run_function(tool)

  def tool(self, func):
    """Decorator for registering a tool"""
    self.assistant.add_tool(func)
    return func
  
  def create_tool(self, 
               tool_name: str,
               description: str,
               parameters: str,
               required_parameters: str,
               return_var: str,
               tool_code: str,
               package_requirements: list
               ):
    """
    Adds a tool that the assistant will be able to use in the future.
    
    Paramters:
    ----------
    tool_name : str
        The name of the tool.
    description : str
        The description of the tool.
    parameters : str
        The JSON representation of the parameters. The format MUST FOLLOW
        the following formats:
        Example with 2 variables, 'location' and 'unit':
        {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
          "unit": {"type": "string", "enum": ["c", "f"]}
        }
        Example with 1 variable, 'location':
        {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"}
        }
        Example with 0 variables:
        {}
    required_parameters : list
        A list of the names of the required variables (e.g. those without
        default values)
    return_var : str
        The value that the tool is meant to return. For example, if the
        tool is meant to add two variable, 'a' and 'b', together, the code
        would be:
          c = a + b
        and the 'return_var' would be 'c'. If multiple values need to be
        returned, then the result should be packed into a dict and saved
        as one variable.
    tool_code : str
        The code for the tool. This code should be in python3.10 or greater,
        should be written to run as is. The following are examples of tool
        implementations.

        Example with basic implementation of an addition tool:
          c = a + b.
        Example of a tool that makes use of a function:
          def foo(a: str):
            return a + " Hello World"
          c = foo(a)
        Example of a tool that returns multiple variables as a dict:
          def foo():
            return 0
          def bar():
            return 1
          c = {'result_1': foo(), 'result_2': bar()}
    package_requirements: list
        A list of all the python packages that are required to execute
        the tool code successfully. This list can be empty if there are no
        package requirements.
          
    Returns:
    --------
    bool
        True if successful, False if unsuccessful

    Raises:
    -------

    """

    def func(**kwargs):
      loc = {'kwargs':kwargs}
      exec(tool_code, {}, loc)
      return loc[return_var]
    
    self.assistant.add_tool_from_gpt(
      tool_name,
      description,
      parameters,
      required_parameters,
      func
    )
    
    return True