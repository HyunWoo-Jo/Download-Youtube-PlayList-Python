import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
import sys
import threading
import re

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):  # 패키징된 경우
        ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
    else:  # 개발 환경
        ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg.exe')
    return ffmpeg_path

def sanitize_filename(filename):
    """파일명에서 허용되지 않는 문자 제거"""
    return re.sub(r'[\/:*?"<>|]', '_', filename)

def download_youtube_playlist_as_mp3(playlist_url, output_dir):
    ffmpeg_path = get_ffmpeg_path()
    AudioSegment.converter = ffmpeg_path
    AudioSegment.ffmpeg = ffmpeg_path

    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # ✅ 제목으로 저장
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',  # ✅ 쿠키 파일 적용
        'noplaylist': False,  # ✅ 재생목록 전체 다운로드 허용
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=True)
        
        if 'entries' not in playlist_info:
            raise ValueError("재생목록을 가져오는 데 실패했습니다.")
        
        downloaded_files = []
        
        for video in playlist_info['entries']:
            if not video:
                continue

            video_title = sanitize_filename(video.get('title', 'output'))  # ✅ 제목 필터링
            output_file = os.path.join(output_dir, f"{video_title}.mp3")

            if os.path.exists(output_file):
                downloaded_files.append(output_file)

    return downloaded_files

def start_download():
    playlist_url = url_entry.get()
    output_dir = filedialog.askdirectory()
    if output_dir:
        download_button.pack_forget()
        status_var.set("재생목록 다운로드 중...")
        root.update_idletasks()

        threading.Thread(target=download_thread, args=(playlist_url, output_dir)).start()

def download_thread(playlist_url, output_dir):
    try:
        mp3_files = download_youtube_playlist_as_mp3(playlist_url, output_dir)
        if mp3_files:
            status_var.set("다운로드 완료!")
            messagebox.showinfo("성공", f"{len(mp3_files)}개의 MP3 파일이 저장되었습니다!")
        else:
            status_var.set("오류 발생")
            messagebox.showerror("오류", "MP3 변환 중 오류가 발생했습니다.")
    except Exception as e:
        status_var.set("오류 발생")
        messagebox.showerror("오류", f"다운로드 중 오류가 발생했습니다: {e}")
    finally:
        download_button.pack(pady=20)

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("YouTube Playlist to MP3")

# URL 입력 필드
tk.Label(root, text="YouTube 재생목록 URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# 다운로드 버튼
download_button = tk.Button(root, text="Download Playlist", command=start_download)
download_button.pack(pady=20)

# 상태 메시지 레이블
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var)
status_label.pack(pady=5)

# Tkinter 이벤트 루프 시작
root.mainloop()