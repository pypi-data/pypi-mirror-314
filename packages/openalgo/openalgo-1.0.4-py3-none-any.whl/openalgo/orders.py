# -*- coding: utf-8 -*-
"""
OpenAlgo REST API Documentation - Order Methods
    https://docs.openalgo.in
"""

import requests
from .base import BaseAPI

class OrderAPI(BaseAPI):
    """
    Order management API methods for OpenAlgo.
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

    def placeorder(self, *, strategy="Python", symbol, action, exchange, price_type="MARKET", product="MIS", quantity=1, **kwargs):
        """
        Place an order with the given parameters. All parameters after 'strategy' must be named explicitly.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - action (str): BUY or SELL. Required.
        - exchange (str): Exchange code. Required.
        - price_type (str, optional): Type of price. Defaults to "MARKET".
        - product (str, optional): Product type. Defaults to "MIS".
        - quantity (int/str, optional): Quantity to trade. Defaults to 1.
        - **kwargs: Optional parameters like:
            - price (str): Required for LIMIT orders
            - trigger_price (str): Required for SL and SL-M orders
            - disclosed_quantity (str): Disclosed quantity
            - target (str): Target price
            - stoploss (str): Stoploss price
            - trailing_sl (str): Trailing stoploss points

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "placeorder"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "symbol": symbol,
            "action": action,
            "exchange": exchange,
            "pricetype": price_type,
            "product": product,
            "quantity": str(quantity)
        }
        # Convert numeric values to strings
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = str(value)
        
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
    
    def placesmartorder(self, *, strategy="Python", symbol, action, exchange, price_type="MARKET", product="MIS", quantity=1, position_size, **kwargs):
        """
        Place a smart order that considers the current position size.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - action (str): BUY or SELL. Required.
        - exchange (str): Exchange code. Required.
        - price_type (str, optional): Type of price. Defaults to "MARKET".
        - product (str, optional): Product type. Defaults to "MIS".
        - quantity (int/str, optional): Quantity to trade. Defaults to 1.
        - position_size (int/str): Required position size.
        - **kwargs: Optional parameters like:
            - price (str): Required for LIMIT orders
            - trigger_price (str): Required for SL and SL-M orders
            - disclosed_quantity (str): Disclosed quantity
            - target (str): Target price
            - stoploss (str): Stoploss price
            - trailing_sl (str): Trailing stoploss points

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "placesmartorder"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "symbol": symbol,
            "action": action,
            "exchange": exchange,
            "pricetype": price_type,
            "product": product,
            "quantity": str(quantity),
            "position_size": str(position_size)
        }
        # Convert numeric values to strings
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = str(value)
        
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def basketorder(self, *, strategy="Python", orders):
        """
        Place multiple orders simultaneously.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - orders (list): List of order dictionaries. Each order dictionary should contain:
            - symbol (str): Trading symbol. Required.
            - exchange (str): Exchange code. Required.
            - action (str): BUY or SELL. Required.
            - quantity (str/int): Quantity to trade. Required.
            - pricetype (str, optional): Type of price. Defaults to "MARKET".
            - product (str, optional): Product type. Defaults to "MIS".
            Optional parameters:
            - price (str): Required for LIMIT orders
            - trigger_price (str): Required for SL and SL-M orders
            - disclosed_quantity (str): Disclosed quantity

        Returns:
        dict: JSON response containing results for each order with format:
            {
                "results": [
                    {
                        "orderid": "order_id",
                        "status": "success/error",
                        "symbol": "symbol_name"
                    },
                    ...
                ],
                "status": "success/error"
            }
        """
        url = self.base_url + "basketorder"
        
        # Ensure all numeric values are strings
        processed_orders = []
        for order in orders:
            processed_order = {}
            for key, value in order.items():
                processed_order[key] = str(value) if isinstance(value, (int, float)) else value
            processed_orders.append(processed_order)
            
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "orders": processed_orders
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def splitorder(self, *, strategy="Python", symbol, action, exchange, quantity, splitsize, price_type="MARKET", product="MIS", **kwargs):
        """
        Split a large order into multiple smaller orders.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - action (str): BUY or SELL. Required.
        - exchange (str): Exchange code. Required.
        - quantity (int/str): Total quantity to trade. Required.
        - splitsize (int/str): Size of each split order. Required.
        - price_type (str, optional): Type of price. Defaults to "MARKET".
        - product (str, optional): Product type. Defaults to "MIS".
        - **kwargs: Optional parameters like:
            - price (str): Required for LIMIT orders
            - trigger_price (str): Required for SL and SL-M orders
            - disclosed_quantity (str): Disclosed quantity

        Returns:
        dict: JSON response containing results for each split order with format:
            {
                "results": [
                    {
                        "order_num": 1,
                        "orderid": "order_id",
                        "quantity": quantity,
                        "status": "success"
                    },
                    ...
                ],
                "split_size": splitsize,
                "status": "success",
                "total_quantity": total_quantity
            }
        """
        url = self.base_url + "splitorder"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "symbol": symbol,
            "action": action,
            "exchange": exchange,
            "quantity": str(quantity),
            "splitsize": str(splitsize),
            "pricetype": price_type,
            "product": product
        }
        
        # Convert numeric values to strings
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = str(value)
        
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def orderstatus(self, *, order_id, strategy="Python"):
        """
        Get the current status of an order.

        Parameters:
        - order_id (str): The ID of the order to check. Required.
        - strategy (str, optional): The trading strategy name. Defaults to "Python".

        Returns:
        dict: JSON response containing order details with format:
            {
                "data": {
                    "action": "BUY/SELL",
                    "exchange": "exchange_code",
                    "order_status": "complete/pending/cancelled/etc",
                    "orderid": "order_id",
                    "price": price_value,
                    "pricetype": "MARKET/LIMIT/etc",
                    "product": "product_type",
                    "quantity": quantity_value,
                    "symbol": "symbol_name",
                    "timestamp": "DD-MMM-YYYY HH:MM:SS",
                    "trigger_price": trigger_price_value
                },
                "status": "success"
            }
        """
        url = self.base_url + "orderstatus"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "orderid": order_id
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def openposition(self, *, strategy="Python", symbol, exchange, product):
        """
        Get the current open position for a specific symbol.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - exchange (str): Exchange code. Required.
        - product (str): Product type. Required.

        Returns:
        dict: JSON response containing position details with format:
            {
                "quantity": position_quantity,
                "status": "success"
            }
        """
        url = self.base_url + "openposition"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "symbol": symbol,
            "exchange": exchange,
            "product": product
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
    
    def modifyorder(self, *, order_id, strategy="Python", symbol, action, exchange, price_type="LIMIT", product, quantity, price, disclosed_quantity="0", trigger_price="0", **kwargs):
        """
        Modify an existing order.

        Parameters:
        - order_id (str): The ID of the order to modify. Required.
        - strategy (str, optional): The trading strategy name. Defaults to "Python".
        - symbol (str): Trading symbol. Required.
        - action (str): BUY or SELL. Required.
        - exchange (str): Exchange code. Required.
        - price_type (str, optional): Type of price. Defaults to "LIMIT".
        - product (str): Product type. Required.
        - quantity (int/str): Quantity to trade. Required.
        - price (str): New price for the order. Required.
        - disclosed_quantity (str): Disclosed quantity. Required.
        - trigger_price (str): Trigger price. Required.
        - **kwargs: Optional parameters

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "modifyorder"
        payload = {
            "apikey": self.api_key,
            "orderid": order_id,
            "strategy": strategy,
            "symbol": symbol,
            "action": action,
            "exchange": exchange,
            "pricetype": price_type,
            "product": product,
            "quantity": str(quantity),
            "price": str(price),
            "disclosed_quantity": str(disclosed_quantity),
            "trigger_price": str(trigger_price)
        }
        # Convert numeric values to strings
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = str(value)
        
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
    
    def cancelorder(self, *, order_id, strategy="Python"):
        """
        Cancel an existing order.

        Parameters:
        - order_id (str): The ID of the order to cancel. Required.
        - strategy (str, optional): The trading strategy name. Defaults to "Python".

        Returns:
        dict: JSON response from the API.
        """
        url = self.base_url + "cancelorder"
        payload = {
            "apikey": self.api_key,
            "orderid": order_id,
            "strategy": strategy
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
    
    def closeposition(self, *, strategy="Python"):
        """
        Close all open positions for a given strategy.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".

        Returns:
        dict: JSON response from the API indicating the result of the close position action.
        """
        url = self.base_url + "closeposition"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
    
    def cancelallorder(self, *, strategy="Python"):
        """
        Cancel all orders for a given strategy.

        Parameters:
        - strategy (str, optional): The trading strategy name. Defaults to "Python".

        Returns:
        dict: JSON response from the API indicating the result of the cancel all orders action.
        """
        url = self.base_url + "cancelallorder"
        payload = {
            "apikey": self.api_key,
            "strategy": strategy
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
