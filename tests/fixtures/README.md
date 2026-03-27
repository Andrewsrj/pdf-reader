# Test Fixtures

Os testes de integracao do pipeline completo podem usar um dos caminhos abaixo:

1. PDFs anonimizados colocados em `tests/fixtures/pdfs/`
2. Um diretorio externo informado pela variavel de ambiente `PDF_READER_SAMPLE_DIR`

Arquivos esperados hoje:

- `NFSE_SP_11964_MT_TIM.pdf`
- `PR_6478_HW_TIM.pdf`
- `PR_6482_HW_TIM.pdf`
- `PR_6483_HW_TIM.pdf`
- `PR_6484_HW_TIM.pdf`

Fluxo recomendado:

1. Anonimizar os PDFs reais validados.
2. Copiar os arquivos para `tests/fixtures/pdfs/`.
3. Rodar `pytest tests/integration`.

Enquanto os PDFs anonimizados nao estiverem no repositorio, os testes de integracao sao automaticamente ignorados quando o diretorio configurado nao estiver disponivel.
