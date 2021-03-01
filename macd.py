import logging
import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def macd(df, n_fast, n_slow):
    EMAfast = pd.Series(df['close'].ewm(span=n_fast, min_periods=n_slow).mean())
    EMAslow = pd.Series(df['close'].ewm(span=n_slow, min_periods=n_slow).mean())
    MACD = pd.Series(EMAfast - EMAslow, name='MACD_' + str(n_fast) + '_' + str(n_slow))
    MACDsign = pd.Series(MACD.ewm(span=9, min_periods=9).mean(), name='MACDsign_' + str(n_fast) + '_' + str(n_slow))
    MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff_' + str(n_fast) + '_' + str(n_slow))
    df = df.join(MACD)
    df = df.join(MACDsign)
    df = df.join(MACDdiff)
    return df