import requests


# Токен и URL API
token = '<pypi-AgEIcHlwaS5vcmcCJDczNmI1NGU1LTYzOTAtNDdkNy1iNzhhLTg0YTQxZWFhNjA2MQACKlszLCI5OWUxZjJkMS00Zjc3LTQ1ODEtYmFiOC1iNzg3NDgxNTgwNGUiXQAABiBMBEswSRemQanp6BPaua5qTLVRJyTwvr5Z10hQtrFPOw>'
url = 'https://pypi.org/pypi/mypackageVeroKulak/json'

# Заголовки с токеном
headers = {
    'Authorization': f'Bearer {token}',
}

# Выполнение запроса
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())  # Обработка данных
else:
    print(f'Ошибка: {response.status_code}')