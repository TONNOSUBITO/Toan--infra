---
name: video-analyzer
description: Guarda e analizza un video (file locale o URL) tramite Gemini Vision, frame per frame con audio. Usalo quando l'utente allega o cita un video e vuole capire cosa succede, trascriverlo, riassumerlo o fare il teardown di un ad/UGC/TikTok. Claude da solo non può vedere video.
argument-hint: <file.mp4|URL> [--mode general|ads] [--prompt "..."] [--fps N] [--model ...]
allowed-tools: Bash, Read
---

# Video Analyzer

Claude non vede i video nativamente: lo script invia il video a Gemini e stampa il report.

## Prerequisiti

- `pip install google-genai`
- `GEMINI_API_KEY` nell'ambiente (chiave gratuita: https://aistudio.google.com/apikey). Se manca, chiedila all'utente: non scriverla mai in file versionati.
- Solo per URL: `yt-dlp` (`pip install yt-dlp`)

## Uso

1. Scegli la modalità:
   - `general` (default): summary, scene con timestamp, audio/trascrizione, dettagli visivi, momenti chiave.
   - `ads`: teardown di ad/UGC/TikTok in 12 sezioni (formato, hook, target, pain point, angle, prodotto, proof, beat-by-beat, CTA, punti di forza, debolezze, pattern copiabili).
2. Esegui:

```bash
python3 skills/video-analyzer/scripts/analyze_video.py <file|URL> --mode ads
```

(Se installata globalmente: `~/.claude/skills/video-analyzer/scripts/analyze_video.py`.)

3. Presenta all'utente lo stdout. I log vanno su stderr.
4. Per fast-cut aggiungi `--fps 2`. Per domande specifiche usa `--prompt`.

## Regole

- Riporta solo ciò che il report contiene: niente nomi di creator o dialoghi inventati. Il prompt già vieta le allucinazioni; se l'audio è assente, dillo.
- Costo indicativo: ~0,30 $ ogni 30 min di video. Avvisa prima di analizzare video molto lunghi.
- Errori: chiave mancante → chiedila; 404 modello → `--model gemini-2.5-flash`; formato non supportato → mp4/mov/webm/avi/mpeg/mpg/wmv/3gp/flv.
