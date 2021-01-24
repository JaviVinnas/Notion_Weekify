from datetime import date
from notion.client import NotionClient


def main():
    year = int(input('Introduce el año -> '))
    weeknumb = int(input('Introduce el número de semana -> '))

    dias = []
    for i in range(7):
        dias.append(date.fromisocalendar(year, weeknumb, i + 1))
    print(dias)


if __name__ == '__main__':
    # creamos la sesión de notion
    client = NotionClient(
        token_v2="010ff674c490e963913b565148ed697edfe8dfb95846b1abb0d2c7dcdbb11dd7245aac4b86ade9001d45a89f5e08bce0c01daf2cabaef4349df6c6bd2c1884069e7714cc8020247ed94eb49af1e7")
    # obtenemos la tabla maestra
    cv = client.get_collection_view(
        "https://www.notion.so/4a1954c0edca41ed91cb2f1b647b0567?v=273b5898c4944737b3a6c2a96d36a295")
    # preparamos consulta
    result = cv.build_query().execute()
    for row in result:
        print( "('{0}','{1}');".format(row.id, row.title))