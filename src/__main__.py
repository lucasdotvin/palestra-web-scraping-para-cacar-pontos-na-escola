from helpers import *

ROOT_FOLDER_URL = r'http://docente.ifrn.edu.br/abrahaolopes/2017.1-integrado/2.02401.1v-poo'


def main():
    session = HTMLSession()
    tree = get_content_tree(ROOT_FOLDER_URL, session)
    for item in tree:
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


if __name__ == "__main__":
    main()
