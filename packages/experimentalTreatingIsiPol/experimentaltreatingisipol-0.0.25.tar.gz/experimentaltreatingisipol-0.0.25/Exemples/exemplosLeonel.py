# -*- coding: utf-8 -*-
"""
Processamento de dados para ensaios de permecao
Testes de Round-Robin - processamento PRELIMINAR
Arquivos de dados com a seguinte ordenacao:
    x (tempo [h]) \t y11 (resposta 1 gás 1) \t y21 (resposta 2 gás 1)
                  \t y12 (resposta 1 gás 2) \t y22 (resposta 2 gás 2)
Esse arquivo é parte do projeto FlexCOP [TC 0050.0124279.23.9]

2024 - Rede SENAI RS de Tecnologia

by Goryunov
"""
## Pacotes/Bibliotecas necessários
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import pandas as pd
import os
import re
import statistics as st
#
## Opção para entrada de fontes customizáveis
import matplotlib as mtp
mtp.rcdefaults()
mtp.rcParams['mathtext.fontset'] = 'stix'
mtp.rcParams['font.family'] = 'calibri' #'STIXGeneral'
#
## ------------ ESSAS ENTRADAS DEVEM SER MODIFICADAS ------------
#
xlbl = 'Tempo $[\\text{h}]$' # label do eixo x
#
ylbl = ['Vazão $[\\text{cm}^3/\\text{min}]$',
        'Vol. Acumulado $[\\text{cm}^3]$'] # labels do eixo y
keys = ['$\\text{CO}_2$',
        '$\\text{CH}_4$'] # entradas para diferenciação de dados
#
## ------------
## selecione se quer salvar as imagens ou nao
## para testar o scrip é recomendado nao salvar
save_fig = 'Y' # 'N' #
## definição do formato padrão para savar as figuras, e.g., .png, .svg, etc.
stdformat = 'pdf' # 'svg' #
#
### ------ FUNÇÕES ÚTEIS QUE PODEM OU NÃO SER USADOS NESSE SCRIPT ------
## salva dados para utilizar em pós-processamento
def savedata(id,datatosave):
    df = pd.DataFrame(data=datatosave.astype(float))
    df.to_csv(id + '.txt',
              sep=' ',
              header=False,
              float_format='%.7f',
              index=False)
#
## função para plots individuais para cada CP
def plot_permeacao(x1,y1,y2,cp,key,ylbl,title):
    fig, ax0 = plt.subplots(figsize=(7,2.5))
    ax0.plot(x1, y1,
              color='blue',
              linestyle='None',#'dotted',
              marker='>',
              markersize=2,
              linewidth=2,
              label=cp+' @ '+key[0])
    # ax0.set_title(str(title[:-4]))
    ax0.set_xlabel('Tempo [h]')
    ax0.set_ylabel(key[0]+' - '+ylbl)
    plt.grid()
    plt.legend()
    # twin object usado para eixo-y duplo no mesmo gráfico
    # ax1 = ax0.twinx()
    # ax1.set_ylabel(key[1]+' - '+ylbl) 
    # ax1.plot(x1, y2,
    #           color='green',
    #           linestyle='None',#'dashed',
    #           marker='H',
    #           markersize=2,
    #           linewidth=2,
    #           label=cp+' @ '+key[1])
    ax0.legend(loc='lower right', bbox_to_anchor=(0.97,0.05), framealpha=1)
    # ax1.legend(loc='lower right', bbox_to_anchor=(0.97,0.175), framealpha=1)
    fig.tight_layout()
    plt.show()
    # plt.close()
    img_format = stdformat
    img_name = title
    if save_fig == 'Y':
        fig.savefig(img_name, format=img_format, bbox_inches='tight', dpi=600)
#
### o codigo para permeação começa AQUI
#
path = os.path.abspath(os.getcwd())
# path = 'custom_path_here'
#
# iteração a partir de todos os arquivos no diretório
ids = []   # file id
spc = []   # specimen id
samp = []  # sample id
for file in os.listdir():
    # Confere se os arquivos estão no formato de texto
    if file.endswith(".txt"):
        name = f"{file}"
        ids += [name]
        samp_temp = re.search('(.*)_', file)
        samp += [str(samp_temp.group(1))]
        spc_temp = re.search('_(.*).txt', file)
        spc += [str(spc_temp.group(1))]
