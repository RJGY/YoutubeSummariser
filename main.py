# Standard library imports
import os

# Third party imports
from dotenv import load_dotenv
import google.generativeai as genai
import whisper
import pytubefix


def main(video_url) -> str:
    # Load environment variables.
    load_dotenv()

    transcribe = whisper.load_model("base")
    # Set up Google Gemini API
    genai.configure(api_key=os.environ['GENERATIVEAI_API_KEY'])

    video = get_video_and_metadata(video_url)

    mp3 = video.streams.get_audio_only().download(filename="audio.mp3")
    
    result = transcribe.transcribe(mp3)
    transcription = result["text"]
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Summarize the following transcript of a youtube video. It is titled {video.title}, made by {video.author} and had the following description: {video.description}. Remove any mention about promotions, advertisments and product placements. Prefer longer explanations of subjects and information over shorter explanations. Transcript: \n\n{transcription} ")
    text = response.text if response.text else "Summary unavailable."
    os.remove(mp3)
    return text

def get_video_and_metadata(video_url: str) -> pytubefix.YouTube:
    try:
        video = pytubefix.YouTube(video_url, 'WEB')
    except pytubefix.exceptions.RegexMatchError:
        raise Exception("Invalid URL")
    
    return video


if __name__ == "__main__":
    text = main('https://www.youtube.com/watch?v=Ufmu1WD2TSk')
    print(text)