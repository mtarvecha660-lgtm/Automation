# Mobile AI YouTube Clipper

## Flow
Telegram `/clip URL` → n8n → GitHub Actions → yt-dlp → Whisper → Gemini → FFmpeg → Telegram

## Setup
1. Create a GitHub repository and upload this folder's files.
2. Add repository Actions secrets:
   - `TELEGRAM_BOT_TOKEN`
   - `GEMINI_API_KEY`
3. Import `n8n-mobile-youtube-clipper.json` into n8n.
4. Create n8n credentials named:
   - `Telegram Bot`
   - `GitHub Actions Token`
5. In `Start GitHub Clipper`, replace `YOUR_GITHUB_OWNER/YOUR_GITHUB_REPO`.
6. Activate the n8n workflow.
7. Message your Telegram bot: `/clip https://www.youtube.com/watch?v=...`

Use only content you have permission or applicable rights to download and reuse.
