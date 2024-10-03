# YouTube-to-Speech-Converter

## Overview
This project downloads a YouTube video, extracts its audio, converts the audio to text using the Deepgram API, and then generates speech from the transcribed text using the Eleven Labs API. 

## Features
- Download YouTube video audio in MP3 format.
- Transcribe audio to text using Deepgram.
- Convert transcribed text back to speech using Eleven Labs.

## Requirements
- Python 3.x
- You can install the required libraries using the provided `requirements.txt` file.

## Installation
To set up this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>

2. Install the required libraries:
   pip install -r `requirements.txt`

## Usage
1. Open the `youtube_to_speech.py` file and replace the placeholders with your actual YouTube video URL and API keys for Deepgram and Eleven Labs.
   
2. Run the script:
   `python youtube_to_speech.py`
   
3. After execution, the generated speech will be saved as `output_speech.mp3`.

## API Keys
- Obtain your Deepgram API key from Deepgram's website: [Get it here](https://developers.deepgram.com/reference/deepgram-api-overview).
- Obtain your Eleven Labs API key from Eleven Labs' website: [Get it here](https://elevenlabs.io/docs/api-reference/text-to-speech).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- [Deepgram](https://deepgram.com/) for their speech-to-text API.
- [Eleven Labs](https://elevenlabs.io/) for their text-to-speech API.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the YouTube download functionality.
