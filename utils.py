#!/usr/bin/env python3
import urllib.request
from urllib.error import HTTPError
import json
from pathlib import Path
import os
import fnmatch



def get_repo(url: str) -> str:
    url = url.replace("github.com/", "") \
             .replace("https://", "") \
             .replace("http://", "") \
             .replace(".git", "")
    try:
        repo = url.split("/")[1]
    except IndexError:
        return ""
    
    return repo


def get_basedir(path: str) -> str:
    basedir = Path(path)
    basedir = basedir.absolute()
    basedir = basedir.as_posix()
    basedir = basedir.split("/")[-1]
    return basedir


def format_url(url: str, branch: str = "main") -> str:
    base_url = r"https://api.github.com/repos/{owner}/{repo}/git/trees/refs/heads/{branch}?recursive=1"
    url = url.replace("github.com/", "") \
             .replace("https://", "") \
             .replace("http://", "") \
             .replace(".git", "")
    try:
        owner = url.split("/")[0]
        repo = url.split("/")[1]
    except IndexError:
        print("Invalid URL")
        exit()
        
    
    url = base_url.replace(r"{owner}", owner) \
                  .replace(r"{repo}", repo) \
                  .replace(r"{branch}", branch)
    return url


def request(url: str) -> dict:
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            data = json.loads(data)
            return data
    except (ValueError, HTTPError) as e:
        print(e)
        exit()
    
    
def __tree_str(tree: list, current: dict, indent: str = "") -> str:
    node_str = f"{indent}├── {current['path'].split('/')[-1]}{'/' if current['type'] == 'tree' else ''}\n"

    if current["type"] == 'blob':
        return node_str
    
    if current['type'] == 'tree':
        child_indent = indent + "│   "
        child_str = ""
        last = ""
        for item in tree:
            if len(item["path"].split("/")) == len(current["path"].split("/")) + 1 and item["path"].startswith(current["path"]):
                if last:
                    child_str += last
                last = __tree_str(tree, item, child_indent)
                
        child_str += last.replace("├── ", "└── ")
        node_str += child_str

        
    return node_str

    
def generate_tree(data: list, base_dir: str) -> str:
    data.sort(key=lambda x: x["type"], reverse=True)

    folders = [x for x in data if x['type'] == 'tree' and "/" not in x['path']]
    root_files = [x for x in data if x['type'] == 'blob' and "/" not in x['path']]
    
    tree = f"{base_dir}/\n" 
    
    for item in folders:
        tree += __tree_str(data, item)
    for idx, item in enumerate(root_files):
        if idx + 1 == len(root_files):
            tree += f"└── {item['path'].split('/')[-1]}{'/' if item['type'] == 'tree' else ''}\n"
        else:
            tree += __tree_str(data, item)
    return tree


def load_gitignore(root):
    patterns = []
    gitignore_path = os.path.join(root, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                patterns.append(line)
    return patterns


def ignore(rel_path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(rel_path), pattern):
            return True
    return False


def percorrer_diretorio(raiz, threshold=1000):
    gitignore_patterns = load_gitignore(raiz)
    ignorar_dirs = {".git", "node_modules", "venv", ".venv"}

    itens = [] 

    for caminho_atual, dirs, files in os.walk(raiz, topdown=True):
        rel_dir = os.path.relpath(caminho_atual, raiz).replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""
            
        if rel_dir and not ignore(rel_dir, gitignore_patterns):
            itens.append({'path': rel_dir, 'type': 'tree'})
        
        novas_dirs = []
        for d in dirs:
            full_dir = os.path.join(caminho_atual, d)
            rel_subdir = os.path.relpath(full_dir, raiz).replace("\\", "/")
            if d in ignorar_dirs:
                continue
            if ignore(rel_subdir, gitignore_patterns):
                continue
            try:
                if len(os.listdir(full_dir)) > threshold:
                    itens.append({'path': rel_subdir, 'type': 'tree'})
                    continue
            except Exception:
                continue
            novas_dirs.append(d)
        dirs[:] = novas_dirs

        for arquivo in files:
            full_arquivo = os.path.join(caminho_atual, arquivo)
            rel_arquivo = os.path.relpath(full_arquivo, raiz).replace("\\", "/")
            if ignore(rel_arquivo, gitignore_patterns):
                continue
            itens.append({'path': rel_arquivo, 'type': 'blob'})

    return itens
