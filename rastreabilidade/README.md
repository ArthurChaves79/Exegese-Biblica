# SRIEC — piloto manual, fases 1 e 2

O método geral continua em [METODO.md](../metodo/METODO.md). Este diretório localiza decisões e registra avaliações de relações; não estabelece conclusões para as passagens. Nenhuma automação nova foi implantada.

- [Estudos e referências](estudos.json): estado real de cada polo, inclusive referência ainda não estudada.
- [Localizadores de decisões](decisoes.json): IDs locais preservados e qualificados pelo estudo; linhas e hashes do commit-base.
- [REL-000001](relacoes/REL-000001.json): hipótese pendente entre 1João 2.18–27 e João 3.3–8.
- [Verificação e limites](VERIFICACAO.md).

## Consulta bidirecional manual

| Polo | Registro único |
|---|---|
| 1JO-02-18-27 — estudo existente | [REL-000001](relacoes/REL-000001.json) |
| JO-03-03-08 — referência não estudada | [REL-000001](relacoes/REL-000001.json) |

Os dois polos apontam para o mesmo JSON. Os índices em estudos.json e nesta página são projeções manuais conferidas contra ele; futura geração automática pertence à fase 3. Não foi criado um estudo fictício de João 3 nem alterado qualquer estudo existente.

## Convenções do piloto

Força usa Alto, Moderado ou Baixo; null significa não avaliada. Cada impacto tem alvo, nível, tipo, estado e consequência próprios. Aprovar uma relação não autoriza suas alterações documentais: aprovação deve identificar a avaliação e o diff exatos. Uma referência recíproca não é uma dependência de conteúdo. Não inserir este grafo no depende_de documental.

A revisão precisa comparar proposição, dois polos e evidências antes de declarar duplicata. Novas proposições entre os mesmos textos são permitidas. Não contar fontes, relatórios ou decisões derivados do mesmo fundamento como apoios independentes. Consultar a decisão e sua evidência no snapshot; o identificador não transforma uma conclusão em fonte primária.

## Limites da primeira implantação

Só as decisões de 1João foram localizadas nesta fase; Mateus conserva os identificadores atuais no catálogo documental. D19 não foi criada para preencher a lacuna. As dependências dos relatórios de 1João ainda não são exaustivas: o catálogo localiza todos os arquivos e oferece mapa conservador da base do manuscrito. Rastrear um relatório isolado pode não enumerar todos os afetados. O índice semântico, detecção automática de duplicatas, validação permanente de relações e propagação por decisão não foram implementados.
