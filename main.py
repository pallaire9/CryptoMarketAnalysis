import matplotlib
import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from pandas.plotting import scatter_matrix
from datetime import date
from apiPull import getCoins
import seaborn as sns
import boto3
import squarify



#
getCoins()


#Stats for Yahoo Finance
currency = "USD"
metric = "Close"

#Ethereum Google Trend
#ethTrend = pd.read_csv("ethGoogleTrend.csv")

start = datetime.datetime(2017,1,1)
end = date.today()

#These are the tickers you will use
cryptoNames = ['BTC','ADA','ETH','XRP','DOGE']

#,'LINK','DOGE','XRP'


#Create A dictionary of each cryptos historical dataframe
coinFrames = {}
indexCount = 0
#Uses python web data reader to pull data from yahoo finance
for coin in cryptoNames:
    coinFrames[cryptoNames[indexCount]] = web.DataReader(f'{cryptoNames[indexCount]}-{currency}',"yahoo",start,end)
    indexCount = indexCount + 1



#Save the daily crypto data to a variable, got from API PULl
dailyCryptData = pd.read_csv('cryptoData.csv')

#Number Of Coins from daily crypto pulls
numCoins = 300


coinTop5MarketCap = dailyCryptData.nlargest(5, 'quote.USD.market_cap')
coin24HourMovers = dailyCryptData.nlargest(numCoins, 'quote.USD.percent_change_24h')
coinVolume10 = dailyCryptData.nlargest(10, 'quote.USD.volume_24h')
coin30dMovers = dailyCryptData.nlargest(numCoins, 'quote.USD.percent_change_30d')


# Gets the amount of money moved in the day and creates new column in dataframe
def getTotalTradedUSD():
    indexCount = 0
    for coin in coinFrames:
        coinFrames[cryptoNames[indexCount]]['TotalTraded']= coinFrames[cryptoNames[indexCount]]['Open'] * coinFrames[cryptoNames[indexCount]]['Volume']
        indexCount += 1



# This gets the percentage Change on the day and creates a new column in dataframe
def getDailyReturns():

    indexCount = 0
    for coin in coinFrames:
        coinFrames[cryptoNames[indexCount]]['returns'] = (coinFrames[cryptoNames[indexCount]]['Close']/coinFrames[cryptoNames[indexCount]]['Close'].shift(1))-1
        indexCount += 1


#Plots Price, Line chart of each crypto
def plotPriceCorr():
    indexCount = 0
    for coin in coinFrames:
        coinFrames[cryptoNames[indexCount]]['Open'].plot(label = cryptoNames[indexCount], figsize = (15,7))
        indexCount += 1

    plt.legend()
    plt.grid()
    plt.yscale('log')
    plt.savefig('CryptoPriceCorr.png')
    plt.title('Cryptocurrency Price')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.show()

    s3 = boto3.resource('s3',
                        aws_access_key_id=,
                        aws_secret_access_key=)
'3w4UU
    s3.meta.client.upload_file('CryptoPriceCorr.png', 'crypttrack-daily', 'CryptoPriceCorr.png',
                               ExtraArgs={'ACL': 'public-read'})




#Volatility Histogram

def getVolatilityHisto():
    indexCount = 0
    for coin in coinFrames:
        coinFrames[cryptoNames[indexCount]]['returns'].hist(bins=100,label = cryptoNames[indexCount], alpha = .5, figsize = (13,6))
        indexCount += 1


    plt.title('CryptoCurrency Volatility Comparison')
    plt.xlabel('Percentage Change')
    plt.ylabel('Total Occurences')
    plt.legend()
    plt.savefig('VolatilityHistogram.png')
    plt.show()

    s3.meta.client.upload_file('VolatilityHistogram.png', 'crypttrack-daily', 'VolatilityHistogram.png',
                               ExtraArgs={'ACL': 'public-read'})

#Smoothed Volatility Levels
def getsmoothVolatility():

    indexCount = 0
    for coin in coinFrames:
        coinFrames[cryptoNames[indexCount]]['returns'].plot(kind='kde', label=cryptoNames[indexCount], figsize = (15,6))
        indexCount += 1


    plt.xlabel = 'Kernel Density'
    plt.title('CryptoCurrency Volatility Comparison SNP500')
    plt.savefig('VolatilityDensity.png')
    plt.legend()
    plt.show()


