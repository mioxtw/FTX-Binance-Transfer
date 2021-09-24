from FtxClient import FtxClient
import json
import sys
from binance.client import Client
import time
import math


print("--------------------------------------------------------------------")
print("FTX to Binance v0.1")
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


if float(sys.argv[1]) < 10:
    print(f"幣安提現BUSD最小數量為10")
    sys.exit()

binance = Client(BapiKey,BapiSecret)
transfer_status = binance.make_universal_transfer(type='UMFUTURE_MAIN', asset='BUSD', amount=sys.argv[1])
#print(transfer_status)
print(f"[Binance] U本位帳戶劃轉 {sys.argv[1]} BUSD 到現貨帳戶")

while True:
    balance = binance.get_asset_balance('BUSD')
    if float(balance['free']) != 0:
        binance.withdraw(coin='BUSD',network='BSC', address=ftx_busd_bsc_address, amount=sys.argv[1])
        print("[Binance] Sending "+ sys.argv[1] + " BUSD now")
        break;
    time.sleep(1)


