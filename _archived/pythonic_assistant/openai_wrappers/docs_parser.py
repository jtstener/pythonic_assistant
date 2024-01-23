"""
Author: Julius Stener
Date: 12/1/23
"""

# imports
import re
import json
import inspect

# constants
JSON_TYPES = {
  "str": "string", 
  "int": "integer",
  "float": "number",
  "dict": "object",
  "list": "array",
  "bool": "boolean",
  "None": "null"
}

FC_EXAMPLES = [
  'pythonic_assistant/openai_wrappers/function_calling_examples/fc_example_1.json',
  'pythonic_assistant/openai_wrappers/function_calling_examples/fc_example_2.json',
  'pythonic_assistant/openai_wrappers/function_calling_examples/fc_example_3.json'
  ]

class DocsParser():

  def __init__(self, client, **kwargs):
    """
    Initializes the parser.
    """
    self.client = client

  def parse(self, func, using_gpt=False):
    """
    Parse a function for function calling
    """
    if using_gpt:
      try:
        return self.parse_gpt(func)
      except Exception as e:
        return {"error": f"{e}"}
      
    # Use the regex parser
    try:
      return self.parse_regex(func)
    except Exception as e:
      pass

    # use the GPT parser
    try:
      return self.parse_gpt(func)
    except Exception as e:
      return {}

  def parse_regex(self, func):
    """
    Parse using regular expressions
    """
    name = func.__name__
    description = str()
    parameters = dict()
    required = list()
    description, parameters, required = self.parse_docs(func.__doc__)
    function = {
        'name': name,
        'description': description,
        'parameters': parameters,
        'required': required
    }
    json_formatted = {'type': 'function', 'function': function}
    return name, json_formatted

  def parse_docs(self, docs):
    """Returns the parsed docs"""
    description = str()
    parameters = dict()
    required = list()
    if docs == None: return description, parameters, required
    docs = docs.split('\n')
    flag = 0  # 0 = description, 1 = Parameters
    for idx, line in enumerate(docs):
      if re.search("Parameters", line):
        flag = 1
        parameters['type'] = 'object'
        parameters['properties'] = dict()
        continue
      if re.search("Returns", line) and flag == 1: flag = 2
      if flag == 0:
        description += line
      if flag == 1:
        if not re.search(' : ', line): continue
        n, t = line.replace(' ', '').replace('\t', '').split(':')
        optional = False
        if re.search(',optional', t):
          optional = True
          t, _ = t.split(',')
        if not optional: 
          required.append(n)
        d = str()
        for i, l in enumerate(docs[idx + 1:]):
          if re.search(' : ', l) or re.search('Returns', l): 
            break
          d += l.strip()
        parameters['properties'][n] = {'type': JSON_TYPES[t], 'description': d}
    return description, parameters, required
  
  def parse_gpt(self, func):
    """
    Parse using the GPT3.5 Turbo API
    """
    fc_examples = []
    for filename in FC_EXAMPLES:
      with open(filename, 'r') as f:
        fc_examples.append(json.load(f))

    func_str = inspect.getsource(func)

    response = self.client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": f"You are a helpful assistant designed to output JSON representations of functions. \
        The following examples of JSON structure MUST BE FOLLOWED for the response for the function code provided by the user.\
        \n\n{fc_examples} "},
        {"role": "user", "content": f"{func_str}"}
      ]
    )
    return func.__name__, json.loads(response.choices[0].message.content)