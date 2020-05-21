import numpy as np
import pandas as pd


def create_balance(coin, start, end, freq):
    idx = pd.date_range(start, end, freq=freq)
    used = np.linspace(1, 20, len(idx))
    free = np.linspace(1, 20, len(idx))
    total = used + free
    df = pd.DataFrame({
        "coin": [coin] * len(idx),
        "used": used,
        "free": free,
        "total": total
    }, index=idx)
    df.index.name = "datetime"
    return df


if __name__ == "__main__":
    coins = ["BTC", "ETH"]
    start = "2020-01-01"
    end = "2020-03-08"
    freq = "5T"
    filename = "data.csv"

    df_list = [create_balance(coin, start, end, freq) for \
        coin in coins]
    df_joined = pd.concat(df_list, sort=False)

    df_joined.to_csv(filename, index=True)