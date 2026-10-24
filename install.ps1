# Toan toolkit - installer per Windows
# Uso (da PowerShell, nella cartella estratta):
#   powershell -ExecutionPolicy Bypass -File .\install.ps1            # tutto tranne Whisper
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -Whisper   # anche Whisper (~3 GB)
param([switch]$Whisper)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Dest = Join-Path $HOME 'Toan-toolkit'
$Desktop = [Environment]::GetFolderPath('Desktop')

function Step($m) { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Ok($m) { Write-Host "    OK  $m" -ForegroundColor Green }
function Refresh-Path {
  $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
              [Environment]::GetEnvironmentVariable('Path', 'User')
}
function Ensure($cmd, $wingetId) {
  if (Get-Command $cmd -ErrorAction SilentlyContinue) { Ok "$cmd gia presente"; return }
  Write-Host "    installo $wingetId ..."
  winget install --id $wingetId -e --silent --accept-source-agreements --accept-package-agreements
  Refresh-Path
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
    throw "$cmd non trovato dopo l'installazione. Chiudi e riapri PowerShell, poi rilancia lo script."
  }
  Ok "$cmd installato"
}

Step 'Controllo winget'
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
  throw 'winget manca. Installa "App Installer" dal Microsoft Store e rilancia.'
}
Ok 'winget presente'

Step 'Programmi di base (Git, Node.js, ffmpeg, Python)'
Ensure 'git' 'Git.Git'
Ensure 'node' 'OpenJS.NodeJS.LTS'
Ensure 'ffmpeg' 'Gyan.FFmpeg'
Ensure 'py' 'Python.Python.3.12'

Step "Copio il toolkit in $Dest"
if ((Resolve-Path $Root).Path -ne $Dest) {
  New-Item -ItemType Directory -Force -Path $Dest | Out-Null
  Get-ChildItem -Path $Root -Force | Where-Object { $_.Name -notin @('node_modules', 'out', '.git') } |
    Copy-Item -Destination $Dest -Recurse -Force
}
Ok 'copiato'

Step 'Claude Code'
if (Get-Command claude -ErrorAction SilentlyContinue) { Ok 'claude gia presente' }
else { npm.cmd install -g @anthropic-ai/claude-code; Refresh-Path; Ok 'claude installato' }

Step 'Motion studio: dipendenze e browser per il render'
Push-Location (Join-Path $Dest 'motion-studio')
npm.cmd install --no-fund --no-audit
npx.cmd playwright install chromium
Ok 'pronto'

Step 'Motion studio: render di prova (3 secondi)'
npm.cmd run test-render
if (Test-Path 'out\silent.mp4') { Ok "video di prova: $Dest\motion-studio\out\silent.mp4" }
else { Write-Warning 'render di prova fallito: copia l''errore qui sopra e mandalo a Claude' }
Pop-Location

Step 'Analisi del ritmo musicale (beats.py)'
py -m pip install --quiet --disable-pip-version-check numpy librosa soundfile
Ok 'librosa installato'

if ($Whisper) {
  Step 'Whisper (trascrizioni gratis in locale)'
  py -m pip install --quiet --disable-pip-version-check openai-whisper
  Ok 'uso: py -m whisper video.mp4 --language Italian'
}

Step 'Skill per Claude Code (valgono in tutte le cartelle)'
$SkillsDir = Join-Path $HOME '.claude\skills'
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
Copy-Item (Join-Path $Dest 'skills\doomscroll') $SkillsDir -Recurse -Force
Copy-Item (Join-Path $Dest 'motion-studio\.claude\skills\motion-reel') $SkillsDir -Recurse -Force
Ok "doomscroll e motion-reel in $SkillsDir"

Step "Skill per l'app Claude desktop"
$Zip = Join-Path $Desktop 'doomscroll-skill.zip'
Compress-Archive -Path (Join-Path $Dest 'skills\doomscroll') -DestinationPath $Zip -Force
Ok "creato $Zip  -> caricalo in Claude: Customize > Skills > +"

Step 'Fatto'
Write-Host @"

  Cartella:      $Dest
  Prompt pronti: $Dest\prompts
  Primo video:   cd $Dest\motion-studio ; claude
                 poi /model -> effort xhigh, e incolla prompts\01-video-lancio.md

"@ -ForegroundColor Yellow
explorer.exe $Dest
