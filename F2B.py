from FtxClient import FtxClient
import json
import sys
from binance.client import Client
import time
import math


print("--------------------------------------------------------------------")
print("FTX to Binance v0.2")
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
ftx_withdrawal_password = data['ftx-withdrawal-password']


ftx = FtxClient(apiKey, apiSecret, subAccount)
coin = 'BUSD'
ftx.withdrawals(coin, sys.argv[1], binance_busd_bsc_address,None, 'bsc', ftx_withdrawal_password, None)

print("[FTX] Sending "+ sys.argv[1] + " BUSD now")
print ("Waiting...")
time_start = time.time()


binance = Client(BapiKey,BapiSecret)
while True:
    balance = binance.get_asset_balance('BUSD')
    if float(balance['free']) != 0:
        print(f"[Binance]現貨帳戶收到 {balance['free']} BUSD")
        time_end = time.time()
        time_c= time_end - time_start 
        print(f"[Time Cost] {math.floor(time_c/60)}m:{math.floor(time_c%60)}s")
        break
    time.sleep(1)
    second = math.floor(time.time()-time_start)
    print(f"[Time Cost] {math.floor(second/60)}m:{second%60}s         ", end = '\r')


transfer_status = binance.make_universal_transfer(type='MAIN_UMFUTURE', asset='BUSD', amount=balance['free'])
#print(transfer_status)
print(f"[Binance] U本位帳戶收到BUSD")