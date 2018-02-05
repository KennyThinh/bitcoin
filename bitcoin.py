import pandas as pd
import matplotlib.pyplot as plt
import os

""" Plot top 10 biggest gained and 10 biggest lost coins
Left: gain
Right: Lose
"""
def top10_subplot(volatility_series,title):
    fig,axes=plt.subplots(1,2,figsize=(10, 6))# 1 rows, 2 col
    # Top 10 loses
    # volatility_series[:10].plot(ax=axes[0],kind="bar",color="darkred",x="id")
    # ax.set_title("Losers"+title)
    # ax.set_ylabel("% change")
    # ax.set_xlabel("")
    #
    # # Top 10 gain
    # volatility_series[-10:].plot(ax=axes[1],kind="bar",color="darkblue",x="id")
    # ax.set_title("Gainers" + title)
    # ax.set_ylabel("% change")
    # ax.set_xlabel("")
    # plt.show()

    fig, axes = plt.subplots(1, 2, figsize=(10, 6))  # 1 rows, 2 col
    ax = volatility_series[:10].plot.bar(ax=axes[0], facecolor="darkred")
    ax.set_title("Losers"+title)
    ax.set_ylabel("% change")
    ax.set_xlabel("")
    ax = volatility_series[-10:].plot.bar(ax=axes[1], facecolor="darkblue")
    ax.set_title("Gainers" + title)
    ax.set_ylabel("% change")
    ax.set_xlabel("")
    fig.suptitle(title)
    plt.show()





# To load files. dirname can be created by 2 ways:
# 1.
dirname = os.path.dirname(__file__)# Get the path of current script
# 2. dirname=os.path.dirname(os.path.abspath(__file__))

csvfilename = os.path.join(dirname, 'coinmarketcap_06122017.csv')
dec6=pd.read_json(csvfilename)
market_cap_raw = dec6[["id","market_cap_usd"]]
print(market_cap_raw.count())
# Count() has axis=0 as default, means row-wise. This means a row which not contain any NaN will be count.


# Filtering rows with market_cap_usd >0
cap = market_cap_raw.query("market_cap_usd > 0")
print(cap.head())
print(cap.count())

""" Visualize top 10 cryptocurrencies
"""
#Select 10 coins and set index to id
cap10=cap[:10].set_index("id")
# Calculate percentage of market capitalization for each coin by
# creating a new column using assign()
cap10=cap10.assign(market_cap_perc=lambda x: (x.market_cap_usd/cap.market_cap_usd.sum())*100)
# Ploting bar plot using numpy function
ax=cap10["market_cap_perc"].plot.bar()
ax.set_title("Top 10 market capitalization")
ax.set_ylabel("% of total cap")

""" Make plot easier to read and informative: 
1. group coins into group and color
2. change y scale to log
"""
COLORS = ['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver', 'orange', 'red', 'green']
ax1=cap10["market_cap_perc"].plot.bar(color=COLORS,logy=True)
ax1.set_title("Top 10 market capitalization (enhanced)")
ax1.set_ylabel("USD")
ax1.set_xlabel("")

""" Prove that cryptocurrencies is volatility 
"""
volatility=dec6[["id","percent_change_24h","percent_change_7d"]]
# Drop row which contains any NaN
volatility.dropna(axis=0,how="any")
volatility.index=volatility["id"]

""" Plot 10 losers and gainers in 24h
"""
# Sort, now using sort_values, default is ascending
volatility.sort_values(["percent_change_24h"])
print(volatility.head())
top10_subplot(volatility.percent_change_24h, "24h")

"""Plot 10 losers and gainers in weeks
"""
volatility.sort_values(["percent_change_7d"])
print(volatility.head())
top10_subplot(volatility.percent_change_7d,"7d")
