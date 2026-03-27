[CmdletBinding()]
param(
    [string]$TesseractDir = ""
)

$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$specPath = Join-Path $projectRoot "packaging\\windows\\pdf-reader.spec"
$distPath = Join-Path $projectRoot "dist"
$workRoot = Join-Path $projectRoot "artifacts\\pyinstaller-work"
$buildPath = Join-Path $workRoot (Get-Date -Format "yyyyMMddHHmmss")
$appDistPath = Join-Path $distPath "pdf-reader"
$defaultBundledTesseract = Join-Path $projectRoot "vendor\\tesseract"

Write-Host "Projeto:" $projectRoot
Write-Host "Spec:" $specPath

if ($TesseractDir) {
    $env:PDF_READER_TESSERACT_DIR = (Resolve-Path $TesseractDir)
    Write-Host "Tesseract para empacotar:" $env:PDF_READER_TESSERACT_DIR
}
elseif (Test-Path $defaultBundledTesseract) {
    $env:PDF_READER_TESSERACT_DIR = (Resolve-Path $defaultBundledTesseract)
    Write-Host "Tesseract para empacotar:" $env:PDF_READER_TESSERACT_DIR
}

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
    if ($env:PDF_READER_TESSERACT_DIR) {
        Write-Host "OCR portatil incluido no pacote."
    }
    else {
        Write-Host "Observacao: o executavel nao embute o Tesseract."
        Write-Host "Instale o Tesseract no Windows, configure TESSERACT_CMD ou gere o build com -TesseractDir."
    }
}
finally {
    Pop-Location
}
