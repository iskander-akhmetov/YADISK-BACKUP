import os
import csv
import time
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote, unquote
from tqdm import tqdm

# === SETTINGS ===
YANDEX_LOGIN = "your_login@yandex.ru"
YANDEX_PASSWORD = "your_password_or_app_password"  # App password if 2FA enabled
BASE_URL = "https://webdav.yandex.ru/"
LOCAL_DIR = "YandexDiskBackup"
LOG_FILE = "backup_log.csv"


# === Initialize CSV log ===
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["file_path", "size_bytes", "status", "time_sec"])


def write_log(file_path, size, status, duration):
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([file_path, size, status, f"{duration:.2f}"])


# === List directory contents via WebDAV ===
def list_files(path=""):
    url = BASE_URL + quote(path)
    headers = {"Depth": "1"}
    resp = requests.request("PROPFIND", url, auth=(YANDEX_LOGIN, YANDEX_PASSWORD), headers=headers)

    if resp.status_code not in (200, 207):
        print(f"Access error {path}: {resp.status_code}")
        return []

    items = []
    ns = {"d": "DAV:"}
    try:
        root = ET.fromstring(resp.text)
        for r in root.findall("d:response", ns):
            href = r.find("d:href", ns)
            if href is not None:
                href_text = unquote(href.text.lstrip("/"))
                if href_text.strip("/") != path.strip("/"):
                    items.append(href_text)
    except Exception as e:
        print("XML parse error:", e)

    return items


# === Download single file with progress bar ===
def download_file(remote_path, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    url = BASE_URL + quote(remote_path)
    start_time = time.time()

    try:
        with requests.get(url, auth=(YANDEX_LOGIN, YANDEX_PASSWORD), stream=True) as r:
            if r.status_code == 200:
                total = int(r.headers.get("content-length", 0))
                with open(local_path, "wb") as f, tqdm(
                    total=total,
                    unit="B",
                    unit_scale=True,
                    desc=os.path.basename(remote_path),
                    ncols=80,
                ) as bar:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
                duration = time.time() - start_time
                write_log(remote_path, total, "OK", duration)
            else:
                print(f"Download error {remote_path}: {r.status_code}")
                write_log(remote_path, 0, f"HTTP {r.status_code}", 0)
    except Exception as e:
        print(f"Error downloading {remote_path}: {e}")
        write_log(remote_path, 0, f"ERROR {type(e).__name__}", 0)


# === Recursive download of folders ===
def recursive_download(path=""):
    items = list_files(path)
    for item in items:
        if item.endswith("/"):
            recursive_download(item)
        else:
            local_path = os.path.join(LOCAL_DIR, item)
            download_file(item, local_path)


# === Main ===
if __name__ == "__main__":
    print("=== Backing up Yandex.Disk ===")
    os.makedirs(LOCAL_DIR, exist_ok=True)
    init_log()
    recursive_download("")
    print("\n✅ Backup completed. Files saved to:", os.path.abspath(LOCAL_DIR))
    print("📘 Log saved to:", os.path.abspath(LOG_FILE))
