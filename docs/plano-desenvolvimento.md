# Plano de Desenvolvimento

## Objetivo

Entregar um MVP funcional do extrator de notas fiscais em PDF para Excel com interface desktop.

## Fase 0 - Fundacao do projeto

Entregas:

- estrutura inicial de pastas
- ambiente Python configurado
- dependencias definidas
- definicao da estrategia de OCR
- padrao de logs e configuracao basica

Resultado esperado:

- projeto executa uma janela inicial vazia com a stack escolhida

## Fase 1 - Interface base

Entregas:

- janela principal
- campo ou label para pasta selecionada
- botao para escolher pasta
- botao `Extrair`
- barra de progresso
- area de status

Resultado esperado:

- usuario consegue selecionar uma pasta e iniciar uma acao simulada com progresso

## Fase 2 - Pipeline de leitura e OCR

Entregas:

- descoberta de PDFs
- worker em segundo plano
- rasterizacao das paginas
- OCR por arquivo
- consolidacao de falhas de leitura

Resultado esperado:

- aplicacao percorre um lote real sem travar a interface e produz texto de entrada para o parser

## Fase 3 - Parser itemizado do MVP

Entregas:

- parser inicial para o layout alvo dos exemplos
- extracao da cidade
- extracao das linhas de item
- normalizacao de campos
- validacoes basicas

Resultado esperado:

- aplicacao extrai cidade, item, quantidade e valor total para ao menos um conjunto inicial de exemplos reais

## Fase 4 - Exportacao para Excel

Entregas:

- dialog de salvamento
- geracao das abas `Base_Itens`, `Resumo_Cidade_Item` e `Erros`
- formatacao minima das colunas

Resultado esperado:

- usuario salva o `.xlsx` ao final do lote com base detalhada e resumo consolidado

## Fase 5 - Qualidade e distribuicao

Entregas:

- testes automatizados principais
- tratamento de erros refinado
- icone e acabamento minimo da interface
- empacotamento inicial com `PyInstaller`

Resultado esperado:

- aplicacao pronta para testes de uso por usuarios reais

## Backlog inicial sugerido

1. Criar estrutura `src/` e ponto de entrada do app.
2. Implementar `MainWindow` com selecao de pasta.
3. Implementar worker de progresso fake para validar UX.
4. Implementar descoberta real de PDFs.
5. Criar pipeline de rasterizacao e OCR.
6. Criar modelos de `ItemExtraido` e `ErroExtracao`.
7. Implementar parser de cidade e linhas de item.
8. Implementar agregacao por cidade e item.
9. Exportar para Excel.
10. Criar testes com PDFs de exemplo.

## Dependencias externas previstas

- biblioteca de interface grafica
- biblioteca de rasterizacao de PDF
- motor OCR local
- biblioteca de planilhas Excel
- amostras reais de notas fiscais para testes

## Definition of Done do MVP

- interface desktop funcional
- processamento em lote com barra de progresso
- OCR funcional para o layout alvo
- extracao de cidade, item, quantidade e valor total
- resumo por cidade e item
- salvamento do Excel definido pelo usuario
- tratamento de falha por arquivo
- documentacao basica atualizada

## Premissas para a proxima etapa

- reunir de 5 a 20 PDFs reais e anonimizados para orientar o parser
- validar se todos os layouts iniciais seguem o mesmo padrao visual
- iniciar a implementacao pelo fluxo completo `OCR -> parser -> resumo`
