"""
Author: Julius Stener
Date: 12/23/23
Description: This file should be thought of as a wrapper for the OpenAI API.
    This file does not contain any execution.
"""

# imports
import json

# import the log
from _log.log import Log
log = Log(log_name=__name__)


class RunsWrapper():
    """
    RunsWrapper serves as a clean way to interact with the OpenAI Runs API.
    """

    def __init__(self, assistant_id, thread_id, client, **kwargs):
        """
        Initializes the RunsWrapper class
        """
        self.client = client

        self.run = self.client.beta.threads.runs.create(
            thread_id = thread_id,
            assistant_id = assistant_id
        )
        log.info(f"Started Run: {self.run.id}\n\t- Thread: {thread_id} \
                 \n\t- Assistant: {assistant_id}")

    def handle_kwargs(self, **kwargs):
        """
        Manage all the kwargs for the Runs APIs in one function
        """
        pass

    def get_id(self):
        """
        Returns the run id
        """
        return self.run.id

    def cancel(self):
        """
        Cancel the run mid-execution
        """
        self.run = self.client.beta.threads.runs.cancel(
            thread_id = self.run.thread_id,
            run_id = self.run.id
        )
        log.info(f"Cancelled Run: {self.run.id}")

    def get_status(self):
        """
        Returns the status of the Run.
        """
        self.run = self.client.beta.threads.runs.retrieve(
            thread_id = self.run.thread_id,
            run_id = self.run.id
        )
        log.info(f"Run <{self.run.id}> Status: {self.run.status}")
        return self.run.status
    
    def get_required_tools(self):
        """
        Returns the required tools by name with their associated tool_call_id
            in a dictionary. An empty list is returned if there are no 
            required tools. Note that this function does not check for an 
            updated status from the OpenAI API.
        """
        output = []
        if self.run.status != 'requires_action':
            log.critical(f"Incorrectly called 'get_required_tools' \
                          on Run: {self.run.id}")
            return output
        for tc in self.run.required_action.submit_tool_outputs.tool_calls:
            output.append({
                'tool_call_id': tc.id,
                'func_name': tc.function.name,
                'func': None,
                'arguments': tc.function.arguments
                }
            )
        return output
    
    def run_function(self, tool_call: dict):
        """
        Executes the function specified by the Run and returns the value to
            the Assistant Run. The tool_dict should be in the format below:
                {
                'tool_call_id': str,
                'func_name': str,
                'func': function,
                'arguments': dict
                }
        """
        func = tool_call['func']
        arguments = json.loads(tool_call['arguments'])

        log.info(f"Attempting to Run Func: {tool_call['func_name']}")

        try:
            output = func(**arguments)
        except Exception as e:
            log.critical(f"Failed Function Call - Function: {tool_call['func_name']}")
            output = f"The function call caused the following exception:\n {e}"

        self.run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id = self.run.thread_id,
            run_id = self.run.id,
            tool_outputs = [
                {
                'tool_call_id': tool_call['tool_call_id'],
                'output': output
                }
            ]
        )
        
