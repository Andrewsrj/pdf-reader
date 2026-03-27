# Tessdata Local

Este diretorio pode conter pacotes de idioma do Tesseract usados localmente pelo projeto.

Estado atual:

- `por.traineddata` adicionado para melhorar OCR em portugues
- `eng.traineddata` mantido para combinar `por+eng` nos documentos atuais

Precedencia usada pelo app:

1. `PDF_READER_TESSDATA_DIR`
2. `TESSDATA_PREFIX`
3. `resources/tessdata`
4. `artifacts/tessdata`
5. `tessdata` ao lado do executavel do Tesseract
