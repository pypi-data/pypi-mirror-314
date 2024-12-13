
# %%
'''
Gráfico de linha simples
'''
from experimentalTreatingIsiPol.main import plot_helper
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = plot_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")

fig.savefig('grafico_linha_simples.svg')

# %%
'''
Gráfico de linha simples, sem grid
'''
from experimentalTreatingIsiPol.main import plot_helper
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = plot_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")

ax.grid()
fig.savefig('grafico_linha_simples_sem_grid.svg')

# %%
from experimentalTreatingIsiPol.main import scatter_helper
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = scatter_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")

fig.savefig('grafico_dispersao.svg')
# %%
'''
Vários gráficos no mesmo meixo eixo (Método 1)
'''
from experimentalTreatingIsiPol.main import plot_helper, color_rnd
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
x = np.linspace(-10,10)
y1 = np.multiply(x,2)
y2 = np.power(x,1/2)
ax = scatter_helper(ax, x=x,
            y=y1, 
            xlabel='x', ylabel='y', 
            label=r"$2x$", color=color_rnd[0])

ax = scatter_helper(ax, x=x,
            y=y2, 
            xlabel='x', ylabel='y', 
            label=r"$x^{\frac{1}{2}}$", color = color_rnd[5], )


# %%
'''
Demonstração da alteração de estilos
'''
import matplotlib.pyplot as plt
from experimentalTreatingIsiPol.main import plot_helper

fig, (ax,ax2) = plt.subplots(1,2,figsize=(10, 3))

x=np.linspace(-10,10)
y1=np.power(x,2)
y2=np.power(x,3)/3

ax = plot_helper(ax,x=x,y=y1, label=r'$y=x^2$', xlabel='x', ylabel='y')
ax.set_title(r"$Math\ mode\ : x^2$",
             math_fontfamily='stixsans', size=14, family='cursive')

ax2 = plot_helper(ax2,x=x,y=y2, label=r'$y=1/3x^3$', xlabel='x', ylabel='y')
ax2.set_title(r"Título em cursivo $\int x^2 dx$",
             math_fontfamily='stixsans', size=14, family='cursive')

fig.savefig('plot_diferentes_fontes.svg')


# %%
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 5))

# A simple plot for the background.
x = np.linspace(1,10,10)
y = np.random.standard_normal(10)

ax.plot(x,y,color="0.9", label='Alguma legenda com tamanho 7')
ax.set_xlabel('Título do eixo x, com tamanho 8', fontsize = 8)
ax.set_ylabel('Título do eixo x, com tamanho 8', fontsize = 8)
ax.legend(fontsize=7)
ax.tick_params(axis='x', labelsize=5) # fonte dos pontos do eixo x com tamanho 5
plt.show()


# %%
import matplotlib as mtp

mtp.rcParams['legend.fontsize'] = 7 # Fonte global da legenda
mtp.rcParams['xtick.labelsize'] = 5 # Fonte dos pontos do eixo x com tamanho 5
mtp.rcParams['axes.labelsize'] = 8 # Fonte dos eixos x e y

fig, ax = plt.subplots(figsize=(6, 5))

# A simple plot for the background.
x = np.linspace(1,10,10)
y = np.random.standard_normal(10)

ax.plot(x,y,color="0.9", label='Alguma legenda com tamanho 7')
ax.set_xlabel('Título do eixo x, com tamanho 8')
ax.set_ylabel('Título do eixo x, com tamanho 8')
ax.legend()
ax.tick_params(axis='x') # fonte dos pontos do eixo x com tamanho 5
plt.show()

# %%
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear
import os
archive = os.path.join(os.getcwd(),r'..\DataArquives\Specimen_RawData_1.csv')
classInit =  MechanicalTestFittingLinear(docConfig='68FM100', archive_name=archive)
classInit.MeasureYoungModulus(length = 50,thickess = 1,width = 12)   
# %%
