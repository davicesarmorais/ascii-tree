# Ascii-Tree

Este projeto é uma ferramenta de linha de comando que **converte a estrutura de diretórios** (por exemplo, de um **repositório GitHub** ou de um **diretório local**) em uma representação visual em **formato de árvore** utilizando caracteres ASCII. Ele percorre recursivamente os diretórios e arquivos, gerando uma saída hierárquica com marcadores como `├──` e `└──` para indicar os diferentes níveis e ramificações da estrutura.

## Funcionalidades
- **Recuperação Recursiva:** Navega por todos os níveis da estrutura de diretórios, identificando pastas e arquivos.
- **Formatação em Árvore:** Gera uma visualização em árvore com a hierarquia dos arquivos e pastas, similar ao comando tree do Unix.
- **Integração com GitHub:** Pode ser utilizado para converter a árvore de um repositório GitHub (obtida via API) em um formato textual legível.

## Exemplos de Uso

**Ao fornecer o caminho do diretorio como entrada, gera uma saída como:**

```
ascii-tree/
├── .gitignore
├── main.py
├── README.md
└── utils.py
```
---
## Como Usar (Recomendado)

1. **Clone o repositório:** <br>
`git clone https://github.com/davicesarmorais/ascii-tree.git`

2. **Colocar no path:** <br>
    **Linux:**
    1. `chmod +x ascii-tree/*.py`
    2. `sudo cp ascii-tree/*.py /usr/local/bin`
    
    ---

    **Windows:**
    1. Crie um arquivo com o nome atree.bat em qualquer lugar do seu computador
    2. Edite ele e coloque isso:
        ```
        @echo off
        python caminho_onde_clonou_o_projeto\ascii-tree\main.py %*
        ```
        *Ex:* 
        ```
        @echo off
        python C:\Users\davic\code\ascii-tree\main.py %*
        ```
    3. Coloque o caminho do atree.bat no path do windows:
        ```
        setx PATH "$env:PATH;C:\caminho\do\diretorio" /M
        ```
        *(OBS): Coloque até a pasta onde ele está. <br>
        **Não** coloque assim: `C:\Users\davic\Documentos\projetos\atree.bat`.<br> 
        **Coloque assim:** `C:\Users\davic\Documentos\projetos`* 

3. **Rodar:**
    - **Linux:**
        - `atree.py {parametros}`
    - **Windows:**
        - `atree {parametros}`

## Parâmetros
```
atree -d <dir_path> [Faz o texto com base em um diretorio]
atree -g <github_repo> -b <branch> (opcional) [Faz o texto com base em um repositorio do github]

Obs: -d Lê o arquivo .gitignore automaticamente e não inclui esses itens
```