#
# def getVolatility():


def get_pie_top5():
#Top 5 Pie Chart
    plt.pie(coinTop5MarketCap['quote.USD.market_cap_dominance'],
                          labels=coinTop5MarketCap.name,explode=(0.1,0,0,0,0),
                        autopct='%1.1f%%',shadow=True)
    plt.title('Coin Market Capital Dominance')
    plt.savefig('TopFiveMarketCap.png')
    plt.show()


def revisedDaily():
    numcoins=15
    coinVolume= dailyCryptData.nlargest(numcoins, 'quote.USD.volume_24h')


    plt.style.use('fivethirtyeight')

    plt.clf()
    #plt.figure(figsize=(14,8))
    #plt.subplot(2, 2, 1)
    plt.barh(coinVolume['name'],coinVolume['quote.USD.volume_24h'])
    plt.xscale('log')
    plt.title('Todays Volume')
    plt.xlabel('Volume (USD)')
    plt.savefig('daily1.png')
    plt.show()



    plt.clf()
    #plt.subplot(2, 2, 4)
    hbars = plt.barh(coinVolume['name'],coinVolume['quote.USD.price'])
    plt.xscale('log')
    plt.title('Todays Price')
    plt.xlabel('Price (USD)')
    plt.bar_label(hbars,list(round(coinVolume['quote.USD.price'],0)))
    plt.tight_layout()
    plt.savefig('daily2.png')
    plt.show()



    plt.clf()
    #plt.subplot(2, 2, 3)
    plt.pie(coinTop5MarketCap['quote.USD.market_cap_dominance'],
            labels=coinTop5MarketCap.name, explode=(0.1, 0, 0, 0, 0),
            autopct='%1.1f%%', shadow=True)
    plt.title('Coin Market Capital Dominance')
    plt.savefig('daily3.png')
    plt.show()



    plt.clf()
    #plt.subplot(2, 2, 2)
    plt.barh(coinVolume['name'], coinVolume['quote.USD.volume_change_24h'])
    plt.title('Volume Percentage Change')
    plt.xlabel('Percentage of Market Cap')
    plt.subplots_adjust(bottom =.1)
    plt.tight_layout()
    plt.savefig("daily4.png")
    plt.show()



    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAZFG4R33ZQZTKGD3P',
                        aws_secret_access_key='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')

    s3.meta.client.upload_file('daily1.png', 'crypttrack-daily', 'daily1.png',
                               ExtraArgs={'ACL': 'public-read'})

    s3.meta.client.upload_file('daily2.png', 'crypttrack-daily','daily2.png',
                               ExtraArgs={'ACL': 'public-read'})

    s3.meta.client.upload_file('daily3.png', 'crypttrack-daily', 'daily3.png',
                               ExtraArgs={'ACL': 'public-read'})

    s3.meta.client.upload_file('daily4.png', 'crypttrack-daily', 'daily4.png',
                           ExtraArgs={'ACL': 'public-read'})


def getmoverScatter():

    sns.set_style("whitegrid")
    ax = sns.scatterplot(data=coin24HourMovers, x ='quote.USD.price', y='quote.USD.percent_change_24h',
                     sizes=(20, 300))
    ax.set_xscale('log')
    # ax.set_yscale('log')



    #Create Plot Point Labels

    # plt.scatter(coinPrice, coin24HChange,
    #             coin24HourMovers['quote.USD.volume_24h']/1000000,
    #             alpha=.5,c = coin24HVolume)

    plt.title('CryptoCurrency 24Hour Price Movers', fontweight='bold', pad='25')
    plt.xlabel("Coin Price", labelpad=10, fontweight='bold')
    plt.ylabel("Coin Percentage Change", labelpad=10, fontweight='bold')
    plt.tight_layout()



    plt.savefig("dailyMoversScatter.png")
    plt.show()

    s3.meta.client.upload_file('dailyMoversScatter.png','crypttrack-daily','dailyMoversScatter.png', ExtraArgs={'ACL':'public-read'})


