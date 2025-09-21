import subprocess
import os

# Constants
YTDLP_PATH = "yt-dlp.exe"
URL_LIST_FILE = "urls.txt"
URLS_PAST_FILE = "URLSpast.txt"
DOWNLOAD_DIR = "ytdlpDOWNLOADS"

def load_urls(file_path):
    """Load URLs from a text file into a list."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_url_to_past(url):
    """Append a single URL to URLSpast.txt"""
    with open(URLS_PAST_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def filter_new_urls(all_urls, past_urls):
    """Return only the URLs that are not in past_urls."""
    return [url for url in all_urls if url not in past_urls]

def download_audio(urls):
    """Download audio in mp3 format from each URL using yt-dlp."""
    for url in urls:
        print(f"\n🎵 Downloading audio from: {url}")
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        result = subprocess.run([
            YTDLP_PATH,
            "-x",  # extract audio
            "--audio-format", "mp3",
            "--audio-quality", "192K",
            "-o", output_template,
            url
        ], capture_output=True, text=True)

        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Error downloading {url}:\n{result.stderr}")
        else:
            save_url_to_past(url)

def download_video(urls):
    """Download best quality video from each URL using yt-dlp."""
    for url in urls:
        print(f"\n🎬 Downloading video from: {url}")
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        result = subprocess.run([
            YTDLP_PATH,
            "-f", "best",
            "-o", output_template,
            url
        ], capture_output=True, text=True)

        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Error downloading {url}:\n{result.stderr}")
        else:
            save_url_to_past(url)

def main():
    # Ensure download folder exists
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    all_urls = load_urls(URL_LIST_FILE)
    past_urls = set(load_urls(URLS_PAST_FILE))

    new_urls = filter_new_urls(all_urls, past_urls)

    if not new_urls:
        print("✅ All URLs in urls.txt have already been downloaded.")
        input("Press Enter to exit...")
        return

    print("Select download format:")
    print("1. Audio (MP3)")
    print("2. Video (Best quality)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        download_audio(new_urls)
    elif choice == "2":
        download_video(new_urls)
    else:
        print("Invalid choice. Exiting.")
        input("Press Enter to exit...")
        return

    print("\n✅ All new downloads completed.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
