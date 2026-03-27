# Plano de Desenvolvimento

## Objetivo

Entregar um MVP funcional do extrator de notas fiscais em PDF para Excel com interface desktop.

## Status atual

Concluido nesta rodada:

- estrutura inicial de pastas em `src/`
- `pyproject.toml` com dependencias e entry point
- janela principal inicial
- selecao de pasta com descoberta real de PDFs
- processamento em segundo plano com progresso
- pipeline inicial de rasterizacao, OCR e parser
- modulos base de dominio, aplicacao, infraestrutura e UI
- testes unitarios iniciais para componentes deterministas e parser

## Fase 0 - Fundacao do projeto

Status: concluida

Entregas:

- estrutura inicial de pastas
- ambiente Python configurado
- dependencias definidas
- definicao da estrategia de OCR
- padrao de logs e configuracao basica

Resultado esperado:

- projeto executa uma janela inicial funcional com a stack escolhida

## Fase 1 - Interface base

Status: concluida

Entregas:

- janela principal
- campo ou label para pasta selecionada
- botao para escolher pasta
- botao `Extrair`
- barra de progresso
- area de status

Resultado esperado:

- usuario consegue selecionar uma pasta, validar os PDFs encontrados e seguir para o processamento em segundo plano

## Fase 2 - Pipeline de leitura e OCR

Status: concluida

Entregas:

- descoberta de PDFs
- worker em segundo plano
- rasterizacao das paginas
- OCR por arquivo
- consolidacao de falhas de leitura

Resultado esperado:

- aplicacao percorre um lote real sem travar a interface e produz texto de entrada para o parser

## Fase 3 - Parser itemizado do MVP

Status: em andamento

Entregas:

- parser inicial para o layout alvo dos exemplos
- extracao da cidade
- extracao das linhas de item
- normalizacao de campos
- validacoes basicas

Resultado esperado:

- aplicacao extrai cidade, item, quantidade e valor total para ao menos um conjunto inicial de exemplos reais

## Fase 4 - Exportacao para Excel

Status: pendente

Entregas:

- dialog de salvamento
- geracao das abas `Base_Itens`, `Resumo_Cidade_Item` e `Erros`
- formatacao minima das colunas

Resultado esperado:

- usuario salva o `.xlsx` ao final do lote com base detalhada e resumo consolidado

## Fase 5 - Qualidade e distribuicao

Status: pendente

Entregas:

- testes automatizados principais
- tratamento de erros refinado
- icone e acabamento minimo da interface
- empacotamento inicial com `PyInstaller`

Resultado esperado:

- aplicacao pronta para testes de uso por usuarios reais

## Backlog inicial sugerido

1. Integrar agregacao por cidade e item ao resultado do lote.
2. Exportar para Excel nas abas `Base_Itens`, `Resumo_Cidade_Item` e `Erros`.
3. Criar testes com PDFs de exemplo anonimizados.
4. Melhorar o OCR com pacote de idioma `por` e calibracoes adicionais de preprocessamento.

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
- ligar o fluxo completo `OCR -> parser -> resumo -> Excel` a partir da base ja criada
