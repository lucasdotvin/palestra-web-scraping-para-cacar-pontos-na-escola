import os

ROOT_FOLDER_URL = r'http://docente.ifrn.edu.br/abrahaolopes/2017.1-integrado/2.02401.1v-poo'

ITEM_CATEGORY_BY_CONTENT_TYPE_CLASS = {
    'contenttype-folder': 'folder',
    'contenttype-file': 'file',
    'contenttype-link': 'link',
    'contenttype-aviso': 'alert',
    'contenttype-document': 'document'
}


def get_item_content_type_class(item_classes):
    for class_ in item_classes:
        if class_.startswith('contenttype'):
            return class_


def get_item_category(content_core_item):
    item_classes = content_core_item.attrs['class']
    content_type_class = get_item_content_type_class(
        item_classes
    )

    item_category = ITEM_CATEGORY_BY_CONTENT_TYPE_CLASS.get(
        content_type_class
    )

    return item_category


def get_item_details(content_core_item, parent_path=''):
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


def get_page_content_items(page_html, parent_path=''):
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


def get_content_tree(session):
    root_data = session.get(ROOT_FOLDER_URL)
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