#
# le os dados e salva as variaveis
data = []
for i, x in enumerate(ids):
    idx = f'{path}\{x}'
    #load raw data
    raw_data = np.genfromtxt(idx)
    data += [raw_data]
    x_t = raw_data[:, 0] #x (tempo [h])
    y_11 = raw_data[:, 1] # y11 (resposta 1 gás 1)
    y_21 = raw_data[:,2] # y21 (resposta 2 gás 1)
    y_12 = raw_data[:, 3] # y12 (resposta 1 gás 2)
    y_22 = raw_data[:, 4] # y22 (resposta 2 gás 2)
    # Vazão
    name = 'Vazao_'+spc[i]+'_'+samp[i]+'.'+stdformat
    plot_permeacao(x_t,y_11,y_12,spc[i],keys,ylbl[0],name) # resposta 1
    # Volume Acumulado
    name = 'Vol.Acumulado_'+spc[i]+'_'+samp[i]+'.'+stdformat
    plot_permeacao(x_t,y_21,y_22,spc[i],keys,ylbl[1],name) # resposta 2

### Esta parte não está automatizada:

color_rnd = ['blue', 'cyan', 'blueviolet', 'dodgerblue', 'teal', 'navy',
             'steelblue', 'deepskyblue', 'maroon', 'red', 'olivedrab', 'forestgreen',
             'olive', 'springgreen', 'limegreen', 'lawngreen', 'yellowgreen', 'green',
             ]

marker_rnd = ['>', 's', 'X', '^', '*', 'o', 'x', 's', 'd',
              's', '^', '<', 'D', 'X', 's', 'v', 'D', 'o',
              ]

ticks = [x[:-4] for x in ids]
### Plot combinado para Vazão considerando CO2 e CH4
fig, ax0 = plt.subplots(figsize=(6,5))
ax1 = ax0.twinx()
for i in range(len(data)):
    xy = data[i]
    ax0.plot(xy[:,0], xy[:,1],
             linestyle='None',
             color = color_rnd[i],
             marker = marker_rnd[i],
             markersize=2,
             label = ticks[i]+' @ '+keys[0],
             )
    ax1.plot(xy[:,0], xy[:,3],
              linestyle='None',
              color = color_rnd[-(i+1)],
              marker = marker_rnd[-(i+1)],
              markersize=2,
              label = ticks[i]+' @ '+keys[1]
              )
ax0.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    framealpha=1,
    )
ax1.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.225), #1 linha
    # bbox_to_anchor=(0.5, -0.3), #2 linhas
    # bbox_to_anchor=(0.5, -0.65), #3 linhas
    ncol=3,
    framealpha=1,
    )
ax0.set_xlabel(xlbl)
ax0.set_ylabel(keys[0]+' - '+ylbl[0])
ax1.set_ylabel(keys[1]+' - '+ylbl[0])
if samp[0] == samp[-1]:
    # ax0.set_title('Vazão - '+samp[0])
    img_name = 'VAZAO-'+samp[0]+'.'+stdformat
else:
    # ax0.set_title('Vazão')
    img_name = 'VAZAO-todos.'+stdformat
ax0.grid(True)
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()
if save_fig == 'Y':
    fig.savefig(img_name, format=stdformat, bbox_inches='tight', dpi=600)

## Plot simples para Vazão considerando só CO2
fig, ax0 = plt.subplots(figsize=(6,4))
for i in range(len(data)):
    xy = data[i]
    ax0.plot(xy[:,0], xy[:,1],
             linestyle='None',
             color = color_rnd[i],
             marker = marker_rnd[i],
             markersize=2,
             label = ticks[i]+' @ '+keys[0],
             )
ax0.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    framealpha=1,
    )
