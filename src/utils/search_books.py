import requests


def get_cleaned_books_list(request_url, params):
    response = requests.get(request_url, params)

    if response.status_code == 200:
        books_data = response.json()['docs']

        return books_data

    else:
        return response.status_code
