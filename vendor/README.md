# Vendor OCR

Use esta pasta para colocar uma distribuicao portatil do `Tesseract OCR` antes de gerar o build do Windows.

Opcoes suportadas:

1. Copiar os binarios para `vendor/tesseract/`
2. Ou chamar `scripts/build_windows.ps1 -TesseractDir "C:\caminho\para\tesseract"`

Estrutura esperada:

```text
vendor/
  tesseract/
    tesseract.exe
    *.dll
    tessdata/
```

Observacoes:

- o build atual ja inclui `resources/tessdata`, mas uma distribuicao portatil do Tesseract normalmente tambem precisa dos DLLs do proprio motor
- revise a licenca e a origem dos binarios que voce decidir redistribuir
