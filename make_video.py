#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配音 mp3 + 口播稿 -> 竖屏口播视频（1080x1920）+ 逐句字幕

用法:
    python make_video.py --audio voice.mp3 --script script.txt \
        --bg host.jpg --title "AI 日报" --out out.mp4
无 --bg 时用深色纯色背景。

依赖: ffmpeg（需自行安装并加入 PATH）
"""
import argparse
import os
import re
import subprocess
import sys

# 字幕字体（Windows 微软雅黑）；其他系统请改为本机中文字体路径
FONT = "C\\:/Windows/Fonts/msyhbd.ttc"


def split_segments(text: str, maxlen: int = 16):
    """按句切分，单段不超过 maxlen 字，避免竖屏溢出。"""
    segs = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        for s in re.split(r"(?<=[。！？])", para):
            s = s.strip()
            if not s:
                continue
            while len(s) > maxlen:
                segs.append(s[:maxlen])
                s = s[maxlen:]
            if s:
                segs.append(s)
    return segs


def audio_duration(ffmpeg: str, path: str) -> float:
    r = subprocess.run([ffmpeg, "-i", path, "-f", "null", "-"],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="ignore")
    m = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        sys.exit("[X] 无法解析音频时长，请确认 ffmpeg 已安装")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main():
    ap = argparse.ArgumentParser(description="口播视频合成")
    ap.add_argument("--audio", required=True, help="配音 mp3")
    ap.add_argument("--script", required=True, help="口播稿 txt，utf-8")
    ap.add_argument("--bg", help="背景图（可选，主播形象照）")
    ap.add_argument("--title", default="AI 日报", help="顶部标题条文字")
    ap.add_argument("--out", default="out.mp4")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    args = ap.parse_args()

    dur = audio_duration(args.ffmpeg, args.audio)
    text = open(args.script, encoding="utf-8").read()
    segs = split_segments(text)
    per = dur / len(segs)
    print(f"[OK] 时长 {dur:.1f}s，字幕 {len(segs)} 段，每段 {per:.2f}s")

    filters = []
    for i, s in enumerate(segs):
        t = s.replace(":", "\\:").replace("'", "’").replace('"', "”")
        filters.append(
            f"drawtext=fontfile='{FONT}':text='{t}'"
            f":fontcolor=white:fontsize=52:line_spacing=16"
            f":box=1:boxcolor=black@0.45:boxborderw=24"
            f":x=(w-text_w)/2:y=h*0.70"
            f":enable='between(t,{i*per:.3f},{(i+1)*per:.3f})'"
        )
    vf = ",".join(filters)

    if args.bg and os.path.exists(args.bg):
        bg_input = ["-loop", "1", "-i", args.bg, "-t", "%.2f" % dur]
        bg_filter = ("scale=1080:1920:force_original_aspect_ratio=increase,"
                     "crop=1080:1920,gblur=sigma=7,eq=brightness=-0.12:saturation=0.9,format=yuv420p")
    else:
        bg_input = ["-f", "lavfi", "-i", f"color=c=0x0b1220:s=1080x1920:d=%.2f" % dur]
        bg_filter = "format=yuv420p"

    title = args.title
    cmd = [
        args.ffmpeg, "-y", *bg_input, "-i", args.audio,
        "-vf", bg_filter + "," + vf + (
            f",drawtext=fontfile='{FONT}':text='{title}':"
            f"fontcolor=white@0.85:fontsize=40:x=(w-text_w)/2:y=120"
        ),
        "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", args.out,
    ]
    print(">> 合成视频 ...")
    p = subprocess.run(cmd, capture_output=True, text=True,
                      encoding="utf-8", errors="ignore")
    if not os.path.exists(args.out):
        sys.exit("[X] 合成失败: " + p.stderr[-1500:])
    print("[OK] 成片:", args.out)


if __name__ == "__main__":
    main()
