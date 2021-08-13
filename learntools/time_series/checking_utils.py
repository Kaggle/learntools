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


def load_average_sales():
    store_sales = load_store_sales()
    average_sales = store_sales.groupby('date').mean()
    return average_sales


def load_family_sales():
    family_sales = (  #
        load_store_sales()  #
        .groupby(['family', 'date'])  #
        .mean()  # 
        .unstack('family')  #
        .loc['2017', ['sales', 'onpromotion']]  #
    )  #
    return family_sales


def load_holidays_events():
    holidays_events = pd.read_csv(
        comp_dir / "holidays_events.csv",
        dtype={
            'type': 'category',
            'locale': 'category',
            'locale_name': 'category',
            'description': 'category',
            'transferred': 'bool',
        },
        parse_dates=['date'],
        infer_datetime_format=True,
    )
    holidays_events = holidays_events.set_index('date').to_period('D')
    return holidays_events


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
