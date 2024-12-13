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
        self.testType = ['tensile']


class _beta():
    def __init__(self) -> None:

        self.colunas  = [
                             r'Tempo'
                            ,r'Deslocamento [mm]'
                            ,r'Força'
                            ,r'Tensão à tração'
                            ,r'Deformação à tração (Deslocamento)'
                            ,r'Extens Bi Axial - Connector 6'
                            ,r'Extens Bi Trans - Conector 5'
                         ]
        self.column_delimitador = ';'
        self.decimal = ','
        self.skip_rows = 18
        self.testType = ['tensile','flexural']


    
class _gamma():
    def __init__(self) -> None:

        self.colunas  = [
                             r'Tempo'
                            ,r'Deslocamento [mm]'
                            ,r'Força'
                            ,r'Tensão à tração'
                            ,r'Deformação à tração (Deslocamento)'
                            ,r'Deformação digital 1'
                         ]
        self.column_delimitador = ';'
        self.decimal = ','
        self.testType = ['tensile']


class _delta():
    def __init__(self) -> None:

        self.colunas  = [
                             r'Tempo'
                            ,r'Deslocamento [mm]'
                            ,r'Força'
                            ,r'Tensão à tração'
                            ,r'Deformação à tração (Deslocamento)'
                         ]
        self.column_delimitador = ';'
        self.decimal = ','
        self.testType = ['tensile']

class _epsilon():
    def __init__(self) -> None:

        self.colunas  = ['Tempo','Deslocamento','Força','Extensometro']
        self.column_delimitador = ';'
        self.decimal = ','
        self.testType = ['tensile'] # Array com tipos de testes utilizados

class _zeta():
    def __init__(self) -> None:

        self.colunas  = [
                             r'Time measurement'
                            ,r'Extension'
                            ,r'Primary load measurement'
                            ,r'W-E401'
                            ,r'Deformação à flexão (W-E401)'
                            ,r'Deslocamento à flexão'
                            ,r'Tensão à flexão'
        ]
        self.column_delimitador = ';'
        self.decimal = ','
        self.skip_rows = 18
        self.testType = ['flexural'] # Array com tipos de testes utilizados



class _eta():
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
        self.testType = ['shear'] # Array com tipos de testes utilizados



class _omicron():
    def __init__(self) -> None:

        self.colunas  = [
                            r'Time',
                            r'Deslocamento',
                            r'Força',
                            r'Tensão ao cisalhamento',
                            r'Deformação ao cisalhamento (Deslocamento)',
                            r'Extensometer 1/Engineering Strain',
                            r'Extensometer 1/True Strain',
                            r'Extensometer 1/Distance Change L(t)-L0',
                            r'Extensometer 1/Distance L(t)',
                            r'Extensometer 2/Engineering Strain',
                            r'Extensometer 2/True Strain',
                            r'Extensometer 2/Distance Change L(t)-L0',
                            r'Extensometer 2/Distance L(t)'
                         ]
        
        self.column_delimitador = ','
        self.decimal = '.'
        self.skip_rows = 100
        self.testType = ['shear'] # Array com tipos de testes utilizados


class _pi():
    def __init__(self) -> None:

        self.colunas  = [
                             r'Tempo'
                            ,r'Deslocamento'
                            ,r'Força'
                            ,r'Deformação à compressão (Deslocamento)'
                            ,r'Tensão à compressão'
                         ]
        
        self.column_delimitador = ';'
        self.decimal = ','
        self.skip_rows = 10
        self.testType = ['compression'] # Array com tipos de testes utilizados



class _rho():
    def __init__(self) -> None:

        self.colunas  = [
                             r'Tempo'
                             ,r'Deslocamento'
                            ,r'Força'
                            ,r'Tensão à tração'
                            ,r'Extens Bi Axial - Connector 6'
                            ,r'Extens Bi Trans - Conector 5'
                            ,r'Deformação à tração (Extens Bi Axial - Connector 6)'
                         ]
        
        self.column_delimitador = ';'
        self.decimal = ','
        self.skip_rows = 30
        self.testType = ['tensile'] # Array com tipos de testes utilizados

mapping_translate = {
    'tensile':'Tração'
    ,'flexural':'Flexão'
    ,'compression':'Compressão'
    ,'shear':'Cisalhamento'
}

def print_docConfig():
    '''
    Função para mostrar cada uma das pré-formatações configuradas para as máquinas.
    '''
    docConfigsClass = [
        _alpha
        ,_beta
        ,_gamma
        ,_delta
        ,_epsilon
        ,_zeta
        ,_omicron
        ,_pi
        ,_rho
    ]

    docConfigParam = [
                '_alpha'
                ,'_beta'
                ,'_gamma'
                ,'_delta'
                ,'_epsilon'
                ,'_zeta'
                ,'_omicron'
                ,'_pi'
                ,'_rho'
    ]
    for each_docConfigClass, each_docConfigName in zip(docConfigsClass, docConfigParam):
        ClassInit = each_docConfigClass()

        string_tests = ""

        for each_test in ClassInit.testType:
            string_tests+=f'''
    - {mapping_translate[each_test]}
'''

        string_coluns = ""
        for each_colum in ClassInit.colunas:
            string_coluns+=f'''
    - {each_colum}
'''
        print(f'''
_________________________________________________________________________________________
              
================================|  Configuração |========================================
docConfig {each_docConfigName}

Geralmente utilizado para testes de :

{string_tests}
================================|    Colunas    |========================================
{string_coluns}
_________________________________________________________________________________________
''')    
            


