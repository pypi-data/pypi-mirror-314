import ccxt
import pandas
import numpy
import ta

def add(a,b) :
    return a+b

def fetch_binance_data(symbol, timeframe, limit=500):
    exchange = ccxt.binance({'options': { 'defaultType': 'future' }})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pandas.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pandas.to_datetime(df['time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    df['HA_Close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    # HA-Open
    for i in range(len(df)):
        if i == 0:
            df['HA_Open'] = (df['open'].iloc[0] + df['close'].iloc[0]) / 2
        else :
            df.loc[i,'HA_Open'] = (df['HA_Open'].iloc[i-1] + df['HA_Close'].iloc[i-1]) / 2
   
    df['HA_Open'] = df['HA_Open'].round(1)

    # HA-High 계산
    df['HA_High'] = df[['high', 'HA_Open', 'HA_Close']].max(axis=1).round(1)

    # HA-Low 계산
    df['HA_Low'] = df[['low', 'HA_Open', 'HA_Close']].min(axis=1).round(1)     

    # rsi
    df['rsi'] = ta.momentum.RSIIndicator(df['HA_Close']).rsi().fillna(0)

    # EMA 200
    df['EMA_200'] = ta.trend.ema_indicator(df['HA_Close'], window=200).fillna(0).round(1)
    
    # 캔들 색
    df['side'] = df.apply(
        lambda row: 'LONG' if row['HA_Close'] > row['HA_Open'] else 'SHORT', axis=1
    )
    
    # 캔들 타입
    df['candle_type'] = numpy.where(
        (df['side'] == 'SHORT') & (df['HA_High'] == df[['HA_Open', 'HA_Close']].max(axis=1)), '1',
        numpy.where(
            (df['side'] == 'LONG') & (df['HA_Low'] == df[['HA_Open', 'HA_Close']].min(axis=1)), '1',
            ''
        )
    )
    
    # stc 
    df['K'] = (ta.momentum.StochRSIIndicator(close=df['HA_Close']).stochrsi_k().fillna(0) * 100).round(2)
    df['D'] = (ta.momentum.StochRSIIndicator(close=df['HA_Close']).stochrsi_d().fillna(0) * 100).round(2)

    return df
