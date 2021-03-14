from binance.client import Client

import config
import time
from datetime import datetime
import csv


client = Client(config.api_key, config.api_secret)
print('logged in')


def write_to_file(data):
    with open('status_and_orders_btcusdt.txt', 'a+') as file:
        write = csv.writer(file)
        write.writerow(data)


def get_online_data_binance():
    cnt = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    sum_prices = 0
    
    candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_5MINUTE, limit=10)
    for i in candles:
        cnt += 1
        close = i[4]
        sum_prices += float(close)

        if cnt == 9:
            mov_avg = (sum_prices/9)
            close_price = i[4]
        if cnt % 10 == 0:
            cnt = 0
            sum_prices = 0

            return (close_price, mov_avg)


def close_position(side, open_posit):    # -> bool:
    '''
    Returns true iff closed a position
    '''
    close, mov_avg = get_online_data_binance()
    open_posit = float(open_posit)
    price = float(close)
    mov_avg = float(mov_avg)

    if side == 'short' and price <= mov_avg:    # close short
        result_short = open_posit - price
        status_closed_short = f'closed short position: {result_short}'
        write_to_file(status_closed_short)
        print(status_closed_short)
        return True
    elif side == 'long' and price >= mov_avg:    # close long  
        result_long = price - open_posit
        status_closed_long = f'closed buy position: {result_long}'
        write_to_file(status_closed_long)
        print(status_closed_long)
        return True
    else:
        date_time = datetime.now()
        status_closed_position = f'not closed position, date-time: {str(date_time)}, close price: {price}, moving average {mov_avg}'
        write_to_file(status_closed_position)
        print(status_closed_position)
        return False


def open_position(price, ma):
    price = float(price)
    ma = float(ma)
    one_percent = price / 100

    if price > ma + one_percent:    # 2. Если цена выше МА на 1% мы продаем 1 ВТСUSDT
        status_opened_short = f'short sell market: {price}'
        write_to_file(status_opened_short)
        print(status_opened_short)
        return 'short' 
    elif price < ma - one_percent:    # 3. Если цена ниже МА на 1% мы покупаем 1 ВТСUSDT
        status_opened_long = f'buy market: {price}'
        write_to_file(status_opened_long)
        print(status_opened_long)
        return 'long'


def main():
    while True:
        close, mov_avg = get_online_data_binance() 
        date_time = datetime.now()
        write_to_file(str(date_time))
        print(date_time)

        price_mov_avg = f'close price: {close}, moving average: {mov_avg}'
        write_to_file(price_mov_avg)
        print(price_mov_avg)
        
        if open_position(close, mov_avg) == 'long':
            check_price = close
            side = 'long'
            while True: 
                if close_position(side, check_price):
                    break
                time.sleep(300)

        elif open_position(close, mov_avg) == 'short':
            check_price = close
            side = 'short'
            while True:
                if close_position(side, check_price):
                    break
                time.sleep(300)

        else:
            status_no_position = 'no conditions for opening position'
            write_to_file(status_no_position)
            print('no conditions for opening position')
        
        time.sleep(300)


if __name__ == '__main__':
    main()

