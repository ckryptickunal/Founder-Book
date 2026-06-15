from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter
import sys
import json


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from a YouTube URL or return the ID directly."""
    if "youtube.com/watch" in url_or_id:
        from urllib.parse import urlparse, parse_qs
        query = parse_qs(urlparse(url_or_id).query)
        return query["v"][0]
    elif "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1].split("?")[0]
    return url_or_id


def fetch_transcript(video_id: str, languages=None):
    """Fetch transcript for a single video."""
    if languages is None:
        languages = ["en"]

    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=languages)
    return transcript


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_transcript.py <video_url_or_id>")
        print("Example: python fetch_transcript.py dQw4w9WgXcQ")
        sys.exit(1)

    video_input = sys.argv[1]
    video_id = extract_video_id(video_input)

    print(f"Fetching transcript for video: {video_id}")
    print("-" * 50)

    try:
        transcript = fetch_transcript(video_id)

        text_formatter = TextFormatter()
        text_output = text_formatter.format_transcript(transcript)

        print(f"Language: {transcript.language} ({transcript.language_code})")
        print(f"Auto-generated: {transcript.is_generated}")
        print(f"Snippets: {len(transcript)}")
        print("-" * 50)
        print(text_output[:2000])

        if len(text_output) > 2000:
            print(f"\n... [truncated, full transcript is {len(text_output)} chars]")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
