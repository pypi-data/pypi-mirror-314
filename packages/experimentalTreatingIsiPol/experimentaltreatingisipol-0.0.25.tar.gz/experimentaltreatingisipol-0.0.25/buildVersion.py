# %%
'''
Reading the .toml file (getting current version)
'''
import toml
 

print("Obtendo informações do projeto....")
with open('pyproject.toml', 'r') as f:
    config = toml.load(f)

version : str = config['project']['version']
minor_version : str = config['project']['version'].split('.')[-1]
major_version_list : list[str] = config['project']['version'].split('.')[:-1]

# %%
'''
Updating version
'''
print("Atualizando versão...")

new_minor_version = int(minor_version)+1
new_version = ".".join(major_version_list) + f".{new_minor_version}"

# %%
'''
Write the .toml file
'''
print("Escrevendo pyproject.toml...")

with open('pyproject.toml', 'w') as nf:
    nf.write(f"""
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "experimentalTreatingIsiPol"
version = "{new_version}"
authors = [
  {{ name="Example Author", email="author@example.com" }},
]
description = "Um package para auxialar no tratamento de dados"
readme = "README.md"
requires-python = ">=3.9"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
Homepage = "https://github.com/jonastieppo/PostProcessingData"
""")
    
# %%
'''
deleting dist folder
'''
import shutil
import os

if "dist" in os.listdir(os.getcwd()):
    "Removendo dist"
    shutil.rmtree('dist')

# %%
import os

print("Compilando versão...")
os.system("py -m build")

# %%
