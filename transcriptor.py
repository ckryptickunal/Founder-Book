import os
import sys
import re
import time
import json
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAILED_LOG = os.path.join(BASE_DIR, "failed_videos.json")


def load_failed_videos() -> list[dict]:
    if os.path.exists(FAILED_LOG):
        with open(FAILED_LOG, "r") as f:
            return json.load(f)
    return []


def save_failed_videos(failed: list[dict]):
    with open(FAILED_LOG, "w") as f:
        json.dump(failed, f, indent=2)


def add_to_failed(video: dict, channel_folder: str, reason: str = "ip_blocked"):
    """Add a video to the persistent failed list (deduplicates by ID)."""
    failed = load_failed_videos()
    existing_ids = {v["id"] for v in failed}
    if video["id"] not in existing_ids:
        video["channel_folder"] = channel_folder
        video["reason"] = reason
        video["failed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        video["attempts"] = 1
        failed.append(video)
    else:
        for v in failed:
            if v["id"] == video["id"]:
                v["attempts"] = v.get("attempts", 0) + 1
                v["last_attempt"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                break
    save_failed_videos(failed)


def remove_from_failed(video_id: str):
    """Remove a video from the failed list after successful fetch."""
    failed = load_failed_videos()
    failed = [v for v in failed if v["id"] != video_id]
    save_failed_videos(failed)


def get_youtube_service():
    if not YOUTUBE_API_KEY:
        print("Error: YOUTUBE_API_KEY not found in .env file")
        sys.exit(1)
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def resolve_channel_id(youtube, channel_input: str) -> tuple[str, str]:
    """Resolve a channel name, URL, or handle to (channel_id, channel_title)."""

    # Handle direct channel ID
    if re.match(r'^UC[\w-]{22}$', channel_input):
        resp = youtube.channels().list(part="snippet", id=channel_input).execute()
        if resp["items"]:
            return channel_input, resp["items"][0]["snippet"]["title"]

    # Handle YouTube URLs
    if "youtube.com" in channel_input:
        parsed = urlparse(channel_input)
        path = parsed.path

        if "/channel/" in path:
            channel_id = path.split("/channel/")[1].split("/")[0]
            resp = youtube.channels().list(part="snippet", id=channel_id).execute()
            if resp["items"]:
                return channel_id, resp["items"][0]["snippet"]["title"]

        elif "/@" in path:
            handle = path.split("/@")[1].split("/")[0]
            resp = youtube.search().list(
                part="snippet", q=handle, type="channel", maxResults=1
            ).execute()
            if resp["items"]:
                channel_id = resp["items"][0]["snippet"]["channelId"]
                title = resp["items"][0]["snippet"]["channelTitle"]
                return channel_id, title

        elif "/c/" in path or "/user/" in path:
            name = path.split("/")[-1]
            resp = youtube.search().list(
                part="snippet", q=name, type="channel", maxResults=1
            ).execute()
            if resp["items"]:
                channel_id = resp["items"][0]["snippet"]["channelId"]
                title = resp["items"][0]["snippet"]["channelTitle"]
                return channel_id, title

    # Handle @handle format
    if channel_input.startswith("@"):
        resp = youtube.search().list(
            part="snippet", q=channel_input[1:], type="channel", maxResults=1
        ).execute()
        if resp["items"]:
            channel_id = resp["items"][0]["snippet"]["channelId"]
            title = resp["items"][0]["snippet"]["channelTitle"]
            return channel_id, title

    # Try as a channel name search
    resp = youtube.search().list(
        part="snippet", q=channel_input, type="channel", maxResults=1
    ).execute()
    if resp["items"]:
        channel_id = resp["items"][0]["snippet"]["channelId"]
        title = resp["items"][0]["snippet"]["channelTitle"]
        return channel_id, title

    print(f"Error: Could not find channel for '{channel_input}'")
    sys.exit(1)


def get_all_video_ids(youtube, channel_id: str) -> list[dict]:
    """Get all video IDs and metadata from a channel using the YouTube Data API."""
    videos = []

    # Get the uploads playlist ID
    resp = youtube.channels().list(part="contentDetails", id=channel_id).execute()
    if not resp["items"]:
        print("Error: Could not find channel content")
        return []

    uploads_playlist_id = resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    next_page_token = None
    while True:
        playlist_resp = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        ).execute()

        for item in playlist_resp["items"]:
            snippet = item["snippet"]
            videos.append({
                "id": snippet["resourceId"]["videoId"],
                "title": snippet["title"],
                "published_at": snippet.get("publishedAt", "Unknown"),
                "description": snippet.get("description", ""),
                "channel_title": snippet.get("channelTitle", ""),
            })

        next_page_token = playlist_resp.get("nextPageToken")
        if not next_page_token:
            break

    return videos


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from a YouTube URL or return the ID directly."""
    if "youtube.com/watch" in url_or_id:
        query = parse_qs(urlparse(url_or_id).query)
        return query["v"][0]
    elif "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1].split("?")[0]
    return url_or_id.strip()




def get_video_metadata(youtube, video_id: str) -> dict:
    """Fetch metadata for a single video via YouTube Data API."""
    resp = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id).execute()
    if not resp["items"]:
        return {}
    item = resp["items"][0]
    snippet = item["snippet"]
    stats = item.get("statistics", {})
    return {
        "title": snippet.get("title", "Unknown"),
        "published_at": snippet.get("publishedAt", "Unknown"),
        "description": snippet.get("description", ""),
        "channel_title": snippet.get("channelTitle", ""),
        "duration": item.get("contentDetails", {}).get("duration", "Unknown"),
        "view_count": stats.get("viewCount", "N/A"),
        "like_count": stats.get("likeCount", "N/A"),
        "tags": snippet.get("tags", []),
    }


def write_transcript_file(filepath: str, video_id: str, metadata: dict, transcript):
    """Write a transcript file with full metadata header."""
    text_formatter = TextFormatter()
    text_output = text_formatter.format_transcript(transcript)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Title: {metadata.get('title', 'Unknown')}\n")
        f.write(f"Video ID: {video_id}\n")
        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        f.write(f"Channel: {metadata.get('channel_title', 'Unknown')}\n")
        f.write(f"Published: {metadata.get('published_at', 'Unknown')}\n")
        if metadata.get("duration"):
            f.write(f"Duration: {metadata.get('duration', 'Unknown')}\n")
        if metadata.get("view_count"):
            f.write(f"Views: {metadata.get('view_count', 'N/A')}\n")
        if metadata.get("like_count"):
            f.write(f"Likes: {metadata.get('like_count', 'N/A')}\n")
        if metadata.get("tags"):
            f.write(f"Tags: {', '.join(metadata['tags'][:15])}\n")
        f.write(f"Transcript Language: {transcript.language} ({transcript.language_code})\n")
        f.write(f"Auto-generated: {transcript.is_generated}\n")
        f.write(f"Snippets: {len(transcript)}\n")
        if metadata.get("description"):
            f.write(f"\nDescription:\n{metadata['description'][:500]}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("TRANSCRIPT\n")
        f.write("=" * 60 + "\n\n")
        f.write(text_output)


def mode_single_video():
    """Handle single video transcript extraction."""
    video_input = input("\nEnter YouTube video URL or ID: ").strip()
    if not video_input:
        print("No input provided.")
        return

    video_id = extract_video_id(video_input)
    print(f"\nFetching transcript for: {video_id}")

    youtube = get_youtube_service()
    metadata = get_video_metadata(youtube, video_id)
    if metadata:
        print(f"Title: {metadata['title']}")
        print(f"Published: {metadata['published_at']}")

    output_dir = os.path.join(BASE_DIR, "single_videos")
    os.makedirs(output_dir, exist_ok=True)

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=["en"])

        filepath = os.path.join(output_dir, f"{video_id}.txt")
        write_transcript_file(filepath, video_id, metadata, transcript)

        print(f"\nTranscript saved to: {filepath}")
        print(f"Language: {transcript.language} | Snippets: {len(transcript)}")

    except Exception as e:
        print(f"\nError: {e}")


def mode_full_channel():
    """Handle full channel transcript extraction."""
    channel_input = input("\nEnter YouTube channel (name, @handle, or URL): ").strip()
    if not channel_input:
        print("No input provided.")
        return

    youtube = get_youtube_service()

    print(f"\nResolving channel...")
    channel_id, channel_title = resolve_channel_id(youtube, channel_input)
    print(f"Found: {channel_title} ({channel_id})")

    print(f"Fetching video list...")
    videos = get_all_video_ids(youtube, channel_id)
    print(f"Total videos found: {len(videos)}")

    if not videos:
        print("No videos found on this channel.")
        return

    safe_title = re.sub(r'[<>:"/\\|?*]', '_', channel_title)
    output_dir = os.path.join(BASE_DIR, safe_title)
    os.makedirs(output_dir, exist_ok=True)

    # Save video list as metadata
    metadata_path = os.path.join(output_dir, "_video_list.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump({"channel": channel_title, "channel_id": channel_id, "videos": videos}, f, indent=2)

    existing = [f.replace(".txt", "") for f in os.listdir(output_dir) if f.endswith(".txt") and not f.startswith("_")]
    remaining = [v for v in videos if v["id"] not in existing]
    print(f"Already downloaded: {len(existing)} | Remaining: {len(remaining)}")

    if not remaining:
        print("All transcripts already downloaded!")
        return

    proceed = input(f"\nProceed to fetch {len(remaining)} transcripts? (y/n): ").strip().lower()
    if proceed != "y":
        print("Aborted.")
        return

    success = 0
    failed = 0
    failed_videos = []
    consecutive_failures = 0

    for i, video in enumerate(remaining, 1):
        vid = video["id"]
        print(f"[{i}/{len(remaining)}] {video['title'][:50]}... ", end="", flush=True)

        filepath = os.path.join(output_dir, f"{vid}.txt")
        if os.path.exists(filepath):
            print("SKIP")
            success += 1
            consecutive_failures = 0
            continue

        metadata = {
            "title": video.get("title", "Unknown"),
            "published_at": video.get("published_at", "Unknown"),
            "description": video.get("description", ""),
            "channel_title": video.get("channel_title", channel_title),
        }

        fetched = False
        for attempt in range(3):
            try:
                ytt_api = YouTubeTranscriptApi()
                transcript = ytt_api.fetch(vid, languages=["en"])

                write_transcript_file(filepath, vid, metadata, transcript)

                print(f"OK ({len(transcript)} snippets)")
                success += 1
                consecutive_failures = 0
                fetched = True
                break

            except Exception as e:
                error_str = str(e).lower()
                if "unplayable" in error_str or "live event" in error_str:
                    print("SKIP (unplayable/live)")
                    failed += 1
                    failed_videos.append(video)
                    add_to_failed(video, output_dir, reason="unplayable")
                    fetched = True
                    break
                if attempt < 2:
                    wait = (attempt + 1) * 5
                    print(f"retry({attempt+1})... ", end="", flush=True)
                    time.sleep(wait)
                else:
                    print("FAILED (IP blocked)")
                    failed += 1
                    failed_videos.append(video)
                    add_to_failed(video, output_dir, reason="ip_blocked")
                    consecutive_failures += 1

        if consecutive_failures >= 3:
            print(f"\n--- IP likely blocked. Waiting 2 minutes before retrying... ---")
            time.sleep(120)
            consecutive_failures = 0

        if fetched:
            time.sleep(4)
        else:
            time.sleep(5)

    print("\n" + "=" * 60)
    print(f"COMPLETE! Success: {success} | Failed: {failed}")
    print(f"Saved to: {output_dir}")
    if failed_videos:
        print(f"\nFailed videos ({len(failed_videos)}):")
        for v in failed_videos[:10]:
            print(f"  - {v['id']} | {v['title'][:60]}")
        if len(failed_videos) > 10:
            print(f"  ... and {len(failed_videos) - 10} more")
        print("\nRe-run this tool later to retry failed videos (already-downloaded ones are skipped).")


def main():
    print("=" * 60)
    print("  TRANSCRIPTOR - YouTube Transcript Extractor")
    print("=" * 60)
    print("\nWhat would you like to do?\n")
    print("  1. Extract transcript from a SINGLE video")
    print("  2. Extract ALL transcripts from a YouTube channel")
    print()

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        mode_single_video()
    elif choice == "2":
        mode_full_channel()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
