import yfinance
import pandas_datareader
import math
import random
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

def operation1(history, shots):
  yf.pdr_override()
  today = date.today()
  decadeAgo = today - timedelta(days=3652)
  data = pdr.get_data_yahoo('NFLX', start=decadeAgo, end=today) 
  data['Buy']=0
  data['Sell']=0

  # Defining final data variables
  final_data = []

  for i in range(len(data)): 
      # Hammer
      realbody=math.fabs(data.Open[i]-data.Close[i])
      bodyprojection=0.1*math.fabs(data.Close[i]-data.Open[i])

      if data.High[i] >= data.Close[i] and data.High[i]-bodyprojection<= data.Close[i] and data.Close[i] >data.Open[i] and data.Open[i] >data.Low[i] and data.Open[i]-data.Low[i] >realbody:
          data.at[data.index[i], 'Buy'] = 1
          temp_data = {str(i): ["H", data.Open[i], data.High[i], data.Low[i], data.Close[i]]}
          final_data.append(temp_data)
          # print("H", data.Open[i], data.High[i], data.Low[i], data.Close[i])   

      # Inverted Hammer
      if data.High[i] >data.Close[i] and data.High[i]-data.Close[i] >realbody and data.Close[i] >data.Open[i] and data.Open[i] >= data.Low[i] and data.Open[i] <= data.Low[i]+bodyprojection:
          data.at[data.index[i], 'Buy'] = 1
          temp_data = {str(i): ["I", data.Open[i], data.High[i], data.Low[i], data.Close[i]]}
          final_data.append(temp_data)
          # print("I", data.Open[i], data.High[i], data.Low[i], data.Close[i])

      # Hanging Man
      if data.High[i] >= data.Open[i] and data.High[i]-bodyprojection<= data.Open[i] and data.Open[i] >data.Close[i] and data.Close[i] >data.Low[i] and data.Close[i]-data.Low[i] >realbody:
          data.at[data.index[i], 'Sell'] = 1
          temp_data = {str(i): ["M", data.Open[i], data.High[i], data.Low[i], data.Close[i]]}
          final_data.append(temp_data)
          # print("M", data.Open[i], data.High[i], data.Low[i], data.Close[i])

      # Shooting Star
      if data.High[i] >data.Open[i] and data.High[i]-data.Open[i] >realbody and data.Open[i] >data.Close[i] and data.Close[i] >= data.Low[i] and data.Close[i] <= data.Low[i]+bodyprojection:
          data.at[data.index[i], 'Sell'] = 1
          temp_data = {str(i): ["S", data.Open[i], data.High[i], data.Low[i], data.Close[i]]}
          final_data.append(temp_data)
          # print("S", data.Open[i], data.High[i], data.Low[i], data.Close[i])
  minhistory = history
  shots = shots
  final_data_1 = []
  for i in range(minhistory, len(data)): 
      if data.Buy[i]==1: 
          mean=data.Close[i-minhistory:i].pct_change(1).mean()
          std=data.Close[i-minhistory:i].pct_change(1).std()
          simulated=[random.gauss(mean,std) for x in range(shots)]
          simulated.sort(reverse=True)
          var95 = simulated[int(len(simulated)*0.95)]
          var99 = simulated[int(len(simulated)*0.99)]
          final_data_1.append({str(1): [var95, var99]})
          # print(var95, var99)
  return (final_data, final_data_1)

if __name__ == "__main__":
    x, y = operation1()
    print(x)
    print(y)