ax0.set_xlabel(xlbl)
ax0.set_ylabel(keys[0]+' - '+ylbl[0])
if samp[0] == samp[-1]:
    # ax0.set_title(keys[0]+' - Vazão - '+samp[0])
    img_name = 'VAZAO_CO2-'+samp[0]+'.'+stdformat
else:
    # ax0.set_title(keys[0]+' - Vazão')
    img_name = 'VAZAO_CO2'+'.'+stdformat
ax0.grid(True)
plt.tight_layout()
plt.show()
# plt.close()
if save_fig == 'Y':
    fig.savefig(img_name, format=stdformat, bbox_inches='tight', dpi=600)

### Plot simples para Vazão considerando só CH4
fig, ax0 = plt.subplots(figsize=(6,4))
for i in range(len(data)):
    xy = data[i]
    ax0.plot(xy[:,0], xy[:,3],
             linestyle='None',
             color = color_rnd[-(i+1)],
             marker = marker_rnd[-(i+1)],
             markersize=2,
             label = ticks[i]+' @ '+keys[1],
             )
ax0.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    framealpha=1,
    )
ax0.set_xlabel(xlbl)
ax0.set_ylabel(keys[1]+' - '+ylbl[0])
if samp[0] == samp[-1]:
    # ax0.set_title(keys[1]+' - Vazão - '+samp[0])
    img_name = 'VAZAO_CH4-'+samp[0]+'.'+stdformat
else:
    # ax0.set_title(keys[1]+' - Vazão')
    img_name = 'VAZAO_CH4'+'.'+stdformat
ax0.grid(True)
plt.tight_layout()
plt.show()
if save_fig == 'Y':
    fig.savefig(img_name, format=stdformat, bbox_inches='tight', dpi=600)

### Plot combinado para Volume Acumulado considerando CO2 e CH4
fig, ax0 = plt.subplots(figsize=(6,5))
ax1 = ax0.twinx()
for i in range(len(data)):
    xy = data[i]
    ax0.plot(xy[:,0], xy[:,2],
             linestyle='None',
             color = color_rnd[i],
             marker = marker_rnd[i],
             markersize=2,
             label = ticks[i]+' @ '+keys[1],
             )
    ax1.plot(xy[:,0], xy[:,4],
              linestyle='None',
              color = color_rnd[-(i+1)],
              marker = marker_rnd[-(i+1)],
              markersize=2,
              label = ticks[i]+' @ '+keys[1],
              )
ax0.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.3),
    ncol=3,
    framealpha=1,
    )
ax1.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.225), #1 linha
    # bbox_to_anchor=(0.5, -0.3), #2 linhas
    # bbox_to_anchor=(0.5, -0.65), #3 linhas
    ncol=3,
    framealpha=1,
    )
ax0.set_xlabel(xlbl)
ax0.set_ylabel(keys[0]+' - '+ylbl[1])
ax1.set_ylabel(keys[1]+' - '+ylbl[1])
if samp[0] == samp[-1]:
    # ax0.set_title('Vol. Acumulado - '+samp[0])
    img_name = 'VOLUME-'+samp[0]+'.'+stdformat
else:
    # ax0.set_title('Vol. Acumulado')
    img_name = 'VOLUME-todos.'+stdformat
ax0.grid(True)
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()
if save_fig == 'Y':
    fig.savefig(img_name, format=stdformat, bbox_inches='tight', dpi=600)

### Plot simples para Vol. Acumulado considerando só CO2
fig, ax0 = plt.subplots(figsize=(6,4))
for i in range(len(data)):
    xy = data[i]
    ax0.plot(xy[:,0], xy[:,2],
             linestyle='None',
             color = color_rnd[i],
             marker = marker_rnd[i],
             markersize=2,
             label = ticks[i]+' @ '+keys[0],
             )
ax0.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    framealpha=1,
    )
ax0.set_xlabel(xlbl)
ax0.set_ylabel(keys[0]+' - '+ylbl[1])
if samp[0] == samp[-1]:
    # ax0.set_title(keys[0]+' - Vol. Acumulado - '+samp[0])
    img_name = 'VOLUME_CO2-'+samp[0]+'.'+stdformat
