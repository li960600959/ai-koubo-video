# ai-koubo-video · 用 Python 做竖屏口播短视频

一套**零成本、可复用**的口播视频制作 SOP：写稿 → edge-tts 免费配音 → ffmpeg 合成竖屏成片（1080×1920）+ 逐句字幕。适合自媒体做 AI 资讯 / 知识口播类内容。

## 效果
- 配音：微软 edge-tts 在线音色，**免费**，男声播报腔（默认 `zh-CN-YunyangNeural`）
- 成片：竖屏 1080×1920，背景图虚化压暗 + 逐句字幕精确对齐 + 顶部标题条
- 两条命令出片，无需剪映手动拖拽

## 环境依赖
1. Python 3.10+
2. `pip install -r requirements.txt`（主要是 `edge-tts`，需 ≥7.3.1；旧版会被微软鉴权挡 403）
3. ffmpeg：自行下载并加入系统 PATH（[官网 https://ffmpeg.org](https://ffmpeg.org)）

## 快速开始

```bash
# 1) 生成配音（口播稿见 example_script.txt）
python tts.py --file example_script.txt --out voice.mp3 --style news

# 2) 合成视频（可选 --bg 你的主播形象照）
python make_video.py --audio voice.mp3 --script example_script.txt --title "AI 日报" --out out.mp4
```

## 参数说明
- `tts.py`
  - `--style news` 男声播报 / `news_f` 女声知性 / `lively` 男声轻快
  - `--rate +4%` 语速微调；`--voice` 可指定任意 edge-tts 音色
- `make_video.py`
  - `--bg 图片路径` 用主播照做虚化背景；不传则用深色纯色背景
  - `--title` 顶部标题条文字
  - 字幕字体默认 Windows 微软雅黑 `C:/Windows/Fonts/msyhbd.ttc`，其他系统请改脚本里的 `fontfile`

## 工作流建议（SOP）
1. 选题：找「反常识 / 故事 / 数字」角度，控制 200–260 字（约 45–65 秒）
2. 写稿：前 3 秒钩子 → 故事递进 → 金句 → 关注引导
3. 配音 + 成片：上面两条命令
4. 发布：导出 mp4 后上传视频号 / 抖音

## 注意事项
- edge-tts 是在线服务，个人使用免费；规模化商业变现前建议换 ElevenLabs 或本地开源方案。
- 字幕按「句」切分，单段默认 ≤16 字，避免竖屏溢出。
- 发布频率注意平台规则，避免被判定营销号。
