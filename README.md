# Extrator de Notas Fiscais em PDF para Excel

Aplicacao desktop em Python para extrair cidade, itens, quantidades e valores totais de notas fiscais em PDF e consolidar os dados em uma planilha Excel.

## Versao atual

- Build local: `0.1.0`
- Repositorio: `https://github.com/Andrewsrj/pdf-reader`
- A interface exibe essa versao e tenta verificar em background se existe release ou tag mais recente no GitHub.

## Objetivo

Entregar um software simples para o usuario final:

1. Selecionar a pasta que contem os PDFs.
2. Clicar em `Extrair`.
3. Acompanhar o progresso em uma barra.
4. Gerar um Excel com resumo por `cidade -> item`.
5. Escolher onde salvar o arquivo Excel ao final do processamento.

## Escopo inicial

O MVP sera focado em:

- Interface desktop em `PySide6`.
- Processamento local, sem dependencia de nuvem.
- OCR para PDFs sem camada de texto acessivel.
- Extracao da cidade presente na nota.
- Extracao das linhas de item com quantidade e valor total.
- Consolidacao por cidade e item em `.xlsx`.
- Relatorio de falhas por arquivo para apoiar revisao manual.

Fica planejado para evolucao posterior:

- Suporte a mais layouts de documentos fiscais.
- Regras avancadas de validacao fiscal.
- Geracao de Tabela Dinamica nativa do Excel, se necessario.
- Empacotamento como executavel para Windows.

## Stack proposta

- `Python 3.11+`
- `PySide6` para interface desktop
- `PyMuPDF` para rasterizacao e apoio na leitura de PDF
- `pytesseract` com `Tesseract OCR` para extracao de texto dos exemplos fornecidos
- `pypdf` para metadados e verificacoes auxiliares
- `pandas` e `openpyxl` para geracao do Excel
- `pytest` para testes
- `PyInstaller` para distribuicao futura

## Documentacao

- [Visao do produto](docs/visao-produto.md)
- [Requisitos](docs/requisitos.md)
- [Especificacao de campos](docs/especificacao-campos.md)
- [Arquitetura](docs/arquitetura.md)
- [Plano de desenvolvimento](docs/plano-desenvolvimento.md)

## Status atual

A fundacao inicial do projeto ja foi criada no repositorio:

- estrutura em camadas dentro de `src/`
- `pyproject.toml` com dependencias e ponto de entrada
- janela principal modernizada em `PySide6`
- cards de indicadores, bloco de versao da build e tema visual customizado
- selecao de pasta e descoberta local de arquivos `.pdf`
- processamento em segundo plano com progresso
- pipeline inicial de rasterizacao, OCR e extracao de itens
- agregacao por cidade e item integrada ao resultado do lote
- exportacao para Excel com abas `Base_Itens`, `Resumo_Cidade_Item` e `Erros`
- reexportacao do ultimo lote, dialog "Sobre o autor" e verificacao opcional de versao no GitHub
- pacote local de idiomas OCR em `resources/tessdata` com selecao automatica de `por+eng`
- empacotamento inicial para Windows com `PyInstaller` em modo `onedir`
- modulos separados para dominio, aplicacao, infraestrutura e UI
- testes unitarios iniciais para descoberta de PDFs, normalizacao, parser, agregacao e exportacao
- suite de integracao pronta para validar OCR, parser, agregacao e exportacao com amostras locais

## Estrutura atual

```text
src/
  app/
  application/
  domain/
  infrastructure/
    aggregation/
    export/
    logging/
    ocr/
    parser/
    pdf/
  ui/
tests/
  integration/
  unit/
docs/
```

## Como executar

1. Criar e ativar um ambiente virtual Python 3.11+.
2. Instalar as dependencias com `pip install -e .[dev]`.
3. Iniciar a aplicacao com `python -m app.main`.

Observacao:
O app detecta automaticamente o `tesseract.exe` em instalacoes comuns do Windows e procura os idiomas em `resources/tessdata`, `PDF_READER_TESSDATA_DIR`, `TESSDATA_PREFIX` ou no diretorio do proprio Tesseract. Quando `por` e `eng` estao disponiveis, o OCR roda em `por+eng`.

## Empacotamento Windows

1. Instalar as dependencias de build com `pip install -e .[build]`.
2. Executar `powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1`.
3. O build sera gerado em `dist\pdf-reader\`.

Observacoes:

- o empacotamento atual usa `PyInstaller` em modo `onedir`
- `resources/tessdata` e incluido no build
- o `Tesseract OCR` nao e embutido no executavel; ele continua precisando estar instalado no Windows ou configurado via `TESSERACT_CMD`

## Testes de integracao

Os testes de integracao do pipeline completo podem usar:

- `tests/fixtures/pdfs/` com PDFs anonimizados
- ou a variavel de ambiente `PDF_READER_SAMPLE_DIR` apontando para um diretorio local

Com as amostras disponiveis, o comando esperado e `pytest tests/integration`.

## Direcao tecnica recomendada

`PySide6` continua sendo a melhor escolha para a interface. Como os PDFs de exemplo nao expuseram texto por leitura simples, o MVP passa a considerar OCR como parte do fluxo principal de extracao.

## Proximos passos sugeridos

- adicionar PDFs anonimizados em `tests/fixtures/pdfs/`
- calibrar OCR e parser para novos layouts de nota
- polir distribuicao Windows com icone, assinatura e instalador
