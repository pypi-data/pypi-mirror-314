# -*- coding: utf-8 -*-
"""
OpenAlgo REST API Documentation - Account Methods
    https://docs.openalgo.in
"""

import requests
from .base import BaseAPI

class AccountAPI(BaseAPI):
    """
    Account management API methods for OpenAlgo.
    Inherits from the BaseAPI class.
    """

    def _handle_response(self, response):
        """Helper method to handle API responses"""
        try:
            if response.status_code != 200:
                return {
                    'status': 'error',
                    'message': f'HTTP {response.status_code}: {response.text}'
                }
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                'status': 'error',
                'message': 'Invalid JSON response from server',
                'raw_response': response.text
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def funds(self):
        """
        Get funds and margin details of the connected trading account.

        Returns:
        dict: JSON response containing funds data with format:
            {
                "data": {
                    "availablecash": "amount",
                    "collateral": "amount",
                    "m2mrealized": "amount",
                    "m2munrealized": "amount",
                    "utiliseddebits": "amount"
                },
                "status": "success"
            }
        """
        url = self.base_url + "funds"
        payload = {
            "apikey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def orderbook(self):
        """
        Get orderbook details from the broker with basic orderbook statistics.

        Returns:
        dict: JSON response containing orders data with format:
            {
                "data": {
                    "orders": [
                        {
                            "action": "BUY/SELL",
                            "exchange": "exchange_code",
                            "order_status": "status",
                            "orderid": "id",
                            "price": price_value,
                            "pricetype": "type",
                            "product": "product_type",
                            "quantity": quantity_value,
                            "symbol": "symbol_name",
                            "timestamp": "DD-MMM-YYYY HH:MM:SS",
                            "trigger_price": trigger_price_value
                        },
                        ...
                    ],
                    "statistics": {
                        "total_buy_orders": count,
                        "total_completed_orders": count,
                        "total_open_orders": count,
                        "total_rejected_orders": count,
                        "total_sell_orders": count
                    }
                },
                "status": "success"
            }
        """
        url = self.base_url + "orderbook"
        payload = {
            "apikey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def tradebook(self):
        """
        Get tradebook details from the broker.

        Returns:
        dict: JSON response containing trades data with format:
            {
                "data": [
                    {
                        "action": "BUY/SELL",
                        "average_price": price_value,
                        "exchange": "exchange_code",
                        "orderid": "id",
                        "product": "product_type",
                        "quantity": quantity_value,
                        "symbol": "symbol_name",
                        "timestamp": "DD-MMM-YYYY HH:MM:SS",
                        "trade_value": value
                    },
                    ...
                ],
                "status": "success"
            }
        """
        url = self.base_url + "tradebook"
        payload = {
            "apikey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def positionbook(self):
        """
        Get positionbook details from the broker.

        Returns:
        dict: JSON response containing positions data with format:
            {
                "data": [
                    {
                        "average_price": "price_value",
                        "exchange": "exchange_code",
                        "product": "product_type",
                        "quantity": quantity_value,
                        "symbol": "symbol_name"
                    },
                    ...
                ],
                "status": "success"
            }
        """
        url = self.base_url + "positionbook"
        payload = {
            "apikey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def holdings(self):
        """
        Get stock holdings details from the broker.

        Returns:
        dict: JSON response containing holdings data with format:
            {
                "data": {
                    "holdings": [
                        {
                            "exchange": "exchange_code",
                            "pnl": pnl_value,
                            "pnlpercent": percentage_value,
                            "product": "product_type",
                            "quantity": quantity_value,
                            "symbol": "symbol_name"
                        },
                        ...
                    ],
                    "statistics": {
                        "totalholdingvalue": value,
                        "totalinvvalue": value,
                        "totalpnlpercentage": percentage,
                        "totalprofitandloss": value
                    }
                },
                "status": "success"
            }
        """
        url = self.base_url + "holdings"
        payload = {
            "apikey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
