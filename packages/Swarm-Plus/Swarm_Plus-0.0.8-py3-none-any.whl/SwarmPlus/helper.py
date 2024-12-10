import sys
sys.dont_write_bytecode =True

def print_colored(text, color):
    """
    Prints the given text in the specified color.

    Parameters:
    text (str): The text to be printed.
    color (str): The color to print the text in. Supported colors are:
                 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    """
    # ANSI escape codes for text colors
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'orange': '\033[38;5;208m',
        'pink': '\033[38;5;205m',
        'purple': '\033[38;5;129m',
        'teal': '\033[38;5;37m',
        'olive': '\033[38;5;58m',
        'peach': '\033[38;5;216m',
        'beige': '\033[38;5;230m',
        'brown': '\033[38;5;94m',
    }

    # Reset code to revert to default color
    reset = '\033[0m'

    # Check if the specified color is supported
    if color in colors:
        print(colors[color] + text + reset)
    else:
        print("Unsupported color! Supported colors are:", ", ".join(colors.keys()))


import re
import json

def extract_json(text: str):
  # Regex pattern to match content between ```json and ```
  pattern = r'```json(.*?)```'
  
  # Search for the first match with ```json
  match = re.search(pattern, text, re.DOTALL)
  
  if match:
      try:
          # Parse the JSON content from the match
          json_object = json.loads(match.group(1).strip())
          return json_object
      except json.JSONDecodeError as e:
          
          return f"Error decoding JSON: {e}"
  else:
      # Fallback: Try to find JSON content starting directly with `{`
      try:
          json_start = text.find('{')
          json_ends = text.rfind('}')

          if json_start != -1:
              json_object = json.loads(text[json_start:json_ends+1].strip())
              return json_object
          else:
              
              return "No JSON block found."
          
      except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"