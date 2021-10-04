from FtxClient import FtxClient
import json
import sys
from binance.client import Client
import time
import math

def F2B(size: float):
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
    #size = float(sys.argv[1])
    withdraw_status = ftx.withdrawals(coin, size, binance_busd_bsc_address,None, 'bsc', ftx_withdrawal_password, None)

    print(f"[FTX] Sending {size} BUSD now")
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


def B2F(size: float):
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


    #size = float(sys.argv[1])



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




print("--------------------------------------------------------------------")
print("Auto Balance v0.2")
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
auto_balance_threshold = data['auto-balance-threshold']


#  if  ABS(A-B)/(A+B) = 5%
#  A>B  A to B   size: (A+B)/2 - B
#  B>A  B to A   size: (A+B)/2 - A
binance = Client(BapiKey,BapiSecret)
ftx = FtxClient(apiKey, apiSecret, subAccount)

while True:
    ftxUSD = round(ftx.get_all_usdValue(),8)
    binanceBalance = binance.futures_account_balance()
    for i in binanceBalance:
        if (i['asset']=='BUSD'):
            binanceUSD = round(float(i['balance']) + float(i['crossUnPnl']),8)

    diff = abs(ftxUSD-binanceUSD)/(ftxUSD+binanceUSD)
    TotalBalance = (binanceUSD+ftxUSD)

    t = time.localtime(time.time())
    tt = f"[{t.tm_year}/{t.tm_mon}/{t.tm_mday} {t.tm_hour}:{t.tm_min}]"
    print(f"{tt} Diff: [{round(diff*100,2)} %]  Binance:[{binanceUSD}] FTX:[{ftxUSD}] TotalBalance:[{round(TotalBalance,8)}]")
    if diff > auto_balance_threshold and binanceUSD > ftxUSD:
        B2F(size = round(TotalBalance/2 - ftxUSD,8))
    if diff > auto_balance_threshold and ftxUSD > binanceUSD:
        F2B(size = round(TotalBalance/2 - binanceUSD,8))

    time.sleep(60);
