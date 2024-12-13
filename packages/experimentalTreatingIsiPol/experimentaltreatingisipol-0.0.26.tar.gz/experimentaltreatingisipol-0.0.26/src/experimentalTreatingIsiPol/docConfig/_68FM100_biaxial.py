'''
Classe utilizada para testes biaxiais. Isso fere, de certa forma, a filosofia original da ferramenta. Contudo, não vejo outra forma por enquanto de ter dois tipos de arquivo para a mesma máquina
'''

class _alpha():
    def __init__(self) -> None:

        self.colunas  = [
                             r'Time'
                            ,r'Deslocamento [mm]'
                            ,r'Força'
                            ,r'Tensão à tração'
                            ,r'Deformação à tração (Deslocamento)'
                            ,r'Strain Gauge 1/Axial Strain' # Deformação axial
                            ,r'Strain Gauge 1/Transverse Strain' # Deformação transversal
                            ,r'Strain Gauge 1/Shear Strain' # Deformação cisalhante
                            ,r'Strain Gauge 1/Minimum Normal Strain' # Deformação mínima local
                            ,r'Strain Gauge 1/Maximum Normal Strain' # Deformação máxima local
                            ,r'Strain Gauge 1/Poissons Ratio' # Razao de Poisson
                            ,r'Strain Gauge 1/Axial Displacement' # Deslocamento axial
                            ,r'Strain Gauge 1/Transverse Displacement' # Deslocamento transversal
                         ]
        
        self.column_delimitador = ','
        self.decimal = '.'