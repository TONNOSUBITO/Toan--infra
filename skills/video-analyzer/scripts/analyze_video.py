#!/usr/bin/env python3
"""Analizza un video (file o URL) con Gemini. Report markdown su stdout, log su stderr.

Uso: analyze_video.py <file|URL> [--mode general|ads] [--prompt "..."] [--fps N] [--model ...]
Env: GEMINI_API_KEY
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    sys.exit("ERROR: google-genai non installato. Esegui: pip install google-genai")

RULES = """REGOLE DI ACCURATEZZA (prima di tutto):
1. Riporta solo ciò che è realmente nel video. Non inferire né riempire con contenuti plausibili.
2. Non inventare mai nome di creator, narratore o speaker. Se non è mostrato o detto, dillo.
3. Non inventare voiceover o dialoghi. Se l'audio è assente o silenzioso scrivi "Nessun parlato rilevato".
4. Distingui ciò che VEDI da ciò che INFERISCI, e marca le inferenze con "(inferito)".
5. Usa timestamp MM:SS. Quando sei incerto, dillo."""

PROMPTS = {
    "general": f"""Analizza questo video e rispondi in markdown con queste sezioni.

{RULES}

## Riassunto
2-3 frasi su cosa accade realmente.
## Scene con timestamp
Per ogni scena/taglio: contenuto a schermo, azioni, testo visibile verbatim.
## Audio
Trascrizione verbatim con timestamp, oppure nota onesta (silenzio, solo musica, rumore ambientale).
## Dettagli visivi
Testi, UI, prodotti, brand, persone (descritte, mai nominate se non esplicito).
## Momenti chiave
3-7 punti `[MM:SS] descrizione`.""",
    "ads": f"""Fai il teardown di questo video pubblicitario/UGC in markdown con ESATTAMENTE queste 12 sezioni.

{RULES}

## 1. Formato e stile di produzione (tipo, durata, setup)
## 2. Hook (primi 3 secondi: cosa si vede e si dice, verbatim)
## 3. Formula (perché funziona, struttura narrativa)
## 4. Target audience
## 5. Pain point e desiderio
## 6. Angle
## 7. Presentazione del prodotto
## 8. Proof e credibilità
## 9. Beat-by-beat (timestamp MM:SS per ogni beat)
## 10. Call to action
## 11. Punti di forza e debolezze (cosa fa bene / cosa migliorerebbe)
## 12. Pattern copiabili da un competitor""",
}

INLINE_LIMIT = 18 * 1024 * 1024
POLL_TIMEOUT, POLL_INTERVAL = 300, 3
MIME = {
    ".mp4": "video/mp4", ".mpeg": "video/mpeg", ".mpg": "video/mpg",
    ".mov": "video/quicktime", ".avi": "video/avi", ".flv": "video/x-flv",
    ".webm": "video/webm", ".wmv": "video/wmv", ".3gpp": "video/3gpp", ".3gp": "video/3gpp",
}


def download(url: str, tmp: Path) -> Path:
    if not shutil.which("yt-dlp"):
        sys.exit("ERROR: per gli URL serve yt-dlp (pip install yt-dlp)")
    print(f"[info] Scarico {url}...", file=sys.stderr)
    out = tmp / "video.%(ext)s"
    subprocess.run(
        ["yt-dlp", "-f", "mp4/best[ext=mp4]/best", "-o", str(out), url],
        check=True, stdout=sys.stderr,
    )
    files = [p for p in tmp.iterdir() if p.suffix.lower() in MIME]
    if not files:
        sys.exit("ERROR: download riuscito ma nessun file video trovato")
    return files[0]


def resolve_input(src: str, tmp: Path) -> Path:
    if src.startswith(("http://", "https://")):
        return download(src, tmp)
    path = Path(src).expanduser().resolve()
    if not path.is_file():
        sys.exit(f"ERROR: file non trovato: {path}")
    if path.suffix.lower() not in MIME:
        sys.exit(f"ERROR: estensione '{path.suffix}' non supportata. Valide: {', '.join(sorted(MIME))}")
    return path


def build_part(client, path: Path, fps):
    size, mime = path.stat().st_size, MIME[path.suffix.lower()]
    meta = types.VideoMetadata(fps=fps) if fps else None
    if size <= INLINE_LIMIT:
        print(f"[info] Invio inline ({size / 1e6:.1f} MB)...", file=sys.stderr)
        return types.Part(inline_data=types.Blob(data=path.read_bytes(), mime_type=mime), video_metadata=meta), None

    print(f"[info] {size / 1e6:.1f} MB: upload via Files API...", file=sys.stderr)
    up = client.files.upload(file=str(path))
    waited = 0
    while waited < POLL_TIMEOUT:
        f = client.files.get(name=up.name)
        state = getattr(f.state, "name", str(f.state))
        if state == "ACTIVE":
            return types.Part(file_data=types.FileData(file_uri=f.uri, mime_type=f.mime_type or mime), video_metadata=meta), up.name
        if state == "FAILED":
            sys.exit("ERROR: Gemini non è riuscito a elaborare il file")
        time.sleep(POLL_INTERVAL)
        waited += POLL_INTERVAL
    sys.exit(f"ERROR: timeout elaborazione dopo {POLL_TIMEOUT}s")


def main():
    ap = argparse.ArgumentParser(description="Analizza un video con Gemini.")
    ap.add_argument("source", help="File video o URL")
    ap.add_argument("--mode", choices=PROMPTS, default="general")
    ap.add_argument("--prompt", help="Prompt custom (sostituisce quello della modalità)")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--model", default="gemini-3-flash-preview")
    args = ap.parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("ERROR: GEMINI_API_KEY non impostata. Chiave gratuita: https://aistudio.google.com/apikey")

    client = genai.Client(api_key=key)
    uploaded = None
    with tempfile.TemporaryDirectory() as tmp:
        try:
            path = resolve_input(args.source, Path(tmp))
            part, uploaded = build_part(client, path, args.fps)
            print(f"[info] Analisi con {args.model} (mode={args.mode})...", file=sys.stderr)
            resp = client.models.generate_content(
                model=args.model,
                contents=types.Content(parts=[part, types.Part(text=args.prompt or PROMPTS[args.mode])]),
            )
            print(resp.text or "(nessun testo restituito)")
        finally:
            if uploaded:
                try:
                    client.files.delete(name=uploaded)
                except Exception:
                    pass


if __name__ == "__main__":
    main()
