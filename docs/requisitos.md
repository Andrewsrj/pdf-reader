# Requisitos

## Requisitos funcionais

### RF-01 Selecionar pasta de entrada

O sistema deve permitir que o usuario selecione uma pasta local contendo arquivos PDF.

### RF-02 Listar quantidade de arquivos elegiveis

Depois da selecao da pasta, o sistema deve identificar os arquivos `.pdf` e informar a quantidade encontrada.

### RF-03 Iniciar extracao

O sistema deve disponibilizar um botao para iniciar a extracao em lote.

### RF-04 Processar arquivos em segundo plano

O processamento deve ocorrer sem bloquear a interface grafica.

### RF-05 Exibir progresso

O sistema deve mostrar:

- barra de progresso percentual
- contador de arquivos processados
- status textual do arquivo atual

### RF-06 Aplicar OCR quando necessario

O sistema deve conseguir extrair texto de PDFs que nao possuam camada de texto acessivel, utilizando OCR como parte do fluxo.

### RF-07 Extrair a cidade da nota

Para cada PDF suportado, o sistema deve identificar a cidade contida na nota, conforme o layout alvo.

### RF-08 Extrair linhas de item

Para cada PDF suportado, o sistema deve extrair ao menos:

- descricao do item
- quantidade do item
- valor total do item

### RF-09 Consolidar por cidade e item

O sistema deve somar quantidade e valor total agrupando os resultados por cidade e descricao do item.

### RF-10 Tratar falhas por arquivo

Quando um arquivo nao puder ser processado, o sistema deve registrar:

- nome do arquivo
- motivo da falha
- status final da tentativa

### RF-11 Concluir lote com sucesso parcial

Falhas em arquivos individuais nao devem interromper o processamento dos demais.

### RF-12 Solicitar local de salvamento

Ao final da extracao, o sistema deve abrir um dialog para o usuario escolher o caminho e o nome do arquivo Excel.

### RF-13 Exportar Excel

O sistema deve gerar um arquivo `.xlsx` contendo:

- aba de base detalhada por item
- aba de resumo consolidado por cidade e item
- aba de erros com os arquivos nao processados ou parcialmente processados

### RF-14 Exibir resumo final

Ao final do processo, o sistema deve informar:

- quantidade total de PDFs
- quantidade de sucessos
- quantidade de falhas
- caminho do arquivo gerado

### RF-15 Exibir versao da build

O sistema deve exibir na interface a versao atual da build e permitir uma verificacao opcional no GitHub para identificar se existe release ou tag mais recente.

### RF-16 Preparar distribuicao Windows

O sistema deve possuir uma configuracao de empacotamento para Windows que gere uma distribuicao executavel com os recursos locais necessarios ao app.

## Status inicial de implementacao

- `RF-01` ja possui implementacao inicial na janela principal.
- `RF-02` ja possui implementacao inicial por meio da descoberta local de arquivos `.pdf`.
- `RF-03` ja dispara o processamento em lote.
- `RF-04` e `RF-05` ja possuem implementacao inicial com worker em segundo plano, barra de progresso e status textual.
- `RF-06`, `RF-07` e `RF-08` ja possuem implementacao inicial para o layout atual dos exemplos analisados.
- `RF-09` ja possui implementacao inicial na camada de aplicacao.
- `RF-10` e `RF-11` ja possuem implementacao inicial no tratamento por arquivo.
- `RF-12`, `RF-13` e `RF-14` ja possuem implementacao inicial com dialog de salvamento, geracao do `.xlsx` e resumo final com caminho do arquivo.
- `RF-15` ja possui implementacao inicial com bloco dedicado na interface e verificacao remota em segundo plano.
- `RF-16` ja possui implementacao inicial com `PyInstaller`, script de build e inclusao de `resources/tessdata` no pacote.

Observacao de qualidade:

- o repositorio ja possui uma suite de integracao preparada para validar o lote completo com um diretorio configuravel de PDFs de exemplo.
- o OCR local ja considera `por+eng` quando os arquivos `.traineddata` estao disponiveis em `resources/tessdata` ou em um diretorio configurado.

## Requisitos nao funcionais

### RNF-01 Plataforma alvo

O software deve funcionar em Windows como plataforma principal na primeira entrega.

### RNF-02 Interface

A interface deve ser simples, direta e adequada para usuario administrativo.

### RNF-03 Performance

O sistema deve ser capaz de processar lotes de tamanho moderado sem travar a interface. Como meta inicial, considerar de 100 a 500 PDFs em um mesmo lote, dependendo da complexidade dos arquivos.

### RNF-03A OCR local

O OCR deve operar localmente, sem envio de imagens ou dados fiscais para servicos externos.

### RNF-04 Confiabilidade

O sistema deve registrar erros de forma rastreavel e evitar perda de resultados do lote por falhas isoladas.

### RNF-05 Manutenibilidade

A extracao deve ser modular para permitir novos parsers e ajustes por layout de documento.

### RNF-06 Privacidade

Todo processamento deve ocorrer localmente, sem envio de dados fiscais para servicos externos.

## Regras de negocio e decisoes iniciais

### RB-01 PDF suportado no MVP

O MVP considera como suportado o PDF cuja estrutura visual seja compativel com os exemplos fornecidos e permita identificar cidade e linhas de item via OCR e parser.

### RB-02 OCR no MVP

Como os exemplos analisados nao exibiram texto por leitura simples com `PyPDF2`, o OCR deixa de ser opcional e passa a ser uma capacidade prevista para o MVP.

### RB-03 Unidade de saida detalhada

Cada linha de item extraida gera uma linha na aba detalhada do Excel.

### RB-04 Unidade de saida consolidada

A aba de resumo deve agrupar os dados por `cidade + item`, somando quantidade e valor total.

### RB-05 Campos obrigatorios minimos

Os campos minimos para considerar uma extracao como util no MVP sao:

- nome do arquivo
- cidade, quando encontrada
- descricao do item, quando encontrada
- quantidade do item, quando encontrada
- valor total do item, quando encontrado
- status da extracao

### RB-06 Nomes de itens dos exemplos

Os nomes de itens observados nos arquivos de exemplo servem apenas para orientar o parser e nao devem ser documentados como lista fixa de valores esperados.

## Criterios de aceite do MVP

1. O usuario consegue selecionar uma pasta com PDFs.
2. O processamento ocorre com feedback visual de progresso.
3. O sistema nao congela durante o lote.
4. O usuario escolhe o nome e o local do `.xlsx` ao final.
5. O Excel e criado com uma aba detalhada, uma aba resumo por cidade e item e uma aba de erros.
6. PDFs com falha nao impedem a exportacao do resultado dos demais.
7. O resumo final apresenta somas de quantidade e valor total por cidade e item.