else:
    # ax0.set_title(keys[0]+' - Vol. Acumulado')
    img_name = 'VOLUME_CO2'+'.'+stdformat
ax0.grid(True)
plt.tight_layout()
plt.show()
if save_fig == 'Y':
    fig.savefig(img_name, format=stdformat, bbox_inches='tight', dpi=600)

### Plot simples para Vol. Acumulado considerando só CH4
fig, ax0 = plt.subplots(figsize=(6,4))
for i in range(len(data)):
    xy = data[i]
    ax0.plot(xy[:,0], xy[:,4],
             linestyle='None',
             color = color_rnd[-(i+1)],
             marker = marker_rnd[-(i+1)],
             markersize=2,
             label = ticks[i]+' @ '+keys[1],
             )
ax0.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    framealpha=1,
    )
ax0.set_xlabel(xlbl)
ax0.set_ylabel(keys[1]+' - '+ylbl[1])
if samp[0] == samp[-1]:
    # ax0.set_title(keys[1]+' - Vol. Acumulado - '+samp[0])
    img_name = 'VOLUME_CH4-'+samp[0]+'.'+stdformat
else:
    # ax0.set_title(keys[1]+' - Vol. Acumulado')
    img_name = 'VOLUME_CH4'+'.'+stdformat
ax0.grid(True)
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()
if save_fig == 'Y':
    fig.savefig(img_name, format=stdformat, bbox_inches='tight', dpi=600)

# ### ### FUNCOES UTEIS QUE PODEM OU NAO SER USADOS NESSE SCRIPT
# # Save file with data for statistical analysis
# def savedata(id,datatosave):
#     df = pd.DataFrame(data=datatosave.astype(float))
#     df.to_csv(id + '.txt',
#               sep=' ',
#               header=False,
#               float_format='%.7f',
#               index=False)

# # Plots graphics from raw data
# def plot_raw(x1,x2,y1,lbl,titleid):
#     fig, axs = plt.subplots(2, 1)
#     axs[0].plot(x1, y1,
#               color='darkblue', linestyle='dotted',
#               label='CP = '+str(lbl))
#     axs[0].legend(loc='lower right')
#     axs[0].set_xlabel('t [s]')
#     axs[0].set_ylabel('F [N]')
#     axs[0].set_title('Dados brutos: '+lbl)
#     axs[0].grid(True)
#     axs[1].plot(x2, y1,
#               color='green', linestyle='dotted',
#               label='CP = '+str(lbl))
#     axs[1].legend(loc='lower right')
#     axs[1].set_ylabel('F [N]')
#     axs[1].set_xlabel('u [mm]')
#     fig.tight_layout()
#     plt.show()
#     # plt.close()
#     img_format = stdformat
#     img_name = 'Dados_brutos_'+titleid
#     if save_fig == 'Y':
#         fig.savefig(img_name, format=img_format, dpi=600)

# # Single plot with friction data
# def plot_SigmaEpson(x1,y1,lbl,titleid):
#     fig, ax = plt.subplots(figsize=(7,4))
#     # make a plot
#     ax.plot(x1, y1,
#               color='darkblue', linestyle='dotted',
#               linewidth=2, label='CP = '+str(lbl))
#     ax.legend(loc='lower right')
#     ax.set_title('Curva tensao X deformacao: '+str(titleid[:-4]))
#     ax.set_xlabel('Strain [mm/mm]')
#     ax.set_ylabel('Stress [Pa]')

#     plt.show()
#     # plt.close()
#     img_format = stdformat
#     img_name = 'Sigma_vs_Epson_'+title
#     if save_fig == 'Y':
#         fig.savefig(img_name, format=img_format, dpi=600)

