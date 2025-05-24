base_url = 'https://qa-scooter.praktikum-services.ru/api/v1'
api_documentation = 'https://qa-scooter.praktikum-services.ru/docs/'

endpoints = {
    'create_courier': f'{base_url}/courier',
    'login_courier': f'{base_url}/courier/login',
    'delete_courier': f'{base_url}/courier/{{id}}',
    'create_order': f'{base_url}/orders',
    'track_order': f'{base_url}/orders/track',
    'order_accept': f'{base_url}/orders/accept/{{}}'
}