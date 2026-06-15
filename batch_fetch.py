import os
import sys
import time
import json
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter


VIDEO_URLS = """
https://www.youtube.com/watch?v=X1NXnLRNIfM
https://www.youtube.com/watch?v=t-G67yKAHBQ
https://www.youtube.com/watch?v=jikOaczZxTY
https://www.youtube.com/watch?v=1egwM88T3C0
https://www.youtube.com/watch?v=DGD9b8K42lk
https://www.youtube.com/watch?v=ZVdgiuiOQ7E
https://www.youtube.com/watch?v=RMmEB9ajmdo
https://www.youtube.com/watch?v=21L-iujzy9U
https://www.youtube.com/watch?v=_y7siiS-V5A
https://www.youtube.com/watch?v=u2z44EkIEHE
https://www.youtube.com/watch?v=cSBdukYWWxQ
https://www.youtube.com/watch?v=ZxwYGbCOuDQ
https://www.youtube.com/watch?v=00YZWlvAMsQ
https://www.youtube.com/watch?v=UGYnC9zqa-k
https://www.youtube.com/watch?v=UpWNdSVWA7M
https://www.youtube.com/watch?v=Yr9mHKxOkLg
https://www.youtube.com/watch?v=ZPGgtBl1v4M
https://www.youtube.com/watch?v=lfzm2SlhbM8
https://www.youtube.com/watch?v=Elm2p_TRPwk
https://www.youtube.com/watch?v=znULXKSAN7o
https://www.youtube.com/watch?v=XcI5IMLEAaE
https://www.youtube.com/watch?v=6iilze3aDkU
https://www.youtube.com/watch?v=hpEXEtycm1Y
https://www.youtube.com/watch?v=OLEjyBLo8sQ
https://www.youtube.com/watch?v=M57MeOY-n3g
https://www.youtube.com/watch?v=s5w7pbpeGZ0
https://www.youtube.com/watch?v=Sr1STQP0cds
https://www.youtube.com/watch?v=6g8qRhCI8AU
https://www.youtube.com/watch?v=1pjiS-t_O0w
https://www.youtube.com/watch?v=3JiVDYL20G4
https://www.youtube.com/watch?v=2RseTTRB2bs
https://www.youtube.com/watch?v=GciivYKTK_Q
https://www.youtube.com/watch?v=L_UjKHUfN7E
https://www.youtube.com/watch?v=6yPs2nDpYZo
https://www.youtube.com/watch?v=mJO10CL-FGI
https://www.youtube.com/watch?v=-moAmKQk72A
https://www.youtube.com/watch?v=KmdN6OQ_PwE
https://www.youtube.com/watch?v=p9qa1IO0Jsw
https://www.youtube.com/watch?v=roI3LfxnqUk
https://www.youtube.com/watch?v=QkKeu1AyCQ0
https://www.youtube.com/watch?v=AVRVMSHjrac
https://www.youtube.com/watch?v=gz4AKzSBwTk
https://www.youtube.com/watch?v=3FJV-Gmrpa8
https://www.youtube.com/watch?v=Tm5NbHUblkA
https://www.youtube.com/watch?v=vRt4ng9V9qA
https://www.youtube.com/watch?v=5jHWBQqiylo
https://www.youtube.com/watch?v=IGXKIL57uwc
https://www.youtube.com/watch?v=wbeHAVonbmw
https://www.youtube.com/watch?v=9ZQP7PfHnuI
https://www.youtube.com/watch?v=W_UgM6iT7Do
https://www.youtube.com/watch?v=IS_y40zY-hc
https://www.youtube.com/watch?v=FTokJt1ioeg
https://www.youtube.com/watch?v=3jN77Aw7Utk
https://www.youtube.com/watch?v=sLFv3RSj_d8
https://www.youtube.com/watch?v=LX_wvUMxVsk
https://www.youtube.com/watch?v=ryHJuYzUejs
https://www.youtube.com/watch?v=AmXE9Gsuw_Q
https://www.youtube.com/watch?v=qDumDlXcMkg
https://www.youtube.com/watch?v=q8TOaXBzcJw
https://www.youtube.com/watch?v=_-ARm9FTFAM
https://www.youtube.com/watch?v=Y4FUaVvBmzg
https://www.youtube.com/watch?v=QBC_cViA7j8
https://www.youtube.com/watch?v=Hk6A1WcJtPs
https://www.youtube.com/watch?v=Nt6mWetw0ak
https://www.youtube.com/watch?v=Aw_qfill_fo
https://www.youtube.com/watch?v=A6tFPd4bclE
https://www.youtube.com/watch?v=UrdN6k1CZBc
https://www.youtube.com/watch?v=QcCPQSd36vQ
https://www.youtube.com/watch?v=F-Y4hDX4nmY
https://www.youtube.com/watch?v=2SbBE9sxyYE
https://www.youtube.com/watch?v=MhsjuJaGLK4
https://www.youtube.com/watch?v=p3L5zATA_HY
https://www.youtube.com/watch?v=JgFE5wrUL6A
https://www.youtube.com/watch?v=EJbhzlqgoYs
https://www.youtube.com/watch?v=dpHBSGS6W5c
https://www.youtube.com/watch?v=ToTAnPW70Us
https://www.youtube.com/watch?v=bk0OWFPqhfU
https://www.youtube.com/watch?v=hFodoGofMtg
https://www.youtube.com/watch?v=UouFu6k45lw
https://www.youtube.com/watch?v=5tluNIMcuTs
https://www.youtube.com/watch?v=p670juDb_5Y
https://www.youtube.com/watch?v=fQvAw5Qj20k
https://www.youtube.com/watch?v=NCY0IUaiLOA
https://www.youtube.com/watch?v=yjIJOfgVgu0
https://www.youtube.com/watch?v=pieVtTrbDBs
https://www.youtube.com/watch?v=9CWbc6pekd8
https://www.youtube.com/watch?v=9h1dxWDFgTU
https://www.youtube.com/watch?v=Jpem6ZqWHt8
https://www.youtube.com/watch?v=O4CA2gBKG9Y
https://www.youtube.com/watch?v=MKEblI7yF_8
https://www.youtube.com/watch?v=t1AHFTCj4yo
https://www.youtube.com/watch?v=py4FHUjc-bY
https://www.youtube.com/watch?v=zgwuPuq7eDM
https://www.youtube.com/watch?v=rwFDkJS4tLU
https://www.youtube.com/watch?v=D2_ClDSbAEA
https://www.youtube.com/watch?v=ix4Ol4e-P7o
https://www.youtube.com/watch?v=JHvwEWsbQCg
https://www.youtube.com/watch?v=pQ9gtaGd-Os
https://www.youtube.com/watch?v=tvNYhwmTal8
https://www.youtube.com/watch?v=8Tpj7bZsUbA
https://www.youtube.com/watch?v=50Yz0O1yexY
https://www.youtube.com/watch?v=2CeRGNhUDYw
https://www.youtube.com/watch?v=3A2neXJIJ2A
https://www.youtube.com/watch?v=fB0H_HId6aM
https://www.youtube.com/watch?v=6W-cu0yp5cA
https://www.youtube.com/watch?v=-5I9lIYZx-A
https://www.youtube.com/watch?v=_7bnpjJB9T0
https://www.youtube.com/watch?v=b_R-lIIYR5Q
https://www.youtube.com/watch?v=2OPhFqmdLQc
https://www.youtube.com/watch?v=F2cuzkQ9kBA
https://www.youtube.com/watch?v=Bw9XaB3aQm4
https://www.youtube.com/watch?v=Ir62zhDol9c
https://www.youtube.com/watch?v=JS_2EQsXkgY
https://www.youtube.com/watch?v=59ZQ-rf6iIc
https://www.youtube.com/watch?v=SHAh6WKBgiE
https://www.youtube.com/watch?v=EHzvmyMJEK4
https://www.youtube.com/watch?v=F4K_qVlYQkg
https://www.youtube.com/watch?v=qAws7eXItMk
https://www.youtube.com/watch?v=uVhTvQXfibU
https://www.youtube.com/watch?v=6fQHLK1aIBs
https://www.youtube.com/watch?v=dQ7ZvO5DpIw
https://www.youtube.com/watch?v=tFVDjrvQJdw
https://www.youtube.com/watch?v=H8Dl8rZ6qwE
https://www.youtube.com/watch?v=RfWgVWGEuGE
https://www.youtube.com/watch?v=uFX95HahaUs
https://www.youtube.com/watch?v=oQOC-qy-GDY
https://www.youtube.com/watch?v=sz_LgBAGYyo
https://www.youtube.com/watch?v=n_yHZ_vKjno
https://www.youtube.com/watch?v=5_0dVHMpJlo
https://www.youtube.com/watch?v=yP176MBG9Tk
https://www.youtube.com/watch?v=ii1jcLg-eIQ
https://www.youtube.com/watch?v=CVfnkM44Urs
https://www.youtube.com/watch?v=CBYhVcO4WgI
"""


def extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    from urllib.parse import urlparse, parse_qs
    if "youtube.com/watch" in url:
        query = parse_qs(urlparse(url).query)
        return query["v"][0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url.strip()


def get_channel_name(video_id: str) -> str:
    """Try to get the channel name from a YouTube video page."""
    try:
        resp = requests.get(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        )
        match = re.search(r'"ownerChannelName":"([^"]+)"', resp.text)
        if match:
            return match.group(1)
        match = re.search(r'"author":"([^"]+)"', resp.text)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "unknown_channel"


def get_video_title(video_id: str) -> str:
    """Try to get the video title from YouTube."""
    try:
        resp = requests.get(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        )
        match = re.search(r'<title>(.+?) - YouTube</title>', resp.text)
        if match:
            title = match.group(1)
            title = re.sub(r'[<>:"/\\|?*]', '_', title)
            return title[:80]
    except Exception:
        pass
    return video_id


def main():
    urls = [u.strip() for u in VIDEO_URLS.strip().split("\n") if u.strip()]
    video_ids = list(dict.fromkeys(extract_video_id(url) for url in urls))

    print(f"Total URLs provided: {len(urls)}")
    print(f"Unique video IDs: {len(video_ids)}")

    print("\nDetecting channel name...")
    channel_name = get_channel_name(video_ids[0])
    safe_channel_name = re.sub(r'[<>:"/\\|?*]', '_', channel_name)
    print(f"Channel: {channel_name}")

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), safe_channel_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output folder: {output_dir}\n")

    text_formatter = TextFormatter()

    success = 0
    failed = 0
    failed_ids = []
    consecutive_failures = 0

    for i, video_id in enumerate(video_ids, 1):
        print(f"[{i}/{len(video_ids)}] Fetching: {video_id} ... ", end="", flush=True)

        filepath = os.path.join(output_dir, f"{video_id}.txt")
        if os.path.exists(filepath):
            print("SKIPPED (already exists)")
            success += 1
            consecutive_failures = 0
            continue

        fetched = False
        for attempt in range(3):
            try:
                ytt_api = YouTubeTranscriptApi()
                transcript = ytt_api.fetch(video_id, languages=["en"])
                text_output = text_formatter.format_transcript(transcript)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Video ID: {video_id}\n")
                    f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                    f.write(f"Language: {transcript.language} ({transcript.language_code})\n")
                    f.write(f"Auto-generated: {transcript.is_generated}\n")
                    f.write(f"Snippets: {len(transcript)}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(text_output)

                print(f"OK ({len(transcript)} snippets)")
                success += 1
                consecutive_failures = 0
                fetched = True
                break

            except Exception as e:
                error_str = str(e)
                if "unplayable" in error_str.lower() or "live event" in error_str.lower():
                    print(f"SKIPPED (unplayable/live)")
                    failed += 1
                    failed_ids.append(video_id)
                    fetched = True
                    break
                if attempt < 2:
                    wait = (attempt + 1) * 5
                    print(f"retry in {wait}s... ", end="", flush=True)
                    time.sleep(wait)
                else:
                    print(f"FAILED - {e}")
                    failed += 1
                    failed_ids.append(video_id)
                    consecutive_failures += 1

        if consecutive_failures >= 3:
            wait_time = 120
            print(f"\n⚠ Too many consecutive failures (IP likely blocked). Waiting {wait_time}s...")
            time.sleep(wait_time)
            consecutive_failures = 0

        if fetched:
            time.sleep(4)
        else:
            time.sleep(5)

    print("\n" + "=" * 60)
    print(f"DONE! Success: {success}, Failed: {failed}")
    print(f"Transcripts saved to: {output_dir}")
    if failed_ids:
        print(f"\nFailed video IDs:")
        for vid in failed_ids:
            print(f"  - {vid}")


if __name__ == "__main__":
    main()
