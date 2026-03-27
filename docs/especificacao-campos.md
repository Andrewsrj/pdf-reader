# Especificacao de Campos

## Objetivo

Definir os campos a extrair no MVP e o formato esperado no arquivo Excel, considerando a necessidade de um resumo por cidade e item como na imagem de referencia.

Observacao:

- a versao da build e o status de verificacao no GitHub sao exibidos apenas na interface do aplicativo e nao fazem parte das abas exportadas para o Excel.

## Aba detalhada sugerida

Nome recomendado da aba: `Base_Itens`

Cada linha representa um item extraido de uma nota.

| Coluna | Tipo | Obrigatorio | Observacao |
| --- | --- | --- | --- |
| arquivo_pdf | texto | sim | Nome do arquivo de origem |
| status_extracao | texto | sim | `sucesso`, `parcial` ou `falha` |
| cidade | texto | nao | Cidade encontrada na nota |
| numero_documento | texto | nao | Numero da nota ou identificador equivalente, quando encontrado |
| data_emissao | data/texto | nao | Data de emissao, quando encontrada |
| item_descricao | texto | nao | Descricao textual do item extraido |
| item_qtd | decimal | nao | Quantidade do item |
| item_valor_total | decimal | nao | Valor total do item na linha |
| observacoes | texto | nao | Mensagens de parser, OCR ou validacao |

## Aba de resumo sugerida

Nome recomendado da aba: `Resumo_Cidade_Item`

Cada linha representa a consolidacao de uma combinacao `cidade + item_descricao`.

| Coluna | Tipo | Obrigatorio | Observacao |
| --- | --- | --- | --- |
| cidade | texto | sim | Agrupador principal do relatorio |
| item_descricao | texto | sim | Agrupador secundario do relatorio |
| soma_item_qtd | decimal | sim | Soma das quantidades por cidade e item |
| soma_item_valor_total | decimal | sim | Soma dos valores totais por cidade e item |

Implementacao atual:

- a consolidacao ja e produzida pelo resultado do lote em memoria
- a ordenacao atual segue `cidade` e depois `item_descricao`
- os totais sao calculados somando os itens extraidos da base detalhada
- a exportacao atual inclui uma linha final de `TOTAL GERAL` na aba de resumo

## Aba de erros sugerida

Nome recomendado da aba: `Erros`

| Coluna | Tipo | Obrigatorio | Observacao |
| --- | --- | --- | --- |
| arquivo_pdf | texto | sim | Nome do arquivo com problema |
| tipo_erro | texto | sim | Exemplo: `ocr_falhou`, `layout_nao_suportado`, `erro_leitura` |
| mensagem | texto | sim | Detalhe do problema |
| etapa | texto | nao | Exemplo: `ocr`, `parser`, `exportacao` |

Implementacao atual:

- as tres abas ja sao gravadas no `.xlsx`
- quando nao ha erros no lote, a aba `Erros` e criada apenas com o cabecalho

## Requisito de apresentacao do resumo

O resumo deve reproduzir a leitura logica mostrada na imagem de referencia:

- cidade como agrupador principal
- item como agrupador secundario
- exibicao das somas de quantidade e valor total
- linha de total geral ao final, quando aplicavel

No MVP, essa entrega pode ser feita por uma aba consolidada ordenada por cidade e item, com formatacao visual para facilitar a leitura, sem obrigar a criacao de uma Tabela Dinamica nativa do Excel.

## Padronizacoes recomendadas

- Datas no padrao `YYYY-MM-DD` quando a conversao for confiavel.
- Valores monetarios exportados como numero decimal.
- Quantidades exportadas como numero decimal.
- Campos nao encontrados devem ficar vazios, nao com texto artificial como `N/A`, exceto em colunas de status.

## Regras de preenchimento

### Regra 1

Se o arquivo for processado com sucesso parcial, ele pode aparecer na aba `Base_Itens` com `status_extracao = parcial` e tambem ter um registro complementar na aba `Erros`.

### Regra 2

Se nenhum item util for extraido, o arquivo deve aparecer ao menos na aba `Erros`.

### Regra 3

Os nomes de itens encontrados nos exemplos nao devem ser documentados como lista fixa. O parser deve tratar a descricao do item como dado variavel.

### Regra 4

O agrupamento da aba `Resumo_Cidade_Item` deve somar os registros a partir da aba `Base_Itens`.

## Evolucoes futuras

- Aba adicional com totais por documento
- Subtotais por cidade formatados automaticamente
- Score de confianca da extracao
- Identificacao automatica de multiplos tipos de nota
