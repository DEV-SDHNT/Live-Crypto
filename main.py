import time
import requests 
import pandas as pd

fileName="cryptoData.xlsx"

def getTop50Crypto():
    url="https://api.coingecko.com/api/v3/coins/markets"
    params={
        "vs_currency":"usd",
        "order":"market_cap_desc",
        "per_page":50,
        "page":1,
        "sparkline":"false"
    }
    response=requests.get(url,params=params)
    data=response.json()

    cryptoList=[]
    for coin in data:
        cryto={
            "Name":coin['name'],
            "Symbol":coin['symbol'].upper(),
            "Current Price (USD)":coin['current_price'],
            "Market Capitalization":coin["market_cap"],
            "24h Trading Volume":coin['total_volume'],
            "24h Price Change (%)":coin["price_change_percentage_24h"],
        }
        cryptoList.append(cryto)
    return pd.DataFrame(cryptoList)

def save(df):
    df.to_excel(fileName,sheet_name="Crypto Data",index=False,engine='openpyxl')
    
while True:
    cryptos=getTop50Crypto()
    save(cryptos)
    print(f"Updated file with {len(cryptos)} cryptos at {pd.Timestamp.now()}")

    # Top 5 cryptos :
    print(f"Top 5 Cryptos :\n {cryptos.head()}")
    # Average Price of top 50 cryptos :
    print(f'Average Price : {cryptos["Current Price (USD)"].mean()}')

    # Highest and Lowest 24hr percentage price
    print("Highest 24hr percentage price among all : \n",cryptos[cryptos["24h Price Change (%)"]==cryptos["24h Price Change (%)"].max()] )
    print("Lowest 24hr percentage price among all : \n",cryptos[cryptos["24h Price Change (%)"]==cryptos["24h Price Change (%)"].min()] )
    
    time.sleep(10)


    
