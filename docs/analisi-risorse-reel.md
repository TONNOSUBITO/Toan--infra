# Analisi risorse dai reel Instagram

Data: 2026-10-24. Legenda certezza: **[Certo]** = letto direttamente · **[Probabile]** = deduzione forte · **[Ipotesi]** = non verificato.

## Verdetto rapido

| # | Risorsa | Cos'è | Installabile? | Costo | Rischio | Voto |
|---|---|---|---|---|---|---|
| 1 | Guida "Motion Design Studio with Opus 5.5" (Google Doc, RayCFU) | Pipeline completa per video in codice | **Sì → installata in `motion-studio/`** | Gratis | Basso | ⭐⭐⭐⭐⭐ |
| 2 | "Every Prompt From the Video" (Google Doc, Tyler Mommsen) | Prompt per launch video, logo, 20 stili | Solo prompt | Gratis | Medio (vedi sotto) | ⭐⭐⭐⭐ |
| 3 | Prompt "Motion graphics director" (Google Doc) | Analizza un video frame-by-frame → prompt per generatore video | Solo prompt | Gratis | Basso | ⭐⭐⭐ |
| 4 | doomscroll-agent (github.com/stidic) | Skill: reel salvati → skill riutilizzabili | **Sì → copiata in `skills/doomscroll/`** | Gratis, MIT | Medio (browser loggato) | ⭐⭐⭐ |
| 5 | editing.ajenepinnock.com + video YouTube | Pacchetto 20 skill di editing per Claude Code | Dopo acquisto | **$99** | Non verificabile | ⭐⭐ |
| 6 | 10 tool open source (Google Doc, @getintoai) | Lista: yt-dlp, Ollama, Whisper, n8n… | Sì, singolarmente | Gratis | Basso | ⭐⭐⭐ |
| 7 | prompts.chat | Libreria open source di prompt | App iOS/Raycast, self-host | Gratis | Basso, ma vedi skill terze | ⭐⭐ |
| 8 | Prompt "Halftone Ink Grain Portrait" (Google Doc) | Prompt immagine: foto → poster collage | Solo prompt | Gratis | Nullo | ⭐⭐ |
| 9 | "Fundamentals of Content Creation" (Zache Seno) | Teoria contenuti: hook, struttura, CTA | No | Gratis | Nullo | ⭐⭐ |
| 10 | "Zero to $1000/day dropshipping" (Mark Builds Brands) | Guida dropshipping + funnel a pagamento | No | Gratis (upsell) | Nullo, molto marketing | ⭐ |
| — | Notion "10 format che funzionano oggi" | — | **Illeggibile**: la pagina si carica solo via JavaScript | — | — | — |
| — | Google Doc `1eP62poC…` | — | **Privato** (HTTP 401) | — | — | — |
| — | Google Doc `12IIm_fJ…` | Appunti tuoi sull'esame di matematica finanziaria | Non c'entra (forse incollato per errore) | — | — | — |
| — | Link `1lRFqzmG…` | Duplicato del #9 | — | — | — | — |

---

## 1. Motion Design Studio con Opus 5.5 ✅ installato

**[Certo]** Claude non genera video: scrive un `index.html` con una funzione `window.seek(t)` che disegna il frame al tempo `t`. Un browser headless (Playwright) fotografa ogni frame e `ffmpeg` li monta in un MP4. Il render è deterministico: per cambiare uno shot modifichi una riga e rifai il render.

Pezzi (tutti in `motion-studio/`):
- `CLAUDE.md`: regole della casa. Vieta il "look da AI" (titolo centrato su gradiente, tutto in dissolvenza, particelle generiche) e impone il loop di autocritica (contact sheet → voto 1-10 → si corregge finché ogni voto è ≥ 8).
- `render.mjs`: renderer con motion blur reale (`--sub 4` renderizza 4 sotto-frame per frame e li fonde).
- `lib/motion.js`: molle (spring) al posto delle curve di easing, per un movimento "costoso".
- `beats.py`: misura i BPM della musica, così i tagli cadono sul beat.
- skill `motion-reel`: tutta la pipeline in una frase.

**[Certo] Bug trovato e corretto:** la `render.mjs` originale apre la pagina con `file://`. Chromium blocca gli `import` ES module da `file://`, quindi appena l'HTML importa `lib/motion.js` (cosa che la guida stessa chiede) si ottiene `window.seek is not a function`. Ora `render.mjs` serve la cartella su `127.0.0.1`. Test eseguito: un MP4 1080×1920 a 30 fps di 3 s generato correttamente.

Consigli utili della guida:
- Effort `xhigh` per i video nuovi, `max` per i lanci importanti. Con `medium` vengono piatti.
- Dai sempre un riferimento (un frame, un video, una cartella di immagini): "prendi la grammatica, mai il contenuto".
- Solo UI reale del prodotto (screenshot via Playwright), mai schermate inventate.
- Chiavi API in `.env`, mai nel prompt.
- Template "Overnight Director's Brief" per video lunghi, con gate: shot list → still → rough cut → animazione → suono → render.

Vende: community Skool (skool.com/raycfu). Il contenuto è comunque completo anche senza.

**[Probabile]** I comandi opzionali `npx skills add remotion-dev/skills` e `npx skills add heygen-com/hyperframes` installano skill di terzi. Remotion è un progetto noto, HyperFrames non l'ho verificato. Non li ho installati: rileggili prima di farlo.

## 2. "Claude Opus 5.5 Motion Graphics: Every Prompt From the Video" (Tyler Mommsen)

