import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Video Downloader", page_icon="📥")

st.title("📥 YouTube & Instagram Downloader")
st.write("Download videos from YouTube 🎥 and Instagram 📸")

url = st.text_input("🔗 Paste video / reel / post URL")

platform = st.selectbox(
    "🌐 Select platform",
    ["Auto Detect", "YouTube", "Instagram"]
)

quality = st.selectbox(
    "🎞️ Select quality (YouTube only)",
    ["Best available", "720p", "480p", "360p"]
)

download_btn = st.button("⬇️ Download")

if download_btn and url:
    with st.spinner("Downloading... ⏳"):
        try:
            ydl_opts = {
                "outtmpl": "%(title)s.%(ext)s",
                "merge_output_format": "mp4"
            }

            # Apply quality only for YouTube
            if platform != "Instagram" and quality != "Best available":
                ydl_opts["format"] = f"bestvideo[height<={quality[:-1]}]+bestaudio/best"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            st.success("✅ Download completed!")
            st.write(f"📁 Saved as: **{os.path.basename(filename)}**")

        except Exception as e:
            st.error(f"❌ Error: {e}")