def getPriceMA():

 plt.style.use('classic')
 #plt.subplot(2,1,1)
 coinFrames['ETH']['Open'].plot(label = 'Ethereum Price', figsize = (20,12))
 coinFrames['ETH']['MA50'] = coinFrames['ETH']['Open'].rolling(50).mean()
 coinFrames['ETH']['MA200'] = coinFrames['ETH']['Open'].rolling(200).mean()
 coinFrames['ETH']['MA50'].plot(label='MovingAverage50')
 coinFrames['ETH']['MA200'].plot(label='MovingAverage200')
 plt.title('Ethereum Price')
 plt.legend(loc = 'upper left')
 plt.grid()
 plt.ylabel('Price')
 plt.savefig('ethPrice.png')
 plt.clf()


 # plt.subplot(3,1,2)
 coinFrames['BTC']['Open'].plot(label =  'Bitcoin Price', figsize = (20,12))
 coinFrames['BTC']['MA50'] = coinFrames['BTC']['Open'].rolling(50).mean()
 coinFrames['BTC']['MA200'] = coinFrames['BTC']['Open'].rolling(200).mean()
 coinFrames['BTC']['MA50'].plot(label='MovingAverage50')
 coinFrames['BTC']['MA200'].plot(label='MovingAverage200')
 plt.title('Bitcoin Price')
 plt.legend(loc = 'upper left')
 plt.grid()
 plt.ylabel('Price')
 plt.savefig('BTCPrice.png')
 plt.clf()


 # plt.subplot(3,1,3)
 coinFrames['ADA']['Open'].plot(label =  'Cardano Price', figsize = (20,12))
 coinFrames['ADA']['MA50'] = coinFrames['ADA']['Open'].rolling(50).mean()
 coinFrames['ADA']['MA200'] = coinFrames['ADA']['Open'].rolling(200).mean()
 coinFrames['ADA']['MA50'].plot(label='MovingAverage50')
 coinFrames['ADA']['MA200'].plot(label='MovingAverage200')
 plt.title('Cardano Price')
 plt.legend(loc = 'upper left')
 plt.grid()
 plt.ylabel('Price')
 plt.savefig('ADAPrice.png')
 plt.clf()


 s3 = boto3.resource('s3',
                        aws_access_key_id ='AKIAZFG4R33ZQZTKGD3P',
                        aws_secret_access_key ='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')
 s3.meta.client.upload_file('ethPrice.png','crypttrack-daily','ethPrice.png', ExtraArgs={'ACL':'public-read'})
 s3.meta.client.upload_file('BTCPrice.png','crypttrack-daily','BTCPrice.png.png', ExtraArgs={'ACL':'public-read'})
 s3.meta.client.upload_file('ADAPrice.png','crypttrack-daily','ADAPrice.png.png', ExtraArgs={'ACL':'public-read'})




def treeMap():
    coinTop10MarketCap = dailyCryptData.nlargest(10, 'quote.USD.market_cap')


    colors = ['#2E7F18', '#45731E', '#675E24', '#8D472B', '#B13433', '#C82538']
    sizes = coinTop10MarketCap['quote.USD.market_cap']
    labels = coinTop10MarketCap['name']
    values = coinTop10MarketCap['quote.USD.percent_change_24h']
    valuesFormat = ["%.2f" % value for value in values]

    squarify.plot(value = valuesFormat, sizes=sizes, label = labels, alpha =0.6,color=colors,pad = True).set(title = 'CryptoCurrency Movements')
    plt.axis('off')
    plt.savefig('priceChange.png')
    plt.show()
    plt.clf()

    s3.meta.client.upload_file('priceChange.png', 'crypttrack-daily', 'priceChange.png', ExtraArgs={'ACL': 'public-read'})

#
# #plotPrice()
# getDailyReturns()
# #getVolatilityHisto()
# #getsmoothVolatility()

s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAZFG4R33ZQZTKGD3P',
                        aws_secret_access_key='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')


getDailyReturns()
getTotalTradedUSD()
getVolatilityHisto()
plotPriceCorr()
#getDailyUpdate()
getPriceMA()
revisedDaily()
# volatilityBox()
treeMap()
getmoverScatter()


# ADD STACKED AVERAGE ON VOLUME BAR CHART