**[Certo]** Stesso concetto del #1, ma tramite il framework **HyperFrames** (oppure Remotion) invece del renderer fatto a mano. Contiene:
- il prompt completo del launch video "Loop", strutturato in PRODUCT / STORY / FORMAT / LOOK / MOTION / SOUND / QUALITY CHECK / RULES;
- il prompt per un'animazione del logo di 6 s, con versione a sfondo trasparente;
- un prompt per far scrivere a Claude il prompt lungo al posto tuo;
- un template da riempire e 20 stili (glassmorphism, kinetic typography, isometrico, VHS, blueprint, neo-brutalism…).

**[Certo] Rischio:** quasi ogni prompt finisce con *"Don't stop and don't ask me anything. Skip any approval steps and make every decision yourself."* Se lo usi con i permessi in auto o bypass, Claude installa pacchetti ed esegue comandi senza chiedere. **Togli quella riga**, oppure sostituiscila con "Chiedimi prima di installare pacchetti; per tutto il resto decidi da solo".

**[Certo]** Cita Higgsfield via MCP per i volti realistici: **ce l'hai già collegato** in questo account.

Vende: community Skool (skool.com/ai-builders), gratuita con upsell.

## 3. Prompt "Motion graphics director" (analisi video → prompt)

**[Certo]** Gli carichi un video. Lui fa (1) un'analisi beat per beat di composizione, tipografia, colori in hex, transizioni e audio, (2) un prompt pronto per un generatore video (Google Omni Flash, 10 s), (3) una sezione per cambiare brand, colori e testi.
**[Probabile]** È utile soprattutto come passo "riferimento → style guide" della pipeline #1: chiedi la Fase 1 e salvala come `docs/style_guide.md`.

## 4. doomscroll-agent ✅ copiato

**[Certo]** È una skill solo testo, licenza MIT, senza codice eseguibile. Lo zip del repo è identico a `SKILL.md`. Va in `skills/doomscroll/SKILL.md`.
Uso: Claude desktop con Claude in Chrome, loggato su Instagram → "Doomscroll la mia collezione X e trasformala in skill per [lavoro]".
**[Probabile] Rischio:** un agente che controlla un browser loggato al tuo account. Una didascalia malevola potrebbe tentare una prompt injection. Usalo solo su collezioni che hai scelto tu, 5-15 reel alla volta.

## 5. Claude Editing Skills, Ajené Pinnock (sito + video YouTube "How I Edit My Videos Using Claude Code")

**[Certo]** Pacchetto a pagamento da **$99** ("tutte le vendite sono definitive") con 20 stili di editing (14 verticali e 4 orizzontali) più 2 tool (una libreria B-roll ricercabile e un convertitore video → testo), un'app "Edit Review" in locale e setup di Node, HyperFrames e ffmpeg. Trascrizione con ElevenLabs (~$0,22/ora) o in locale.
**[Probabile]** Il nucleo tecnico è lo stesso del #1 e del #2, che sono gratis. Paghi i 20 stili già tarati e la comodità.
**[Ipotesi]** Le testimonianze "Verified buyer" non si possono verificare. Della pagina YouTube ho letto solo il titolo (YouTube blocca i server).
**Consiglio:** non comprarlo finché non hai provato `motion-studio/` con gli stili del #2.
⚠️ I link che mi hai passato contenevano `mcp_token=…` (token del sistema di DM automatici del creator). Non li ho usati e non condividerli.

## 6. 10 tool open source (@getintoai)

**[Certo]** yt-dlp, Ollama, Fooocus, Whisper, Plausible, AppFlowy, Penpot, n8n, Cal.com, Bitwarden: progetti reali e noti.
Rilevanti per te:
- **Whisper** (trascrizione locale, gratis): sostituisce ElevenLabs nel #5.
- **yt-dlp**: scarica i reel. **[Probabile]** Scaricare contenuti altrui da Instagram viola i ToS. Usalo solo per studio personale, mai per ripubblicare.
- **n8n**: automazioni. **Ollama**: modelli in locale.

## 7. prompts.chat

**[Certo]** Libreria open source di prompt (github.com/f/prompts.chat), con self-hosting, un'app iOS/macOS e un'estensione Raycast.
**[Probabile] Rischio:** alcuni prompt ("ANTIGRAVITY GLOBAL RULES") chiedono di eseguire `npx antigravity-awesome-skills` o di clonare repo di terzi non verificati. Non eseguirli alla cieca.

## 8. Halftone Ink Grain Portrait

**[Certo]** È un prompt per modelli di immagini (Nano Banana, GPT-image…): la foto originale sopra, la ricostruzione collage halftone/ASCII sotto, formato 3:4. Pronto all'uso. Puoi usarlo con il tuo Higgsfield `generate_image`.

## 9-10. Guide testuali

- **Fundamentals of Content Creation [Certo]:** struttura hook → contesto → idea → rinforzo → CTA. Tutto sensato, ma generico.
- **Dropshipping $1000/day [Certo]:** formula prodotto + funnel + ads. Il funnel finale porta a "Brand Builders Academy" (a pagamento). Utile solo se fai e-commerce.

---

## Cosa fare adesso (ordine consigliato)

1. **Cambia la password di Instagram** (l'hai scritta in chat) e attiva il 2FA.
2. Sul Mac: `cd motion-studio && npm install && npx playwright install chromium && npm run test-render`.
3. Apri Claude Code in `motion-studio/`, effort `xhigh`, e prova il prompt "Loop" del #2 **senza** la riga "Don't stop and don't ask me anything".
4. Se ti piace, installa la skill doomscroll: `skills/doomscroll/` → zippa la cartella → Claude → Customize → Skills → **+**.
5. Rimanda l'acquisto da $99 finché il punto 3 non ti ha deluso.
