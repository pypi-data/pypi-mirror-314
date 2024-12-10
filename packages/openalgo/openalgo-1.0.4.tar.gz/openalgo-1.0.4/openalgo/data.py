# -*- coding: utf-8 -*-
"""
OpenAlgo REST API Documentation - Data Methods
    https://docs.openalgo.in
"""

import requests
import pandas as pd
from datetime import datetime
import time
from .base import BaseAPI

class DataAPI(BaseAPI):
    """
    Data API methods for OpenAlgo.
    Inherits from the BaseAPI class.
    """

    def _handle_response(self, response, max_retries=3, retry_delay=1):
        """Helper method to handle API responses with retry logic"""
        retries = 0
        while retries < max_retries:
            try:
                if response.status_code == 500:  # Server error, might be temporary
                    retries += 1
                    if retries < max_retries:
                        time.sleep(retry_delay)
                        continue
                
                if response.status_code != 200:
                    return {
                        'status': 'error',
                        'message': f'HTTP {response.status_code}: {response.text}',
                        'code': response.status_code,
                        'error_type': 'http_error'
                    }
                
                data = response.json()
                if data.get('status') == 'error':
                    return {
                        'status': 'error',
                        'message': data.get('message', 'Unknown error'),
                        'code': response.status_code,
                        'error_type': 'api_error'
                    }
                return data
                
            except requests.exceptions.JSONDecodeError:
                return {
                    'status': 'error',
                    'message': 'Invalid JSON response from server',
                    'raw_response': response.text,
                    'error_type': 'json_error'
                }
            except Exception as e:
                return {
                    'status': 'error',
                    'message': str(e),
                    'error_type': 'unknown_error'
                }
        return response.json()  # Return last response if all retries failed

    def quotes(self, *, symbol, exchange):
        """
        Get real-time quotes for a symbol.

        Parameters:
        - symbol (str): Trading symbol. Required.
        - exchange (str): Exchange code. Required.

        Returns:
        dict: JSON response containing quote data including bid, ask, ltp, volume etc.
        """
        url = self.base_url + "quotes"
        payload = {
            "apikey": self.api_key,
            "symbol": symbol,
            "exchange": exchange
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def depth(self, *, symbol, exchange):
        """
        Get market depth (order book) for a symbol.

        Parameters:
        - symbol (str): Trading symbol. Required.
        - exchange (str): Exchange code. Required.

        Returns:
        dict: JSON response containing market depth data including top 5 bids/asks.
        """
        url = self.base_url + "depth"
        payload = {
            "apikey": self.api_key,
            "symbol": symbol,
            "exchange": exchange
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)

    def history(self, *, symbol, exchange, interval, start_date, end_date):
        """
        Get historical data for a symbol in pandas DataFrame format.

        Parameters:
        - symbol (str): Trading symbol. Required.
        - exchange (str): Exchange code. Required.
        - interval (str): Time interval for the data. Required.
                       Use interval() method to get supported intervals.
        - start_date (str): Start date in format 'YYYY-MM-DD'. Required.
        - end_date (str): End date in format 'YYYY-MM-DD'. Required.

        Returns:
        pandas.DataFrame or dict: DataFrame with historical data if successful,
                                error dict if failed. DataFrame has timestamp as index.
                                For intraday data (non-daily timeframes), timestamps
                                are converted to IST. Daily data is already in IST.
        """
        url = self.base_url + "history"
        payload = {
            "apikey": self.api_key,
            "symbol": symbol,
            "exchange": exchange,
            "interval": interval,
            "start_date": start_date,
            "end_date": end_date
        }

        response = requests.post(url, json=payload, headers=self.headers)
        result = self._handle_response(response)
        
        if result.get('status') == 'success' and 'data' in result:
            try:
                df = pd.DataFrame(result['data'])
                if df.empty:
                    return {
                        'status': 'error',
                        'message': 'No data available for the specified period',
                        'error_type': 'no_data'
                    }
                
                # Convert timestamp to datetime
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
                
                # Convert to IST for intraday timeframes
                if interval not in ['D', 'W', 'M']:  # Not daily/weekly/monthly
                    df["timestamp"] = df["timestamp"].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
                
                # Set timestamp as index
                df.set_index('timestamp', inplace=True)
                
                # Sort index to ensure chronological order
                df.sort_index(inplace=True)
                
                # Add basic indicators
                df['returns'] = df['close'].pct_change()
                df['change%'] = df['returns'] * 100
                
                return df
            except Exception as e:
                return {
                    'status': 'error',
                    'message': f'Failed to process historical data: {str(e)}',
                    'error_type': 'processing_error',
                    'raw_data': result['data']
                }
        return result

    def interval(self):
        """
        Get supported time intervals for historical data.

        Returns:
        dict: JSON response containing supported intervals categorized by type
              (seconds, minutes, hours, days, weeks, months)
        """
        # Since the interval endpoint is not available, return the supported intervals directly
        return {
            'status': 'success',
            'data': {
                'seconds': ['5s', '10s', '15s', '30s', '45s'],
                'minutes': ['1m', '2m', '3m', '5m', '10m', '15m', '20m', '30m'],
                'hours': ['1h', '2h', '4h'],
                'days': ['D'],
                'weeks': ['W'],
                'months': ['M']
            }
        }
