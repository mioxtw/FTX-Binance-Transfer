from FtxClient import FtxClient
import json
import sys
from binance.client import Client
import time
import math


print("--------------------------------------------------------------------")
print("Binance to Ftx v0.6")
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
print ("Waiting...")
time_start = time.time()

time.sleep(1)

while True:
    balance = binance.get_asset_balance('BUSD')
    if float(balance['free']) != 0:
        timestamp = time.time()
        withdraw_status = binance.withdraw(coin='BUSD',network='BSC', address=ftx_busd_bsc_address, amount=size, withdrawOrderId=timestamp)
        time.sleep(1)

        finished2 = False
        while True:
            w_history = binance.get_withdraw_history(withdrawOrderId=timestamp, status=2)
            for i in w_history:
                if (i['status'] == 2):
                    print(f"[Binance] 等待確認")
                    finished2 = True
                    break;
            if (finished2):
                break;
            time.sleep(1)
            print(f"[Time Cost] {math.floor(math.floor(time.time()-time_start)/60)}m:{math.floor(time.time()-time_start)%60}s         ", end = '\r')

        finished4 = False
        while True:
            w_history = binance.get_withdraw_history(withdrawOrderId=timestamp, status=4)
            for i in w_history:
                if (i['status'] == 4 and 'txId' in i):
                    txid = i['txId']
                    print(f"[Binance] 處理中 txid:{txid}")
                    finished4 = True
                    break;
            if (finished4):
                break;
            time.sleep(1)
            print(f"[Time Cost] {math.floor(math.floor(time.time()-time_start)/60)}m:{math.floor(time.time()-time_start)%60}s         ", end = '\r')
        


#        finished6 = False
#        while True:
#            w_history = binance.get_withdraw_history(withdrawOrderId=timestamp, status=6)
#            for i in w_history:
#                if (i['status'] == 6):
#                    print(f"[Binance] 提現完成 txid:{i['txId']}")
#                    finished6 = True
#                    break;
#            if (finished6):
#                break;
#            time.sleep(1)






        print(f"[Binance] Sending {size} BUSD now")
        break;
    time.sleep(1)
    print(f"[Time Cost] {math.floor(math.floor(time.time()-time_start)/60)}m:{math.floor(time.time()-time_start)%60}s         ", end = '\r')



ftx = FtxClient(apiKey, apiSecret, subAccount)
finished = False
getTxid = False
while True:
    deposit = ftx.get_deposits_history()
    for i in deposit:
        if(i['coin'] == 'BUSD' and  'txid' in i and i['txid'] == txid):
            if (getTxid == False):
                print(f"[FTX] Get txid: {txid} status:{i['status']}")
                getTxid = True
        if (i['coin'] == 'BUSD' and  'txid' in i and i['txid'] == txid and i['status'] == 'confirmed'):
            print(f"[FTX] Get txid: {txid} status:{i['status']}")
            finished = True
            break;
    if (finished):   
        break;
    time.sleep(1)
    print(f"[Time Cost] {math.floor(math.floor(time.time()-time_start)/60)}m:{math.floor(time.time()-time_start)%60}s         ", end = '\r')
print(f"[Time Cost] {math.floor((time.time() - time_start) /60)}m:{math.floor((time.time() - time_start) %60)}s")