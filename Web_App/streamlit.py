import streamlit as st
import yt_dlp
import os
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

st.set_page_config(page_title="Video Downloader", page_icon="📥")

st.title("📥 YouTube & Instagram Downloader")
st.caption("Live process & error logs visible below 🧾")

url = st.text_input("🔗 Paste YouTube / Instagram URL")

platform = st.selectbox(
    "🌐 Platform",
    ["Auto Detect", "YouTube", "Instagram"]
)

quality = st.selectbox(
    "🎞️ Quality (YouTube only)",
    ["Best available", "720p", "480p", "360p"]
)

download_btn = st.button("⬇️ Start Download")

log_box = st.empty()

def log_writer(text):
    existing = log_box.session_state.get("logs", "")
    updated = existing + text
    log_box.session_state["logs"] = updated
    log_box.text_area("📜 Download Logs", updated, height=300)

if download_btn and url:
    log_box.session_state["logs"] = ""
    log_writer("🚀 Starting download process...\n")

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    try:
        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "progress_hooks": [
                lambda d: log_writer(
                    f"⬇️ {d.get('status', '').upper()} | "
                    f"{d.get('_percent_str', '')} | "
                    f"{d.get('_speed_str', '')}\n"
                )
            ],
        }

        if platform != "Instagram" and quality != "Best available":
            ydl_opts["format"] = f"bestvideo[height<={quality[:-1]}]+bestaudio/best"

        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

        log_writer(stdout_buffer.getvalue())

        if stderr_buffer.getvalue():
            log_writer("\n⚠️ STDERR OUTPUT:\n")
            log_writer(stderr_buffer.getvalue())

        st.success("✅ Download finished!")
        st.write(f"📁 File saved as: **{os.path.basename(filename)}**")

    except Exception as e:
        log_writer("\n❌ ERROR OCCURRED:\n")
        log_writer(str(e) + "\n")
        st.error("Download failed ❌")

