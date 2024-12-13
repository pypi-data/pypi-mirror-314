# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from experimentalTreatingIsiPol.docConfig import _alpha, _beta, _gamma, _delta, _epsilon, _zeta, _eta, _omicron, _pi,_rho
from experimentalTreatingIsiPol.docConfig._generalMachine import GeneralMachine
import os
import re
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io  # For working with in-memory files
from matplotlib.backends.backend_pdf import PdfPages
import warnings


blue_tonalities_options = [
    '#1f0794', 
    '#000080', 
    '#6476d1', 
    '#00008B', 
    '#003366', 
    '#191970', 
    '#0000CD', 
    '#27414a', 
    '#4B0082', 
    '#2f6b6b', 
    '#00688B', 
    '#483D8B', 
    '#4682B4', 
    '#708090', 
    '#4169E1', 
    '#778899', 
    '#7B68EE', 
    '#6495ED'
]


linestyles_options = [
    "-",    # solid
    "--",   # dashed
    "-.",   # dashdot
    ":",    # dotted
    " ",    # no line (blank space)
    "-",    # solid (thicker)
    (0, (1, 10)), # loosely dotted
    (0, (5, 10)), # loosely dashed
    (0, (3, 5, 1, 5)), # dashdotted
    (0, (3, 1, 1, 1)), # densely dashdotted
    (0, (5, 5)),  # dashed with same dash and space lengths
    (5, (10, 3)), # long dashes with offset
    (0, (3, 10, 1, 15)), # complex custom dash pattern
    (0, (1, 1)), # densely dotted
    (0, (1, 5)), # moderately dotted
    (0, (3, 1)), # densely dashed
    (0, (3, 5, 1, 5, 1, 5)), # dashdotdot
    (0, (3, 10, 1, 10, 1, 10)), # dashdashdash
]

marker_options = [
    ".",      # point
    ",",      # pixel
    "o",      # circle
    "v",      # triangle down
    "^",      # triangle up
    "<",      # triangle left
    ">",      # triangle right
    "1",      # tripod down
    "2",      # tripod up
    "3",      # tripod left
    "4",      # tripod right
    "s",      # square
    "p",      # pentagon
    "*",      # star
    "h",      # hexagon1
    "H",      # hexagon2
    "+",      # plus
    "x",      # x
    "D",      # diamond
    "d",      # thin diamond
]

def plot_helper(ax,x,y,label,xlabel,ylabel,color='blue', linestyle='-.', marker='<', markersize=1, linewidth=1,**kwargs):

    ax.plot(x,y, label = label, color = color, marker = marker, 
            markersize = markersize, 
            linestyle = linestyle,
            linewidth = linewidth,**kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def scatter_helper(ax,x,y,label, xlabel, ylabel,color='blue', marker='+', markersize=10, **kwargs):

    ax.scatter(x,y, label = label, color = color, marker = marker,
             s = markersize,
             **kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def several_plots_helper(ax,xs,ys,labels,xlabel,ylabel,colors: list | None = None, 
                         linestyles: list | None =None, markers : list | None = None, 
                         markersize=1, linewidth=1.5, 
                         color_scheme = 'blue_tonalities_options',
                         filter_data = False,
                         **kwargs
                         ):
    '''
    Função para plotar diversos gráficos.
    '''
    if len(xs)!=len(ys):
        raise Exception('As dimensões das variáveis xs e ys devem ser iguais.')
    
    if len(labels)!=len(ys):
        raise Exception('A quantidade de labels deve ser igual à quantidade de pares.')
    

    if not (colors and markers and linestyles): 

        for each_x, each_y, each_label in zip(xs,ys,labels):
 
            if len(each_x)>100 and filter_data:
                slice = int(len(each_x)/100)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            if color_scheme ==  'blue_tonalities_options': # adicionando opcao para tonalidade de azul
                color = blue_tonalities_options[np.random.random_integers(0,17)]
            if color_scheme ==  'matplotlib_default':
                color = None
            marker = marker_options[np.random.random_integers(0,17)]
            linestyle = linestyles_options[np.random.random_integers(0,17)]

            ax.plot(each_x,each_y, label = each_label, color = color, marker = None, 
                    markersize = markersize, 
                    linestyle = None,
                    linewidth = linewidth,**kwargs)

    else:
        for each_x, each_y, each_label,each_color, each_marker, each_linestyle in zip(xs,ys,labels,colors,markers,linestyles): 
            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            ax.plot(each_x,each_y, label = each_label, color = each_color, marker = each_marker, 
                    markersize = markersize, 
                    linestyle = each_linestyle,
                    linewidth = linewidth,**kwargs)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig_obj = ax.get_figure()
    fig_height = fig_obj.get_figheight()
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -fig_height/20),
        ncol=3,
        framealpha=1,
        )
    
    return ax

def several_scatter_helper(ax,xs,ys,labels,xlabel,ylabel,colors: list | None = None, linestyles: list | None =None, markers : list | None = None, markersize=1, linewidth=1, **kwargs):
    '''
    Função para plotar diversos gráficos.

    PAREI AQUI
    '''
    if len(xs)!=len(ys):
        raise Exception('As dimensões das variáveis xs e ys devem ser iguais.')
    
    if len(labels)!=len(ys):
        raise Exception('A quantidade de labels deve ser igual à quantidade de pares.')
    
    ax.grid()

    if not (colors and markers and linestyles): 

        for each_x, each_y, each_label in zip(xs,ys,labels): 

            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            color = blue_tonalities_options[np.random.random_integers(0,17)]
            marker = marker_options[np.random.random_integers(0,17)]

            ax.scatter(each_x,each_y, label = each_label, color = color, marker = marker, 
                    s = markersize, 
                    **kwargs)

    else:
        for each_x, each_y, each_label,each_color, each_marker in zip(xs,ys,labels,colors,markers): 
           
            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            ax.scatter(each_x,each_y, label = each_label, color = each_color, marker = each_marker, 
                    s = markersize, 
                    **kwargs)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig_obj = ax.get_figure()
    fig_height = fig_obj.get_figheight()
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -fig_height/15),
        ncol=3,
        framealpha=1,
        )
    
    return ax

class ReadExperimentalData():
    
    def __init__(self, archive_name,
                 column_delimitador = ';',
                 skiprows = 10,
                 decimal = ','):
        
        self.raw_data = pd.read_csv(archive_name, sep=column_delimitador,
                                                encoding_errors='backslashreplace', 
                                                on_bad_lines='skip', 
                                                skiprows=skiprows, 
                                                decimal=decimal)

