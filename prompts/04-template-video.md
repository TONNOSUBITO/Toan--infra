# Template vuoto per qualsiasi video

Fonte: Tyler Mommsen

**Come si usa:** compila le parentesi quadre, cancella quello che non serve.

```text
Create a [length] second [type of video] for [product, brand or topic], following CLAUDE.md in this folder (render.mjs pipeline).

PRODUCT
- [What it is and who it's for, in one line.]
- Promise: [the one thing the viewer should remember].
- Show [number] [features or points] in this order: [list them].

STORY
- [The structure, for example: hook, three features, logo.] You design the scenes and write the words.
- One idea runs through the whole video: [a visual thread, like a line, a shape or a color].
- Every scene must transform into the next one. Nothing fades or cuts.
- End on [the logo, a call to action or a final message].

FORMAT
- [1920x1080, 16:9 or 1080x1920, 9:16], 60 fps, exactly [length] seconds, exported as an MP4.

LOOK
- [The feeling, for example: premium and calm, or loud and playful.]
- Background [hex], text [hex], one accent color only, [hex].
- Headlines in [font]. Body text in [font].
- Style: [any style from the list below, for example: glassmorphism].
- Avoid: [anything you don't want, for example: gradients, stock icons, anything that looks like a template].

MOTION
- The camera is always moving slowly. Nothing sits frozen on screen.
- Give it real depth: soft shadows, blur on things far away.
- Real motion blur: render extra in-between frames and blend them.

SOUND
- Make the music and every sound effect in code. No stock files.
- [Music style] at about [number] beats per minute. Scene changes land on the beat.
- Every sound sits on the exact frame of the thing it belongs to.

QUALITY CHECK
- Render it and look at a frame from every half second.
- Critique it the way a senior motion designer would: story, layout, spacing, type, timing,
  readability, and whether the sound matches the picture.
- Fix everything you find, render again, and critique again. Do at least four full rounds.

RULES
- Decide tutto da solo sul design, ma chiedimi prima di installare pacchetti o eseguire comandi fuori da questa cartella.
- When it's finished, give me the final MP4 and list what you fixed in each round.
```
