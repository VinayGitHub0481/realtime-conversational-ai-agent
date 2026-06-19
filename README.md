# 🎙️ AI Voice Agent

A simple AI Voice Agent built with Python that supports:

* 🎤 Speech-to-Text (STT)
* 🤖 LLM-based tool selection
* 🌦️ Weather lookup tool
* 💻 Windows Command Execution tool
* 🔊 Text-to-Speech (TTS)

The agent listens to voice input, decides which tool to use through an LLM, executes the tool, and responds back using speech.

---

## Features

### Weather Tool

Get weather information for one or multiple cities.

Example:

```
Weather in Goa
```

Output:

```
The weather in Goa is Partly cloudy +31°C
```

### Command Line Tool

Execute valid Windows CMD commands through voice.

Examples:

```
Create a folder named test
```

The agent converts it into:

```cmd
mkdir test
```

and executes it.

---

## Architecture

```
User Speech
      │
      ▼
Speech Recognition (Google STT)
      │
      ▼
GPT-4.1 Mini
(Select Tool)
      │
      ▼
Tool Execution
(Weather / CMD)
      │
      ▼
GPT-4.1 Mini
(Summarize Result)
      │
      ▼
GPT-4o Mini TTS
      │
      ▼
Audio Response
```

---

## Technologies Used

* Python
* OpenAI API
* SpeechRecognition
* PyAudio
* AsyncOpenAI
* Requests
* JSON

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/voice-agent-ai.git
cd voice-agent-ai
```

Install dependencies:

```bash
pip install openai
pip install speechrecognition
pip install pyaudio
pip install python-dotenv
pip install requests
```

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Run the Project

```bash
python main.py
```

---

## Example Commands

### Weather Queries

```
Weather in Goa
```

```
Weather in Chennai and Mumbai
```

### Windows Commands

```
Create folder test
```

```
Show current directory
```

```
List files
```

---

## Project Flow

1. Listen to user speech.
2. Convert speech to text using Google Speech Recognition.
3. Send text to GPT-4.1 Mini.
4. LLM selects the appropriate tool.
5. Execute weather or command tool.
6. Generate a natural language response.
7. Convert response to speech using GPT-4o Mini TTS.
8. Play audio back to the user.

---

## Disclaimer

The command execution tool can run Windows CMD commands on the host machine. Use only in a trusted environment.

---

## Author

Built as a learning project to understand:

* AI Agents
* Tool Calling
* Speech-to-Text
* Text-to-Speech
* OpenAI APIs
* Voice Interfaces
