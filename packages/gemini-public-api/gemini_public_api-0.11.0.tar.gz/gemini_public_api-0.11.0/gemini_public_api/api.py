from typing import Optional

import requests

import gemini_public_api.public_endpoints as production
import gemini_public_api.public_sandbox_endpoints as sandbox


def get_symbols(use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves all available trading symbols.

    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(url=sandbox.SYMBOLS if use_sandbox else production.SYMBOLS)


def get_symbol_details(symbol: str, use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves detailed information for a specific symbol.

    :param symbol: symbol for which details are required.
    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(
        url=sandbox.SYMBOL_DETAILS.format(symbol=symbol) if use_sandbox else production.SYMBOL_DETAILS.format(
            symbol=symbol)
    )


def get_network(token: str, use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves the network status of a token.

    :param token: token for which network status is required.
    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(
        url=sandbox.NETWORK.format(token=token) if use_sandbox else production.NETWORK.format(token=token)
    )


def get_ticker(symbol: str, use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves the ticker for a specific symbol.

    :param symbol: symbol for which ticker is required.
    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(
        url=sandbox.PUBLIC_TICKER.format(
            symbol=symbol) if use_sandbox else production.PUBLIC_TICKER.format(symbol=symbol)
    )


def get_ticker_v2(symbol: str, use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves the ticker (version 2) for a specific symbol.

    :param symbol: symbol for which ticker (version 2) is required.
    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(
        url=sandbox.PUBLIC_TICKER_V2.format(
            symbol=symbol) if use_sandbox else production.PUBLIC_TICKER_V2.format(symbol=symbol)
    )


def get_candles(symbol: str, time_frame: str, use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves the candles data for a specific symbol and time frame.

    :param symbol: symbol for which candles data is required.
    :param time_frame: time frame for the candles data.
    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(
        url=sandbox.CANDLES.format(
            symbol=symbol, time_frame=time_frame
        ) if use_sandbox else production.CANDLES.format(symbol=symbol, time_frame=time_frame)
    )


def get_free_promos(use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves all available free promotions.

    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(url=sandbox.FREE_PROMOS if use_sandbox else production.FREE_PROMOS)


def get_current_order_book(
        symbol: str,
        bid_limit: int = 500,
        ask_limit: int = 500,
        use_sandbox: bool = False
) -> requests.Response:
    """
    Retrieves the current order book for a specific symbol.

    :param symbol: symbol for which order book is required.
    :param bid_limit: limit for bid orders.
    :param ask_limit: limit for ask orders.
    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(
        url=sandbox.CURRENT_ORDER_BOOK.format(symbol=symbol) if use_sandbox else production.CURRENT_ORDER_BOOK.format(
            symbol=symbol),
        params={'bid_limit': bid_limit, 'ask_limit': ask_limit}
    )


def get_trade_history(
        symbol: str,
        timestamp: Optional[int] = None,
        limit_trades: int = 500,
        include_breaks: bool = False,
        use_sandbox: bool = False
) -> requests.Response:
    """
    Retrieves the trade history for a specific symbol.

    :param symbol: symbol for which trade history is required.
    :param timestamp: starting timestamp for the trade history.
    :param limit_trades: limit for number of trades in the history.
    :param include_breaks: flag to include breaks in the trade history.
    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(
        url=sandbox.TRADE_HISTORY.format(symbol=symbol) if use_sandbox else production.TRADE_HISTORY.format(
            symbol=symbol),
        params={
            'timestamp':      timestamp,
            'limit_trades':   limit_trades,
            'include_breaks': str(include_breaks).lower()
        } if timestamp is not None else {
            'limit_trades':   limit_trades,
            'include_breaks': str(include_breaks).lower()
        }
    )


def get_price_feed(use_sandbox: bool = False) -> requests.Response:
    """
    Retrieves the price feed.

    :param use_sandbox: flag to use sandbox endpoints.
    :return: Returns a Response object.
    """
    return requests.get(url=sandbox.PRICE_FEED if use_sandbox else production.PRICE_FEED)
