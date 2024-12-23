import json
import time
import requests
from utils import *

def temp_sleep(seconds=0.1):
  time.sleep(seconds)

def llama_single_request(prompt):
    try:
        chat_completion_endpoint = url + 'chat/completions/'
        headers =  {
                    "Content-Type": "application/json"
                }
        messages = [{"role": "user", "content": prompt}]
        # Prepare the data payload for Llama3
        data = {
            "model": 'llama',
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(chat_completion_endpoint, headers=headers, data=json.dumps(data))
        result = response.json()

        return result['choices'][0]['message']['content']
    
    except:
        print ("ChatGPT ERROR")
        return "ChatGPT ERROR"   
    
def LLAMA_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt = '"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 

    try: 
      curr_gpt_response = llama_single_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]

      # print ("---ashdfaf")
      # print (curr_gpt_response)
      # print ("000asdfhia")
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass

  return False

def LLAMA_safe_generate_response_OLD(prompt, 
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  if verbose: 
    print ("PROMPT")
    print (prompt)

  for i in range(repeat): 
    try: 
      curr_gpt_response = llama_single_request(prompt).strip()
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose: 
        print (f"---- repeat count: {i}")
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass
  print ("FAIL SAFE TRIGGERED") 
  return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================

def llama_request(prompt, parameter): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT-3's response. 
  """
  temp_sleep()
  try: 
    completion_endpoint = url + 'completions/'
    headers =  {
                "Content-Type": "application/json"
            }

    # Prepare the data payload for Llama3
    data = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": parameter["max_tokens"],
        "temperature": parameter["temperature"],
        "top_p": parameter["top_p"],
        "stream": parameter["stream"],
        "stop": parameter["stop"]
    }

    response = requests.post(completion_endpoint, headers=headers, data=json.dumps(data))
    result = response.json()

    return result['choices'][0]['text']

  except: 
    print ("TOKEN LIMIT EXCEEDED")
    return "TOKEN LIMIT EXCEEDED"


def llama_generate_prompt(curr_input, prompt_lib_file): 
  """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the GPT3 server. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to OpenAI's GPT server.  
  """
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


def llama_safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  if verbose: 
    print (prompt)

  for i in range(repeat): 
    curr_response = llama_request(prompt, gpt_parameter)
    if func_validate(curr_response, prompt=prompt): 
      return func_clean_up(curr_response, prompt=prompt)
    if verbose: 
      print ("---- repeat count: ", i, curr_response)
      print (curr_response)
      print ("~~~~")
  return fail_safe_response


def get_llama_embedding(text):
  text = text.replace("\n", " ")

  if not text: 
    text = "this is blank"

  embed_endpoint = url_emb + 'embeddings/'

  data = {
    "model": model_name,
    "input": [text],
    }
  
  headers =  {
        "Content-Type": "application/json"
    }
  
  response = requests.post(embed_endpoint, headers=headers, data=json.dumps(data))
  result = response.json()
  

  return result['data'][0]['embedding']

if __name__ == '__main__':
  gpt_parameter = {"engine": "llama3.2-3B", "max_tokens": 50, 
                   "temperature": 0, "top_p": 1, "stream": False,
                   "frequency_penalty": 0, "presence_penalty": 0, 
                   "stop": ['"']}
  curr_input = ["driving to a friend's house"]
  prompt_lib_file = "prompt_template/safety/anthromorphosization_v1.txt"
  prompt = llama_generate_prompt(curr_input, prompt_lib_file)

  def __func_validate(llama_response, prompt): 
    if len(llama_response.strip()) <= 1:
      return False
    if len(llama_response.strip().split(" ")) > 1: 
      return False
    return True
  def __func_clean_up(llama_response, prompt):
    cleaned_response = llama_response.strip()
    return cleaned_response

  output = llama_safe_generate_response(prompt, 
                                 gpt_parameter,
                                 5,
                                 "rest",
                                 __func_validate,
                                 __func_clean_up,
                                 True)

  print (output)