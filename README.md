# Acervo de Exegese Bíblica

Pesquisa de Arthur Chaves: fontes preservadas, investigação revisável e redação acadêmica progressiva.

- [Método vigente](metodo/METODO.md) — aprovado em 27/10/2026.
- [Manuscrito acadêmico de Mateus 17.14–21](estudos/mateus/17-14-20/manuscrito-academico.md) — exposição cumulativa principal.
- [Acervo e relatórios de Mateus](estudos/mateus/17-14-20/README.md).
- [Notas preparadas para o Logos](estudos/mateus/17-14-20/notas-logos.md) — não transferidas.
- [Revisão de adequação ao método](estudos/mateus/17-14-20/revisao-metodo.md).
- [Operação](docs/OPERACAO.md) · [Continuidade](AGENTS.md) · [Adoção e histórico](metodo/historico/ADOCAO-2026-10-27.md).

## Consulta

Python 3.10+ com SQLite FTS5, sem dependências pip. Markdown/TXT/JSON são a fonte; SQLite é reconstruível.

```bash
python exegese.py status
python exegese.py buscar "pouca fé" --tipo manuscrito
python exegese.py documentos
python exegese.py auditar
python exegese.py revisar estudos/mateus/17-14-20/manuscrito-academico.md
python exegese.py verificar
```

A busca separa manuscrito, acervo, fontes, derivados e método. Materiais históricos são omitidos por padrão; use `--historico` para incluí-los. Os controles automáticos verificam organização e vínculos, não o mérito das interpretações.

Git, manifesto e backups verificáveis protegem o acervo; manter também cópia externa e histórico Git. Não há garantia de perda zero, ingestão automática do chat ou integração direta com Logos. Trechos de terceiros conservam seus direitos; o projeto não concede licença de redistribuição sobre essas obras.
