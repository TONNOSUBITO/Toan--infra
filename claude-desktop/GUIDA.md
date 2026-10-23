# Skill e plugin per Claude Desktop — guida d'installazione

Analisi fatta il 23/10/2026 leggendo il codice dei repository (clone `--depth 1`).

## Regola chiave prima di installare qualunque cosa

Claude Desktop ha tre ambienti diversi, e non tutti vedono il tuo PC:

| Ambiente | Dove gira | Vede `localhost`, Docker, file del PC? |
| --- | --- | --- |
| **Chat** (con skill/plugin caricati) | sandbox cloud di Anthropic | **No** |
| **Cowork** | VM/sandbox gestita dall'app | Solo le cartelle che condividi |
| **Code** (Claude Code, tab nell'app o CLI) | il tuo PC | **Sì** |

Tutto ciò che richiede un server locale, Docker o un CLI installato (Rizzo Flow, Strix, FreeLLMAPI,
claude-mem, Agent Reach) va usato da **Claude Code**, non dalla chat.

## Tabella riassuntiva

| Risorsa | Cos'è | Dove usarla | Come si installa |
| --- | --- | --- | --- |
| Rizzo Flow | Classificatore locale: testo → decisioni tipizzate con probabilità (~50 ms, 0 token generati) | Claude Code | `uv` + server locale, poi la skill in `skills/rizzo-flow.zip` |
| LinkedIn skills | 12 skill: post, commenti, risposte, umanizzatore, piano editoriale | Chat / Cowork / Code | Marketplace plugin `sergebulaev/linkedin-skills` |
| Taste Skill | Direzione artistica per siti/UI, verifica nel browser | Code (serve Node 22 + Chrome) | Già presente nel tuo account come `design-taste-frontend` |
| Impeccable | 1 skill, 24 comandi `/impeccable …` di design + 62 regole anti-"AI slop" | Code | Già presente nel tuo account come `impeccable` |
| YouTube agent skill | 11 skill `/yt-*` (script, titoli, retention, Shorts, SEO…) | Chat / Cowork / Code | Marketplace plugin `Jakeschincariol/youtube-agent-skill` |
| Find Skills | Cerca e installa skill con `npx skills` | Code | Già presente nel tuo account come `find-skills` |
| FreeLLMAPI | Router di 34 provider LLM gratuiti dietro un endpoint OpenAI/Anthropic | Server locale (Docker/Node 20) | `curl -fsSL https://freellmapi.co/install.sh \| bash` |
| Strix | Pentest autonomo con agenti AI in Docker | Code / terminale | `curl -sSL https://strix.ai/install \| bash` + chiave LLM |
| claude-mem | Memoria persistente tra sessioni di Claude Code (hook) | Code | `npx claude-mem install` |
| Agent Reach | Lettura di piattaforme con login (soprattutto cinesi) per agent | Code | Prompt d'installazione dal repo |
| claude-code-setup | Plugin ufficiale: analizza un progetto e suggerisce hook/skill/MCP | Code | `/plugin install claude-code-setup@claude-plugins-official` |

---

## 1. Rizzo Flow (`Rizzo-AI-Academy/rizzo-flow`)

**Cosa fa.** Prende uno *state* (testo o JSON) e domande chiuse (`boolean`, `choice`, `score`,
`numeric`) e restituisce per ognuna la distribuzione di probabilità letta dai logit di un modello
locale (Spark-X2.5 4B + LoRA, eseguito da llama.cpp). Non genera testo. API compatibile con Jev/TypeSafe.

**Quando serve:** triage di ticket/email, checklist su documenti, moderazione, guardrail per agent,
filtri prima di chiamare un LLM costoso. **Non serve** per scrivere, riassumere o tradurre.

**Requisiti:** Python ≥ 3.11, git, [uv](https://docs.astral.sh/uv/), ~4.4 GB di disco.
GPU consigliata (~5.6 GiB VRAM a Q8_0); funziona anche su CPU, più lento.
Testato dai maintainer solo su Windows 10 + RTX 5060 Ti.

**Installazione (Windows PowerShell / macOS / Linux):**

```bash
git clone https://github.com/Rizzo-AI-Academy/rizzo-flow
cd rizzo-flow
uv sync --locked
uv run rizzo devices          # vedi quale GPU/CPU userà
uv run rizzo download         # runtime llama.cpp + modello 4B (~4.4 GB)
                              # PC debole: uv run rizzo download --size 1.7b (meno accurato)
uv run rizzo serve            # → http://127.0.0.1:8017/playground
```

Prova senza server: `uv run rizzo decide examples/ticket.json`.

**Integrazione con Claude:** la skill `skills/rizzo-flow.zip` insegna a Claude quando e come
chiamare l'API. Funziona solo dove Claude raggiunge `127.0.0.1:8017`, cioè **Claude Code**:

```bash
# Windows: %USERPROFILE%\.claude\skills\   macOS/Linux: ~/.claude/skills/
unzip rizzo-flow.zip -d ~/.claude/skills/
```

Caricarla in Customize → Skills della chat è possibile ma inutile: la sandbox cloud non vede il tuo PC.

## 2. LinkedIn skills (`sergebulaev/linkedin-skills`)

12 skill (post-writer, comment-drafter, reply-handler, humanizer, hook-extractor, content-planner,
profile-optimizer, repurposer, interviewer, thread-monitor, engager-analytics, employee-advocacy).
Flusso: bozza → tua approvazione → (opzionale) pubblicazione.

**Claude Desktop:** Customize → Plugins → Add → Add marketplace → Add from a repository →
`sergebulaev/linkedin-skills` → sync → tab **Discover** → **+** sulla card → verifica in **Yours**.
Poi nuova chat: "Scrivimi un post LinkedIn su …".

Opzionali: **Apify** (lettura automatica di post/commenti; in chat usa il connettore MCP Apify,
non il token) e **Publora** (pubblicazione diretta). Senza, incolli tu il testo e pubblichi tu.

## 3. Taste Skill (`Leonxlnx/taste-skill`, tasteskill.dev)

Dà a Claude una direzione artistica (20 direzioni da 247 siti studiati), immagini reali da archivi
aperti e un controllo nel browser a 3 larghezze con fino a 3 cicli di correzione.
Una build richiede 30–45 minuti. Richiede **Node 22+ e Chrome/Edge/Chromium** → usala in Claude Code.

Già nel tuo account come `design-taste-frontend`. Per Claude Code:

```
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
```

Uso: "Costruisci la landing page per <brief>, usa design-taste-frontend".

## 4. Impeccable (`pbakaus/impeccable`, impeccable.style)

Una skill con 24 comandi. Flusso tipico in un progetto web:

```
npx impeccable install        # nella root del progetto
/impeccable init              # scrive PRODUCT.md (pubblico, scopo, vincoli, voce)
/impeccable critique landing  # revisione UX
/impeccable audit             # a11y, performance, responsive
/impeccable polish            # passata finale
```

Già nel tuo account come `impeccable`. Complementare a Taste: Taste costruisce, Impeccable rivede.

## 5. YouTube agent skill (`Jakeschincariol/youtube-agent-skill`)

11 comandi `/yt-script`, `/yt-package`, `/yt-edit`, `/yt-comment`, `/yt-plan`, `/yt-viral`,
`/yt-retention`, `/yt-shorts`, `/yt-seo`, `/yt-chapters`, `/yt-audit` + 6 script Python senza dipendenze.
Non pubblica nulla.

**Claude Desktop:** stesso percorso del plugin LinkedIn con `Jakeschincariol/youtube-agent-skill`.
**Claude Code:** `/plugin marketplace add Jakeschincariol/youtube-agent-skill` → `/plugin install youtube-agent@youtube-agent-skill`.

Primo passo obbligato: compila `templates/voice.md` (o manda a Claude 3 tuoi video e chiedi
"scrivi il mio voice.md"). Tutte le skill lo leggono.

## 6. Find Skills (`vercel-labs/skills`)

Skill che usa il CLI `npx skills find <query>` / `npx skills add <owner/repo>` per cercare e
installare skill dal catalogo skills.sh. Serve un terminale → Claude Code. Già nel tuo account.

## 7. FreeLLMAPI (`tashfeenahmed/freellmapi`)

Server Node che aggrega i free tier di 34 provider dietro un endpoint OpenAI/Anthropic-compatibile,
con failover sui rate limit e chiavi cifrate. Installazione Docker:

```bash
curl -fsSL https://freellmapi.co/install.sh | bash
npx freellmapi setup-claude --url http://localhost:3001 --api-key <unified-key>
```

Attenzione: `setup-claude` reindirizza **Claude Code** sui modelli gratuiti al posto di Claude.
Ha senso per script/app tue, non come sostituto del tuo abbonamento Claude.

## 8. Strix (`usestrix/strix`)

Agenti di pentest autonomi in sandbox Docker, con PoC verificati e report.
Requisiti: Docker attivo + chiave API di un LLM (costo a token).

```bash
curl -sSL https://strix.ai/install | bash
export STRIX_LLM="anthropic/<modello>"; export LLM_API_KEY="..."
strix --target ./cartella-della-tua-app
npx skills add usestrix/strix     # 9 skill per Claude Code
```

Solo su applicazioni tue o con autorizzazione scritta.

## 9. claude-mem (`thedotmack/claude-mem`)

Hook che registrano l'uso degli strumenti in Claude Code, ne fanno riassunti e li reiniettano nelle
sessioni successive. `npx claude-mem install`. L'installer propone l'account cmem.ai (servizio
ospitato, trial 30 giorni): i tuoi dati di sessione escono dal PC. Per restare locale passa
`--provider` esplicito o `CLAUDE_MEM_ONLINE_OPTIN=false`. Esiste una variante per Cowork che
invece manda tutto a cmem.ai per forza.

## 10. Agent Reach (`Panniantong/agent-reach`)

CLI + skill che danno all'agent accesso in sola lettura a Bilibili, Xiaohongshu, V2EX, Xueqiu,
YouTube (sottotitoli/trascrizione), Reddit, X, LinkedIn jobs… Per i siti con login **copia i cookie
di Chrome** nel suo browser dedicato (usa un account secondario). Installazione: dire a Claude Code
"Installa Agent Reach: https://raw.githubusercontent.com/Panniantong/Agent-Reach/main/docs/install.md".
Il pacchetto `agent-reach` su PyPI **non** è questo progetto.

## 11. claude-code-setup (`anthropics/claude-plugins-official`)

Plugin ufficiale, sola lettura: analizza il progetto e suggerisce 1–2 automazioni per categoria
(MCP, skill, hook, subagent, slash command).

```
/plugin install claude-code-setup@claude-plugins-official
"recommend automations for this project"
```
