# Analizza un video di riferimento

Fonte: Google Doc condiviso (motion graphics director)

**Come si usa:** carica il video in Claude e incolla. Salva la FASE 1 come `motion-studio/docs/style_guide.md`.

```text
Claude Prompt -
You are a motion graphics director and prompt engineer. I've uploaded a video
(motion graphics / animation / product demo / SaaS explainer). Do this in two
phases. Do not skip steps or summarize loosely — treat this as a professional
shot-by-shot breakdown that another creator could rebuild the video from
without ever seeing the original.
PHASE 1 — FULL FRAME-BY-FRAME ANALYSIS
Extract and inspect frames across the entire duration (don't just sample the
first few seconds). For each distinct scene/beat, report:
1. Timestamp range (e.g. 0.0–2.5s)
2. Composition & camera — framing, aspect ratio, camera movement (push,
   pan, orbit, static), depth of field, focal point
3. Subject/content — every object, icon, illustration, photo, or 3D
   element on screen; its exact shape, style (flat/3D/line/glass/etc.),
   position, and size relative to frame
4. Text & typography — exact wording, font style/weight (serif, sans,
   rounded, condensed), size hierarchy, color, letter-spacing, any kinetic
   animation (fade, slide, mask-reveal, letter-by-letter, blur-in)
5. Color palette — background color(s), foreground/accent colors, note
   any hex-approximate values, gradients, or monochrome treatment
6. Lighting, shadow & texture — light direction, shadow softness/hardness,
   surface textures (paper, metal, glass, matte, glossy), grain/noise,
   vignetting
7. Icons/graphics/UI elements — describe each precisely: shape,
   line-weight, fill vs. outline, any brand marks, buttons, cursors, progress
   indicators, chart/data visuals
8. Motion & transitions — how this beat animates in and how it transitions
   to the next (cut, morph, wipe, dissolve, liquid transition, particle
   dissolve, match-cut)
9. Audio (if audible/inferable) — music mood/tempo, sound effects (whoosh,
   click, chime), voiceover presence and tone
Also summarize once at the top:
- Total duration, resolution/aspect ratio, frame rate (if determinable)
- Overall visual style in one line (e.g. "cinematic B&W kinetic typography
  with metaphor visuals" or "flat glossy SaaS dashboard UI motion")
- Pacing (cuts per second, energy level)
- Any recurring visual motif or through-line connecting the beats
PHASE 2 — CONVERT THE ANALYSIS INTO AN OMNI FLASH GENERATION PROMPT
Using everything found in Phase 1, write a single, ready-to-paste Google
Omni Flash video generation prompt that would recreate this video's look,
pacing, and structure as closely as possible (not a copy of copyrighted
specifics — recreate the style and technique, not any protected content).
The prompt must include:
- Style line — one dense sentence covering mood, lighting, color grading,
  camera behavior, and finish quality (premium/cinematic/glossy/etc.)
- Technical specs — resolution, aspect ratio, fps, duration (match Omni
  Flash's native output — currently 10 seconds; if the source is longer,
  compress the same number of beats proportionally into 10 seconds)
- Beat-by-beat timeline — same structure as Phase 1, rewritten as
  generation instructions (what appears, how it moves, how it transitions),
  with exact color values, exact typography description, and exact icon/shape
  geometry so nothing is left ambiguous
- Typography spec — one line locking the font style so it stays consistent
  across every text beat
- Sound design line — score mood + key SFX moments, timed to the visual
  beats
- Final frame spec — describe exactly what the last held frame should look
  like (this is what viewers remember most)
Format the final prompt as a single copy-paste block, written as direct
generation instructions (not questions, not commentary).
PHASE 3 — CUSTOM CHANGE REQUEST (fill this in before sending, or leave as-is to recreate faithfully)
Apply these swaps/changes to the Phase 2 prompt before finalizing it:
- Brand name / logo: [e.g. "flevo" — attach brand kit image if available]
- Color palette override: [e.g. keep original palette / use these hex
  codes instead: ___]
- Text/copy override: [replace the on-screen lines with: ___]
- Duration override: [default 10s / specify other]
- Tone/style shift: [e.g. "make it full color instead of B&W" / "make it
  more playful, less corporate" / no change]
- Anything to remove or add: [e.g. "remove the falling-man metaphor, add a
  data-chart metaphor instead"]
```