class MechanicalTestFittingLinear():
    '''
    Classe para determinar propriedades mecânicas em regimes lineares. Ela servirão para Moduli de Young e Cisalhamento. 
    '''
    def __init__(self, docConfig: str, archive_name : str, linearRegionSearchMethod='Deterministic', verbose : bool = True, 
                 direction : str = '11',
                 generalMachineData : GeneralMachine = None,
                 x_min = None,
                 x_max = None 
                 ) -> None:
        
        self.verbose = verbose
        self.docConfig = docConfig
        self.x_min = x_min
        self.x_max = x_max

        self.direction = direction

        self.rawdata, self.cleaned_raw_data, deformation_range_x, force = self.dataExtract(docConfig=docConfig, 
                                                                archive_name= archive_name,
                                                                linearRegionSearchMethod=linearRegionSearchMethod,
                                                                generalMachineData  = generalMachineData,
                                                                x_min = x_min,
                                                                x_max = x_max  
                                                                )
        self.deformationRange = None
        pass

    def _alpha_data_aquisition(self, archive_name : str, linearRegionSearchMethod,
                                **kwargs
                               ):
        '''
        Método para a leitura e aquisição de dados de ensaio efetuados na 68FM100
        '''
        docConfig  = _alpha() # Instanciando um novo objeto do tipo Instron 
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=10, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas

        x_strain_DIC = 5

        # Gambiarra para não dividir 2x a deformação do strain gauge
        if x_strain_DIC == 4:
            raw_data[docConfig.colunas[x_strain_DIC]] = raw_data[docConfig.colunas[x_strain_DIC]]/100 # porque está em % (axial)
            raw_data[docConfig.colunas[5]] = raw_data[docConfig.colunas[5]]/100 # porque está em % (axial)
        elif x_strain_DIC == 5:
            raw_data[docConfig.colunas[x_strain_DIC]] = raw_data[docConfig.colunas[x_strain_DIC]]/100 # porque está em % (axial)

        raw_data[docConfig.colunas[6]] = raw_data[docConfig.colunas[6]]/100 # porque está em % (transversal)

        def filter_na(x : float):
            return 2*x == x + x # Se for um nan, retornará como falso
            
        raw_data = raw_data[raw_data[docConfig.colunas[x_strain_DIC]].apply(filter_na)] # filtrando NaN

        x = raw_data[docConfig.colunas[x_strain_DIC]]
        y = raw_data[docConfig.colunas[3]]

        self.y_original = y
        self.x_original = x
        
        new_x, new_y = self.__generalDataAquisition(x=x,y=y, x_label=docConfig.colunas[4], y_label=docConfig.colunas[3], linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[3]]>new_y[0]]

        return raw_data,cleaned_raw_data,new_x,new_y
    
    def _beta_data_aquisition(self, archive_name :  str, linearRegionSearchMethod):
        '''
        Method to analyse data of the older machine (the one used before instron arrived)
        '''

        docConfig  = _beta() # Instanciando um novo objeto do tipo _Older_Machine 
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=docConfig.skip_rows, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas
        offset_num = self.__filterInitGraph(y=raw_data[docConfig.colunas[2]],linearRegionSearchMethod=linearRegionSearchMethod)
        x = raw_data[docConfig.colunas[3]].abs()
        y = raw_data[docConfig.colunas[2]]
        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)
    
        if linearRegionSearchMethod == 'Custom':
            x_linear, y_linear = self.__chooseRegionLinear(x,y,x_min=self.x_min, x_max=self.x_max)

        a,b,root = self.__equationFit(x_linear, y_linear)

        if self.verbose:
            self.plotDataFinalComparison(x,y,x_linear,y_linear,docConfig.colunas[3],docConfig.colunas[2])
            self.plotComparisonExcludedData(x,y,x_linear,y_linear,docConfig.colunas[3],docConfig.colunas[2])

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        if self.verbose:
            self.plotCleanedData(new_x, new_y, docConfig.colunas[3],docConfig.colunas[2])

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)
        self.x_original = x
        self.y_original = y

        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[2]]>new_y[0]]

        return raw_data,cleaned_raw_data, new_x, new_y
    
    def _gamma_data_aquisition(self, archive_name : str, linearRegionSearchMethod,):
        '''
        Método para a aquisição de dados dos testes biaxiais
        '''
        docConfig =  _gamma()
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=3, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas
        raw_data = raw_data.dropna(axis=0) # remove linhas com na
        
        raw_data[docConfig.colunas[4]] = raw_data[docConfig.colunas[4]]/100 # porque está em % (axial)
        raw_data[docConfig.colunas[5]] = raw_data[docConfig.colunas[5]]/100 # porque está em % (axial)
        raw_data[docConfig.colunas[6]] = raw_data[docConfig.colunas[6]]/100 # porque está em % (transversal)
        raw_data[docConfig.colunas[3]] = raw_data[docConfig.colunas[3]]

        x = raw_data[docConfig.colunas[4]]
        y = raw_data[docConfig.colunas[3]]

        self.y_original = y
        self.x_original = x

        new_x, new_y  = self.__generalDataAquisition(x=x,
                                      y=y,
                                      x_label=docConfig.colunas[4], 
                                      y_label=docConfig.colunas[3], 
                                      linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[3]]>new_y[0]]

        return raw_data, cleaned_raw_data, new_x, new_y
    
    def _delta_data_aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Método para aquisição de dados do tipo tração tipo 5 AVE
        '''

        docConfig =  _delta()
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=3, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas
        raw_data = raw_data.dropna(axis=0) # remove linhas com na
        
        x = raw_data[docConfig.colunas[5]]/100 # porque é %
        y = raw_data[docConfig.colunas[3]]
    
        self.y_original = y
        self.x_original = x

        new_x, new_y  = self.__generalDataAquisition(x=x,y=y,
                                      x_label=docConfig.colunas[5], 
                                      y_label=docConfig.colunas[3], 
                                      linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[3]]>new_y[0]]

        return raw_data, cleaned_raw_data, new_x,new_y
    
    def _epsilon_data_aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Metodologia para a aquisição de dados para o corpo de prova tipo 1 
        '''
        docConfig =  _epsilon()
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=3, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas
        raw_data = raw_data.dropna(axis=0) # remove linhas com na
        
        x = raw_data[docConfig.colunas[4]]/100 # porque é %
        y = raw_data[docConfig.colunas[3]]

        self.y_original = y
        self.x_original = x

        new_x, new_y  = self.__generalDataAquisition(x=x,y=y,
                                      x_label=docConfig.colunas[4], 
                                      y_label=docConfig.colunas[3], 
                                      linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[3]]>new_y[0]]

        return raw_data, cleaned_raw_data, new_x,new_y

    def _zeta_data_aquisition(self, archive_name : str, linearRegionSearchMethod):
        docConfig =  _zeta()
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=docConfig.skip_rows, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas
        raw_data = raw_data.dropna(axis=0) # remove linhas com na
    
        force_column_number = 2
        displacement_column_number = 3
        
        x = raw_data[docConfig.colunas[displacement_column_number]].abs()
        y = raw_data[docConfig.colunas[force_column_number]]

        self.y_original = y
        self.x_original = x

        new_x, new_y  = self.__generalDataAquisition(x=x,y=y,
                                      x_label=docConfig.colunas[displacement_column_number], 
                                      y_label=docConfig.colunas[force_column_number], 
                                      linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[force_column_number]]>new_y[0]]

        return raw_data, cleaned_raw_data, new_x,new_y
        pass

    def _eta_data_aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Aquisição para um arquivo do tipo _eta
        '''
        docConfig  = _eta() # Instanciando um novo objeto do tipo Instron 
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=10, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas

        strain_column = 7
        stress_column = 3

        raw_data[docConfig.colunas[strain_column]] = raw_data[docConfig.colunas[strain_column]]/100 # porque está em % (axial)

        x = raw_data[docConfig.colunas[strain_column]]
        x = np.multiply(2,x) # multiplicando por 2, para pegar o "tau"
        y = raw_data[docConfig.colunas[stress_column]]

        self.x_original = x
        self.y_original = y
        
        new_x, new_y = self.__generalDataAquisition(x=x,y=y, x_label=docConfig.colunas[strain_column], y_label=docConfig.colunas[stress_column], linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[stress_column]]>new_y[0]]

        return raw_data,cleaned_raw_data,new_x,new_y
    
    def _omicron_data_aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Ler dados de um arquivo do tipo omicron (dados de cisalhamento com extensometros virtuais)
        '''

        docConfig  = _omicron() # Instanciando um novo objeto do tipo Instron 
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=docConfig.skip_rows, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas

        strain_column_1 = 6
        strain_column_2 = 10
        stress_column = 3

        def filter_na(x : float):
            return 2*x == x + x # Se for um nan, retornará como falso
        
        raw_data = raw_data[raw_data[docConfig.colunas[strain_column_1]].apply(filter_na)]
        raw_data = raw_data[raw_data[docConfig.colunas[strain_column_2]].apply(filter_na)]

        strain_1 = raw_data[docConfig.colunas[strain_column_1]]/100 # porque está em % (Cisalhamento  1)
        strain_2 = raw_data[docConfig.colunas[strain_column_2]]/100 # porque está em % (Cisalhamento  2)


        sum_array = np.sum([np.abs(strain_1.tolist()), np.abs(strain_2.tolist())], axis=0)

        raw_data['ShearStrainTotal'] = sum_array

        x = raw_data['ShearStrainTotal']
        y = raw_data[docConfig.colunas[stress_column]]

        self.x_original = x
        self.y_original = y
        
        new_x, new_y = self.__generalDataAquisition(x=x,y=y, x_label='ShearStrainTotal', y_label=docConfig.colunas[stress_column], linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[stress_column]]>new_y[0]]

        return raw_data,cleaned_raw_data,new_x,new_y

    def _pi_data_aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Aquisição dos dados para o ensaio de compressão
        '''
        docConfig = _pi() # Instanciando um novo objeto do tipo Instron 
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=docConfig.skip_rows, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas

        strain_column = 3
        stress_column = 4

        raw_data[docConfig.colunas[strain_column]] = raw_data[docConfig.colunas[strain_column]]/100 # porque está em % (axial)

        x = raw_data[docConfig.colunas[strain_column]]
        x = np.multiply(2,x) # multiplicando por 2, para pegar o "tau"
        y = raw_data[docConfig.colunas[stress_column]]

        self.x_original = x
        self.y_original = y
        
        new_x, new_y = self.__generalDataAquisition(x=x,y=y, x_label=docConfig.colunas[strain_column], y_label=docConfig.colunas[stress_column], linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[stress_column]]>new_y[0]]

        return raw_data,cleaned_raw_data,new_x,new_y

    def _rho_data_aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Aquisição para dados biaxiais
        '''
    
        docConfig = _rho() # Instanciando um novo objeto do tipo Instron 
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=docConfig.skip_rows, decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas

        strain_column = 4
        stress_column = 3
        transverse_strain = 5

        raw_data[docConfig.colunas[strain_column]] = raw_data[docConfig.colunas[strain_column]]/100 # porque está em % (axial)
        raw_data[docConfig.colunas[transverse_strain]] = raw_data[docConfig.colunas[transverse_strain]]/100 # porque está em % (axial)

        x = raw_data[docConfig.colunas[strain_column]]
        y = raw_data[docConfig.colunas[stress_column]]

        self.x_original = x
        self.y_original = y
        
        new_x, new_y = self.__generalDataAquisition(x=x,y=y, x_label=docConfig.colunas[strain_column], y_label=docConfig.colunas[stress_column], linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[docConfig.colunas[stress_column]]>new_y[0]]

        return raw_data,cleaned_raw_data,new_x,new_y
    def __filterDataOnlyBelowMaxForce(self, deformation_range_x, force):
        '''
        Method to only consider the strain data below de max force point
        '''
        #  Selecionando porção dos dados na região menor do que a máxima força
        deformation_range_x = pd.Series(deformation_range_x)
        force = pd.Series(force)
        forceMaxIndex = force[force==max(force)].index[0] # Pegando o índice
        force = force[0:forceMaxIndex]
        deformation_range_x = deformation_range_x[0:forceMaxIndex]

        return deformation_range_x, force


    def __selectStandardRange(self,standardName, deformation_range_x):
        '''
        Method to select the range of deformation, based on the standard
        '''
        if standardName == 'standard-ASTM-D3039':

            if max(deformation_range_x) > 0.006:
                inf_limit = 0.001
                sup_limit = 0.003
                return inf_limit,sup_limit
            # Como o ensaio é biaxial, e foi parado antes, não faz sentido a regra da norma, e mantêm-se a regra básica de 0.1% a 0.3%
            elif self.docConfig == '_rho':
                inf_limit = 0.001
                sup_limit = 0.003
                return inf_limit,sup_limit   
            else:
                inf_limit = 0.25
                sup_limit = 0.5
                np.quantile([1,1,2,2],0.25)
                return np.quantile(deformation_range_x.tolist(),inf_limit), np.quantile(deformation_range_x.tolist(),sup_limit)
            

            
        if standardName == 'standard-ASTM-D7264': # flexão
            inf_limit = 0.001
            sup_limit = 0.003
            return inf_limit, sup_limit
        
        if standardName == 'standard-ASTM-D7078': # Cisalhamento
            inf_limit = 1500e-6
            sup_limit = 1500e-6 + 4000e-6
            return inf_limit, sup_limit

        if standardName == 'linearSearch' or standardName == 'standard-ASTM-D638':
            inf_limit = 0
            sup_limit = 0.01
            return np.quantile(deformation_range_x,inf_limit), np.quantile(deformation_range_x,sup_limit)

    def __onlyReadData(self, archive_name, archive_data):
        '''
        Método apenas para ler os dados
        '''

        self.raw_data = pd.read_csv(archive_name, sep=archive_data.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=archive_data.skiprows, decimal=archive_data.decimal)
    
    def __general_machine_data_aquisition(self,  archive_name :  str, linearRegionSearchMethod, 
                                          generalMachineData : GeneralMachine,
                                          x_min = None,
                                          x_max = None):
        '''
        Trata dos dados de forma customizada
        '''
    
        docConfig  = generalMachineData # Instanciando um novo objeto do tipo _Older_Machine 
        raw_data = pd.read_csv(archive_name, sep=docConfig.column_delimitador, 
                               encoding_errors='backslashreplace', 
                               on_bad_lines='skip', skiprows=docConfig.skip_rows, 
                               decimal=docConfig.decimal)
        raw_data.columns = docConfig.colunas
        offset_num = self.__filterInitGraph(y=raw_data[docConfig.y_column],linearRegionSearchMethod=linearRegionSearchMethod)
        x = raw_data[docConfig.x_column]
        y = raw_data[docConfig.y_column]
        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)

        if linearRegionSearchMethod == 'Custom':
            x_linear, y_linear = self.__chooseRegionLinear(x,y,x_min=x_min, x_max=x_max)

        a,b,root = self.__equationFit(x_linear, y_linear)
        if self.verbose:
            self.plotDataFinalComparison(x,y,x_linear,y_linear,docConfig.x_column,docConfig.y_column)
            self.plotComparisonExcludedData(x,y,x_linear,y_linear,docConfig.x_column,docConfig.y_column)

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        if self.verbose:
            self.plotCleanedData(new_x, new_y, docConfig.x_column,docConfig.y_column)

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)

        cleaned_raw_data = raw_data[raw_data[docConfig.y_column]>new_y[0]]

        return raw_data,cleaned_raw_data, new_x, new_y
    
    def __chooseRegionLinear(self, x : pd.Series, y: pd.Series, x_min, x_max):
        '''
        Method to uniquely choose the linear region
        '''
        x_index_min = x[x>=x_min].index[0]
        x_index_max = x[x>x_max].index[0]

        return x[x_index_min:x_index_max], y[x_index_min:x_index_max]    
    
    
    def __equationFit(self, x_linear, y_linear):
        '''
        Retorna os coeficientes a, b, e a raiz (-b/a) de uma equaçãoo linear f(x)=ax+b
        '''
        def linear(x,a,b):
            return a*x+b

        popt,_ = curve_fit(linear, x_linear, y_linear)
        return tuple([popt[0],popt[1],-popt[1]/popt[0]])
    
    def __compositeUltimateStress(self,stress_info):
        '''
        Método para cálcular o stress último, baseado na norma 
        '''
        return 1,1,max(stress_info)
    
    def __cut_garbage_data(self,x,y,x_linear,a,b,root):
        '''
        Método para cortar os dados iniciais do ensaio
        x -> Dados Originais (x)
        y -> Dados Originais (y)
        x_linear -> Conjunto do eixo x, dos dados originais, em que a informação é válida
        a,b -> Coef. das retas ajustadas na região linear
        root -> Raiz da eq. ajustada na parte linear
        '''

        x_cleaned = x[x_linear.index[-1]:x.index[-1]] # Exclui os primeiros dados
        y_cleaned = y[x_linear.index[-1]:x.index[-1]] # Exclui os primeiros dados
        x_init = np.linspace(root,x[x_linear.index[-1]],20) # Array da raiz do gráfico até o início dos dados originais
        y_init = [a*x+b for x in x_init] # Y ajustado na parte linear
        
        new_x = list(x_init) + list(x_cleaned) 
        new_x = np.subtract(new_x,root) # descontando a raiz
        new_y = list(y_init) + list(y_cleaned)
        return new_x, new_y
    
    def __selectGraphRange(self, var, i, scale=1):
        '''
        Método para retornar um range de dados, dado seu tamanho, e posição. 
        '''
        offset = int(len(var)/50)*scale
        return var[offset*(i-1):offset+offset*(i-1)]

    def __findConvergencePoisson(self, x_strain_linear, y_strain_linear, x_load_linear):
        '''
        Método para encontrar a convergênci da razão de Poisson
        '''
        # Corta os dados no mesmo tamanho
        if len(x_strain_linear)>len(y_strain_linear):
            x_strain_linear = x_strain_linear[0:len(y_strain_linear)]
        else:
            y_strain_linear = y_strain_linear[0:len(x_strain_linear)]

        ratio = np.divide(y_strain_linear,x_strain_linear)
        ratio_inverted = ratio[::-1]

        convergedRatio = self.__selectGraphRange(ratio_inverted,1)

        if len(convergedRatio)>0:
            return np.mean(convergedRatio)

        else:
            last_50_p = int(len(ratio)/2)
            return np.mean(ratio[:-last_50_p])
    
    def __filterInitGraph(self, y : pd.Series, linearRegionSearchMethod: str = 'Deterministic', scale=1)->int:
        '''
        Recebe os dados de ensaios experimentais, e encontra a primeira região linear pela diminuição do desvio padrão da segunda derivada
        '''
        if linearRegionSearchMethod == 'Deterministic':
            i=1
            y_current = self.__selectGraphRange(y,i,scale=scale)
            derivative = np.gradient(y_current)
            # second_order_derivative = np.gradient(derivative)
            std_derivative = np.std(derivative)
            mean_derivative = np.mean(derivative)
            init_caos = std_derivative/mean_derivative
            cov = init_caos
            convergence_criteria = init_caos/2

            # Se os dados já estão lineares, não há porque filtrar
            if init_caos<0.1:
                return i #

            while(cov > convergence_criteria):
                i+=1
                y_current = self.__selectGraphRange(y,i)
                derivative = np.gradient(y_current)
                second_order_derivative = np.gradient(derivative)
                cov = np.std(second_order_derivative)
                if i>100:
                    raise Exception('loop inf')

            return i    
        
        if linearRegionSearchMethod =='Custom':
            return 1
        raise Exception('Método de determinação da região Linear Inválido')

    def __findEndLinearRegion(self, y : pd.Series):
        '''
        TODO -> Progrmar uma forma de se obter a região linear, ou seja, até onde realizar o fitting para o módulo
        '''
        pass     

    def __selectYoungModulusRange(self, strain : np.array, stress: np.array, init : float, end :float):
        '''
        Método para selecionar a faixa, baseada na % inicial e final de deformação
        '''

        strain = pd.Series(strain)
        stress = pd.Series(stress)

        init_index = strain[strain>init].index[0]
        end_index = strain[strain<end].index[-1]

        return strain[init_index:end_index], stress[init_index:end_index]
    
    def __selectStrainRange(self, strain_axial : np.array, strain_tranversal: np.array, init : float, end :float):
        '''
        Method to selecet the range of parallel and tranverse strain
        '''    
        strain_axial = pd.Series(strain_axial)
        strain_tranversal = pd.Series(strain_tranversal)

        init_index = strain_axial[strain_axial>init].index[0]
        end_index = strain_axial[strain_axial>end].index[0]

        return strain_axial[init_index:end_index], strain_tranversal[init_index:end_index]


    def __findYeldStress(self, x: pd.Series, y: pd.Series, E, 
                         calculus_method = 'linearSearch', 
                         max_percentil : float = 0.25,
                         offset_yield : float = 0.002
                         ):
        '''
        Metodo para determinar a tensao de escoamento basead em medo
        '''
        if calculus_method == 'standard-ASTM-D3039':
            x_offset, y_offset, ultimateStress = self.__compositeUltimateStress(y)
            self.strengthLimits = {'Tensão Máxima [MPa]' : ultimateStress}
            return x_offset, y_offset,ultimateStress
        if calculus_method == 'linearSearch' or calculus_method == 'standard-ASTM-D638' or calculus_method == 'standard-ASTM-D7078':
            x_offset, y_offset, yieldStress = self.__percentYeldStressMethod(x, y, E, max_percentil,offset_yield)
            _, _, ultimateStress = self.__compositeUltimateStress(y)
            self.strengthLimits = {'Tensão Máxima [MPa]' : ultimateStress,
                                   'Tensão de Escoamento [MPa]' : yieldStress
                                   }
            return x_offset, y_offset,yieldStress
    
    def __findMaxPolymerStress(self,x : pd.Series, y: pd.Series):
        '''
        Encontra o máximo do polímero, e retorna o x max
        '''
        y = pd.Series(y)
        x = pd.Series(x)
        y_derivative = np.gradient(y)
        y_derivative = pd.Series(y_derivative)

        # Divide o gráfico em 50 partes iguais:
        y_derivative_divided = []
        for i in range(50):
            y_derivative_divided.append(self.__selectGraphRange(y_derivative,i))

        for i in range(50):
            grad_mean = np.mean(y_derivative_divided[i])

            if grad_mean<0.04:
                max_y_region = i
                break

    
        index_y_max = y_derivative_divided[max_y_region].index[0]

        return x[int(index_y_max)]


    def __percentYeldStressMethod(self, x: pd.Series, y: pd.Series, E : float, max_percentil : float = 0.25, offset_yield = 0.002):
        '''
        Metodo para encontrar a tensao de escoamento baseado em um offset de 0.2%
        '''
        y = pd.Series(y)
        x = pd.Series(x)
        '''
        Nas linahs abaixo, usa-se a derivada para encontrar a região
        com declividade nula, indicando um máximo. Mas, por algum motivo,
        não está funcionando em alguns casos.

        Logo, por motivos de simplificidade, vamos pegar o máximo encontrado na curva.
        '''

        y_max_index = y[y==max(y)].index[0]
        y_new = y[0:y_max_index]
        y_cutted = np.quantile(y_new,q=0.5)
        index_y_max = max(y_new[y_new<y_cutted].index)
        x_max = x[index_y_max]
        x_linear = np.linspace(0,x_max,1000)
        y_linear = [E*x for x in x_linear]
        x_offset = x_linear + offset_yield
        y_offset = [E*x for x in x_offset]
        y_interpolated = np.interp(x_offset, x,y)

        def FindYield():
            minGlobal = min(abs(y_interpolated- y_linear))
            for each_i in range(len(y_interpolated)):
                if abs(y_interpolated[each_i]-y_linear[each_i])==minGlobal:
                    return y_interpolated[each_i]
                
        yieldPoint = FindYield()
        
        return x_offset, y_linear, yieldPoint

    def __generalDataAquisition(self, x : pd.Series, y : pd.Series, 
                                x_label : str, y_label : str, linearRegionSearchMethod : str):
        '''
        Metodo DRY para executar os comandos referentes a aquisicao de dados
        '''
        offset_num = self.__filterInitGraph(y=y,linearRegionSearchMethod=linearRegionSearchMethod)

        # Filtrando apenas os dados de deslocamento para serem monotonicamente crescentes (No futuro,  pode-se pensar em desabilitar)
        x_series = pd.Series(x)

        x = x_series[np.gradient(x_series)>0]

        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)

        if self.x_min!=None and self.x_max!=None:
            if linearRegionSearchMethod != 'Custom':
                warnings.warn(f'''x_min e x_max foram passados, porém linearRegionSearchMethod é do tipo {linearRegionSearchMethod}.
                              Logo, x_min e x_max não surtirão efeitos. Para tal, use  linearRegionSearchMethod='Custom'.
                              ''')
                # colocando os valores calculados automaticamente
                self.x_max = max(x_linear)
                self.x_min = min(x_linear)
            else:
                x_linear, y_linear = self.__chooseRegionLinear(x=x,y=y, x_min=self.x_min, x_max=self.x_max)
        
        else:
            self.x_max = max(x_linear)
            self.x_min = min(x_linear)
        a,b,root = self.__equationFit(x_linear, y_linear)
        if self.verbose:
            self.plotDataFinalComparison(x,y,x_linear,y_linear,x_label,y_label)
        if offset_num>1 and self.verbose:
            self.plotComparisonExcludedData(x,y,x_linear,y_linear,x_label,y_label)

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        if self.verbose:
            self.plotCleanedData(new_x, new_y, x_label, y_label)

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)

        return new_x, new_y

    def __typeCheck(self, var, type_correct):
        '''
        Função de apoio para checar se o tipo passo estão correto
        '''
        if type(var) != type_correct:
            raise Exception(f'O argumento docConfig deve ser uma {type_correct}. Recebeu um {type(var)}')
        
    def __standard_ASTM_D638(self, axial_strain_linear,transverse_strain_linear,load_linear_axial):
        '''
        Method to compute the poisson ratio following D638
        '''

        coef_axial, _, _ = self.__equationFit(load_linear_axial,axial_strain_linear)
        coef_transversal, _, _ = self.__equationFit(load_linear_axial,transverse_strain_linear)

        ratio = abs(coef_transversal/coef_axial)
        return ratio
    
    def __FlexuralPostProcessing(self, deflection, applied_force, L, width_beam, thickness, procedure = 'A'):
        '''
        Returns the flexural stress and strain
        '''
        if procedure=='A':
            stress = np.multiply(3,applied_force)*L/(2*width_beam*(thickness**2))
            strain = np.multiply(6,deflection)*thickness/(L**2)

            return strain, stress
        else:
            raise Exception('ASTM D7264 procedure B not yet implemented.')
        
    def __Inverse_FlexuralPostProcessing(self, strain, stress, L, width_beam, thickness, procedure = 'A'):
        '''
        Returns the flexural stress and strain
        '''
        if procedure=='A':
            applied_force = (2*width_beam*(thickness**2))/(3*applied_force*L)
            deflection = (L**2)/(6*thickness)
            return deflection, applied_force
        else:
            raise Exception('ASTM D7264 procedure B not yet implemented.')
        
    def __Inverse_FlexuralDeflection(self, strain, L, thickness, procedure = 'A'):
        '''
        Returns the flexural stress and strain
        '''
        if procedure=='A':
            deflection = (L**2)/(6*thickness)*strain
            return deflection
        else:
            raise Exception('ASTM D7264 procedure B not yet implemented.')
    
    def __standard_ASTM_D3039(self, axial_strain_linear, transverse_strain_linear)->float:
        '''
        Method to compute the poisson ration following the chord method by ASTM D3039
        '''

        deltaAxial = max(axial_strain_linear) - min(axial_strain_linear)
        deltaTransversal = max(transverse_strain_linear) - min(transverse_strain_linear)
        poissonRatio = -deltaTransversal/deltaAxial
        # Plotando o gráfico para comparação
        # post processing
        # if self.verbose:
        #     fig, ax = plt.subplots(figsize=(8,4))

        #     if self.direction == 'paralell':
        #         label =  r'$\nu_{12}$='+f'{poissonRatio:.4f}'
        #     else:
        #         label =  r'$\nu_{21}$='+f'{poissonRatio:.4f}'

        #     ax = scatter_helper(ax=ax, x = axial_strain_computation, y=transversal_strain_computation, 
        #                     label=label, 
        #                     ylabel=r'$\varepsilon_{t}$', 
        #                     xlabel=r'$\varepsilon_{l}$', 
        #                     color=blue_tonalities_options[10], linestyle=linestyles_options[10])
            
        #     ax.plot(new_axial_strain_data, new_transversa_strain_data)
            
        #     axial_strain_as_list = list(axial_strain_computation)

        #     lim_sup_x = axial_strain_as_list[-1]
        #     lim_inf_x = axial_strain_as_list[0]

        #     limit_y = max(transversal_strain_computation)
        #     text_x_position = (lim_inf_x+lim_sup_x)/2.5
        #     text_y_position =limit_y
        #     ax.text(text_x_position, text_y_position, r'$\frac{\Delta \varepsilon_t}{\Delta \varepsilon_l}=$'+fr'{deltaTransversal:.2e}/{deltaAxial:.2e}', fontsize=15, bbox={'facecolor': 'orange', 'alpha': 0.8, 'pad': 2})

        return poissonRatio

    def dataExtract(self, docConfig : str, archive_name : str, linearRegionSearchMethod : str,
                     generalMachineData : GeneralMachine = None,
                     x_min = None,
                     x_max = None
                     )->pd.DataFrame:
        '''
        Funçãoo para obter, a parte de um tipo de máquina, identificado pelo nome, os dados brutos do ensaio.
        '''
        # Verificação dos argumentos
        self.__typeCheck(docConfig, str)
        self.__typeCheck(archive_name, str)

        if docConfig == '_alpha':
            return self._alpha_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_beta':
            return self._beta_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_gamma':
            return self._gamma_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_delta':
            return self._delta_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_epsilon':
            return self._epsilon_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_zeta':
            return self._zeta_data_aquisition(archive_name, linearRegionSearchMethod)

        if docConfig == '_eta':
            return self._eta_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_omicron':
            return self._omicron_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_pi':
            return self._pi_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == '_rho':
            return self._rho_data_aquisition(archive_name, linearRegionSearchMethod)
        
        if docConfig == 'generalMachine':
            return self.__general_machine_data_aquisition(archive_name, linearRegionSearchMethod, generalMachineData, x_min, x_max)
        
        raise Exception('Tipo de Máquina não encontrado')
    
    def MeasureFlexuralModulus(self,length : float = None,
                            thickness : float = None,
                            width : float = None, 
                            max_percentil : float = 0.25,
                            calculus_method : str = 'linearSearch',
                            overwrite_standard_range : bool = False
                            ):
        
        deflection, applied_force = self.__filterDataOnlyBelowMaxForce(self.new_x, self.new_y)

        self.deflection = self.new_x
        self.applied_force = self.new_y

        # transformando dados para deformação e tensão
        self.strain, self.stress = self.__FlexuralPostProcessing(deflection=self.new_x, applied_force=self.new_y, L=length, width_beam=width, thickness=thickness) 
        a, b = self.__selectStandardRange(calculus_method,self.strain) # selecionando o range de deformação, seguindo a norma passada
        a_original = self.__Inverse_FlexuralDeflection(a, L=length, thickness=thickness)
        b_original = self.__Inverse_FlexuralDeflection(b, L=length, thickness=thickness)
        # salvando a região de cálculo para uso futuro
        self.E_lim_inf = a
        self.E_lim_sup = b
        self.E_lim_inf_original = a_original
        self.E_lim_sup_original = b_original

        linear_region_strain, linear_region_stress = self.__selectYoungModulusRange(self.strain, self.stress, a,b)
        linear_region_deflection, linear_region_force = self.__selectYoungModulusRange(deflection, applied_force, a_original,b_original)
        
        E_chord,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
        m,b,root=self.__equationFit(x_linear=linear_region_deflection, y_linear=linear_region_force)
        E_secant = (length**3)*m/(4*width*(thickness**3))
        self.strengthLimits = {'Tensão Máxima [MPa]':max(self.stress)}
        self.E = {
                  'Módulo de Flexão (Corda) [MPa]' : E_chord,
                  'Módulo de Flexão (Secante) [MPa]' : E_secant
                  }
    
    def MeasureCompressionStrenth(self, calculus_method):
        '''
        No caso de compressão, temos uma tratativa totalmente diferente. O objetivo é apenas limpar os 
        dados iniciais, e obter a tensão máxima.
        '''
        self.strengthLimits = {'Tensão Máxima [MPa]' : max(self.new_y),
                            }
        self.strain = self.new_x
        self.stress = self.new_y


    def MeasureYoungModulus(self,length : float = None,
                            thickess : float = None,
                            width : float = None, 
                            max_percentil : float = 0.25,
                            calculus_method : str = 'linearSearch',
                            offset = 0.002,
                            overwrite_standard_range : bool = False
                            ):
        '''
        Método para medir o módulo de Young
        '''
        axial_strain, force_data = self.__filterDataOnlyBelowMaxForce(self.new_x, self.new_y)

        a, b = self.__selectStandardRange(calculus_method,axial_strain) # selecionando o range de deformação, seguindo a norma passada
        
        # salvando a região de cálculo para uso futuro
        self.E_lim_inf = a
        self.E_lim_sup = b
        linear_region_strain, linear_region_stress = self.__selectYoungModulusRange(axial_strain, force_data, a,b)
        
        # Caso seja desejado, a região de cálculo do módulo de elasticidade pode ser alterada, saindo da convenção da norma.
        if overwrite_standard_range:
            self.E_lim_inf = 0
            self.E_lim_sup = self.x_max - self.x_min
            linear_region_strain, linear_region_stress = self.__selectYoungModulusRange(axial_strain, force_data, self.x_min,self.x_max)    
        E,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
        self.E = {'Módulo de Young [MPa]': E}
        self.__findYeldStress(self.new_x, self.new_y, calculus_method=calculus_method, offset_yield=offset, E=E)
        self.strain = self.new_x
        self.stress = self.new_y
        # # plotando os dados em 5 em 5
        # slice = int(len(self.new_x)/100)
        # x=self.new_x[::slice]
        # y=self.new_y[::slice]
        # self.plotStressStrain(x,y,E, max_percentil)

    def MeasurePoissonRatio(self, calculus_method = 'linearSearch'):
        '''
        Método para medir a razão de poisson
        '''
        if self.docConfig == '_alpha':
            machineConfig = _alpha()

            scale_find_linear = 4
            scale_calculus = 10
            self.poisson_computation_procedure(scale_calculus=scale_calculus 
                                            ,scale_find_linear=scale_find_linear
                                            ,strain_parallel_column=5
                                            ,strain_transverse_column=6
                                            ,load_column=2
                                            ,machineConfig=machineConfig
                                            ,calculus_method=calculus_method
                                            )
            return 
        if self.docConfig == '_beta':
            machineConfig = _beta()

            scale_find_linear = 4
            scale_calculus = 10
            self.poisson_computation_procedure(scale_calculus=scale_calculus 
                                               ,scale_find_linear=scale_find_linear
                                               ,strain_parallel_column=5
                                               ,strain_transverse_column=6
                                               ,load_column=2
                                               ,machineConfig=machineConfig
                                               ,calculus_method=calculus_method
                                               )
            return 
        
        if self.docConfig == '_rho':
            machineConfig = _rho()

            scale_find_linear = 4
            scale_calculus = 10
            self.poisson_computation_procedure(scale_calculus=scale_calculus 
                                               ,scale_find_linear=scale_find_linear
                                               ,strain_parallel_column=4
                                               ,strain_transverse_column=5
                                               ,load_column=2
                                               ,machineConfig=machineConfig
                                               ,calculus_method=calculus_method
                                               )
            return 

        warnings.warn(f"A máquina {self.docConfig} não possui dados de deformação transversa")

    def MeasureShearModulus(self, calculus_method = 'linearSearch', overwrite_standard_range : bool =  False):
        '''
        Calcula do módulo de cisalhamento baseado em alguma metologia
        '''
        axial_strain, axial_stress = self.__filterDataOnlyBelowMaxForce(self.new_x, self.new_y)

        a, b = self.__selectStandardRange(calculus_method,axial_strain) # selecionando o range de deformação, seguindo a norma passada
        
        # salvando a região de cálculo para uso futuro
        self.G_lim_inf = a
        self.G_lim_sup = b
        linear_region_strain, linear_region_stress = self.__selectYoungModulusRange(axial_strain, axial_stress, a,b)
        
        # Caso seja desejado, a região de cálculo do módulo de elasticidade pode ser alterada, saindo da convenção da norma.
        if overwrite_standard_range:
            self.G_lim_inf = 0
            self.G_lim_sup = self.x_max - self.x_min
            linear_region_strain, linear_region_stress = self.__selectYoungModulusRange(axial_strain, axial_stress, self.x_min,self.x_max)    
        G,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
        self.G = {'Módulo de Cisalhamento [MPa]': G}
        self.__findYeldStress(axial_strain,axial_stress,G,offset_yield=0.002, calculus_method=calculus_method)
        self.strain = self.new_x
        self.stress = self.new_y

    def selectPoissonRatioRange(self, calculus_method):
        pass
    
    def poisson_computation_procedure(self, scale_find_linear:int , scale_calculus : int,strain_parallel_column : int, strain_transverse_column :int, load_column : int, machineConfig,calculus_method : str):
        '''
        Medida do poisson generalziada para cada método
        '''
        axial_strain, load = self.__filterDataOnlyBelowMaxForce(self.new_x, self.new_y)
        a, b = self.__selectStandardRange(calculus_method,axial_strain)

        # Encontrar a região linear da deformação axial pela carga
        axial_strain =  np.abs(self.cleaned_raw_data[machineConfig.colunas[strain_parallel_column]])
        axial_strain_linear, load_linear = self.__selectYoungModulusRange(axial_strain, load, a,b)

        # Encontrar a região linear da deformação transversal pela carga (assumida a ser a mesma da axial)
        transverse_strain =  np.abs(self.cleaned_raw_data[machineConfig.colunas[strain_transverse_column]])
        transverse_strain_linear = transverse_strain[axial_strain_linear.index]
    
        if self.x_min and self.x_max and calculus_method=='linearSearch': # Caso não tenha sido passado nenhuma norma, utilizar limites dados pelo usuário
            axial_strain_linear, load_linear_axial = self.__chooseRegionLinear(x=axial_strain,y=load, x_min=self.x_min, x_max=self.x_max)
            transverse_strain_linear = transverse_strain[axial_strain_linear.index]

        if calculus_method == 'standard-ASTM-D3039':
            self.poisson_ratio = self.__standard_ASTM_D3039(axial_strain_linear, transverse_strain_linear)
        if calculus_method == 'standard-ASTM-D638':
            self.poisson_ratio = self.__standard_ASTM_D638(axial_strain_linear,transverse_strain_linear,load_linear)
        else:
            self.poisson_ratio = self.__findConvergencePoisson(axial_strain_linear,transverse_strain_linear,load_linear)

        # Tarefas de pós processamento

        # def selectData(data):

        #     slice = int(len(data)/80)
        #     return data[::1]
        
        # axial_strain = selectData(axial_strain)
        # transverse_strain = selectData(transverse_strain)
        # axial_strain_linear = selectData(axial_strain_linear)
        # load = selectData(load)
        # load_linear_axial = selectData(load_linear_axial)
        # transverse_strain_linear = selectData(transverse_strain_linear)
        # load_linear_tranversal = selectData(load_linear_tranversal)
        
        # if calculus_method == 'linearSearch' and self.verbose:
        #     ax_total, ax_linear = self.plotComparisonPoissonRatioLinear(axial_strain_total=axial_strain,
        #                                         transversal_strain_total=transverse_strain
        #                                         ,axial_train_linear=axial_strain_linear
        #                                         ,load_total=load
        #                                         ,load_axial_linear = load_linear_axial
        #                                         ,transversal_strain_linear=transverse_strain_linear
        #                                         ,load_transversal_linear=load_linear_tranversal
        #                                         )
            
        
        #     plt.show()

        # if calculus_method == 'standard-ASTM-D638' and self.verbose:

        #     self.plotASTMD638_poission(axial_strain_total=axial_strain,
        #                                         transversal_strain_total=transverse_strain
        #                                         ,axial_train_linear=axial_strain_linear
        #                                         ,load_total=load
        #                                         ,load_axial_linear = load_linear_axial
        #                                         ,transversal_strain_linear=transverse_strain_linear
        #                                         ,load_transversal_linear=load_linear_tranversal
        #                                         )
            
        
        #     plt.show()

    def plotComparisonExcludedData(self, x,y, x_linear,y_linear, x_label, y_label):
        '''
        Método comparar dados excluídos da análise
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x[0:len(x_linear)], y=y[0:len(y_linear)], label='Dados Originais', ylabel=y_label, xlabel=x_label)
        ax = plot_helper(ax=ax, x = x_linear, y=y_linear, label='Curva linear', ylabel=y_label, xlabel=x_label, color='red')
        lim_sup_x = x[len(x_linear)] 
        lim_inf_x = x[0] 
        y_max= y[len(y_linear)]
        y_min= y[0]
        
        ax.arrow(x=lim_sup_x,y=y_min,dx=0,dy=(y_max-y_min)*1.2, color='orange')
        ax.arrow(x=lim_inf_x,y=y_min,dx=0,dy=(y_max-y_min)*1.2, color='orange')
        text_x_position = (lim_inf_x)*1.01
        text_y_position = y_max*1.3
        ax.text(text_x_position, text_y_position, r'Região excluída', fontsize=7, bbox={'facecolor': 'orange', 'alpha': 0.1, 'pad': 2})
        ax.legend(loc ='lower right')
        plt.show()

    def plotCleanedData(self, x,y, x_label, y_label):
        '''
        Método para plotar os dados limpos
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x, y=y, label='Dados Ajustados', ylabel=y_label, xlabel=x_label)    
        plt.show()

    def plotComparisonPoissonRatioLinear(self,axial_strain_total
                                             ,transversal_strain_total
                                             ,load_total
                                             ,axial_train_linear, load_axial_linear
                                             ,transversal_strain_linear, load_transversal_linear
                                         ):
        '''
        Método para plotar a comparação entre as regiões lineares na parte das deformações axial (para gerar um gráfico parecido com a norma)
        '''
        fig_total, ax = plt.subplots(figsize=(8,4), constrained_layout=True)
        # partes totais

        y_label =  r"Deformação absoluta $||\varepsilon||$"
        ax = plot_helper(ax=ax, x = load_total, y=axial_strain_total, label='Dados da deformação axial totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[0], linestyle=linestyles_options[0])
        ax = plot_helper(ax=ax, x = load_total, y=transversal_strain_total, label='Dados da deformação transversal totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[5], linestyle=linestyles_options[5])
        ax = plot_helper(ax=ax, x = load_axial_linear, y=axial_train_linear, label='Parte linear da deformação axial', ylabel=y_label, xlabel='Carregamento [kN]', color='orange', linestyle=linestyles_options[10])
        ax = plot_helper(ax=ax, x = load_transversal_linear, y=transversal_strain_linear, label='Parte linear da deformação transversal', ylabel=y_label, xlabel='Carregamento [kN]', color='red', linestyle=linestyles_options[12])
        
        fig_total.savefig('total_poisson.pdf')
        fig_total.savefig('total_poisson.svg')
        fig_total.savefig('total_poisson.png')

        fig, ax3 = plt.subplots(figsize=(8,4), constrained_layout=True)
        ratio = np.divide(transversal_strain_total, axial_strain_total)

        if self.direction == '11':
            label = r'Convergência do razão de Poisson, $\nu_{12}$'+f'={self.poisson_ratio:.3f}'
        else:
            label = r'Convergência do razão de Poisson, $\nu_{21}$'+f'={self.poisson_ratio:.3f}'

        ax3 = plot_helper(ax=ax3, x = load_total, y=ratio, 
                          label=label, 
                          ylabel=r'$||\frac{\varepsilon_{y}}{\varepsilon_{x}}||$', 
                          xlabel='Carregamento [kN]', 
                          color=blue_tonalities_options[10], linestyle=linestyles_options[10])
        
        load_linear_as_list = list(load_axial_linear)

        lim_sup_x = load_linear_as_list[-1]
        lim_inf_x = load_linear_as_list[0]

        ax3.arrow(x=lim_sup_x,y=0,dx=0,dy=max(ratio)/2, color='orange', head_width=0.05)
        ax3.arrow(x=lim_inf_x,y=0,dx=0,dy=max(ratio)/2, color='orange', head_width=0.05)
        text_x_position = (lim_inf_x)*1.2
        text_y_position = max(ratio)/2
        ax3.text(text_x_position, text_y_position, r'Região de Cálculo', fontsize=7, bbox={'facecolor': 'orange', 'alpha': 0.1, 'pad': 2})
        

        plt.show()
    

        return ax, ax3


    def plotASTMD638_poission(self,axial_strain_total
                                             ,transversal_strain_total
                                             ,load_total
                                             ,axial_train_linear, load_axial_linear
                                             ,transversal_strain_linear, load_transversal_linear
                                ):
        
        fig_total, ax = plt.subplots(figsize=(8,4), constrained_layout=True)
        # partes totais

        y_label =  r"Deformação absoluta $||\varepsilon||$"
        ax = plot_helper(ax=ax, x = load_total, y=axial_strain_total, label='Dados da deformação axial totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[0], linestyle=linestyles_options[0])
        ax = plot_helper(ax=ax, x = load_total, y=transversal_strain_total, label='Dados da deformação transversal totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[5], linestyle=linestyles_options[5])
        ax = plot_helper(ax=ax, x = load_axial_linear, y=axial_train_linear, label='Parte linear da deformação axial', ylabel=y_label, xlabel='Carregamento [kN]', color='orange', linestyle=linestyles_options[10])
        ax = plot_helper(ax=ax, x = load_transversal_linear, y=transversal_strain_linear, label='Parte linear da deformação transversal', ylabel=y_label, xlabel='Carregamento [kN]', color='red', linestyle=linestyles_options[12])
        text_x_position = max(load_total)/10

        if max(axial_strain_total)>max(transversal_strain_total):
            y = max(axial_strain_total)
        else:
            y = max(transversal_strain_total)

        text_y_position = y*0.1
        ax.text(text_x_position, text_y_position,r"$\nu_{12}$"+f" = {self.poisson_ratio:.4f}", bbox={'facecolor': 'orange', 'alpha': 0.8, 'pad': 2})

        fig_total.savefig('total_poisson.pdf')
        fig_total.savefig('total_poisson.svg')
        fig_total.savefig('total_poisson.png')

        plt.show()
    

        return 
    
    def plotDataFinalComparison(self,x,y, x_linear,y_linear, x_label,y_label):
        '''
        Método para graficar os dados originais e a parte linear
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x, y=y, label='Dados Originais', ylabel=y_label, xlabel=x_label)
        ax = plot_helper(ax=ax, x = x_linear, y=y_linear, label='Curva linear', ylabel=y_label, xlabel=x_label, color='red')
        plt.show()

    def plotStressStrain(self,x,y,E, max_percentil : float = 0.25,
                         offset = 0.002,
                         calculus_method = 'linearSearch'
                         ):
        '''
        Método para graficar a curva de tensão e deformação

        TODO - generalizar para a função receber um eixo, assim ela pode receber diversos corpos de prova
        '''
        y = pd.Series(y)
        x = pd.Series(x)
        index_y_max = y[y==max(y)].index[0]
        x_max = x[index_y_max]
        x_linear = np.linspace(0,x_max)
        y_linear = [E*x for x in x_linear]

        if self.direction == '11':
            modulus_text = r"$E_1$"
            ylabel = r'$\sigma_{1} \ [MPa]$'
        else:
            modulus_text = r"$E_2$"
            ylabel = r'$\sigma_{2} \ [MPa]$'
        if self.verbose:
            fig, ax = plt.subplots(figsize=(6,3), constrained_layout=True)
            ax = plot_helper(ax=ax, x = x, y=y, 
                             label='Curva de tensão', 
                             ylabel=ylabel, 
                             xlabel=r'$\varepsilon \ \frac{mm}{mm}$',
                             linestyle='-.',
                             )
            ax = plot_helper(ax=ax, x = x_linear.astype(float),
                              y=y_linear, 
                             label='Módulo ajustado', 
                             ylabel=ylabel,
                              xlabel=r'$\varepsilon \ \frac{mm}{mm}$', 
                              color='orange',
                              linestyle='-',
                              marker=None,
                              )
            ax.text(x_linear[-1]*0.8,y_linear[-1]*0.3,modulus_text+fr'={E:.2f} [MPa]',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 3})
        x_offset, y_offset , yieldStress= self.__findYeldStress(x,y,E,max_percentil=max_percentil, offset_yield=offset, calculus_method=calculus_method)
        if self.verbose and (calculus_method == 'linearSearch' or calculus_method == 'standard-ASTM-D638'):
            ax = plot_helper(ax=ax, x = x_offset, y=y_offset, label=fr'Offset ($\sigma_y={yieldStress:.2f} [MPa]$)', ylabel=r'$\sigma_{x} \ [MPa]$', xlabel=r'$\varepsilon \ \frac{mm}{mm}$', color=blue_tonalities_options[8], linewidth=0.1, linestyle='-.')
            pass
        self.strain = x
        self.stress = y

class SeveralMechanicalTestingFittingLinear():

    def __init__(self, docConfig: str, archive_name: str,
                 linearRegionSearchMethod='Deterministic',
                 direction : str = '11',
                 calculus_method : str = 'linearSearch',
                 verbose : bool = False,
                 testType: str = 'tensile',
                 offset :float = 0.002,
                 generalMachineData : GeneralMachine = None,
                 x_min : float = None,
                 x_max : float = None,
                **kwargs
                 ) -> None:
        '''
        Classe destinada à análise de dados experimentais de diversos CPs. 

        ## Parâmetros

        + *docConfig*: Parâmetros destinado ao nome da máquina. Para retornar todos os nomes, e as colunas subentendidas,
        basta executar a função `print_docConfig`:

        ```python
        from experimentalTreatingIsiPol.machines import print_docConfig
        print_docConfig() 
        ```
        + *archive_name*` (str) : Caminho completo de um dos arquivos do ensaio.

        + *linearRegionSearchMethod* (str) :  Metodologia para identificação da região linear do ensaio. Até o momento, estão implementadas
        duas metodologias:
        | linearRegionSearchMethod  |       Semântica       |
        |:-------------------------:|:---------------------:|
        |       Deterministic       |  Programa a região linear baseada em uma regra de mudança de derivada;      |
        |       Custom              |  O usuário decide a região em que o material se comporta de maneira hookeana.  |

        Esse argumento tem por objetivo primordial limpar qualquer erro de ensaio devido à acomodação da garra. Portanto, não deve influenciar no cálculo
        do módulo, ou na região utilizada para cálculo de módulo. No entando, se não for passada nenhuma norma para ser seguida, o software irá assumir os
        primeiros pontos limpos como o módulo do material.

        + *direction* (str) : Direção de ensaio. Isso influencia a forma de apresentação final dos dados. Para aperecer, por exemplo, $\nu_{12}$ ou $\nu_{21}$, por exemplo:

        | direction                 |       Semântica       |
        |:-------------------------:|:---------------------:|
        |       11                  |  Direção alinhada às fibras     |
        |       22                  |  Direção transversal às fibras  |

        + *calculus_method* (str) : Método de cálculo das propriedades mecânicas, ou seja, a norma utilizada. Caso não seja passada nenhuma norma, obrigatoriamente deverá ser 
        utilizado o argumento **dimension_flexural**, descrito logo abaixo. Normas utilizadas:

        | calculus_method            |       Semântica       |
        |:-------------------------: |:---------------------:|
        |       standard-ASTM-D638   |  --     |
        |       standard-ASTM-D3039  |  ---     |
        |       standard-ASTM-D7264  |  ---     |
        |       standard-ASTM-D7078 |  ---     |


        + *offset* (str) : Offset utilizado para calcular a perda de linearidade.
        + *generalMachineData* (generalMachineData) : Argumento customizar a leitura de algum arquivo com output não implementado (colunas por ventura distintas)
        + *x_min* & *x_max* : Valor de input customizado para consideração da região inicial linear da curva. Serve para uma limpezada "customizada" dos dados (chamada Toe compensation)
        Para surgir efeito, o linearRegionSearchMethod deve ser do tipo 'Custom'.


        kwargs:

        dimension_flexural : dict {'path': str, 'sheet_name': str} : dicionário com o caminho e planilha para a obtenção da dimensão dos CPs.  Caso não tenha sido passada alguma planilha, será
        utilizada a primeira. Em cada panilha, os dados devem estar nomeados de acordo com o nome do arquivo .csv de cada CP. Ainda mais, deve-se ter necessária mente 3 colunas 
        : name, thickness e width. Assim, o software vai poder obter corretamente cada propriedade mecânica. Por exemplo, o arquivo excel deve ser desse tipo:
        
        No Arquivo Excel:

            name	thickness	width
            PLACA_07_F_CP1	1,753	13,064
            PLACA_07_F_CP2	1,721	13,074
            PLACA_07_F_CP3	1,713	13,053
            PLACA_07_F_CP4	1,684	13,101
            PLACA_07_F_CP5	1,754	13,067
            PLACA_07_F_CP6	1,765	13,086

        '''

        self.E_lim_inf = [] # array para armazenar os limites no cálculo do módulo
        self.E_lim_sup = [] # array para armazenar os limites no cálculo do módulo
        self.G_lim_inf = [] # array para armazenar os limites no cálculo do módulo
        self.G_lim_sup = [] # array para armazenar os limites no cálculo do módulo
        self.E_lim_inf_original = []
        self.E_lim_sup_original = []
        self.E_lim_chord = [] # array para armazenar os limites no cálculo do módulo
        self.E_lim_secant = [] # array para armazenar os limites no cálculo do módulo
        self.dimension_flexural = kwargs.get('dimension_flexural')
        self.x_min_array = []
        self.x_max_array = []

        self.__verifications(docConfig, archive_name, 
                                 linearRegionSearchMethod, 
                                 direction,
                                 calculus_method,
                                 verbose=verbose,
                                 testType = testType,
                                 offset = offset,
                                 generalMachineData = generalMachineData,
                                 x_min = x_min,
                                 x_max = x_max,
                                 )
        
        self.__findOtherArchives(docConfig, archive_name, 
                                 linearRegionSearchMethod, 
                                 direction,
                                 calculus_method,
                                 verbose=verbose,
                                 testType = testType,
                                 offset = offset,
                                 generalMachineData = generalMachineData,
                                 x_min = x_min,
                                 x_max = x_max,
                                 )
        

        
    def __verifications(self, docConfig: str, archive_name :  str, 
                            linearRegionSearchMethod='Deterministic', 
                            direction :  str = '11',
                            calculus_method : str = 'linearSearch',
                            testType: str = 'tensile',
                            verbose : bool = False,
                            offset : bool  = 0.002,
                            generalMachineData : GeneralMachine = None,
                            x_min : float = 0,
                            x_max : float = 0.005
                            ):
        
        if testType == 'flexural' and docConfig not in ['_beta','_zeta']:
            raise Exception('Para o teste  de flexão, utilizar o docConfig = "_beta" ou docConfig = "_zeta"')
        
        if testType == 'shear' and docConfig not in ['_eta','_omicron']:
            raise Exception('Para o teste  de cisalhamento, utilizar o docConfig = _eta ou docConfig = _omicron')
        
        if testType == 'compression' and docConfig !='_pi': # confirmar depois
            raise Exception('Para o teste  de compressão, utilizar o docConfig = _beta')
    
    def __mergeDicts(self, dicts : list):
        
        dict_new = {}
        for each_dict in dicts:
            for k,v in each_dict.items():
                if k not in dict_new.keys():
                    dict_new[k] = []
                    dict_new[k].append(v)
                else:
                    dict_new[k].append(v)
        
        return dict_new
    
    def __simpliflyDict(self, dict :dict):

        new_dict = {}

        for k in dict.keys():
            new_dict[k] = dict[k][0]

        return new_dict
    def __findOtherArchives(self, docConfig: str, archive_name :  str, 
                            linearRegionSearchMethod='Deterministic', 
                            direction :  str = '11',
                            calculus_method : str = 'linearSearch',
                            testType: str = 'tensile',
                            verbose : bool = False,
                            offset : bool  = 0.002,
                            generalMachineData : GeneralMachine = None,
                            x_min : float = 0,
                            x_max : float = 0.005
                            ):
        '''
        Method to find others files based on the archive name
        '''
        # get parent dir
        parent_dir = os.path.dirname(archive_name)
        # get all files
        files = os.listdir(parent_dir)
        youngModulusArray = []
        StrengthStressArray = []
        PoissonArray = []
        forceDeflectionArray = []
        rawDataArray = []
        cpName = []
        stress_array = []
        strain_array = []

        for each_file in os.listdir(parent_dir):
            if re.search(pattern=r"\d*.csv", string=each_file):
                full_path_name = os.path.join(parent_dir, each_file)
                c = MechanicalTestFittingLinear(docConfig=docConfig, archive_name=full_path_name, 
                                                linearRegionSearchMethod=linearRegionSearchMethod, verbose=verbose,
                                                direction=direction,
                                                generalMachineData=generalMachineData,
                                                x_max=x_max,
                                                x_min=x_min
                                                )
                
                if testType == 'tensile' and (docConfig == '_alpha' or docConfig == '_beta' or docConfig == '_rho'):
                    c.MeasureYoungModulus(max_percentil=0.75, calculus_method=calculus_method, offset=offset)
                    c.MeasurePoissonRatio(calculus_method=calculus_method)
                    self.E_lim_inf.append(c.E_lim_inf)
                    self.E_lim_sup.append(c.E_lim_sup)
                    youngModulusArray.append(c.E)
                    PoissonArray.append(c.poisson_ratio)
                    rawDataArray.append({
                                            'stress_raw': c.y_original,
                                            'strain_raw' : c.x_original
                    })
                    self.x_max_array.append(c.x_max)
                    self.x_min_array.append(c.x_min)
                else:
                    PoissonArray.append(0)

                if testType == 'compression':
                    c.MeasureCompressionStrenth(calculus_method=calculus_method)
                    rawDataArray.append({
                                            'stress_raw': c.y_original,
                                            'strain_raw' : c.x_original
                    })
                
                if testType == 'flexural':
                    # check if arq with thickness and width was passed:
                    if not self.dimension_flexural:
                        raise Exception(r'''Para o teste de flexão, é necessário passar o argumento dimension_flexural, 
                                        que é o caminho de um arquivo com as dimensões dos CPs de flexão''')
                    length, width, thickness = self.__getFlexuralDimensions(cp_name=each_file.split(sep='.csv')[0])
                    if calculus_method != 'standard-ASTM-D7264':
                        warnings.warn(f'Foi passada a norma {calculus_method}, porém para o ensaio de flexão, apenas faz sentido analisar os dados com a norma standard-ASTM-D7264.')

                    c.MeasureFlexuralModulus(length=length, width=width, thickness=thickness, 
                                             calculus_method='standard-ASTM-D7264')
                    youngModulusArray.append(c.E)
                    self.E_lim_inf.append(c.E_lim_inf)
                    self.E_lim_sup.append(c.E_lim_sup)
                    self.E_lim_inf_original.append(c.E_lim_inf_original)
                    self.E_lim_sup_original.append(c.E_lim_sup_original)
                    self.x_max_array.append(c.x_max)
                    self.x_min_array.append(c.x_min)
                    forceDeflectionArray.append({
                                                'force': c.applied_force,
                                                'deflection' : c.deflection
                                                })
                    rawDataArray.append({
                                            'force_raw': c.y_original,
                                            'deflection_raw' : c.x_original
                                            })
                    
                if testType == 'shear':
                    if calculus_method != 'standard-ASTM-D7078':
                        warnings.warn(f'Foi passada a norma {calculus_method}, porém para o ensaio de flexão, apenas faz sentido analisar os dados com a norma standard-ASTM-D7078.')
                    c.MeasureShearModulus(calculus_method=calculus_method)
                    self.G_lim_inf.append(c.G_lim_inf)
                    self.G_lim_sup.append(c.G_lim_sup)
                    youngModulusArray.append(c.G)
                    rawDataArray.append({
                                            'stress_raw': c.y_original,
                                            'strain_raw' : c.x_original
                                            })
                    self.x_max_array.append(c.x_max)
                    self.x_min_array.append(c.x_min)
                
                StrengthStressArray.append(c.strengthLimits) # Vai adicionar um array de dicionário de limites
                
                cpName.append(each_file.split(sep='.csv')[0])
                stress_array.append(c.stress)
                strain_array.append(c.strain)

        
        # Dicionario com os dados para o boxPlot
        dictMechanicalPrimary = {'Corpo de Prova': cpName
                          ,'Poisson': PoissonArray
                          ,'strain': strain_array
                          ,'stress': stress_array
                          }
        
        dictStressLimits = self.__mergeDicts(StrengthStressArray)
        if testType !='compression':
            dictModulus = self.__mergeDicts(youngModulusArray)
        dictRawData = self.__mergeDicts(rawDataArray)

        if testType == 'compression':
            dictMechanical = self.__mergeDicts([dictStressLimits,dictMechanicalPrimary,dictRawData])
        elif testType == 'flexural':
            dictForceFlection = self.__mergeDicts(forceDeflectionArray)
            dictMechanical = self.__mergeDicts([dictStressLimits,dictMechanicalPrimary,dictModulus, dictForceFlection,dictRawData])
        elif testType == 'shear':
            dictMechanical = self.__mergeDicts([dictStressLimits,dictMechanicalPrimary,dictModulus,dictRawData])
        else:
            dictMechanical = self.__mergeDicts([dictStressLimits,dictMechanicalPrimary,dictModulus,dictRawData])

        dictMechanical = self.__simpliflyDict(dictMechanical)



        dict_plots = {}
        for each_k in dictMechanical.keys():
            if (each_k != 'stress' and each_k !='strain' and 
                each_k != 'Corpo de Prova' 
                and each_k!='force' and each_k !='deflection'
                and each_k!='force_raw' and each_k !='deflection_raw'
                and each_k!='stress_raw' and each_k !='strain_raw'
                ):

                if not (testType != 'tensile' and each_k =='Poisson'):

                    fig, ax = plt.subplots(figsize=(8,2))
                    sns.boxplot(data=dictMechanical, x=each_k, ax=ax)
                    
                    if each_k == 'Poisson' and direction =='11':
                        ax.set_xlabel(r'$\nu_{12}$')
                    if each_k == 'Poisson' and direction =='22':
                        ax.set_xlabel(r'$\nu_{21}$')


                    dict_plots[f'{each_k}'] = {
                        'fig': fig
                    }

        self.dictMechanical =  dictMechanical
        self.__plotStressStrain(direction, testType=testType)

        self.__createExcelReport()
        # array_figures = [fig_YoungModuls, fig_YieldStress, fig_stress_mat]

        # self.__createrPDFReport(array_figures)

    def __getFlexuralDimensions(self, cp_name)->tuple:
        '''
        Método para obter as dimensões dos CP's para o teste de flexão.

        Acessa a planilha de excel com os dados dos CPs, que estão linkados pelo nome de arquivo de saída. 
        '''

        arq_path = self.dimension_flexural['path']
        if self.dimension_flexural.get('sheet_name'):
            sheet_name = self.dimension_flexural['sheet_name']
        else:
            sheet_name = None

        data =  pd.read_excel(arq_path, sheet_name=sheet_name)

        length = 50 # Span padrão
        width  = data[data['name']==cp_name]['width'].values[0]
        thickness = data[data['name']==cp_name]['thickness'].values[0]

        return length, width, thickness
    def __createExcelReport(self):
        '''
        Método para salvar os resultados em um Excel
        '''

        df = pd.DataFrame(self.dictMechanical)
        dfList = []
        for each_cpName in df['Corpo de Prova']:
            data = {
                    'strain': list(df[df['Corpo de Prova']==each_cpName]['strain'].values)[0],
                    'stress': list(df[df['Corpo de Prova']==each_cpName]['stress'].values)[0]
                    }
            dfList.append(pd.DataFrame(data=data))

        df1 = df.drop(columns=['strain', 'stress'])
        try:
            with pd.ExcelWriter('resultados.xlsx', mode='w') as writer:  
                df1.to_excel(writer, sheet_name='Resultados Mecânicos')
                df1.describe().to_excel(writer, sheet_name='Estatística Básica')
                for each_cpName, df_stress_strain in zip(df['Corpo de Prova'], dfList):
                    df_stress_strain.to_excel(writer, sheet_name=f'{each_cpName} | Tensão | Deformação')
        except Exception as e:
            print(e)

    def __plotStressStrain(self, direction : str, testType : str):
        '''
        Metodo para plotar as curvas de tensao/deformacao, para comparacao posterior
        '''        
        xs = self.dictMechanical['strain']
        ys = self.dictMechanical['stress']

        # parte referente ao plotly
        # x_E_s =[]
        # y_E_s =[]

        # dict_property = {'flexural' : 'Módulo de Flexão (Corda) [MPa]',
        #                  'tensile' : 'Módulo de Young [MPa]',
        #                  'shear' : 'Módulo de Cisalhamento [MPa]',
        #                  }
        # for each_E in self.dictMechanical[dict_property[testType]]:
        #     x_linear = np.linspace(0,0.008)
        #     x_E_s.append(x_linear)   
        #     y_E_s.append([x*each_E for x in x_linear])
        
        labels = self.dictMechanical['Corpo de Prova']

        if testType == 'compression':
            fig_raw,ax_raw = plt.subplots(figsize=(10,4))
            xs_raw = self.dictMechanical['strain_raw']
            ys_raw= self.dictMechanical['stress_raw']
            several_plots_helper(ax=ax_raw, xs=xs_raw, ys=ys_raw,labels=labels,xlabel=r'Deformação [mm/mm]', ylabel=r'$\sigma$ [MPa]', color_scheme= 'matplotlib_default')
            ax_raw.set_title('Dados brutos dos Ensaios')

            return
        
        fig,ax = plt.subplots(figsize=(10,4))
        fig_E_lim,ax_E_lim = plt.subplots(figsize=(10,4))

   
        if direction == '11':
            several_plots_helper(ax=ax, xs=xs, ys=ys,labels=labels,xlabel=r'Deformação $[mm/mm]$', ylabel=r'$\sigma _1 $ [MPa]', color_scheme= 'matplotlib_default')
            several_plots_helper(ax=ax_E_lim, xs=xs, ys=ys,labels=labels,xlabel=r'Deformação $[mm/mm]$', ylabel=r'$\sigma _1 $ [MPa]', color_scheme= 'matplotlib_default')

        if direction == '22':
            several_plots_helper(ax=ax, xs=xs, ys=ys,labels=labels,xlabel=r'Deformação $[mm/mm]$', ylabel=r'$\sigma _2 $ [MPa]', color_scheme= 'matplotlib_default')
            several_plots_helper(ax=ax_E_lim, xs=xs, ys=ys,labels=labels,xlabel=r'Deformação $[mm/mm]$', ylabel=r'$\sigma _2 $ [MPa]', color_scheme= 'matplotlib_default')
        fig.show()

        if testType == 'tensile':
            fig_raw,ax_raw = plt.subplots(figsize=(10,4))
            xs_raw = self.dictMechanical['strain_raw']
            ys_raw= self.dictMechanical['stress_raw']
            several_plots_helper(ax=ax_raw, xs=xs_raw, ys=ys_raw,labels=labels,xlabel=r'Deformação [mm/mm]', ylabel=r'$\sigma$ [MPa]', color_scheme= 'matplotlib_default')
            ax_raw.set_title('Dados brutos dos Ensaios (Ilustrando região do filtro)')
            for each_li, each_ls, each_lim_inf_filter, each_lim_sup_filter in zip(self.E_lim_inf, self.E_lim_sup, self.x_min_array, self.x_max_array):
                ax_E_lim.axvline(x=each_li, color='orange', alpha = 0.2)
                ax_E_lim.axvline(x=each_ls, color='orange', alpha = 0.2)
                ax_E_lim.set_title('Ilustrando a região do cálculo do módulo')
                ax_raw.axvline(x=each_lim_inf_filter, color='orange', alpha = 0.2)
                ax_raw.axvline(x=each_lim_sup_filter, color='orange', alpha = 0.2)
        
        if testType == 'shear':
            fig_raw,ax_raw = plt.subplots(figsize=(10,4))
            ax.set_ylabel(r'$\sigma _{12} $ [MPa]')
            ax_E_lim.set_ylabel(r'$\sigma _{12} $ [MPa]')

            xs_raw = self.dictMechanical['strain_raw']
            ys_raw= self.dictMechanical['stress_raw']
            several_plots_helper(ax=ax_raw, xs=xs_raw, ys=ys_raw,labels=labels,xlabel=r'Deformação [mm/mm]', ylabel=r'$\sigma$ [MPa]', color_scheme= 'matplotlib_default')
            ax_raw.set_title('Dados brutos dos Ensaios (Ilustrando região do filtro)')
            
            for each_li, each_ls, each_lim_inf_filter, each_lim_sup_filter in zip(self.G_lim_inf, self.G_lim_sup, self.x_min_array, self.x_max_array):
                ax_E_lim.axvline(x=each_li, color='orange', alpha = 0.2)
                ax_E_lim.axvline(x=each_ls, color='orange', alpha = 0.2)
                ax_E_lim.set_title('Ilustrando a região do cálculo do módulo')
                ax_raw.axvline(x=each_lim_inf_filter, color='orange', alpha = 0.2)
                ax_raw.axvline(x=each_lim_sup_filter, color='orange', alpha = 0.2)
            
        if testType == 'flexural':
            fig_E_lim,ax_E_lim_original = plt.subplots(figsize=(10,4))
            fig_raw,ax_raw = plt.subplots(figsize=(10,4))
            xs = self.dictMechanical['deflection']
            ys = self.dictMechanical['force']
            xs_raw = self.dictMechanical['deflection_raw']
            ys_raw= self.dictMechanical['force_raw']
            several_plots_helper(ax=ax_E_lim_original, xs=xs, ys=ys,labels=labels,xlabel=r'Deflexão [mm]', ylabel=r' Força [N]', color_scheme= 'matplotlib_default')
            several_plots_helper(ax=ax_raw, xs=xs_raw, ys=ys_raw,labels=labels,xlabel=r'Deflexão [mm]', ylabel=r' Força [N]', color_scheme= 'matplotlib_default')
            ax_raw.set_title('Dados brutos de força e deslocamento')
            for each_li_original, each_ls_original, each_filter_inf, each_filter_sup in zip(self.E_lim_inf_original, self.E_lim_sup_original, self.x_min_array, self.x_max_array):
                ax_E_lim_original.axvline(x=each_li_original, color='orange', alpha = 0.2)
                ax_E_lim_original.axvline(x=each_ls_original, color='orange', alpha = 0.2)
                ax_E_lim_original.set_title('Ilustrando a região do cálculo do módulo (Curva de força e deslocamanto)')
                ax_raw.axvline(x=each_filter_inf, color='orange', alpha = 0.2)
                ax_raw.axvline(x=each_filter_sup, color='orange', alpha = 0.2)
    
            
        # retirando a figura do plotly
        # fig_plotly = go.Figure()
        # for each_cp,x,y,x_E,y_E in zip(labels,xs,ys, x_E_s, y_E_s):
        #             fig_plotly.add_trace(
        #     go.Scatter(
        #         x=x,  # X-axis (assuming 10 time points or measurements)
        #         y=y,
        #         mode="lines",
        #         name=f"{each_cp}",  # Legend entry
        #     )
        # )
        #             fig_plotly.add_trace(
                     
        #                          go.Scatter(
        #         x=x_E,  # X-axis (assuming 10 time points or measurements)
        #         y=y_E,
        #         mode="lines",
        #         name=f"{each_cp} - Módulo",  # Legend entry
        #     )
        #          )
        # fig_plotly.update_layout(title='Ensaio de Tração Realizado',
        # xaxis_title='Deformação [mm/mm]',
        # yaxis_title='Tensão [MPa]')
        # fig_plotly.show()
        # fig_plotly.write_html('exp_data.html')

        return None

    def __createrPDFReport(self, figs_array : list):
        '''
        Save info into a pdf (PENSAR EM UM FORMA DE COMO CRIAR UM REPORT COM AS INFORMACOES, ASSIM COM E FEITO NA INSTRON)
        '''
        # with PdfPages("output_plots.pdf") as pdf:
        #     for fig in figs_array:
        #         fig.show()
        #         pdf.savefig()  # Save each plot to the PDF file
        #         plt.close()

class MonteCarloErrorPropagation():
    '''
    Classe para calcular a propagação de erros mediante uma simulação de Monte Carlo

    Ex.:

    def density(m,r,t):
        return m/(np.pi*r**2*t)

    measured_r = [10.01,10.02,10.00,10.05]
    measured_t = [1.01,1.02,1.00,1.05]
    measured_m = [10.50,10.35,10.44,10.42]

    MonteCarloErrorPropagation(density, measured_r,measured_t,measured_m)

    '''

    def __init__(self, f : any, *measured_vars):
        self.__computeError(f, *measured_vars)
        self.__plotDistribution()

        pass

    def __computeError(self,f, *params):
        '''
        
        '''
        array_distributions = []

        for each_param in params:
            var = np.array(each_param)
            var_MC = var.mean()+var.std()*np.random.normal(size=10000)
            array_distributions.append(var_MC)

        self.f_MC : np.array = f(*array_distributions)
        self.f_mean = self.f_MC.mean()
        self.f_max = self.f_MC.mean() + 2*self.f_MC.std()
        self.f_min = self.f_MC.mean() - 2*self.f_MC.std()

    def __plotDistribution(self):
        
        graph_limit_min = min(self.f_MC)
        graph_limit_max = max(self.f_MC)
        confidence_inf = self.f_MC.mean()-2*self.f_MC.std()
        confidence_sup = self.f_MC.mean()+2*self.f_MC.std()

        y_confidence_lenght = len(self.f_MC[self.f_MC>confidence_sup])
        fig,ax = plt.subplots(figsize=(4,3))
        ax.hist(self.f_MC, bins=np.linspace(graph_limit_min,graph_limit_max))
        ax.plot([confidence_inf,confidence_inf],[0, y_confidence_lenght], color='orange')
        ax.plot([confidence_sup,confidence_sup],[0,y_confidence_lenght],color='orange')

        self.ax = ax

class SimpleStatistics():
    '''
    Classe para avaliação simples de estatíticas, dado um conjunto de dados
    '''
    def __init__(self, samples : np.array):

        self.samples : np.array = samples
        self.__computeStatistics()
        pass
    
    def __computeStatistics(self):
        '''
        Calcula estatísticas simples
        '''
        self.std = self.samples.std()
        self.mean = self.samples.mean()
        self.median = np.median(self.samples)
        self.first_quartil = np.quantile(self.samples,0.25)
        self.third_quartil = np.quantile(self.samples,3/4)

    def plot_results(self):
        
        self.fig, self.ax = plt.subplots(figsize=(4,3))
        height_bar =  len(self.samples[self.samples>np.quantile(self.samples,0.9)])
        self.ax.hist(self.samples, bins=20)
        self.ax.plot([self.first_quartil, self.first_quartil],[0,height_bar], color='orange')
        self.ax.plot([self.third_quartil, self.third_quartil],[0,height_bar], color='orange')
        self.ax.plot([self.mean, self.mean],[0,height_bar], color='green', label='Média')
        self.ax.plot([self.median, self.median],[0,height_bar], color='red', label='Mediana')
        self.ax.arrow(x=self.first_quartil,y=height_bar,dx=(self.third_quartil-self.first_quartil),dy=0, color='orange', label='Interquartil')
        self.ax.legend()

if __name__ == '__main__':
    # classInitOne =  MechanicalTestFittingLinear('68FM100', archive_name=r'D:\Jonas\ExperimentalData\OS894_22_PP40RE3AM.is_tens_Exports\YBYRÁ_Tensile_PP40RE3AM_SP-01.csv')

    # classInitOne.MeasureYoungModulus()  
    # classInit = SeveralMechanicalTestingFittingLinear('68FM100', archive_name=r'D:\Jonas\ExperimentalData\OS894_22_PP40RE3AM.is_tens_Exports\YBYRÁ_Tensile_PP40RE3AM_SP-01.csv')  
    classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'D:\Jonas\FlexCop\Experimental data\Tensile 90_SENAI_2.csv')
    classInit.MeasureYoungModulus(max_percentil=0.5, calculus_method='standard-ASTM-D3039')
    # classInit.MeasurePoissonRatio(calculus_method='linearSearch')
    # classInit.MeasurePoissonRatio(calculus_method='standard-ASTM-D3039')

# %%
# %%
# %%
