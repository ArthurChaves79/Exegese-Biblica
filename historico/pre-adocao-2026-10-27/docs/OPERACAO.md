# Operação e recuperação

## Modelo

- metodo/originais: 22 anexos preservados sem alteração de bytes.
- fontes/logos: transcrições e metadados; cada registro indica cobertura.
- estudos: produção própria, decisões, dúvidas e situação de cada etapa.
- .cache: SQLite reconstruível, fora do Git.
- manifesto-sha256.json: inventário de integridade revisado a cada lote.

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

As referências LEIA-PRIMEIRO, VAL-06, FONTES-01, POSTURA-01, CTL-02 e EXE-16 aparecem em módulos fornecidos, mas seus arquivos não vieram neste lote. Não presumir seu conteúdo. EXE-07 também não foi fornecido.
