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

    def test_acervo_parcial_recuperavel_com_aviso_e_revisao(self):
        (self.root/'relatorio.md').write_text('Emanuel')
        (self.root/'revisao.md').write_text('Eco deliberado não demonstrado')
        d=self.doc('R','relatorio.md'); d.update(estado='parcialmente_superado',revisao_vigente='revisao.md',alcance_superacao='Eco deliberado')
        self.cadastro([d,self.doc('V','revisao.md')])
        found=app.search(self.root,'Emanuel',kind='acervo')
        self.assertEqual(found[0][0],'relatorio.md')
        self.assertIn('PARCIALMENTE SUPERADO',found[0][1])
        self.assertIn('revisao.md',found[0][1])
        self.assertEqual(app.audit(self.root),[])
        (self.root/'revisao.md').unlink()
        self.assertTrue(any('Superação parcial' in e for e in app.audit(self.root)))

if __name__=='__main__':unittest.main()