# # Filter
# def plot_filter(x1,y1,y2,lbl1,lbl2,lbl3,title):
#     fig, ax1 = plt.subplots(figsize=(7,4))
#     ax1.plot(x1, y1,
#               color='darkblue', linestyle='dotted',
#               linewidth=2, label='RAW data ('+'Weight = '+str(lbl1)+'kg)')
#     ax1.plot(x1, y2,
#               color='orange', linestyle='dashed',
#               linewidth=2, label='Filtered data')
#     # ax1.set_title('Specimen = '+str(lbl3)+'       Repetition = '+str(lbl2))
#     ax1.set_title('Filtered data: '+str(title[:-4]))
#     ax1.set_xlabel('Displacement [mm]')
#     ax1.set_ylabel('Force [N]')
#     plt.grid()
#     plt.legend()
#     # twin object for two different y-axis on the sample plot
#     ax2 = ax1.twinx()
#     ax2.set_ylabel('Friction Coefficient') 
#     ax2.set_ylim(ax1.get_ylim()[0]/(lbl1*9.8182),
#                   ax1.get_ylim()[1]/(lbl1*9.8182))
#     plt.show()
#     # plt.close()
#     img_format = stdformat
#     img_name = 'FILTER_'+title
#     if save_fig == 'Y':
#         fig.savefig(img_name, format=img_format, dpi=600)


# # BoxPlot for two data sets (RAW and Filtered)
# def BoxP(data,titleid,lbl):
#     myflierprops1 = dict(markerfacecolor = 'r',marker = 's')
#     myboxprops1 = dict(facecolor = 'DarkBlue', linewidth = 1, color = 'black')
#     mymeanprops1 = dict(linestyle = '--', linewidth = 2, color = 'limegreen')
#     mymedianprops1 = dict(linestyle = '--', linewidth = 2, color = 'DarkGrey')
#     mycapprops1 = dict(linestyle = '-', linewidth = 2, color = 'black')
#     #
#     fig, ax = plt.subplots(figsize=(7,4))
#     ax.boxplot(data, showmeans=1, meanline=True,
#                 positions=[0.5],
#                 notch=0, vert=1, patch_artist=1,
#                 flierprops = myflierprops1,
#                 boxprops = myboxprops1,
#                 meanprops = mymeanprops1,
#                 medianprops = mymedianprops1,
#                 capprops = mycapprops1,
#                 )
#     ax.set_xticklabels(['Elasticidade'])
#     ax.set_title(titleid)
#     ax.set_xlim( [ 0.25, 0.75 ] )
#     plt.ylabel(lbl)
#     plt.grid()
#     ls = [plt.Line2D([0], [0], linestyle = '--', linewidth = 2, color = 'limegreen'),
#           plt.Line2D([0], [0], linestyle = '--', linewidth = 2, color = 'DarkGrey'),
#           plt.Line2D([0], [0], linestyle = 'None', markerfacecolor = 'r',
#                       markeredgecolor = 'black', marker = 's', markersize = 6),
#           ]
#     labels = ['Media', 'Mediana', 'Outlier']
#     plt.legend(ls, labels, loc='lower right')
#     plt.show()
#     # plt.close()
#     img_format = stdformat
#     img_name = 'BoxPlot_'+titleid.replace(" ","_")+'.'+stdformat
#     if save_fig == 'Y':
#         fig.savefig(img_name, format=img_format, dpi=600)

# # BarPlot for two data sets (RAW and Filtered)
# def BarP(bars,titleid,spc):
#     avg_bars = st.mean(bars)
#     sigma_bars = st.stdev(bars)
#     # width of the bars
#     barWidth = 0.3
#     # Choose the height of the error bars (bars1)
#     yer = sigma_bars*np.ones(len(bars))
#     # The x position of bars
#     r1 = np.arange(len(bars))
#     r2 = [x + barWidth for x in r1]
#     fig, ax = plt.subplots(figsize=(7,6))#figsize=(9,6))
#     # Create orange bars
#     plt.bar(r1, bars, width = barWidth, color = 'blue', edgecolor = 'black',
#             yerr=yer, capsize=2, label='Dados brutos')
#     # add mean lines
#     plt.axhline(y=avg_bars,
#                 color='Red', linestyle='-',
#                 label='Media =  '+str(round(avg_bars,3)))
#     plt.legend(bbox_to_anchor=(0.8,0.2), loc='center left', borderaxespad=0,
#                 facecolor='white', framealpha = 1)
#     # general layout
#     plt.xticks([r + barWidth for r in range(len(bars))], spc, rotation=75)
    
