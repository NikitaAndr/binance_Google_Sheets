import requests
from googlee import Table


def main():
    all_info = requests.get('https://api.binance.com/api/v3/ticker/price').json()[::]
    symbols = requests.get('https://api.binance.com/api/v3/exchangeInfo').json()['symbols'][::]
    sl = {}
    for i in range(len(symbols)):
        sl[symbols[i]['symbol']] = symbols[i]['baseAsset'] + '/' + symbols[i]['quoteAsset']

    ald_all_info = all_info[::]
    for i in range(len(ald_all_info)):
        try:
            symbol = sl[all_info[i]['symbol']]
            all_info[i] = [symbol, all_info[i]['price']]
        except KeyError:
            print(all_info[i]['symbol'])
    table.write_in_table(all_info, f'A1:C{len(ald_all_info)}')


table = Table()
table.new_table()
table.open_table()
while 1:
    main()
