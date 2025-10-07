# ☁️ Yandex.Disk Backup with Python (via WebDAV)

> A simple Python tool to download **all your files, photos, and videos from Yandex.Disk** — preserving folder structure, Cyrillic filenames, and progress tracking.  
> Originally created to back up an entire archive before canceling a Yandex.Disk subscription and migrating to another cloud provider.

[The link to my article on Medium](https://medium.com/gitconnected/how-i-backed-up-my-entire-yandex-disk-archive-with-python-before-canceling-my-subscription-111b4a9ddec3)

---

## 🧭 Overview

Yandex.Disk offers no easy “Export all” feature for users with large archives.  
This script connects directly to Yandex.Disk via **WebDAV**, recursively lists all directories, and downloads every file locally — with **progress bars, logging, and resume support**.

Perfect for:
- Migrating to another cloud (Google Drive, Dropbox, Mega, etc.)
- Creating a full local mirror of your data
- Automated or scheduled backups

---

## ⚙️ Features

✅ Full folder structure preserved  
✅ Works with Cyrillic and special characters  
✅ Progress bars for each file  
✅ CSV log (`backup_log.csv`) with file size, status, and time  
✅ Compatible with 2FA (application passwords)  
✅ Cross-platform: Windows, macOS, Linux  

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your_username>/yadisk-backup.git
cd yadisk-backup
```

### 2️⃣ Install dependencies
```bash
pip install requests tqdm
```

## 🚀 Usage
### 1️⃣ Edit the script

Open yadisk_backup.py and update your credentials:
```
YANDEX_LOGIN = "your_login@yandex.ru"
YANDEX_PASSWORD = "your_password_or_app_password"
```

🔐 If you have 2-factor authentication, create a password for applications at
https://id.yandex.ru/security/app-passwords

### 2️⃣ Run the backup
```
python yadisk_backup.py
```

The script will:
- Connect to https://webdav.yandex.ru/
- Recursively traverse all folders
- Download each file to the local directory YandexDiskBackup/
- Log every action to backup_log.csv

## 🧾 Example log output

backup_log.csv is created automatically:

| file_path                              | size_bytes | status    | time_sec |
|----------------------------------------|-------------|------------|-----------|
| Документы/Отчеты/2024/annual.pdf       | 186452      | OK         | 2.37      |
| Фото/Путешествия/IMG_001.jpg           | 523947      | OK         | 1.58      |
| Фото/Путешествия/IMG_002.jpg           | 0           | HTTP 404   | 0.00      |

📂 Folder Structure Example
```
YandexDiskBackup/
├── Documents/
│   └── Reports/
│       └── 2024/
│           └── Annual.pdf
├── Photos/
│   └── Travel/
│       └── Turkey/
│           └── IMG_001.jpg
└── Videos/
    └── Family/
        └── 2020_Birthday.mp4
```
## ⚡ Optional Enhancements

You can easily extend this script:
- 🧵 Multithreading with ThreadPoolExecutor to speed up downloads
- 🔁 Resume interrupted backups (skip existing files)
- 🕓 Scheduling with cron or Windows Task Scheduler

Example snippet for skipping existing files:
```
if os.path.exists(local_path):
    continue
```

## 🧠 Why This Project Exists

“I needed to download my entire Yandex.Disk archive before canceling my subscription and moving to a more convenient cloud storage.”

This project was created out of a real-world need: to take back control of one’s own data, without relying on vendor-locked sync clients or limited export options.

## 🪪 License

This project is released under the **YADISK-BACKUP License** (Version 1.0, October 2025).  
It is **free for personal and educational use**, but **commercial use is prohibited** without prior written permission from the author.

You may:
- ✅ Use, copy, and modify the software for personal or academic purposes  
- ✅ Share or adapt the code for learning and research  
- 🚫 Not sell, license, or integrate it into any paid product or service without consent  

For full terms, see the [LICENSE](LICENSE) file.  
For commercial licensing inquiries, please email **iskander.akhmetov@gmail.com**.  
Attribution is appreciated 🙌

## 💬 Author

Iskander Akhmetov
PhD in Computer Science
📍 Almaty, Kazakhstan
[🌐 LinkedIn](https://www.linkedin.com/in/iskander-akhmetov-ba8a9a1a/)
[✉️ iskander.akhmetov@gmail.com](mailto:iskander.akhmetov@gmail.com)

## ☕ Support & Feedback

If you find this useful:
- ⭐ Star the repository
- 🐛 Report issues or suggest improvements
- ☕ [Donate](https://www.paypal.com/paypalme/AkhmetovIskander) 

Let’s make cloud migration simpler, safer, and open-source 🚀
