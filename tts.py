#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""口播稿 -> 配音 mp3（edge-tts，微软免费在线 TTS）

用法:
    python tts.py --file script.txt --out voice.mp3 --style news
    python tts.py --text "今天AI圈发生三件事" --out voice.mp3
"""
import argparse
import asyncio

import edge_tts

# 快捷音色：男声播报 / 女声知性 / 男声轻快
VOICES = {
    "news": "zh-CN-YunyangNeural",
    "news_f": "zh-CN-XiaoxiaoNeural",
    "lively": "zh-CN-YunxiNeural",
}


async def run(text: str, out: str, voice: str, rate: str):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(out)


def main():
    ap = argparse.ArgumentParser(description="edge-tts 口播配音")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", help="直接传口播稿文本")
    g.add_argument("--file", help="口播稿文本文件（utf-8）")
    ap.add_argument("--out", default="voice.mp3")
    ap.add_argument("--voice", default=None, help="指定 edge-tts 音色，覆盖 --style")
    ap.add_argument("--style", choices=VOICES.keys(), default="news",
                    help="快捷选择音色（默认 news 男声播报）")
    ap.add_argument("--rate", default="+4%", help="语速，如 +4% / -10%")
    args = ap.parse_args()

    voice = args.voice or VOICES[args.style]
    text = open(args.file, encoding="utf-8").read() if args.file else args.text

    asyncio.run(run(text, args.out, voice, args.rate))
    print("OK ->", args.out, "| voice:", voice, "| rate:", args.rate)


if __name__ == "__main__":
    main()
