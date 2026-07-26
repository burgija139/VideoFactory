# 🎬 Chess Video AI Generator

A system that generates viral chess short-form videos using AI (Gemini), chess engine logic, and automated video rendering pipeline.

---

## 🚀 Features

- ♟ Chess puzzle processing (python-chess)
- 🎬 Automated video generation (FFmpeg pipeline)
- 🧠 AI-driven video planning (Google Gemini)
- 📝 Structured timeline generation (Pydantic schema)
- 🎵 Audio event synchronization
- 🗄 PostgreSQL integration for data storage
- 🎨 Custom video overlays (Pillow rendering system)

---

# 🧱 Architecture

AIContextGenerator (Gemini)
↓
VideoPlanSchema (Pydantic)
↓
ChessVideoBuilder
├── BoardRenderer (SVG → PNG)
├── OverlayRenderer (Pillow UI layer)
├── AudioBuilder (numpy wave synthesis)
├── FFmpeg video stream (frames → mp4)
└── Post-processing merge (audio + video)
↓
Final MP4 Output
↓
PostgreSQL (optional storage)

---

# ⚙️ Features

## ♟ Chess Engine

- Uses `python-chess`
- Supports FEN parsing
- Move validation and game simulation
- Detects:
  - captures
  - check
  - castling

---

## 🧠 AI Director (Gemini)

AI generates:

- video title
- pacing strategy
- intro duration
- full timeline (intro → timer → moves → ending)
- retention hooks

Enforced via structured schema:

- Pydantic validation
- strict timeline rules
- max 8-word captions
- forced viral pacing logic

---

## 🎬 Video Rendering

- FFmpeg pipe streaming (real-time frame encoding)
- 1080x1920 vertical format (TikTok / Shorts)
- Gaussian blurred chess background
- dynamic overlays (rating, title, text)

---

## 🎨 Overlay System

Built with Pillow:

- dynamic text rendering
- chessboard overlay
- timer circle animation
- pause/reveal screens
- thematic coloring per video type

---

## 🔊 Audio System

- numpy-based audio mixing
- event-driven sound system:
  - move
  - capture
  - check
  - castle
- precise timestamp synchronization

---

## 🗄 Database (PostgreSQL)

Used for:

- storing generated puzzles
- storing video metadata
- tracking processing history

---

# 📦 Installation

## 1. Clone repository

```bash
git clone <repo-url>
cd chess-video-ai
```

## 2. Install Python dependecies

```bash
pip install -r requirements.txt
```

## 3. Install system dependencies

-Linux

```bash
sudo apt install ffmpeg
```

-Mac

```bash
brew install ffmpeg
```

-Windows
Download FFmpeg
Add to PATH

---

# Environment setup

- GEMINI_API_KEY=your_api_key_here

---

# ▶️ Running the project

```bash
python main.py
```

---

# ⚠️ Notes

- Requires FFmpeg installed
- Requires valid Gemini API key
- Designed for vertical video format (TikTok / YouTube Shorts)
- CPU-only compatible (no GPU required)
