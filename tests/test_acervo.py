import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
import exegese as app

class AcervoTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'acervo'; self.root.mkdir()

    def test_importar_preserva_bytes_e_recusa_sobrescrita(self):
        source = self.base / 'original.txt'; source.write_bytes('ὀλιγοπιστία\r\nFé\n'.encode())
        path = app.ingest(self.root, source, 'bdag', 'BDAG', 'Mt 17.20')
        self.assertEqual(path.read_bytes(), source.read_bytes())
        with self.assertRaises(FileExistsError):
            app.ingest(self.root, source, 'bdag', 'BDAG', 'Mt 17.20')

    def test_manifesto_detecta_alteracao_e_exclusao(self):
        p = self.root / 'a.md'; p.write_text('origem')
        (self.root / 'manifesto-sha256.json').write_text(json.dumps(app.manifest(self.root)))
        self.assertEqual(app.verify(self.root), [])
        p.write_text('alterado'); self.assertIn('ALTERADO: a.md', app.verify(self.root))
        p.unlink(); self.assertIn('AUSENTE: a.md', app.verify(self.root))

    def test_busca_atualiza_arquivos_removidos_e_nao_interpreta_sql(self):
        p = self.root / 'fonte.md'; p.write_text('Fé e mostarda', encoding='utf-8')
        self.assertTrue(app.search(self.root, 'fe'))
        p.unlink(); self.assertFalse(app.search(self.root, 'mostarda'))
        self.assertEqual(app.search(self.root, '"; DROP TABLE documentos;'), [])

    def test_backup_restaura_bytes_e_recusa_destino_existente(self):
        p = self.root / 'greek.txt'; p.write_bytes('πίστις\r\n'.encode())
        archive = self.base / 'copia.zip'; app.backup(self.root, archive)
        dest = self.base / 'restaurado'; app.restore(archive, dest)
        self.assertEqual(p.read_bytes(), (dest / 'greek.txt').read_bytes())
        with self.assertRaises(FileExistsError): app.restore(archive, dest)

    def test_backup_rejeita_corrupcao(self):
        archive = self.base / 'ruim.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('a.txt', 'modificado')
            z.writestr('BACKUP-SHA256.json', json.dumps({'a.txt': hashlib.sha256(b'original').hexdigest()}))
        with self.assertRaises(ValueError): app.check_backup(archive)

    def test_backup_rejeita_escape(self):
        archive = self.base / 'escape.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('../escape', b'x')
            z.writestr('BACKUP-SHA256.json', json.dumps({'../escape': hashlib.sha256(b'x').hexdigest()}))
        with self.assertRaises(ValueError): app.restore(archive, self.base / 'dest')
        self.assertFalse((self.base / 'escape').exists())

if __name__ == '__main__': unittest.main()
