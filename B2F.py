from FtxClient import FtxClient
import json
import sys
from binance.client import Client
import time
import math


print("--------------------------------------------------------------------")
print("Binance to Ftx v0.3")
print("--------------------------------------------------------------------")
print("")
print("")

with open('config.json', 'r') as json_file:
    data = json.load(json_file)

subAccount = data["ftx-subaccount"]
apiKey = data["ftx-api-key"]
apiSecret = data["ftx-api-secret"]
BapiKey = data["binance-api-key"]
BapiSecret = data["binance-api-secret"]
ftx_busd_bsc_address = data['ftx-busd-bsc-address']
binance_busd_bsc_address = data['binance-busd-bsc-address']


size = float(sys.argv[1])


if size < 10:
    print(f"幣安提現BUSD最小數量為10")
    sys.exit()

binance = Client(BapiKey,BapiSecret)
transfer_status = binance.make_universal_transfer(type='UMFUTURE_MAIN', asset='BUSD', amount=size)
#print(transfer_status)
print(f"[Binance] U本位帳戶劃轉 {size} BUSD 到現貨帳戶")

time.sleep(1)

while True:
    balance = binance.get_asset_balance('BUSD')
    if float(balance['free']) != 0:
        binance.withdraw(coin='BUSD',network='BSC', address=ftx_busd_bsc_address, amount=size)
        print(f"[Binance] Sending {size} BUSD now")
        break;
    time.sleep(1)


