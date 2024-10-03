# Code to install required libraries
!pip install -U yt-dlp
!pip install pytube moviepy requests

import yt_dlp
import os
import pytube
from moviepy.editor import *
import requests
import json

def youtube_to_speech(youtube_url, deepgram_api_key, elevenlabs_api_key):
    """
    Main function to download YouTube video audio, convert it to text,
    and then synthesize speech from that text.

    Parameters:
    youtube_url (str): The URL of the YouTube video.
    deepgram_api_key (str): API key for Deepgram.
    elevenlabs_api_key (str): API key for Eleven Labs.

    Returns:
    str: The name of the generated speech audio file.
    """
    try:
        # Step 1: Download YouTube video audio
        print("Starting the process...")
        print("Downloading YouTube video audio...")
        audio_file = download_youtube_audio(youtube_url)
        print(f"Audio downloaded: {audio_file}")

        # Step 2: Extract audio (already done in step 1)
        print("Audio extraction completed in the download step.")

        # Step 3: Convert audio to text using Deepgram API
        print("Converting audio to text using Deepgram API...")
        transcribed_text = audio_to_text(audio_file, deepgram_api_key)
        print("Transcription completed.")
        print(f"Transcribed text: {transcribed_text[:100]}...")  # Print first 100 characters

        # Step 4: Convert text back to speech using Eleven Labs API
        print("Converting text back to speech using Eleven Labs API...")
        output_audio_file = text_to_speech(transcribed_text, elevenlabs_api_key)
        print(f"Speech generation completed. Output file: {output_audio_file}")

        print("Process completed successfully.")
        return output_audio_file

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
def download_youtube_audio(url):
    """
    Downloads audio from a YouTube video and saves it as an MP3 file.

    Parameters:
    url (str): The URL of the YouTube video to download.

    Returns:
    str: The name of the downloaded MP3 file.
    """
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting video info...")
            info = ydl.extract_info(url, download=False)
            print(f"Title: {info['title']}")
            print("Downloading audio...")
            ydl.download([url])
            filename = ydl.prepare_filename(info)
            base, ext = os.path.splitext(filename)
            new_file = base + '.mp3'
            print(f"Download complete: {new_file}")
            return new_file
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        raise Exception(f"Error downloading YouTube audio: {str(e)}")

def audio_to_text(audio_file, api_key):
    """
    Converts audio file to text using Deepgram API.

    Parameters:
    audio_file (str): Path to the audio file to convert.
    api_key (str): API key for Deepgram.

    Returns:
    str: The transcribed text from the audio file.
    """
    try:
        with open(audio_file, 'rb') as f:
            audio_data = f.read()

        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "audio/mp3"
        }

        response = requests.post(
            "https://api.deepgram.com/v1/listen",
            headers=headers,
            data=audio_data
        )

        if response.status_code == 200:
            result = response.json()
            return result['results']['channels'][0]['alternatives'][0]['transcript']
        else:
            raise Exception(f"Deepgram API error: {response.status_code} - {response.text}")

    except Exception as e:
        raise Exception(f"Error in audio to text conversion: {str(e)}")

def text_to_speech(text, api_key):
    """
    Converts text to speech using Eleven Labs API.

    Parameters:
    text (str): The text to convert to speech.
    api_key (str): API key for Eleven Labs.

    Returns:
    str: The name of the generated speech audio file.
    """
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"  # Voice ID for "Adam"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            output_file = "output_speech.mp3"
            with open(output_file, "wb") as f:
                f.write(response.content)
            return output_file
        else:
            raise Exception(f"Eleven Labs API error: {response.status_code} - {response.text}")

    except Exception as e:
        raise Exception(f"Error in text to speech conversion: {str(e)}")
    
if __name__ == "__main__":
    # Replace these with your actual YouTube URL and API keys
    youtube_url = "https://youtu.be/pcC4Dr6Wj2Q?si=Pcnz-LeXBGOaRMnlD"
    deepgram_api_key = "1315bf1f806bd351ea3dfebaec84914f11039a4c"  # Use environment variable in production
    elevenlabs_api_key = "sk_f7e6a5ead8e5ac69465e5aa296926d6c1c19d4973eb78e72"  # Use environment variable in production

    output_file = youtube_to_speech(youtube_url, deepgram_api_key, elevenlabs_api_key)

    if output_file:
        print(f"Process completed successfully. Final output file: {output_file}")
    else:
        print("Process failed. Please check the error messages above.")
