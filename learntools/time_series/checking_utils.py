from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression

comp_dir = Path('../input/store-sales-time-series-forecasting')
data_dir = Path('../input/ts-course-data/')


def load_store_sales():
    dtype = {
        'store_nbr': 'category',
        'family': 'category',
        'sales': 'float32',
        'onpromotion': 'uint32',
    }
    store_sales = pd.read_csv(
        comp_dir / 'train.csv',
        dtype=dtype,
        parse_dates=['date'],
        infer_datetime_format=True,
    )
    store_sales = store_sales.set_index('date').to_period('D')
    store_sales = store_sales.set_index(['store_nbr', 'family'], append=True)
    return store_sales


def load_average_sales(with_promo=False):
    store_sales = load_store_sales()
    average_sales = store_sales.groupby('date').mean()
    if not with_promo:
        return average_sales['sales']
    else:
        return average_sales


def load_oil():
    oil = pd.read_csv(
        comp_dir / "oil.csv",
        dtype='float32',
        parse_dates=["date"],
        infer_datetime_format=True,
    )
    oil = oil.set_index('date').to_period('D').squeeze()
    return oil


def load_retail_sales():
    retail_sales = pd.read_csv(
        data_dir / "us-retail-sales.csv",
        parse_dates=['Month'],
        index_col='Month',
    ).to_period('D')
    return retail_sales
