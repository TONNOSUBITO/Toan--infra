# Toan--infra
Mcp connectors skills everything that can upgrade my Claude or so

## Installazione su Windows (una volta)

1. Scarica `toan-toolkit.zip` in Download.
2. Apri PowerShell e incolla:

```powershell
cd $HOME\Downloads; Expand-Archive .\toan-toolkit.zip -DestinationPath .\toan-toolkit -Force; powershell -ExecutionPolicy Bypass -File .\toan-toolkit\install.ps1
```

Lo script installa Git, Node.js, ffmpeg, Python e Claude Code, copia tutto in `%USERPROFILE%\Toan-toolkit`,
mette le skill in `%USERPROFILE%\.claude\skills`, fa un video di prova e lascia `doomscroll-skill.zip` sul Desktop.
Aggiungi `-Whisper` in fondo se vuoi anche le trascrizioni locali (~3 GB).

## Contenuto

- `install.ps1`: installer per Windows
- `prompts/`: prompt pronti (video di lancio, logo, 20 stili, analisi video, poster halftone)
- `motion-studio/`: pipeline per video motion-graphics fatti in codice con Claude Code (testata)
- `skills/doomscroll/`: skill che trasforma i reel salvati in skill riutilizzabili (MIT, stidic/doomscroll-agent)
- `docs/analisi-risorse-reel.md`: analisi delle risorse trovate nei reel (cosa sono, rischi)