#     plt.ylabel('E [MPa]')
#     plt.xlabel('Especime')
#     ax.set_title(titleid + '  -  ' + 'Desvio padrao = '+str(round(sigma_bars,3)))
#     plt.tight_layout()
#     plt.show()
#     img_format = stdformat
#     img_name = 'BarPlot_'+titleid.replace(" ","_")+'.'+stdformat
#     if save_fig == 'Y':
#         fig.savefig(img_name, format=img_format, dpi=600)

# # Histogram plot
# def histg(data,titleid):
#     fig, ax = plt.subplots(sharey=True, tight_layout=True)
#     plt.hist(data, bins= 'auto',
#               #'auto','fd','doane','scott','stone','rice','sturges','sqrt'
#               color='DarkBlue', label='Dados brutos',
#               alpha=0.75, rwidth=0.25, density=True)
#     plt.grid(axis='y', alpha=0.75)
#     plt.xlabel('Elasticidade [MPa]')
#     plt.ylabel('Frequencia')
#     plt.title(titleid)
#     plt.legend()
#     plt.show()
#     img_format = stdformat
#     img_name = 'Histograma_'+titleid.replace(" ","_")+'.'+stdformat
#     if save_fig == 'Y':
#         fig.savefig(img_name, format=img_format, dpi=600)

# # Fitting plot (Fnorm X Ffrict)
# def polyplot(data1,data2,lin_inf,lin_sup,titleid,colorid):
#     fig, ax = plt.subplots(figsize=(7,4))
#     # Plots data
#     plt.plot(data1, data2,
#               linestyle='dotted', linewidth=1.5,
#               color = colorid, label= titleid
#               )
#     # adjust data to linear limits
#     lindata = np.where((data1 > lin_sup), np.nan, [data1])
#     lindata = np.where((lindata < lin_inf), np.nan, [lindata])
#     newdata1 = lindata[~np.isnan(lindata)]
#     idnan = np.argwhere(np.isnan(lindata))
#     remov_id = idnan[:,-1]
#     newdata2 = np.delete(data2,remov_id)
#     # Linear fit
#     m, b = np.polyfit(newdata1, newdata2, 1, 'full'==False)
#     y_lin = m*newdata1 + b
#     y_bar = np.mean(y_lin)
#     R2 = np.sum((y_lin - y_bar)**2) / np.sum((newdata2 - y_bar)**2)
#     # print(R2)
#     # Add mean lines
#     plt.plot(newdata1, y_lin,
#               '-', color = 'Violet', linewidth=1.5, label='Linear fit')
#     plt.ylabel('Tensao [MPa')
#     plt.xlabel('Deformacao [mm/mm]')
#     plt.legend(loc='lower right')
#     ax.set_title('Linear fit')
#     plt.text(1.1*np.min(data1), 0.9*np.max(data2), 'Slope = '+str(np.round(m,3)),
#               fontsize=12, bbox=dict(facecolor=colorid, alpha=0.25))
#     plt.text(1.1*np.min(data1), 0.8*np.max(data2), 'R2 = '+str(np.round(R2,3)),
#               fontsize=12, bbox=dict(facecolor=colorid, alpha=0.25))
#     plt.show()
#     img_format = stdformat
#     img_name = 'LinearFit_'+titleid.replace(" ","_")+'.'+stdformat
#     if save_fig == 'Y':
#         fig.savefig(img_name, format=img_format, dpi=600)
#     return(m)
    
