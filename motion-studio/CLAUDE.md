# Motion studio rules

## Render contract
- Every film is a pure function of time: window.seek(t) paints frame t on a canvas with id="c".
- No CSS transitions, no setTimeout, no requestAnimationFrame in render mode,
  no state carried between frames. Seeded noise only, never Math.random.
- Render with node render.mjs --fps 60 --dur N --sub 4 (add --w 1920 --h 1080 for 16:9; default is 1080x1920).
  Encode H.264 yuv420p, CRF 16.
- Springs from lib/motion.js, not easing curves. Any value with more than one target uses track().

## Look
- Banned: centered title on a gradient, everything fading in,
  corner labels and frame borders, glow on UI, generic particle bursts.
- One display font, one UI font. One accent color unless the brief says otherwise.
- Every 2 to 4 seconds something new must happen on screen.
- Real product UI only. Never invent screens.

## Sound
- Music and sound effects are synthesized in code unless a track is supplied.
- Place hits on the measured beat grid (beats.json). Loudness -14 LUFS.
- Only use music we have the rights to.

## Loop before you show me anything
1. Render one frame per beat as a contact sheet and LOOK at it:
   ffmpeg -i out/final.mp4 -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 out/contact.png
2. Score it 1-10 on: hook in first 2s, readability at phone size,
   motion quality, variety, brand accuracy, sound sync.
3. Fix the 3 worst problems. Repeat until every score is 8+.
4. Only then do the full render.

## Safety
- API keys only in .env, never in a prompt or in a committed file.
- Ask before installing new packages or skills.
