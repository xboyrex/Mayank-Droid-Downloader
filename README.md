# MAYANK DROID — Instaloader Edition

A MAYANK DROID branded web wrapper around the bundled **Instaloader** source.

> This is an independent project. It is not affiliated with, authorized by, or endorsed by Instagram.

## Included

- Bundled Instaloader source
- MAYANK DROID dark Web UI
- Flask API wrapper
- Background download jobs with status polling
- Public profile posts without login
- Optional server-side Instaloader session for stories/highlights
- `/health` endpoint
- Reproducible ZIP builder

## Legal / license

The bundled Instaloader source remains under its original MIT license and copyright notices. Do not remove upstream notices.

Use this project only for media you are authorized to save. Respect Instagram's Terms of Service and applicable copyright/privacy law.

## Quick start

Requirements: Python 3.9+.

```bash
python -m venv .venv
```

Linux/macOS/Termux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Health check:

```bash
curl http://127.0.0.1:5000/health
```

## Optional authenticated session

Instaloader requires an authenticated session for stories and highlights. This wrapper does **not** collect Instagram passwords through the Web UI.

Configure an already-created Instaloader session on the server:

```text
INSTAGRAM_SESSION_USERNAME=your_instagram_username
INSTAGRAM_SESSIONFILE=/absolute/path/to/session-file
```

Never commit session files, cookies, passwords, or tokens.

## Download directory

Default:

```text
~/MAYANK_DROID_Downloads
```

Override:

```text
MAYANK_DROID_DOWNLOAD_DIR=/path/to/downloads
```

## Build the ZIP

```bash
python build_zip.py
```

Output:

```text
MAYANK_DROID_Instaloader.zip
```

## Ecosystem

- https://otaku-hub-pro.pages.dev
- https://onyx-services.pages.dev
- https://mayank-droid.pages.dev
- https://portfolio-hbo.pages.dev/

### Connect

- https://t.me/OnyxHub7
- https://t.me/RoranoaxZORO
- https://t.me/MayankDroid7
- https://youtube.com/@mayankdroid
- https://youtube.com/@onyxdroid89
- https://www.instagram.com/mayank.droid/
- https://www.instagram.com/mayank.zx7/

© MAYANK DROID TEAM
