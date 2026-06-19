#here create an agent that should call the weather report tool and command line tool to give the commands 

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import speech_recognition as sr 
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os 
import requests
import json
import asyncio

client=OpenAI()
async_client=AsyncOpenAI()

#LLM Model (TTS)
async def text_to_speech(text:str):

    async with async_client.audio.speech.with_streaming_response.create(

        model="gpt-4o-mini-tts",
        voice="ash",
        input=text,
        instructions="Always Speak in Cheerful way",
        response_format="pcm"  #pulse code modulation. 
        #these response_format plays role in getting type of audio like pcm or wav or mp3 audio
    ) as response:
     
     await LocalAudioPlayer().play(response)
     #here waiting until the speech agent speech gets completed 


#tool-1
def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response=requests.get(url)

    if (response.status_code==200):
        return (f"The weather in {city} is {response.text}")
    
    return f"weather info of {city} not found "


#tool-2
def command_prompt(cmd:str):
   result= os.system(cmd)

   return result 

available_tools={
    "weather":get_weather,
    "prompt":command_prompt
}


#  - Executes a valid Windows CMD command.
def main():
   
   SYSTEM_PROMPT= """
   You are an AI Agent.

You should respond based on the given input tools 

Available Tools:

1. get_weather(city:str)
   - Retrieves weather information for a city.

2. command_prompt(cmd:str)
 - Accepts a valid Windows CMD command as input.
   - The command will be executed by the system.
   - Do not generate command results yourself.
RULES
------

1. Always return valid JSON.
2. Never execute commands yourself.


JSON FORMAT
------------

Weather (single city):

{
    "tool": "get_weather",
    "response": "goa"
}

Weather (multiple cities):

{
    "tool": "get_weather",
    "response": ["goa", "chennai", "mumbai"]
}

CMD command:

{
    "tool": "command_prompt",
    "response": "mkdir test"
}

Unsupported request:

{
    "tool": "message",
    "response": "I can help with weather reports and Windows commands."
}


EXAMPLES
----------

User: weather in goa

Assistant:
{
    "tool": "get_weather",
    "response": "goa"
}

User: weather in goa and chennai

Assistant:
{
    "tool": "get_weather",
    "response": ["goa","chennai"]
}

User: create folder test

Assistant:
{
    "tool": "command_prompt",
    "response": "mkdir test"
}

"""
   

   messages=[]
   messages.append({"role":"system","content":SYSTEM_PROMPT})

   recognizer=sr.Recognizer()   #here this Recognize() method will recognize the text from speech 
          
   with sr.Microphone() as source:  #here Microphone() internally depends on PyAudio lib
        recognizer.adjust_for_ambient_noise(source) 
  

        while True:
            
            recognizer.pause_threshold=2
            print("listening audio")
            user_query=recognizer.listen(source)
            print("Processing audio after noise removal ...STT")
            google_response=recognizer.recognize_google(user_query)   #here google web api recognize the audio 

            print("Google response :",google_response)

            messages.append({"role":"user","content":google_response})

            if google_response.lower()=='exit':
             break


            resp=client.chat.completions.create(
                model='gpt-4.1-mini',
                response_format={"type":'json_object'},
                messages=messages ,
                temperature=0.3   #to get more accurate data
            )

            data=json.loads(resp.choices[0].message.content)   #we get in json  format and json.load() dict form 
            messages.append({"role":"assistant","content":json.dumps(data) })

            tool_name=data['tool']
            response_type=data['response']

            final_response=[]

            if tool_name=="get_weather":
                if isinstance(response_type,list):
                 for city in response_type:
                  result= get_weather(city)
                  final_response.append(result)          #if list of cities are mention then it will append to the final_response
                else:
                 result=get_weather(response_type)
                final_response.append(result)
            

            elif tool_name=="command_prompt":
                result2=command_prompt(response_type)
                if result2==0:
                    final_response.append("Command executed successfully")         #here os.system() response will be int we should convert to string
                else:
                   final_response.append("Command execution failed",result2)


            elif tool_name=="message":
                final_response.append(response_type)



            tool_output = "\n".join(final_response)

            summary = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Convert tool results into a short natural spoken response."
                    },
                    {
                        "role": "user",
                        "content": tool_output
                    }
                ]
            )

            spoken_text = summary.choices[0].message.content
            print(spoken_text)

            print("speech started")
            asyncio.run(text_to_speech(spoken_text))
            #so here the text response from chat llm will be
            #sent to the tts llm and speech audio response will be obtained 
            print("speech completed ")
            print(__name__)

       
main()














































