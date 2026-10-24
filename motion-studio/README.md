# motion-studio

Pipeline per far creare a Claude Code video motion-graphics in codice (HTML + canvas → Playwright → ffmpeg → MP4).
Basata sulla guida "How to Build a Motion Design Studio With Opus 5.5" (vedi `../docs/analisi-risorse-reel.md`),
con un fix: `render.mjs` serve la cartella su `127.0.0.1` invece di `file://`, perché Chromium blocca gli
import ES module da `file://` e la versione originale falliva con `window.seek is not a function`.

## Setup (Mac)

```bash
brew install node ffmpeg python
pip install numpy librosa soundfile      # solo se usi beats.py
cd motion-studio && npm install && npx playwright install chromium
npm run test-render                       # → out/silent.mp4 di 3 secondi con la demo
```

## Uso

Apri Claude Code dentro `motion-studio/`. Legge `CLAUDE.md` (regole della casa) e la skill `motion-reel`.
Poi: `/motion-reel per [URL], 20s, verticale, riferimento ./refs/frame.png`

| File | Cosa fa |
|---|---|
| `CLAUDE.md` | regole: render puro in funzione di t, look vietati, loop di autocritica |
| `render.mjs` | `node render.mjs --fps 60 --dur 15 --sub 4 [--w 1920 --h 1080]` |
| `lib/motion.js` | molle (spring) e `track()` per animazioni "costose" |
| `beats.py` | `python beats.py song.wav > beats.json` → griglia dei beat |
| `.claude/skills/motion-reel/` | la skill che fa tutto con una frase |
| `index.html` | demo minima, sostituita da Claude a ogni video |