# # Detection of Outliers – IQR approach
# # This MIGHT NOT WORK if IQR affects RAW and Filtered differently
# def IQR(sample,add1,add2):
#     q75,q25 = np.percentile(sample,[75,25])
#     intr_qr = q75-q25
#     v_max = q75+(1.5*intr_qr)
#     v_min = q25-(1.5*intr_qr)
#     sample = np.where((sample > v_max), np.nan, [sample])
#     sample = np.where((sample < v_min), np.nan, [sample])
#     new_sample = sample[~np.isnan(sample)]
#     idnan = np.argwhere(np.isnan(sample))
#     remov_id = idnan[:,-1]
#     new_add1 = np.delete(add1,remov_id)
#     new_add2 = np.delete(add2,remov_id)
#     return(new_sample,new_add1,new_add2)

# ### ### o codigo do Yuri comeca aqui

# path = os.path.abspath(os.getcwd())
# # path = 'custom_path_here'

# # iterate through all files
# ids = []   # file id
# spc = []   # specimen id
# for file in os.listdir():
#     # Check whether file is in text format or not
#     if file.endswith(".txt"):
#         name = f"{file}"
#         ids += [name]
#         spc_temp = re.search('(.*).txt', file)
#         spc += [str(spc_temp.group(1))]
# #---


# # le os dados e salva as variaveis
# Fmax = []
# data = []
# sigma_epson = []
# E = []
# for i, x in enumerate(ids):
#     idx = f'{path}\{x}'
#     #load raw data
#     raw_data = np.genfromtxt(idx)
#     data += [raw_data]
#     x_t = raw_data[:, 0]
#     x_d = raw_data[:, 1]
#     y_f = raw_data[:,2]
#     x_d = x_d[:-3] # remover picos depois do CP quebrar
#     x_t = x_t[:-3]
#     y_f = y_f[:-3]
#     # deformacao DeltaL/L0 (u/L)
#     strain = x_d*1e-3/L0 # [mm/mm]
#     stress = y_f/A*1e-6 # [MPa]
#     sigma_epson += [stress,strain]
#     Fmax += [max(y_f)]
#     lbl = spc[i] # spc
#     title = spc[i]+'.'+stdformat
#     plot_raw(x_t,x_d,y_f,lbl,title)
#     plot_SigmaEpson(strain,stress,lbl,title)
#     Elasticidade = polyplot(strain, stress, lin_inf, lin_sup, title, 'orange')
#     E += [Elasticidade]

# histg(E,title)
# BoxP(E,'Grafico de caixa','E [MPa]')
# BarP(E,'Grafico de barras',spc)
# #---

# # # # Force VS Force plots (Full data)
# # # polyplot(Fnorm,Ffrict_peak,'Full data - Filtered','orange')
# # # polyplot(Fnorm,Ffrict_raw,'Full data - RAW','DarkBlue')
# #     raw_data = np.genfromtxt(idx)
# #     data += [raw_data]
# #     x_t = raw_data[:, 0]
# #     x_d = raw_data[:, 1]
# #     y_f = raw_data[:,2]
# #     lbl1 = round(wg[i],3) # weight in kg
# #     lbl2 = rpt[i] # test repetition
# #     lbl3 = spc[i] # specimen id
# #     title = str(x[:-3])+stdformat
# #     plot_raw(x_t,x_d,y_f,lbl1,lbl2,lbl3,title)
# #     plot_friction(x_d,y_f,lbl1,lbl2,lbl3,title)
# #     # Filter the data, and plot both the original and filtered signals.
# #     y_filter = butter_lowpass_filter(y_f, cutoff, fs, order)
# #     mu_raw += [np.max(y_f)/(lbl1*9.8182)]
# #     mu_peak += [np.max(y_filter)/(lbl1*9.8182)]
# #     Ffrict_raw += [np.max(y_f)]
# #     Ffrict_peak += [np.max(y_filter)]
# #     Fnorm += [wg[i]*9.8182]
# #     plot_filter(x_d,y_f,y_filter,lbl1,lbl2,lbl3,title)
# # #---


# # # Full data statistics plots:
# # ticks = [x[:-4] for x in ids]
# # BarP(mu_raw,mu_peak,'Complete Data',ticks)
# # BoxP(mu_raw,mu_peak,'Complete Data','Friction Coefficient')
# # BoxP(Ffrict_raw,Ffrict_peak,'Complete Data - Force','Friction Force [N]')

