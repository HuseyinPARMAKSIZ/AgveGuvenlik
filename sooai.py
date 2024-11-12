!pip install youtube-transcript-api
from openai import OpenAI
import re

client = OpenAI(
    base_url="https://apiv2.sooai.com.tr/openai",  # /openai ile işaretliyoruz
    api_key="sk-soo-*****"
)

from youtube_transcript_api import YouTubeTranscriptApi

'''
# Function to fetch YouTube transcript
def fetch_youtube_transcript(video_url):
    video_id = video_url.split("v=")[-1]  # Extract video ID from the URL
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Combine transcript into a single string
    transcript_text = " ".join([entry['text'] for entry in transcript])
    return transcript_text
# Fetch and print transcript
#transcript = fetch_youtube_transcript(video_url)
'''



# Fetch the Turkish transcript
# Video ID for the desired YouTube video
def extract_video_id(url):
    # Regular expression pattern for matching YouTube video IDs
    pattern = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|\S+\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    
    # Search for the pattern in the URL
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)  # Return the extracted video ID
    else:
        return None  # Return None if no match is found

# Example YouTube URL
video_url = "https://www.youtube.com/watch?v=bCnj14k8xWw"

# Extract video ID from the URL
video_id = extract_video_id(video_url)
print(f"Video ID: {video_id}")
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['tr'])
print(transcript)

try:
    stream = client.chat.completions.create(
        model="default",
        messages=[
            {"role": "user", "content": f"As a professional summarizer specialized in video content, create a detailed and comprehensive summary of the YouTube video transcript: {transcript}."}
        ],
        stream=True
    )

    print("Yanıt:\n")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)
    print("\n")

except Exception as e:
    print(f"Hata oluştu: {str(e)}")
