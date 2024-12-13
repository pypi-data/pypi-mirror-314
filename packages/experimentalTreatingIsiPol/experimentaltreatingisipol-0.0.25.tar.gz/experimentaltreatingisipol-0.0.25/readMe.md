# Introdução e filosofia da implementação

Esse repositório é uma iniciativa, por parte da PDI, de criar ferramentas para pós-processamento de resultados experimentais. Tais ferramentas serão auditáveis, abertas, e com o intuito de serem colaborativas.


## Sumário

- [Pós Processamento de Ensaios Experimentais](#pós-processamento-de-ensaios-experimentais)
    - [Máquinas ajustadas]()
- [Exemplos de gráficos](#exemplos-de-gráficos)
    - [Gráfico de linha simples](#gráfico-de-linha-simples)
    - [Gráfico de dispersão simples](#gráfico-de-dispersão-simples)
- [Estilização dos gráficos](#estilização-dos-gráficos)
    - [Formatação de fonte](#formatação-de-fonte)
        - [Estilo de fonte](#estilo-de-fonte)
        - [Tamanho de fonte](#tamanho-de-fonte)

# Pós processamento de ensaios experimentais mecânicos
O pós-processamento de ensaios experimentais segue o paradigma universal de existir medição de uma entidade de força e um descolamento. Esse paradigma é comum em diferentes metodologias experimentais, tais como a determinação de *Moduli* de Young, cisalhamento, entre outros. Logo, para cada tipo específico de ensaio, existirão métodos especializados, muito embora a base seja compartilhada. 

Um exemplo de utilização do ajuste encontra-se a seguir:

```python
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear
import os
archive = os.path.join(os.getcwd(),r'..\DataArquives\Specimen_RawData_1.csv')
classInit =  MechanicalTestFittingLinear(machineName='68FM100', archive_name=archive)
classInit.MeasureYoungModulus(length = 50,thickess = 1,width = 12)   
```

## Máquinas ajustadas
A lista de máquinas ajustadas encontra-se abaixo:

| Máquina         | machine |
|-----------------|---------|
| Instron 68FM100 | 68FM100 |

## Métodos para determinação da região linear
## Cálculo Módulo de Young
[Volta ao topo](#introdução-e-filosofia-da-implementação)
# Exemplos de gráficos
[Volta ao topo](#introdução-e-filosofia-da-implementação)

## Gráfico de linha simples
Um gráfico padronizado pode ser gerado ao se utilizar a função `plot_helper()` da biblioteca. 

```python
from experimentalTreatingIsiPol.main import plot_helper
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = plot_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")
```

![Grafico de linha simples](/Exemples/grafico_simples.svg "Grafico de linha simples")

A função retorna o próprio objeto do eixo, `ax`. Portanto, todos os métodos do matplotlib são herdados. Por exemplo, pode-se retirar as linhas de grade, caso seja de interesse do usuário:

```python
ax.grid()
```

![Grafico de linha simples](/Exemples/grafico_linha_simples_sem_grid.svg "Grafico de linha simples")

[Volta ao topo](#introdução-e-filosofia-da-implementação)

## Gráfico de dispersão simples
Um gráfico de dispersão é facilmente gerado ao se utilizar a função `scatter_helper()`.

```python
from experimentalTreatingIsiPol.main import scatter_helper
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = scatter_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")
```

![Grafico de linha simples](/Exemples/grafico_dispersao.svg "Grafico de Dispersão")

[Volta ao topo](#introdução-e-filosofia-da-implementação)
# Estilização dos gráficos
[Volta ao topo](#introdução-e-filosofia-da-implementação)

## Formatação de fonte 
Em termos de estilos de fonte, os gráficos podem ser estilizados modificando a propriedade rcParams do matplotlib. A seguir, um exemplo de como atribuir a fonte calibri para o texto, e a fonte stix para texto *matemático*, em um determinado gráfico.

[Volta ao topo](#introdução-e-filosofia-da-implementação)

### Estilo de fonte
O estilo de fonte pode ser alterado de forma global:

```python
import matplotlib as mtp

mtp.rcdefaults() # retorna ao padrão
mtp.rcParams['mathtext.fontset'] = 'stix'# STIX Fonts used in LaTeX rendering. 
mtp.rcParams['font.family'] = 'calibri' #'STIXGeneral'
```
O mesmo efeito pode ser aplicado localmente:


```python
import matplotlib.pyplot as plt

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(6, 5))

# A simple plot for the background.
ax1.plot(range(11), color="0.9")
ax2.plot(range(11), color="0.9")
ax1.set_title(r"$Title\ in\ math\ mode:\ \int_{0}^{\infty } x^2 dx$",
             math_fontfamily='stixsans', size=14, family='cursive')
ax2.set_title(r"Title in cursive $\int_{0}^{\infty } x^2 dx$",
             math_fontfamily='stixsans', size=14, family='cursive')
plt.show()
```
[Volta ao topo](#introdução-e-filosofia-da-implementação)

### Tamanho de fonte

O tamanho de fonte pode ser alterado através do parâmetros fontsize, para as legendas, títulos dos eixos, e rótulo dos dados. Faz-se a seguir um exemplo:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 5))

# A simple plot for the background.
x = np.linspace(1,10,10)
y = np.random.standard_normal(10)

ax.plot(x,y,color="0.9", label='Alguma legenda com tamanho 7')
ax.set_xlabel('Título do eixo x, com tamanho 8', fontsize = 8)
ax.set_ylabel('Título do eixo y, com tamanho 8', fontsize = 8)
ax.legend(fontsize=7)
ax.tick_params(axis='x', labelsize=5) # fonte dos pontos do eixo x com tamanho 5
plt.show()
```

Os tamanhos de fonte também podem ser alterados de forma global, através dos rcParams:

```python
import matplotlib as mtp

mtp.rcParams['legend.fontsize'] = 7 # Fonte global da legenda
mtp.rcParams['xtick.labelsize'] = 5 # Fonte dos pontos do eixo x com tamanho 5
mtp.rcParams['axes.labelsize'] = 8 # Fonte dos eixos x e y
```
[Volta ao topo](#introdução-e-filosofia-da-implementação)