# # # Removing outliers
# # IQR_mu_peak, IQR_mu_raw, IQR_ticks = IQR(mu_peak, mu_raw, ticks)
# # IQR_ticks = IQR_ticks.tolist() # to fix list operation
# # IQR_Ffrict_peak, IQR_Ffrict_raw, new_Fnorm = IQR(Ffrict_peak, Ffrict_raw, Fnorm)

# # # Force VS Force plots (IQR treated data)
# # polyplot(new_Fnorm,IQR_Ffrict_peak,'Post IQR - Filtered','orange')
# # polyplot(new_Fnorm,IQR_Ffrict_raw,'Post IQR - RAW','DarkBlue')

# # # Full data statistics plots:
# # BarP(IQR_mu_raw,IQR_mu_peak,'IQR Outliers Removed',IQR_ticks)
# # BoxP(IQR_mu_raw,IQR_mu_peak,'IQR Outliers Removed','Friction Coefficient')
# # BoxP(IQR_Ffrict_raw,IQR_Ffrict_peak,'IQR Outliers Removed - Force','Friction Force [N]')

# # # Histogram data plots:
# # histg(mu_raw,mu_peak,'Full Data Histogram')
# # histg(IQR_mu_raw,IQR_mu_peak,'IQR Data Histogram')

# # ### ### script ends HERE

# # # 1. Setting prop cycle on default rc parameter
# # plt.rc('lines', linewidth=1)
# # plt.rc('axes', prop_cycle=(cycler('color',
# #                                   [
# #                                     'black', 'gray', 'silver',
# #                                     'cornflowerblue', 'blue', 'navy',
# #                                     'red', 'maroon', 'crimson',
# #                                     'darkgreen', 'lime', 'springgreen',
# #                                     'goldenrod', 'gold', 'yellow',
# #                                     'magenta', 'violet', 'darkviolet',
# #                                     'black', 'gray', 'silver',
# #                                     'cyan', 'blue', 'navy',
# #                                     'red', 'maroon', 'crimson'
# #                                     ]) +
# #                             cycler('linestyle',
# #                                   [
# #                                     '-.', '--', ':', '-.', '-.', '-', 
# #                                     '--', ':','-',
# #                                     '-.', '--', ':', '-.', '-.', '-', 
# #                                     '--', ':','-', 
# #                                     '-.', '--', ':', '-.', '-.', '-', 
# #                                     '--', ':','-'
# #                                     ]) +
# #                             cycler('marker',
# #                                   [
# #                                     'p', 'd', 'o', '+', '*', '^', 'x', 's', 'X',
# #                                     'p', 'd', 'o', '+', '*', '^', 'x', 's', 'X',
# #                                     'p', 'd', 'o', '+', '*', '^', 'x', 's', 'X',
# #                                     ])
# #                             ))

# # if len(spc) > 20:
# #     fig, axs = plt.subplots(figsize=(7,9))
# # else:
# #     fig, axs = plt.subplots(figsize=(7,5))
# # for i in range(len(data)):
# #     xy = data[i]
# #     axs.plot(xy[:,1], xy[:,2], markersize=1,
# #               label = ticks[i]
# #               # label='Spc.: '+str(spc[i])+' - LF: 0'+str(lf[i])+
# #               # ' - Repetition: '+str(rpt[i])
# #               )
# # # axs.set_xlim([0, 12])
# # axs.set_xlim([0, 7])
# # axs.legend(
# #     loc='upper center',
# #     bbox_to_anchor=(0.5, -0.15),
# #     ncol=4,
# #     )
# # axs.set_xlabel('Displacement [mm]')
# # axs.set_ylabel('Force [N]')
# # axs.set_title('RAW data - all tests overlapped')
# # axs.grid(True)
# # fig.tight_layout()
# # plt.show()
# # # plt.close()
# # img_name = 'RAW data - all tests overlapped'+'.'+stdformat
# # if save_fig == 'Y':
# #     fig.savefig(img_name, format=stdformat, dpi=600)