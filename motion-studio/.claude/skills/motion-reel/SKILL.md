---
name: motion-reel
description: Make a product or showreel motion video rendered from code. Use when the user asks for a launch video, showreel, product reel, animated explainer or motion ad.
---

# Motion reel

## Inputs to collect first
Product + URL, duration, formats (9:16 / 1:1 / 16:9), brand colors + fonts,
a reference (frame, video, or image folder), music (file or "synthesize").

## Pipeline
1. Gather assets from the URL with Playwright into ./assets. List them.
2. If a reference exists, extract one frame every 0.5s with ffmpeg and write docs/style_guide.md
   (palette hex, type, shot lengths, transitions, camera moves). Take the grammar, never the content.
3. Measure or synthesize music. beats.py → beats.json.
4. Write docs/shotlist.md on the beat grid. Show it and wait for OK.
5. Build index.html with window.seek(t) using lib/motion.js springs. Follow CLAUDE.md.
6. Contact sheet → critique → fix. 3 rounds minimum, every score 8+.
7. node render.mjs → sound → mix to -14 LUFS → out/final.mp4, all formats.
8. Deliver final.mp4, contact.png, poster.png. Say what you'd improve next.

## Hard rules
- Real product UI only. Never invent screens.
- No Math.random, no timers, no CSS transitions in render mode.
- Banned: corner labels, centered title on gradient, everything fading in.
