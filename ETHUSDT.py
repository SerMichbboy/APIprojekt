import time
import requests


# data from the free API service(couple ETH/USDT)
url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD'
headers = {'X-CoinAPI-Key': '15EF9C78-69E5-4458-BF3B-D2972E5FEE56'}
response = requests.get(url, headers=headers).json()

# adding an initial price
start_price = response['rate']
print(start_price)

# creating list, that include values of dates
list_of_value = []


# creating a list len < 60
def add_to_list(vle, rfshtime):
    if len(list_of_value) >= 60 // rfshtime:
        list_of_value.pop(0)
    list_of_value.append(vle)


# creating the function calculating the price change
def calc_price(old_prices, now_price):
    for i in range(len(old_prices)):
        if (abs(now_price - old_prices[i]) / old_prices[i] * 100) > 1:
            return True


refresh_time = int(input('частота обновления данных(сек): '))
check_count = 0

# start an infinity cycle of checking incoming data
while True:
    check_count += 1
    new_price = requests.get(url, headers=headers).json()
    print(new_price['rate'])

    # creating a condition if the price change in the last hour is more than 1% - we display a message:
    if calc_price(list_of_value, new_price['rate']):
        print('Цена ETH/USDT изменилась на 1% за последние 60 минут')
    elif check_count >= 60 / refresh_time:
        add_to_list(new_price, refresh_time)
        check_count = 0

    # frequency of data output
    time.sleep(refresh_time)
