# Operação e recuperação

## Organização vigente

- metodo/METODO.md: único corpo normativo aprovado.
- metodo/originais e metodo/propostas: fontes históricas preservadas.
- fontes/logos: transcrições intactas, metadados e cobertura.
- estudos: manuscrito cumulativo, relatórios completos, decisões e derivados em funções distintas.
- documentos.json: função, estado e dependências identificadas; não certifica execução.
- historico: registros anteriores à adoção.
- .cache: SQLite reconstruível, fora do Git; manifesto-sha256.json: integridade revisada por lote.

## Revisar e consultar

```bash
python exegese.py documentos
python exegese.py buscar "mostarda" --tipo manuscrito
python exegese.py buscar "mostarda" --historico
python exegese.py revisar MT1714-21-MANUSCRITO
python exegese.py auditar
```

`revisar` lista impacto transitivo potencial pelo cadastro; não edita nem marca aprovação. Ao cadastrar um novo documento, declarar suas fontes de dependência e função. Se o argumento mudou, registrar decisão anterior, nova, evidências, confiança e alcance; revisar manualmente os dependentes pertinentes. Atualizar o cadastro quando surgir relação nova. O mapa por arquivo pode apontar documentos que não precisam de mudança: explicar a conferência no registro de revisão.

`auditar` confere cadastro, existência, ciclos, links locais dos documentos atuais cadastrados, IDs/âncoras/fontes das notas e alguns marcadores internos proibidos no manuscrito. Não verifica links externos, autenticidade de edições, correção do grego, completude do cadastro ou qualidade exegética. A conferência humana do texto acadêmico continua necessária.

A busca comum inclui relatórios preservados e parcialmente superados; estes exibem aviso e caminho da revisão vigente. `--historico` acrescenta versões integralmente históricas. Função documental e situação interpretativa são distintas. A revisão vinculada informa o alcance da superação; não implica revalidar automaticamente o restante. Perguntas e decisões estão cadastradas e devem acompanhar a revisão de suas bases.

## Acrescentar uma fonte

Salvar o texto recebido como UTF-8 e executar:

```bash
python exegese.py importar novo-trecho.txt --id carson-mt17-complemento --referencia "CARSON, D. A. Matthew, 1984, p. 390–392" --passagem "Mt 17.14–20"
python exegese.py buscar "mostarda"
```

Importação preserva bytes, exige identificação e recusa ID já existente. Uma revisão recebe novo ID. Ler o arquivo e comparar com o texto recebido; checksum não prova fidelidade à mensagem original ou à edição impressa. No lote inicial, transcrições foram transportadas da conversa; não são exportações autenticadas pelo Logos.

## Fechar um lote

```bash
python -m unittest discover -s tests -v
python exegese.py auditar
python exegese.py selar
python exegese.py verificar
git diff --stat
git diff
git add .
git commit -m "Documenta etapa e fontes do estudo"
git push
```

Revisar antes de selar: atualizar o manifesto sem revisão pode legitimar alteração acidental. Os comandos Git pressupõem clone configurado e autenticação do proprietário. Não armazenar tokens neste projeto.

## Cópias e restauração

```bash
python exegese.py backup ../copias/exegese-2026-10-26.zip
python exegese.py restaurar ../copias/exegese-2026-10-26.zip ../exegese-restaurada
```

ZIP inclui inventário interno, valida todos os hashes antes de restaurar e não substitui pasta existente. Caminhos de escape são recusados. Guardar a cópia fora da pasta do projeto e, idealmente, em outro dispositivo/serviço. O ZIP contém os arquivos atuais, não todo o histórico Git. Para preservar também o histórico, depois de clonar:

```bash
git bundle create ../copias/exegese-historico.bundle --all
git bundle verify ../copias/exegese-historico.bundle
```

O programa não agenda nem envia backups sozinho. GitHub, clone local e cópia externa são proteções distintas. No iPad, os arquivos podem ser consultados diretamente no GitHub; a execução Python ocorre em computador ou ambiente compatível.

## Limites atuais

Busca lexical, com suporte a acentos e caracteres gregos, sem equivalência automática entre tradução e lema. Não há RAG, interface gráfica, importação direta da base do Logos nem ingestão automática do chat. Esses recursos só devem ser acrescentados sobre uma base documental verificada.

LEIA-PRIMEIRO, FONTES-01 e POSTURA-01 não foram localizados. A autorização de27/10/2026 permite seguir com o corpo consolidado; seus critérios novos são registrados como novos, nunca recuperados. EXE-07,VAL01–06 eCTL02/03 foram encontrados no backup e reavaliados. EXE-16 está retirado; não é pendência operacional.
