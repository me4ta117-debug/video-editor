import os
import subprocess
from pathlib import Path

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

SPEED = 1.05
ZOOM = 1.06
BRIGHTNESS = 0.03
CONTRAST = 1.08
SATURATION = 1.12
WATERMARK_TEXT = "my page"


def process_video(input_path: Path, output_path: Path):
    vf_filter = (
        f"scale=iw*{ZOOM}:ih*{ZOOM},"
        f"crop=iw/{ZOOM}:ih/{ZOOM},"
        f"eq=brightness={BRIGHTNESS}:contrast={CONTRAST}:saturation={SATURATION},"
        f"setpts={1 / SPEED}*PTS,"
        f"drawtext=text='{WATERMARK_TEXT}':"
        f"x=20:y=20:"
        f"fontsize=28:"
        f"fontcolor=white@0.75:"
        f"box=1:"
        f"boxcolor=black@0.25"
    )

    af_filter = f"atempo={SPEED}"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vf", vf_filter,
        "-af", af_filter,
        "-map_metadata", "-1",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_path)
    ]

    subprocess.run(command, check=True)


def main():
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    video_extensions = [".mp4", ".mov", ".mkv", ".avi"]

    files = [
        file for file in Path(INPUT_FOLDER).iterdir()
        if file.suffix.lower() in video_extensions
    ]

    if not files:
        print("Положи видео в папку input")
        input("Нажми Enter для выхода...")
        return

    for file in files:
        output_file = Path(OUTPUT_FOLDER) / f"edited_{file.stem}.mp4"
        print(f"Обработка: {file.name}")

        try:
            process_video(file, output_file)
            print(f"Готово: {output_file}")
        except Exception as e:
            print(f"Ошибка при обработке {file.name}: {e}")

    print("Все видео обработаны.")
    input("Нажми Enter для выхода...")


if __name__ == "__main__":
    main()
