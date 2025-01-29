이 프로젝트는 YouTube 재생목록을 MP3 파일로 변환 및 다운로드하는 Python GUI 응용 프로그램입니다.

### install Windows
python을 3.7 버전 이상 설치하세요
```
python 3.7
```
다음 명령어를 실행하여 필요한 패키지를 설치하세요.
``` bash
pip install yt-dlp pydub tk
```
mp3 변환을 위해 ffmpeg 필요합니다.

[ffmpeg](https://ffmpeg.org/download.html) 다운로드 후 폴더에 배치하세요.

쿠키 파일 다운로드 방법
- Get cookies.txt 확장 프로그램을 크롬에 설치
- 유튜브에 로그인한 상태에서 https://www.youtube.com 방문
- 확장 프로그램 실행 → Export 클릭 → cookies.txt 다운로드
- 파일명을 cookies.txt로 변경후 폴더에 배치

### 실행
```
python app.py
```
재생목록의 링크를 입력하면 다운로드가 진행됩니다.
