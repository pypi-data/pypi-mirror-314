class GeneralMachine():

    def __init__(self, colunas, column_delimitador, decimal, skip_rows, x_column, y_column) -> None:

        self.colunas  = colunas
        self.column_delimitador = column_delimitador
        self.decimal = decimal
        self.skip_rows = skip_rows
        self.x_column =  x_column
        self.y_column =  y_column