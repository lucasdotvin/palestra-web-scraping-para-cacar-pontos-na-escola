from requests_html import HTMLSession

from helpers import *


def main():
    session = HTMLSession()
    tree = get_content_tree(session)
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