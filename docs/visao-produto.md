# Visao do Produto

## Resumo

O projeto tem como objetivo transformar um conjunto de notas fiscais em PDF em uma planilha Excel consolidada por cidade e item, por meio de uma aplicacao desktop simples de operar.

## Status atual da implementacao

A base inicial do produto ja existe no repositorio com:

- estrutura modular em `src/`
- ponto de entrada do aplicativo
- janela principal modernizada em `PySide6`
- selecao da pasta de entrada
- contagem de arquivos `.pdf` encontrados
- area de status, cards de indicadores e barra de progresso conectadas ao processamento em segundo plano
- bloco de versao da build com verificacao opcional de release/tag no GitHub
- pipeline inicial de OCR e extracao de cidade e itens para o layout atual dos exemplos
- pacote local de idiomas OCR com `por+eng` para melhorar leitura dos PDFs reais
- consolidacao inicial por `cidade + item` no resultado do lote
- dialog de salvamento e geracao inicial do arquivo Excel com as tres abas do MVP
- menu de ajuda com dialog do autor e link direto para o repositorio
- suite de integracao preparada para validar o fluxo completo com amostras locais

## Problema

Hoje a extracao manual de dados fiscais de PDFs consome tempo, aumenta a chance de erro e dificulta a consolidacao rapida de informacoes para controles administrativos, financeiros e contabeis.

## Objetivo do produto

Permitir que um usuario selecione uma pasta com arquivos PDF, execute a extracao da cidade da nota e das linhas de item e salve um arquivo Excel com os resultados, acompanhando o andamento da operacao por uma barra de progresso e mensagens de status.

## Perfil de usuario

- Assistente administrativo
- Analista financeiro
- Operador fiscal
- Pequena empresa que precisa consolidar notas sem ERP integrado

## Premissas do MVP

- O foco inicial sera em notas com estrutura semelhante aos exemplos fornecidos.
- Os exemplos analisados nao expuseram texto por leitura simples com `PyPDF2`, portanto o MVP deve prever OCR.
- O processamento sera 100 por cento local.
- Cada PDF sera tratado como uma unidade de entrada, mas a saida principal sera itemizada.
- O Excel final tera uma aba de base detalhada, uma aba de resumo por cidade e item e uma aba de erros.

## Fluxo principal do usuario

1. Abrir o aplicativo.
2. Selecionar a pasta onde estao os PDFs.
3. Visualizar a quantidade de arquivos encontrados.
4. Clicar em `Extrair`.
5. Acompanhar o progresso e o status do processamento.
6. Ao final, escolher o caminho e o nome do arquivo Excel.
7. Salvar e receber confirmacao de termino com o resumo consolidado gerado.

## Escopo do MVP

- Selecionar pasta de entrada
- Validar existencia de arquivos PDF
- Rasterizar e aplicar OCR aos arquivos
- Identificar a cidade contida na nota
- Extrair descricao do item, quantidade e valor total por linha
- Consolidar os dados por cidade e item
- Exibir progresso total
- Registrar erros por arquivo
- Permitir salvar em `.xlsx`
- Exibir mensagem final de sucesso ou falha parcial

## Fora do escopo inicial

- Importacao por arrastar e soltar
- Edicao manual dos dados dentro da interface
- Integracao com banco de dados
- Integracao com API da SEFAZ
- Tabela Dinamica nativa do Excel, caso o relatorio consolidado equivalente ja atenda
- Validacao fiscal avancada fora dos campos necessarios ao resumo

## Metas de qualidade

- Interface responsiva durante o processamento
- Operacao simples para usuario nao tecnico
- Logica de extracao modular para suportar novos layouts
- Resultado exportado em formato amigavel para filtros e analise
- Resumo final com leitura equivalente ao agrupamento `cidade -> item` mostrado na imagem de referencia

## Criterios de sucesso

- O usuario consegue processar uma pasta com multiplos PDFs sem travar a interface.
- O aplicativo gera um Excel valido e legivel.
- Arquivos com falha nao interrompem o lote inteiro.
- O usuario consegue identificar o que foi extraido e o que falhou.
- O resumo consolidado mostra a cidade da nota e os itens com suas somas de quantidade e valor total.
