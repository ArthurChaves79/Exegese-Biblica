# Verificação da implantação manual

Base: commit 71b5b88e501ff54b6bed2af3fc2bbfb042f4609e da branch estudo/1joao-2-18-27-rodada-01.

Antes das alterações: 11 testes existentes passaram. Auditoria documental apresentou duas falhas antigas nas fontes das notas de Mateus (URL externa tratada como arquivo e caminho com fragmento tratado como arquivo). O manifesto global já estava desatualizado para arquivos de 1João e alterações anteriores de Mateus/método. Essas falhas não foram corrigidas ou certificadas como resolvidas nesta implantação.

O cadastro e o piloto não editam método, estudos, decisões ou manuscritos. A checagem local deve demonstrar IDs únicos, caminhos existentes, decisões localizadas no snapshot, múltiplos impactos, estado pendente, ausência de autorização de mudança, duas consultas ao mesmo registro e classificação do manuscrito de 1João. A fase 3 automatizará validações recorrentes; estes testes são conferência de implantação.

O manifesto recebe somente hashes dos arquivos desta implantação; as divergências anteriores permanecem visíveis. Isso não equivale a selagem completa do acervo nem aprovação exegética da relação.

## Resultado local

- Os 11 testes existentes passaram antes e depois do cadastro.
- Cadastrados 37 arquivos de 1João; 83 IDs de decisão localizados, preservando a ausência de D19.
- Conferidos unicidade, caminhos, IDs candidatos, linhas e hashes dos localizadores.
- Confirmados quatro níveis de impacto, hipótese pendente sem grau atribuído e nenhuma autorização para alterar estudos.
- Os dois polos consultam REL-000001; João 3 continua referência sem estudo criado.
- Busca por manuscrito encontra 1João; propagação da síntese para seu manuscrito funciona. Dependências não exaustivas continuam declaradas.
- A auditoria documental mantém somente as duas falhas antigas de Mateus.
- Método e todos os arquivos dos estudos permanecem sem diferenças em relação ao commit-base.

Estes resultados verificam a implantação documental, não a força exegética da relação.
