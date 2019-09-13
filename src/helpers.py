import os
from typing import Dict, List

from requests_html import Element, HTMLSession

ITEM_CATEGORY = {
    'contenttype-folder': 'folder',
    'contenttype-file': 'file',
    'contenttype-link': 'link',
    'contenttype-aviso': 'alert',
    'contenttype-document': 'document'
}


def get_item_content_type_class(item_classes: List[str]) -> str:
    """Retorna a classe com a definição do tipo de conteúdo do item.
    
    Arguments:
        item_classes {List[str]} -- Lista de classes.
    
    Returns:
        str -- Classe com a definição do tipo de conteúdo do item.
    """
    for class_ in item_classes:
        if class_.startswith('contenttype'):
            return class_


def get_item_category(content_core_item: Element) -> str:
    """Retorna a categoria adequada do item a partir de suas classes.
    
    Arguments:
        content_core_item {Element} -- Objeto Element do elemento div alvo da função.
    
    Returns:
        str -- Categoria do elemento. Pode ser: folder, file, link, alert ou document.
    """
    item_classes = content_core_item.attrs['class']
    content_type_class = get_item_content_type_class(
        item_classes
    )

    item_category = ITEM_CATEGORY.get(
        content_type_class
    )

    return item_category


def get_item_details(
    content_core_item: Element,
    parent_path: str=''
) -> Dict[str, str]:
    """Obtém os detalhes do item fornecido.
    
    Arguments:
        content_core_item {Element} -- Objeto Element do elemento div do objeto a ser detalhado.
    
    Keyword Arguments:
        parent_path {str} -- Caminho do diretório pai. Quando definido, é adicionado ao caminho do objeto trabalhado pela função. (default: {''})
    
    Returns:
        Dict[str, str] -- Dicionário com detalhes do item.
    """
    item_category = get_item_category(content_core_item)

    item_path = content_core_item.text
    if parent_path:
        item_path = os.path.join(parent_path, item_path)

    item_url = content_core_item.attrs['href']
    item_details = {
        'category': item_category,
        'path': item_path,
        'url': item_url
    }

    return item_details


def get_page_content_items(
    page_html: Element,
    parent_path: str=''
) -> List[Dict[str, str]]:
    """Obtém os itens de uma página (diretório).
    
    Arguments:
        page_html {Element} -- Objeto Element da página.
    
    Keyword Arguments:
        parent_path {str} -- Caminho do diretório superior. Quando definido, é adicionado ao caminho de todos os itens filhos desse diretório. (default: {''})
    
    Returns:
        List[Dict[str, str]] -- Lista de dicionários com detalhes de cada item da página.
    """
    content_core_div = page_html.find(
        'div#content-core',
        first=True
    )

    content_items = content_core_div.find(
        'a'
    )

    detailed_content_items = [
        get_item_details(item, parent_path)
        for item in content_items
    ]

    return detailed_content_items


def get_content_tree(
    inital_url: str,
    session: HTMLSession
) -> List[Dict[str, str]]:
    """Gera uma árvore de diretórios a partir da URL inicial definida.
    
    Arguments:
        inital_url {str} -- URL do diretório no topo da árvore.
        session {HTMLSession} -- Objeto HTMLSession para execução das requisições HTTP.
    
    Returns:
        List[Dict[str, str]] -- Lista de dicionários com detalhes dos itens e sub-itens.
    """

    root_data = session.get(inital_url)
    root_content = get_page_content_items(root_data.html)

    tree = root_content.copy()
    for item in tree:
        if item['category'] == 'folder':
            item_page_data = session.get(item['url'])
            sub_content = get_page_content_items(
                item_page_data.html,
                parent_path=item['path']
            )

            tree.extend(sub_content)

    return tree


def compare_trees(
    base_tree: List[Dict[str, str]],
    target_tree: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """Compara duas árvores de diretórios e retorna as discrepâncias.
    Cada item da árvore-alvo será buscado na árvore-base para comparação.
    Os itens não encontrados são retornados.
    
    Arguments:
        base_tree {List[Dict[str, str]]} -- Árvore base para comparação.
        target_tree {List[Dict[str, str]]} -- Árvore a ser comparada.
    
    Returns:
        List[Dict[str, str]] -- Itens discrepantes entre as duas árvores.
    """
    difference = [
        item
        for item in target_tree
        if item not in base_tree
    ]

    return difference
