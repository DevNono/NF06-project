# Projet E-Zone Manager - 2022

## Description

Projet réalisé dans le cadre de l'UE NF06 de l'UTT.

## Installation

### Prérequis

- Compilateur C (GCC)
- Python 3.X

### Installation

- Cloner le dépôt
```bash
git clone https://github.com/DevNono/NF06-Project.git
```
- Compiler le programme C
```bash
gcc -shared -O2 -o ./python/main.dll -fPIC ./c/main.c
```
- Installer les dépendances Python
```bash
pip install -r python/requirements.txt
```

## Utilisation

- Lancer le programme
```bash
cd python
python main.py
```
