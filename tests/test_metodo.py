import json
from pathlib import Path
import tempfile
import unittest
import exegese as app

class MetodoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def cadastro(self, items):
        (self.root/'documentos.json').write_text(json.dumps({'documentos':items}))

    def doc(self, id, path, tipo='acervo', deps=()):
        return dict(id=id,path=path,tipo=tipo,estado='atual',depende_de=list(deps))

    def test_busca_separa_manuscrito_e_historico(self):
        (self.root/'manuscrito.md').write_text('mostarda')
        h=self.root/'metodo/originais';h.mkdir(parents=True);(h/'antigo.md').write_text('mostarda')
        self.cadastro([self.doc('M','manuscrito.md','manuscrito')])
        self.assertEqual([p for p,_ in app.search(self.root,'mostarda')],['manuscrito.md'])
        self.assertEqual(len(app.search(self.root,'mostarda',historical=True)),2)
        self.assertEqual(len(app.search(self.root,'mostarda',kind='manuscrito')),1)

    def test_impacto_transitivo_e_recusa_caminho_desconhecido(self):
        self.cadastro([self.doc('A','a.md'),self.doc('B','b.md',deps=['A']),self.doc('C','c.md',deps=['B'])])
        self.assertEqual([d['id'] for d in app.dependents(self.root,'a.md')],['B','C'])
        with self.assertRaises(ValueError): app.dependents(self.root,'desconhecido.md')

    def test_auditoria_detecta_ciclo_link_metadado_e_dependencia(self):
        (self.root/'a.md').write_text('EXE-03 [ausente](nada.md)')
        (self.root/'b.md').write_text('texto')
        self.cadastro([self.doc('A','a.md','manuscrito',['B','X']),self.doc('B','b.md',deps=['A'])])
        errors='\n'.join(app.audit(self.root))
        for marker in ['Ciclo','Vínculo ausente','Metadados internos','Dependência desconhecida']:
            self.assertIn(marker,errors)

    def test_notas_detectam_ancora_perdida(self):
        (self.root/'a.md').write_text('texto')
        self.cadastro([self.doc('A','a.md')])
        d=self.root/'estudos/teste';d.mkdir(parents=True)
        (d/'notas-logos.json').write_text(json.dumps({'notes':[dict(id='N001',master=dict(path='a.md',anchor='perdida'),sources=[])]}))
        self.assertTrue(any('Âncora de nota ausente' in e for e in app.audit(self.root)))

if __name__=='__main__':unittest.main()
