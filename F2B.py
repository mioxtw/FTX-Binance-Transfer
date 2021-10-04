from FtxClient import FtxClient
import json
import sys
from binance.client import Client
import time
import math


print("--------------------------------------------------------------------")
print("FTX to Binance v0.3")
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
size = sys.argv[1]
withdraw_status = ftx.withdrawals(coin, size, binance_busd_bsc_address,None, 'bsc', ftx_withdrawal_password, None)

print("[FTX] Sending "+ size + " BUSD now")
print ("Waiting...")
time_start = time.time()

hasRequsted = False
hasTxid = False
while True:
    for i in ftx.get_withdrawals_history():
        if (i['id'] == withdraw_status['id'] and hasRequsted == False):
            print(f"[FTX] status: {i['status']}")
            hasRequsted = True
        if (i['id'] == withdraw_status['id'] and i['txid'] != None):
            txid = i['txid']
            print(f"[FTX] status: {i['status']}  txid:{i['txid']}") 
            hasTxid = True
            break;
    if(hasTxid):
        break
    time.sleep(1);
    print(f"[Time Cost] {math.floor(math.floor(time.time()-time_start)/60)}m:{math.floor(time.time()-time_start)%60}s         ", end = '\r')


binance = Client(BapiKey,BapiSecret)
hasTxid = False
hasSuccess = False
while True:
    deposit_history = binance.get_deposit_history()
    for i in deposit_history:
        if i['txId'] == txid and hasTxid == False:
            print(f"[Binance] Get Txid:{txid}")
            hasTxid = True
        if i['txId'] == txid and i['status'] == 1:
            print(f"[Binance] Status: BUSD確認完成，現貨帳戶收到 {i['amount']} BUSD")
            hasSuccess = True
            break
    if (hasSuccess):
        break
    time.sleep(1)
    print(f"[Time Cost] {math.floor(math.floor(time.time()-time_start)/60)}m:{math.floor(time.time()-time_start)%60}s         ", end = '\r')

transfer_status = binance.make_universal_transfer(type='MAIN_UMFUTURE', asset='BUSD', amount=size)
#print(transfer_status)
print(f"[Binance] U本位帳戶收到 {size} BUSD")
print(f"[Time Cost] {math.floor((time.time() - time_start) /60)}m:{math.floor((time.time() - time_start) %60)}s")