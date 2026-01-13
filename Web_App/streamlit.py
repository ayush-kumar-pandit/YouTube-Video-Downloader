import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Video Downloader", page_icon="📥")

st.title("📥 YouTube & Instagram Downloader")
st.caption("Live process & error logs 🧾")

url = st.text_input("🔗 Paste YouTube / Instagram URL")

quality = st.selectbox(
    "🎞️ Quality (YouTube only)",
    ["Best available", "720p", "480p", "360p"]
)

download_btn = st.button("⬇️ Start Download")

# Initialize session state
if "logs" not in st.session_state:
    st.session_state.logs = ""

log_placeholder = st.empty()

def log_writer(message):
    st.session_state.logs += message
    log_placeholder.text_area(
        "📜 Download Logs",
        st.session_state.logs,
        height=300
    )

if download_btn and url:
    st.session_state.logs = ""
    log_writer("🚀 Starting download...\n")

    try:
        def progress_hook(d):
            if d["status"] == "downloading":
                log_writer(
                    f"⬇️ {d.get('_percent_str','')} | "
                    f"{d.get('_speed_str','')} | "
                    f"{d.get('_eta_str','')} ETA\n"
                )
            elif d["status"] == "finished":
                log_writer("✅ Download finished, merging...\n")

        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "progress_hooks": [progress_hook],
        }

        if quality != "Best available":
            ydl_opts["format"] = f"bestvideo[height<={quality[:-1]}]+bestaudio/best"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        log_writer("🎉 All done!\n")
        st.success("Download completed ✅")
        st.write(f"📁 Saved as: **{os.path.basename(filename)}**")

    except Exception as e:
        log_writer(f"\n❌ ERROR:\n{e}\n")
        st.error("Download failed ❌")
