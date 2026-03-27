# Extrator de Notas Fiscais em PDF para Excel

Aplicacao desktop em Python para extrair cidade, itens, quantidades e valores totais de notas fiscais em PDF e consolidar os dados em uma planilha Excel.

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

## Direcao tecnica recomendada

`PySide6` continua sendo a melhor escolha para a interface. Como os PDFs de exemplo nao expuseram texto por leitura simples, o MVP passa a considerar OCR como parte do fluxo principal de extracao.

## Proximo passo sugerido

Com esta base documental pronta, o proximo passo e criar o esqueleto do projeto em Python com:

- estrutura de pastas
- janela principal
- servico de varredura da pasta
- pipeline de OCR e extracao com progresso
- parser de cidade e itens
- exportador do resumo consolidado e da base detalhada
