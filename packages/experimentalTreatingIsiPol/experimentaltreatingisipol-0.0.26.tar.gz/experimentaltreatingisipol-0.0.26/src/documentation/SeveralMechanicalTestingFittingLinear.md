# Classe destinada à análise de dados experimentais de diversos CPs. 

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

| linearRegionSearchMethod  |                                             Semântica                          |
|:-------------------------:|:-------------------------------------------------------------------------------|
|       Deterministic       |  Programa a região linear baseada em uma regra de mudança de derivada          |
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

## Exemplos:

Em uma pasta, chamada **experimental_data**, temos 4 arquivos de um ensaio de tração. Abra um dos arquivos dos testes, e:
a) Identifique o tipo de arquivo. Tenha em mente que o teste utilizado é o de tração. (Dica: Use a função `print_docConfig()`)

b) Modifique o seguinte código, para o padrão acima identificado (modifique também o caminho do arquivo):

```python
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear

arq_path = "caminho_do_arquivo" # Modifique o caminho do arquivo
configuracao = "_configuracao" # Modifique o caminho da configuração

c = SeveralMechanicalTestingFittingLinear(
                            docConfig = configuracao, 
                            archive_name=arq_path,
                            direction = '11',
                            testType='tensile',
)

```
c) Modifique o seguinte código, adicione o argumento `calculus_method='standard-ASTM-D3039'` na criação da classe SeveralMechanicalTestingFittingLinear

```python
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear

arq_path = "caminho_do_arquivo" # Modifique o caminho do arquivo
configuracao = "_configuracao" # Modifique o caminho da configuração

c = SeveralMechanicalTestingFittingLinear(
                            docConfig = configuracao, 
                            archive_name=arq_path,
                            calculus_method = "coloque_a_norma" # Modificar aqui
                            direction = '11',
                            testType='tensile',
)

d) Modifique o código acima, e teste o efeito de outras normas: 
    - 'standard-ASTM-D638'
    - 'standard-ASTM-D7078'

```

e) Modifique o código abaixo, e altere a região de limpeza dos dados. Para isso, coloque
`linearRegionSearchMethod='Custom'`, e brinque com os valores de x_max e x_min:


```python
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear

arq_path = "caminho_do_arquivo" # Modifique o caminho do arquivo
configuracao = "_configuracao" # Modifique o caminho da configuração

c = SeveralMechanicalTestingFittingLinear(
                            docConfig = configuracao, 
                            archive_name=arq_path,
                            direction = '11',
                            calculus_method='standard-ASTM-D3039',
                            linearRegionSearchMethod='_colocar_metodo_aqui', # Modificar aqui
                            x_min=0.4, # Modificar aqui
                            x_max=1, # Modificar aqui
                            verbose=False,
                            testType='tensile',
)

```
