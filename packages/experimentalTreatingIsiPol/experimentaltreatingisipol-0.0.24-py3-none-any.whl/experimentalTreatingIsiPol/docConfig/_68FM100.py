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