# FFmpeg(Video transform)
- [FFmpeg Site](https://www.ffmpeg.org/)는 Video을 Audio로 변환시켜주는 CLI 도구이다.
- `FFmpeg -i {video path}.mp4 -vn {audio path}.mp3` : `cmd`에서 해당 명령어를 통해 video를 audio로 바꾸어 준다. `-vn`은 영상을 무시하고 음성만 추출하라는 의미이다.
- `python`에서 `subprocess`를 통해 cmd의 명령어를 실행 시킬 수 있다.
- `import subprocess`로 `subprocess`를 불러 올 수 있다.
```python
import subprocess

def extract_audio_from_video(video_path, audio_path):
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-vn",
        audio_path,
    ]
    subprocess.run(command)
    
extract_audio_from_video("./files/Bible_summary.mp4", "./files/Bible_audio.mp3")
```
# Pydub(Audio Splite)
- `pydub`은 Audio을 List 형식으로 다룰 있도록 해주는 Module이다.
- `from pydub import AudioSegment`로 불러 올 수 있다.
- 이를 이용해 audio를 `Track 단위`로 나눌 수도 있고 새로운 Track을 가져다 붙일 수도 있는 등 Audio를 여러가지로 다룰 수 있다.
- `AudioSegment.from_mp3({audio_path})` : `audio_path` 경로의 audio를 불러 올 수 있다.
```python
from pydub import AudioSegment
track = AudioSegment.from_mp3("./files/Bible_audio.mp3")
```
- `.duration_seconds` : audio의 전체 `seconds`를 알 수 있다.
```python
track.duration_seconds
```
- `track[start_time:end_time]` : AudioSegment을 사용하면 `List` 형식으로 track을 분리 할 수 있다. track의 시간은 **MilliSecond** 단위로 계산한다.
- `.export(f"./files/chunks/chunk_{i}.mp3", format="mp3")` : 나누어진 Track을 다른 파일로 저장한다.
```python
import math
from pydub import AudioSegment

track = AudioSegment.from_mp3("./files/Bible_audio.mp3")

ten_minutes = 10 * 60 * 1000

chunks = math.ceil(len(track) / ten_minutes)

for i in range(chunks):
    start_time = i * ten_minutes
    end_time = (i+1) * ten_minutes
    chunk = track[start_time:end_time]
    chunk.export(f"./files/chunks/chunk_{i}.mp3", format="mp3")
```
- audio을 그냥 나누게 되면 파일과 파일 사이의 `음성이 끊겨 인식이 어려워진다.` 따라서 Splitter 처럼 각각의 audio에 **overlap을 설정하여 문장이 끊기지 않도록 한다.**
```python
def cut_audio_in_chunks(audio_path, chunk_size, chunks_folder):
    track = AudioSegment.from_mp3(audio_path)
    chunk_overlap = 10 * 1000 # overlap_size = 10 seconds
    chunk_len = chunk_size * 60 * 1000 - chunk_overlap
    chunks = math.ceil(len(track) / chunk_len)
    for i in range(chunks):
        start_time = i * chunk_len
        end_time = (i+1) * chunk_len + chunk_overlap
        chunk = track[start_time:end_time]
        chunk.export(f"./{chunks_folder}/chunk_{i}.mp3", format="mp3")
        
cut_audio_in_chunks("./files/Bible_audio.mp3", 10, "./files/chunks")
```
# Glob(Search files)
- `glob`은 디렉토리 내부의 파일을 검색할 수 있도록 해주는 `Module`이다.
 - `glob.glob("{dic_path}}*.mp3")` : `dic_path` 에 있는 mp3 파일을 모두 검색해 list화 시켜준다. 단, 불러온 파일을 **순서대로 담아주진 않기 때문에 이를 `sort` 시켜주어야 한다.**
```python
import glob
files = glob.glob("./files/chunks/*.mp3")
files.sort()
```
# Whisper(Audio transform)
- `Whisper`은 `Open AI`에서 만든 `Audio Transcribe Model`이다.
- `openai.Audio.transcribe({model_name}, open.{file_path, "rb"}, language="{language}")`: 해당 명령어를 통해 `Open AI Audio Transcribe Model`을 이용해 `Audio Transcribe` 결과 값을 만들 수 있다.
- `Whisper`의 결과물은 `Json` 형태로 나오기 때문에 `trsanscribe` 된 내용을 얻을려면 결과 값의`["text"]` 값을 가져오면 된다.
- `Whisper-1`의 `Input` Size는 최대 10분이기 때문에 **audio file을 10분 간격으로 분할하는 작업**이 필요하다.
```python
import openai

transcipts = openai.Audio.transcribe(
    "whisper-1",
    open("./files/chunks/chunk_0.mp3", "rb"),
    language="ko",
)

print(transcipts["text"])
```
- `glob`로 mp3 files을 찾고 Whisper-1로 모든 mp3를 text로 변환 그 결과값을 하나의 txt로 만들어 저장하면 **Audio file을 txt로 변환 할 수 있다.**
- 이 과정을 `with`을 사용하여 `mp3 file`과 `text file`을 지정 후 진행하는 것이 편리하다.
- `open()`에서 `"a"`는 append mode로 결과 값들을 이어서 적어준다.
```python
import openai
import glob

def transcribe_chunks(chunk_folder, destination):
    files = glob.glob(f"{chunk_folder}/*.mp3")
    files.sort()
    for file in files:
        with open(file, "rb") as audio_file, open(destination, "a") as text_file:
            transcipts = openai.Audio.transcribe(
                "whisper-1",
                audio_file,
                language="ko",
            )
            text_file.write(transcipts["text"])
  
transcribe_chunks("./files/chunks", "./files/chunks/transcipts.txt")
```