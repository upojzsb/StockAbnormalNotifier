# Notification
from win10toast import ToastNotifier
# Data source
from get_stock_info import GetStockInfo, GetMarketInfo, StockType

import time
import multiprocessing

import pandas as pd

# Display all infos
pd.set_option('display.expand_frame_repr', False)

monitoring_code = [
    str(i) for i in [
        113569,
        113578,
        127049,
        113596,
        128085,
        128074,
        128108,
        127051,
        123128,
        113576,
        127047,
        113624,
        128105,
        128114,
        128116,
        110072,
        128100,
        128124,
    ]
]
update_period = 10
max_display_num = 4  # No more than 4, otherwise they will only display 4
threshold = 0.5  # Percent

toaster = ToastNotifier()


def continuous_monitor():
    while True:
        current_market_info = GetMarketInfo(StockType.EXCHANGE_BOND).market_info()

        selected_stock_list = current_market_info[current_market_info['code'].isin(monitoring_code)]
        sorted_selected_list = selected_stock_list.sort_values('changepercent', ascending=False)[0:max_display_num]

        eb_name = sorted_selected_list['name'].to_list()
        eb_price = list(map(float, sorted_selected_list['trade'].to_list()))
        eb_percentage = list(map(float, sorted_selected_list['changepercent'].to_list()))

        text_to_display = '\n'.join(
            [
                '{0:4s}  {1:8.3f}  {2:7.3f}%'.format(name, price, percent)
                for (name, price, percent) in zip(eb_name, eb_price, eb_percentage)
            ]
        )

        toaster.show_toast(
            f'EB Price Notifier@{time.strftime("%y%m%d-%H:%M:%S")}',
            text_to_display,
            icon_path=None,
            duration=update_period,
            threaded=True
        )
        print(text_to_display)

        time.sleep(update_period)


def threshold_monitor():
    while True:
        current_market_info = GetMarketInfo(StockType.EXCHANGE_BOND).market_info()

        selected_stock_list = current_market_info[current_market_info['code'].isin(monitoring_code)]

        selected_stock_list.reindex(selected_stock_list['changepercent'].astype('float').abs().sort_values().index)
        sorted_selected_list = selected_stock_list

        eb_name = sorted_selected_list['name'].to_list()
        eb_price = list(map(float, sorted_selected_list['trade'].to_list()))
        eb_percentage = list(map(float, sorted_selected_list['changepercent'].to_list()))

        text_to_display = '\n'.join(
            [
                '{0:4s}  {1:8.3f}  {2:7.3f}%'.format(name, price, percent)
                for (name, price, percent) in zip(eb_name, eb_price, eb_percentage)
                if abs(percent) > threshold
            ]
        )

        toaster.show_toast(
            f'EB Price Notifier@{time.strftime("%y%m%d-%H:%M:%S")}',
            text_to_display,
            icon_path=None,
            duration=update_period,
            threaded=True
        )
        print(text_to_display)

        time.sleep(update_period)


if __name__ == '__main__':
    threshold_monitor()
