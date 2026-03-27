# Arquitetura Atual e Planejada

## Estado atual do codigo

O repositorio ja possui a fundacao da arquitetura em camadas:

- `app/` com bootstrap e ponto de entrada
- `ui/` com janela principal, dialogs e worker em segundo plano
- `application/` com descoberta de PDFs, orquestracao do lote e servicos de agregacao
- `domain/` com modelos, validacoes e normalizadores puros
- `infrastructure/` com modulos separados para PDF, OCR, parser, agregacao, exportacao e logging
- `tests/` com testes unitarios iniciais, alem de uma suite de integracao orientada por amostras locais

Nesta etapa, OCR, parser inicial, agregacao e exportacao para Excel ja estao ligados ao fluxo principal da UI.
Tambem existe um bloco de versao na interface que consulta o GitHub em background para comparar a build local com releases ou tags publicadas.

## Decisoes principais

### Interface desktop

Usar `PySide6` como framework principal da interface.

Motivos:

- bom suporte a aplicacoes desktop no Windows
- componentes nativos para selecao de pasta e salvamento de arquivo
- sinais e slots adequados para comunicar progresso
- verificacao de versao remota sem bloquear a UI
- melhor caminho para empacotamento futuro com `PyInstaller`

### Pipeline de leitura

Usar uma arquitetura orientada a OCR.

Motivos:

- os PDFs de exemplo nao expuseram texto via leitura simples com `PyPDF2`
- a extracao depende de reconhecer cidade e linhas de item em layout visual
- o parser precisara trabalhar sobre texto reconstruido a partir do OCR

### Rasterizacao e OCR

Stack recomendada para o MVP:

- `PyMuPDF` para abrir e rasterizar a pagina do PDF
- `pytesseract` com `Tesseract OCR` para obter o texto
- `pypdf` para metadados e verificacoes auxiliares

Implementacao atual:

- renderizacao em 250 DPI para melhorar a leitura das linhas de item
- autodeteccao do `tesseract.exe` em caminhos comuns do Windows
- resolucao automatica do `tessdata` em `resources/tessdata`, variaveis de ambiente ou instalacao local do Tesseract
- OCR padrao em `por+eng` quando ambos os idiomas estao disponiveis
- OCR orientado a linhas com `image_to_string`, que preservou melhor o layout dos exemplos atuais
- heuristicas de parser para recuperar valores monetarios quando o OCR omite separadores decimais

### Geracao do Excel

Usar `pandas` com engine `openpyxl` para montar as abas e salvar em `.xlsx`.

Implementacao atual:

- exportacao das abas `Base_Itens`, `Resumo_Cidade_Item` e `Erros`
- formatacao minima com cabecalho em negrito, filtros, congelamento da primeira linha e larguras de coluna
- linha final de `TOTAL GERAL` na aba de resumo

## Arquitetura em camadas

### 1. UI

Responsavel por:

- janela principal
- selecao da pasta
- botao de extracao
- barra de progresso
- mensagens de status
- dialog para salvar o Excel

### 2. Application

Responsavel por:

- orquestrar o lote
- controlar estados da execucao
- publicar eventos de progresso
- consolidar resultados detalhados e agregados

### 3. Domain

Responsavel por:

- entidades de nota e resultado de extracao
- regras de validacao
- padronizacao de datas, moedas e identificadores

### 4. Infrastructure

Responsavel por:

- leitura e rasterizacao dos arquivos PDF
- OCR
- consulta opcional de versao no GitHub
- parser de layout
- agregacao por cidade e item
- exportacao para Excel
- logging local

## Fluxo tecnico

1. A UI recebe a pasta de entrada.
2. O servico lista os PDFs elegiveis.
3. Um worker em segundo plano percorre os arquivos.
4. Cada arquivo e rasterizado em imagem.
5. O OCR reconstrui o texto e, quando possivel, a ordem das linhas.
6. O parser identifica a cidade e as linhas de item.
7. O resultado detalhado e normalizado.
8. O agregador soma quantidade e valor total por cidade e item.
9. A UI recebe atualizacoes de progresso.
10. Ao final, a UI solicita o caminho de saida.
11. O exportador grava o Excel com abas de base, resumo e erros.

## Estrategia de concorrencia

Para o MVP, recomenda-se:

- `QThread` ou `QRunnable` com `QThreadPool`
- um worker dedicado para o lote
- emissao de sinais para atualizar progresso sem travar a interface

Motivo: simplicidade e boa integracao com o loop da interface.

## Estrategia de extracao

### Etapa 1. Rasterizacao

- converter cada pagina do PDF em imagem com resolucao adequada para OCR
- aplicar preprocessamento quando necessario

### Etapa 2. OCR

- extrair texto da imagem
- preservar a ordem logica de leitura o maximo possivel
- registrar confianca e falhas do OCR quando disponivel

### Etapa 3. Parser de layout

- localizar a cidade no cabecalho ou area relevante da nota
- localizar a grade de itens
- extrair descricao, quantidade e valor total por linha

### Etapa 4. Normalizacao

- unir linhas quebradas quando necessario
- limpar espacos excessivos
- padronizar quantidades e valores monetarios

### Etapa 5. Agregacao

- consolidar registros por `cidade + item_descricao`
- calcular somas para a aba de resumo

## Estrutura de pastas atual

```text
src/
  app/
    __init__.py
    bootstrap.py
    main.py
  application/
    __init__.py
    aggregation_service.py
    extraction_service.py
    progress.py
  domain/
    __init__.py
    models.py
    normalizers.py
    validators.py
  infrastructure/
    __init__.py
    aggregation/
      __init__.py
      city_item_aggregator.py
    export/
      __init__.py
      excel_exporter.py
    logging/
      __init__.py
      logger.py
    ocr/
      __init__.py
      image_preprocessor.py
      ocr_engine.py
    parser/
      __init__.py
      city_parser.py
      invoice_layout_parser.py
      item_line_parser.py
    pdf/
      __init__.py
      metadata_reader.py
      renderer.py
  ui/
    __init__.py
    dialogs.py
    main_window.py
    workers.py
tests/
  conftest.py
  integration/
  unit/
docs/
```

## Evolucao prevista da estrutura

A estrutura atual ja e a base alvo do projeto. As proximas iteracoes devem aprofundar principalmente:

- calibracoes adicionais de OCR e parser para novos layouts
- refinamentos de exportacao e apresentacao do workbook

## Observabilidade e erros

- registrar erros por arquivo com contexto minimo
- manter logs locais para diagnostico
- nao encerrar o lote por falha individual

## Testes recomendados

- testes unitarios do parser de cidade
- testes unitarios do parser de linhas de item
- testes de normalizacao de quantidades e moedas
- testes de integracao do fluxo OCR -> parser -> agregacao
- testes de exportacao do Excel
- testes de UI em pontos criticos com `pytest-qt`, se adotado

Implementacao atual:

- a suite de integracao aceita `tests/fixtures/pdfs/` ou `PDF_READER_SAMPLE_DIR`
- as expectativas atuais cobrem extracao, resumo agregado e estrutura do workbook exportado

## Riscos tecnicos

- grande variacao de layout entre notas
- OCR com ruido em textos pequenos ou tabelas densas
- informacoes quebradas por layout em colunas
- necessidade de ajustar o parser por fornecedor ou modelo de nota

## Mitigacoes

- comecar por um layout alvo claro baseado nos exemplos fornecidos
- armazenar exemplos reais anonimizados para testes
- separar OCR, parser, agregacao e exportacao desde o inicio
- prever evolucao para estrategia com multiplos parsers
