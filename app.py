import os
import re
import threading
import uuid
from pathlib import Path

import instaloader
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
DOWNLOAD_DIR = Path(os.environ.get("MAYANK_DROID_DOWNLOAD_DIR", Path.home() / "MAYANK_DROID_Downloads"))
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")
jobs = {}
jobs_lock = threading.Lock()
USERNAME_RE = re.compile(r"^[A-Za-z0-9._]{1,30}$")

def set_job(job_id, **values):
    with jobs_lock:
        jobs.setdefault(job_id, {}).update(values)

def make_loader():
    return instaloader.Instaloader(
        dirname_pattern=str(DOWNLOAD_DIR / "{target}"),
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=True,
        save_metadata=True,
        compress_json=True,
    )

def prepare_session(loader):
    session_file = os.environ.get("INSTAGRAM_SESSIONFILE")
    session_user = os.environ.get("INSTAGRAM_SESSION_USERNAME")
    if session_file and session_user:
        loader.context.load_session_from_file(session_user, session_file)
        return True
    return False

def download_worker(job_id, username, options):
    set_job(job_id, status="running", message=f"Downloading {options} for @{username}…")
    try:
        loader = make_loader()
        session_loaded = prepare_session(loader)
        profile = instaloader.Profile.from_username(loader.context, username)

        if options == "posts":
            loader.download_profiles({profile}, posts=True, profile_pic=False, stories=False, highlights=False)
        elif options == "stories":
            if not session_loaded:
                raise RuntimeError("Stories require an authenticated Instaloader session. Configure INSTAGRAM_SESSIONFILE and INSTAGRAM_SESSION_USERNAME.")
            loader.download_profiles({profile}, posts=False, profile_pic=False, stories=True, highlights=False)
        elif options == "highlights":
            if not session_loaded:
                raise RuntimeError("Highlights require an authenticated Instaloader session. Configure INSTAGRAM_SESSIONFILE and INSTAGRAM_SESSION_USERNAME.")
            loader.download_profiles({profile}, posts=False, profile_pic=False, stories=False, highlights=True)
        elif options == "all":
            if session_loaded:
                loader.download_profiles({profile}, posts=True, profile_pic=True, stories=True, highlights=True)
            else:
                loader.download_profiles({profile}, posts=True, profile_pic=True, stories=False, highlights=False)
                set_job(job_id, message="Posts completed. Stories/highlights were skipped because no authenticated session is configured.")
        else:
            raise ValueError("Invalid download option.")

        set_job(job_id, status="done", message=f"Finished downloading @{username}. Files are in {DOWNLOAD_DIR}.")
    except Exception as exc:
        set_job(job_id, status="error", message=str(exc))

@app.get("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")

@app.post("/api/download")
def download():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip().lstrip("@")
    options = str(data.get("options", "posts")).strip().lower()
    if not USERNAME_RE.fullmatch(username):
        return jsonify(error="Enter a valid Instagram username."), 400
    if options not in {"posts", "stories", "highlights", "all"}:
        return jsonify(error="Invalid download option."), 400
    job_id = uuid.uuid4().hex
    set_job(job_id, status="queued", message="Queued.")
    threading.Thread(target=download_worker, args=(job_id, username, options), daemon=True).start()
    return jsonify(job_id=job_id, status="queued", message=f"Download queued for @{username}.")

@app.get("/api/status/<job_id>")
def status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
    if not job:
        return jsonify(error="Job not found."), 404
    return jsonify(job)

@app.get("/health")
def health():
    return jsonify(ok=True, app="MAYANK DROID Instaloader")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
