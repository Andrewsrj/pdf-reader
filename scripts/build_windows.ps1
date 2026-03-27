$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$specPath = Join-Path $projectRoot "packaging\\windows\\pdf-reader.spec"
$distPath = Join-Path $projectRoot "dist"
$workRoot = Join-Path $projectRoot "artifacts\\pyinstaller-work"
$buildPath = Join-Path $workRoot (Get-Date -Format "yyyyMMddHHmmss")
$appDistPath = Join-Path $distPath "pdf-reader"

Write-Host "Projeto:" $projectRoot
Write-Host "Spec:" $specPath

Push-Location $projectRoot
try {
    New-Item -ItemType Directory -Force -Path $buildPath | Out-Null

    if (Test-Path $appDistPath) {
        Remove-Item -LiteralPath $appDistPath -Recurse -Force
    }

    python -m PyInstaller --noconfirm --clean --distpath $distPath --workpath $buildPath $specPath
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller falhou com codigo $LASTEXITCODE."
    }

    Write-Host ""
    Write-Host "Build concluido em:" $appDistPath
    Write-Host "Observacao: o executavel nao embute o Tesseract."
    Write-Host "Instale o Tesseract no Windows ou configure TESSERACT_CMD antes de usar."
}
finally {
    Pop-Location
}
