# Acervo de Exegese Bíblica

Pesquisa de Arthur Chaves. Arquivos abertos e versionados, com consulta local em Python.

## Começar

Requer Python 3.10 ou superior com SQLite FTS5 (disponível nas distribuições usuais). Sem serviços externos, API ou dependências pip.

```bash
python exegese.py status
python exegese.py buscar "pouca fé"
python exegese.py verificar
python -m unittest discover -s tests -v
```

- [Estudo atual — Mateus 17.14–20](estudos/mateus/17-14-20/README.md)
- [Método original](metodo/originais/)
- [Fontes e procedência](fontes/README.md)
- [Operação e preservação](docs/OPERACAO.md)
- [Protocolo para continuidade com assistentes](AGENTS.md)

Markdown/TXT/JSON são a fonte de verdade. SQLite é somente índice reconstruível. Não há conexão automática com ChatGPT ou Logos. Este programa não interpreta as Escrituras autonomamente: organiza material para pesquisa responsável.

## Estado inicial

Versão 0.1, 26/10/2026. Migração retrospectiva do material disponível nesta conversa. Etapas anteriores ao EXE-08B estão consolidadas como sínteses, não como transcrição integral das respostas históricas. Não se declara recuperação integral de conversas não disponíveis. EXE-08C e etapas seguintes continuam pendentes; Mt 17.1–13 permanece reservado.

## Preservação

Git mantém versões; `verificar` detecta alteração em relação ao manifesto; `backup` cria ZIP verificável; `restaurar` recupera em pasta nova. Não existe garantia de perda zero. Manter um clone e uma cópia fora do GitHub é parte do procedimento. CI verifica testes e integridade a cada push, quando executado pelo GitHub.

## Direitos

O projeto não concede licença sobre obras de terceiros. Trechos de fontes têm titularidade e referência próprias. A visibilidade do repositório deve ser considerada ao acrescentar material do Logos; uma coleção de pesquisa com transcrições extensas é mais adequada a repositório privado. A ferramenta não muda a visibilidade do GitHub.
