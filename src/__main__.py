import json

from requests_html import HTMLSession

from helpers import compare_trees, get_content_tree

MAIN_URL = r'http://docente.ifrn.edu.br/abrahaolopes/2017.1-integrado/2.02401.1v-poo'


def main():
    session = HTMLSession()
    current_tree = get_content_tree(MAIN_URL, session)
    with open('storage/tree.json', 'r') as stored_tree_file:
        stored_tree = json.load(stored_tree_file)

    difference = compare_trees(
        stored_tree,
        current_tree
    )

    if difference:
        for item in difference:
            category = item['category'].upper()
            category = category.rjust(8)

            path = item['path']
            url = item['url']

            print(
                f'{category} | {path}'
            )

            print(
                f'{url}\n'
            )

        with open('storage/tree.json', 'w') as stored_tree_file:
            stored_tree_file.write(
                json.dumps(current_tree)
            )

if __name__ == "__main__":
    main()
