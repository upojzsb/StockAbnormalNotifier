# Get the market value
import akshare as ak


class StockType:
    UNKNOWN = 0
    STOCK = 1
    EXCHANGE_BOND = 2


class GetStockInfo(StockType):
    def __init__(self, code, update_before_get=True):
        if not isinstance(code, str):
            raise ValueError('The code must be a string')
        if code.upper() != code.lower():
            raise ValueError('The code must only contain digital')

        # Automatically update data before return data
        self.update_before_get = update_before_get

        # Only Chinese market are available now
        # TODO: Support other countries' market
        self.code = code
        if code.startswith('60') or code.startswith('68'):
            self.market = 'sh'
            self.type = self.STOCK
        elif code.startswith('00') or code.startswith('300'):
            self.market = 'sz'
            self.type = self.STOCK
        elif code.startswith('11'):
            self.market = 'sh'
            self.type = self.EXCHANGE_BOND
        elif code.startswith('12'):
            self.market = 'sz'
            self.type = self.EXCHANGE_BOND
        else:
            self.market = ''
            self.type = self.UNKNOWN

        # Only EBs are available
        # TODO: Support other kinds of A Stock
        if self.type != self.EXCHANGE_BOND:
            raise NotImplemented('Only Chinese EBs are available')

    def history_daily(self):
        # TODO: Support other kinds of A Stock
        if self.type == self.STOCK:
            raise NotImplemented('Only Chinese EBs are available')
        elif self.type == self.EXCHANGE_BOND:
            return ak.bond_zh_hs_cov_daily(
                symbol=self.market + self.code
            )
        else:
            raise NotImplemented('Only Chinese EBs are available')

    def history_time_div(self, period='1', adjust='', start_date='1979-09-01 09:32:00', end_date='2222-01-01 09:32:00'):
        # TODO: Support other kinds of A Stock
        if self.type == self.STOCK:
            raise NotImplemented('Only Chinese EBs are available')
        elif self.type == self.EXCHANGE_BOND:
            return ak.bond_zh_hs_cov_min(
                symbol=self.market + self.code,
                period=period,
                adjust=adjust,
                start_date=start_date,
                end_date=end_date
            )
        else:
            raise NotImplemented('Only Chinese EBs are available')

    def pre_market(self):
        # TODO: Support other kinds of A Stock
        if self.type == self.STOCK:
            raise NotImplemented('Only Chinese EBs are available')
        elif self.type == self.EXCHANGE_BOND:
            return ak.bond_zh_hs_cov_pre_min(
                symbol=self.market + self.code
            )
        else:
            raise NotImplemented('Only Chinese EBs are available')


class GetMarketInfo(StockType):
    def __init__(self, market_type, update_before_get=True):
        # Automatically update data before return data
        self.update_before_get = update_before_get

        # Only Chinese market are available now
        # TODO: Support other countries' market
        self.type = market_type

        # Only EBs are available
        # TODO: Support other kinds of A Stock
        if self.type != self.EXCHANGE_BOND:
            raise NotImplemented('Only Chinese EBs are available')

    def market_info(self):
        # TODO: Support other kinds of A Stock
        if self.type == self.STOCK:
            raise NotImplemented('Only Chinese EBs are available')
        elif self.type == self.EXCHANGE_BOND:
            return ak.bond_zh_hs_cov_spot()
        else:
            raise NotImplemented('Only Chinese EBs are available')


# For test purpose
if __name__ == '__main__':
    zbzz = GetStockInfo(code='128114', update_before_get=True)
    print(zbzz.history_daily())
    print(zbzz.history_time_div(period='1'))
    print(zbzz.pre_market())

    cb = GetMarketInfo(market_type=StockType.EXCHANGE_BOND)
    print(cb.market_info())
