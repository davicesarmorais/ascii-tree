#!/usr/bin/env python3
usage = f""" 
Usage:

atree -d <dir_path> (Faz o texto com base em um diretorio)
atree -g <github_repo> -b <branch> (Faz o texto com base em um repositorio do github)

Obs: -d Lê o arquivo .gitignore automaticamente e não inclui esses itens
"""

import sys
from utils import *

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print(usage)
        return
   
    flag = sys.argv[1]
    arg = sys.argv[2]

    if flag == '-d':
        basedir = get_basedir(arg)
        tree = generate_tree(percorrer_diretorio(arg), basedir)
        with open('out.txt', 'w', encoding='utf-8') as f:
            f.write(tree)
            print("Árvore criada com sucesso em out.txt")
    
    elif flag == '-g':
        repo = get_repo(arg)
        if len(sys.argv) == 5 and sys.argv[3] == '-b':
            url = format_url(arg, sys.argv[4])
        else:
            url = format_url(arg)
        
        data = request(url)
        tree = generate_tree(data['tree'], repo) 
        with open('out.txt', 'w', encoding='utf-8') as f:
            f.write(tree)
            print("Árvore criada com sucesso em out.txt")
    
    else:
        print(usage)


if __name__ == "__main__":
    main()