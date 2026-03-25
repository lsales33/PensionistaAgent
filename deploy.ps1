# ============================================
# PensionistaAgent - Script de Deploy
# ============================================
# Execute este script no PowerShell:
#   .\deploy.ps1
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PensionistaAgent - Deploy para Web" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] Git nao instalado!" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Git encontrado" -ForegroundColor Green

# 2. Verificar GitHub CLI
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] GitHub CLI (gh) nao instalado!" -ForegroundColor Red
    Write-Host "  Instale com: winget install GitHub.cli"
    exit 1
}
Write-Host "[OK] GitHub CLI encontrado" -ForegroundColor Green

# 3. Autenticar no GitHub (se necessario)
$authStatus = gh auth status 2>&1 | Out-String
if ($authStatus -match "not logged") {
    Write-Host ""
    Write-Host "[!] Voce precisa fazer login no GitHub" -ForegroundColor Yellow
    Write-Host "    Um navegador vai abrir para autenticacao..." -ForegroundColor Yellow
    Write-Host ""
    gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha na autenticacao" -ForegroundColor Red
        exit 1
    }
}
Write-Host "[OK] Autenticado no GitHub" -ForegroundColor Green

# 4. Verificar se o commit existe
$commitCount = git rev-list --count HEAD 2>$null
if (-not $commitCount -or $commitCount -eq "0") {
    Write-Host "[!] Fazendo commit inicial..." -ForegroundColor Yellow
    git add -A
    git commit -m "PensionistaAgent - AI assistant for retirees"
}
Write-Host "[OK] Commit encontrado: $(git log --oneline -1)" -ForegroundColor Green

# 5. Criar repositorio no GitHub
Write-Host ""
Write-Host "[...] Criando repositorio no GitHub..." -ForegroundColor Yellow
gh repo create PensionistaAgent --public --source=. --remote=origin --push 2>&1
if ($LASTEXITCODE -ne 0) {
    # Talvez o repo ja exista, tenta push direto
    Write-Host "[!] Repo pode ja existir, tentando push..." -ForegroundColor Yellow
    $username = gh api user --jq .login 2>$null
    if ($username) {
        git remote remove origin 2>$null
        git remote add origin "https://github.com/$username/PensionistaAgent.git"
        git branch -M main
        git push -u origin main
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCESSO! Codigo no GitHub!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
    $username = gh api user --jq .login 2>$null
    Write-Host ""
    Write-Host "  Repo: https://github.com/$username/PensionistaAgent" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  PROXIMO PASSO - Deploy no Render.com:" -ForegroundColor Yellow
    Write-Host "  1. Acesse https://render.com e faca login com GitHub" -ForegroundColor White
    Write-Host "  2. Clique 'New +' > 'Web Service'" -ForegroundColor White
    Write-Host "  3. Conecte o repo 'PensionistaAgent'" -ForegroundColor White
    Write-Host "  4. Em Environment, adicione:" -ForegroundColor White
    Write-Host "     GROQ_API_KEY = sua_chave_groq" -ForegroundColor White
    Write-Host "  5. Clique 'Create Web Service'" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "[ERRO] Falha no push. Verifique sua autenticacao." -ForegroundColor Red
}
