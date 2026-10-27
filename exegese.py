#!/usr/bin/env python3
"""Acervo exegético: arquivos são a fonte; SQLite é um índice descartável."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
EXCLUDED = {'.git', '.cache', 'backups', '__pycache__'}

def files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and not any(x in EXCLUDED for x in p.relative_to(root).parts))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def manifest(root):
    return {p.relative_to(root).as_posix(): digest(p) for p in files(root)
            if p.name != 'manifesto-sha256.json'}

def verify(root):
    target = root / 'manifesto-sha256.json'
    if not target.exists():
        return ['Manifesto ausente. Execute selar após revisar os arquivos.']
    expected = json.loads(target.read_text(encoding='utf-8'))
    actual = manifest(root)
    errors = []
    for name in sorted(set(expected) | set(actual)):
        if name not in expected:
            errors.append('NOVO: ' + name)
        elif name not in actual:
            errors.append('AUSENTE: ' + name)
        elif expected[name] != actual[name]:
            errors.append('ALTERADO: ' + name)
    for p in sorted((root / 'fontes').rglob('*.json')):
        if p.name.endswith('.meta.json'):
            record = json.loads(p.read_text(encoding='utf-8'))
            text = p.with_name(p.name.replace('.meta.json', '.txt'))
            if not text.exists() or digest(text) != record['sha256']:
                errors.append('FONTE INCONSISTENTE: ' + str(p.relative_to(root)))
    return errors

def catalog(root):
    path = root / 'documentos.json'
    return json.loads(path.read_text(encoding='utf-8'))['documentos'] if path.exists() else []

def classification(root, name):
    for item in catalog(root):
        if item['path'] == name:
            return item['tipo'], item['estado']
    if name.startswith(('historico/', 'metodo/originais/', 'metodo/propostas/')):
        return 'historico', 'historico'
    if name.startswith('fontes/'):
        return 'fonte', 'preservado'
    return 'acervo', 'atual'

def dependents(root, changed):
    records = catalog(root)
    by_id = {d['id']: d for d in records}
    starts = {d['id'] for d in records if changed in (d['id'], d['path'])}
    if not starts:
        raise ValueError('Documento não cadastrado; cadastre seu vínculo antes de rastrear revisão.')
    affected = set(starts)
    while True:
        found = {d['id'] for d in records if set(d.get('depende_de', [])) & affected}
        if found <= affected:
            break
        affected |= found
    return [by_id[i] for i in sorted(affected - starts)]

def audit(root):
    records = catalog(root)
    if not records:
        return ['Cadastro documentos.json ausente ou vazio.']
    errors = []
    ids = [d['id'] for d in records]; paths = [d['path'] for d in records]
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        errors.append('Cadastro com IDs ou caminhos duplicados.')
    by_id = {d['id']: d for d in records}
    for d in records:
        path = root / d['path']
        if not path.is_file():
            errors.append('Documento ausente: ' + d['path']); continue
        for dep in d.get('depende_de', []):
            if dep not in by_id:
                errors.append('Dependência desconhecida: ' + dep)
        if d['tipo'] == 'manuscrito':
            text = path.read_text(encoding='utf-8')
            if re.search(r'EXE[-‐–]?\d|VAL[-‐–]?\d|CTL[-‐–]?\d|\bcommit\b|\bversão\s*\d|módulo\s*\d', text, re.I):
                errors.append('Metadados internos no manuscrito: ' + d['path'])
        if path.suffix == '.md' and d['estado'] == 'atual':
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#'):
                    continue
                target = (path.parent / link.split('#')[0]).resolve()
                if not target.exists():
                    errors.append('Vínculo ausente em ' + d['path'] + ': ' + link)
    # Dependency cycles would make propagation ambiguous.
    def visit(identifier, active, done):
        if identifier in active:
            errors.append('Ciclo de dependências: ' + identifier); return
        if identifier in done or identifier not in by_id:
            return
        active.add(identifier)
        for dep in by_id[identifier].get('depende_de', []):
            visit(dep, active, done)
        active.remove(identifier); done.add(identifier)
    done = set()
    for identifier in by_id:
        visit(identifier, set(), done)
    for p in (root / 'estudos').rglob('notas-logos.json'):
        notes = json.loads(p.read_text(encoding='utf-8'))['notes']
        note_ids = [n['id'] for n in notes]
        if len(note_ids) != len(set(note_ids)):
            errors.append('IDs de notas duplicados: ' + str(p))
        for note in notes:
            master = root / note['master']['path']
            if not master.exists() or ('id="' + note['master']['anchor'] + '"') not in master.read_text(encoding='utf-8'):
                errors.append('Âncora de nota ausente: ' + note['id'])
            for source in note.get('sources', []):
                if not (root / source).is_file():
                    errors.append('Fonte de nota ausente: ' + source)
    return errors

def index(root):
    cache = root / '.cache'
    cache.mkdir(exist_ok=True)
    db = sqlite3.connect(cache / 'consulta.sqlite3')
    with db:
        db.execute('DROP TABLE IF EXISTS documentos')
        db.execute("CREATE VIRTUAL TABLE documentos USING fts5(caminho UNINDEXED, texto, tokenize='unicode61 remove_diacritics 2')")
        for p in files(root):
            if p.suffix in {'.md', '.txt', '.json'} and p.name != 'manifesto-sha256.json':
                db.execute('INSERT INTO documentos VALUES (?, ?)',
                           (p.relative_to(root).as_posix(), p.read_text(encoding='utf-8')))
    db.close()

def search(root, query, kind=None, historical=False):
    # Reconstruir evita resultados de documentos apagados ou versões antigas.
    index(root)
    terms = re.findall(r'\w+', query, re.UNICODE)
    if not terms:
        return []
    expression = ' AND '.join('"' + term + '"' for term in terms)
    with sqlite3.connect(root / '.cache' / 'consulta.sqlite3') as db:
        rows = db.execute("SELECT caminho, snippet(documentos, 1, '[', ']', ' … ', 36) FROM documentos WHERE documentos MATCH ? ORDER BY rank", (expression,)).fetchall()
        selected = []
        for name, snippet in rows:
            item_kind, state = classification(root, name)
            if (historical or state != 'historico') and (kind is None or item_kind == kind):
                selected.append((name, snippet))
        return selected[:30]

def ingest(root, source, identifier, reference, passage, coverage='trecho fornecido pelo usuário'):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,100}', identifier):
        raise ValueError('ID deve conter apenas letras minúsculas, números e hífens.')
    data = Path(source).read_bytes()
    data.decode('utf-8')  # validar, sem transformar os bytes
    folder = root / 'fontes' / 'logos'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / (identifier + '.txt')
    metadata = folder / (identifier + '.meta.json')
    if target.exists() or metadata.exists():
        raise FileExistsError('ID já existe; preserve o original e use um novo ID para a revisão.')
    record = dict(id=identifier, referencia=reference, passagem=passage,
                  cobertura=coverage, origem='Logos — texto fornecido pelo usuário',
                  recebido_em=datetime.now(timezone.utc).isoformat(),
                  sha256=hashlib.sha256(data).hexdigest(),
                  direitos='Direitos da obra pertencem aos respectivos titulares; nenhuma licença de redistribuição é concedida pelo projeto.')
    # Falha intermediária fica detectável; nenhuma fonte existente é substituída.
    with target.open('xb') as f:
        f.write(data)
    with metadata.open('x', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return target

def backup(root, destination):
    destination = Path(destination).resolve()
    members = files(root)
    if destination.exists():
        raise FileExistsError('Backup existente; escolha outro nome.')
    # Arquivo temporário só é publicado depois da leitura e validação completa.
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=destination.parent, suffix='.zip')
    os.close(fd)
    try:
        sums = {}
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in members:
                name = p.relative_to(root).as_posix()
                data = p.read_bytes()
                sums[name] = hashlib.sha256(data).hexdigest()
                z.writestr(name, data)
            z.writestr('BACKUP-SHA256.json', json.dumps(sums, ensure_ascii=False, indent=2))
        check_backup(Path(temp))
        os.replace(temp, destination)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)

def check_backup(path):
    with zipfile.ZipFile(path) as z:
        sums = json.loads(z.read('BACKUP-SHA256.json'))
        if set(z.namelist()) != set(sums) | {'BACKUP-SHA256.json'}:
            raise ValueError('Inventário do backup não confere.')
        if len(z.namelist()) != len(set(z.namelist())):
            raise ValueError('Entradas duplicadas no backup.')
        for name, expected in sums.items():
            if hashlib.sha256(z.read(name)).hexdigest() != expected:
                raise ValueError('Checksum incorreto: ' + name)
        return sums

def restore(archive, destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError('Restaure em uma pasta nova para não substituir dados.')
    sums = check_backup(archive)
    for name in sums:
        if '\\' in name or ':' in name or name.startswith('/') or '..' in Path(name).parts:
            raise ValueError('Caminho inseguro no backup.')
    destination.mkdir(parents=True)
    with zipfile.ZipFile(archive) as z:
        for name in sums:
            write_atomic(destination / name, z.read(name))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raiz', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    for cmd in ('verificar', 'selar', 'indexar', 'status', 'auditar', 'documentos'):
        sub.add_parser(cmd)
    p = sub.add_parser('buscar'); p.add_argument('consulta')
    p.add_argument('--tipo', choices=['metodo', 'manuscrito', 'acervo', 'fonte', 'derivado', 'historico'])
    p.add_argument('--historico', action='store_true')
    p = sub.add_parser('revisar'); p.add_argument('documento')
    p = sub.add_parser('importar'); p.add_argument('arquivo', type=Path)
    p.add_argument('--id', required=True); p.add_argument('--referencia', required=True)
    p.add_argument('--passagem', required=True)
    p = sub.add_parser('backup'); p.add_argument('destino', type=Path)
    p = sub.add_parser('restaurar'); p.add_argument('arquivo', type=Path); p.add_argument('destino', type=Path)
    args = parser.parse_args(); root = args.raiz.resolve()
    try:
        if args.command == 'verificar':
            errors = verify(root)
            print('\n'.join(errors) if errors else 'Integridade verificada.')
            return 1 if errors else 0
        if args.command == 'selar':
            write_atomic(root / 'manifesto-sha256.json', (json.dumps(manifest(root), ensure_ascii=False, indent=2) + '\n').encode())
            print('Manifesto atualizado. Revise o diff antes do commit.')
        elif args.command == 'indexar':
            index(root); print('Índice reconstruído.')
        elif args.command == 'buscar':
            for name, snippet in search(root, args.consulta, args.tipo, args.historico):
                print(name + '\n' + snippet + '\n')
        elif args.command == 'importar':
            print(ingest(root, args.arquivo, args.id, args.referencia, args.passagem))
            print('Importado localmente. Ainda é necessário revisar, selar, fazer commit e enviar ao GitHub.')
        elif args.command == 'backup':
            backup(root, args.destino); print('Backup criado e verificado: ' + str(args.destino))
        elif args.command == 'restaurar':
            restore(args.arquivo, args.destino); print('Backup restaurado em pasta nova.')
        elif args.command == 'auditar':
            errors = audit(root)
            print('\n'.join(errors) if errors else 'Organização e vínculos conferidos; mérito exegético não avaliado.')
            return 1 if errors else 0
        elif args.command == 'documentos':
            for item in catalog(root):
                print(item['id'] + ' | ' + item['tipo'] + ' | ' + item['estado'] + ' | ' + item['path'])
        elif args.command == 'revisar':
            for item in dependents(root, args.documento):
                print(item['id'] + ' | ' + item['path'])
            print('Lista de impacto potencial; revisão de conteúdo precisa ser registrada pelo pesquisador.')
        elif args.command == 'status':
            print((root / 'estudos/mateus/17-14-20/estado.json').read_text(encoding='utf-8'))
        return 0
    except (OSError, ValueError, sqlite3.Error, KeyError, zipfile.BadZipFile) as exc:
        print('ERRO: ' + str(exc)); return 1

if __name__ == '__main__':
    raise SystemExit(main())
