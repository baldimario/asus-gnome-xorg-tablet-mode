"""Data class"""
import os
import json

ABSPATH = os.path.abspath(os.path.dirname(__file__))
class Data:
    """Data class"""
    @staticmethod
    def load(key, default=None):
        """Load data"""
        try:
            with open(os.path.join(ABSPATH, f'../data/{key}.json'), 'r', encoding='utf-8') as file_handler:
                return json.load(file_handler)
        except Exception as exc:
            print(exc)
            return default

    @staticmethod
    def save(key, data):
        """Save data"""
        with open(os.path.join(ABSPATH, f'../data/{key}.json'), 'w', encoding='utf-8') as file_handler:
            file_handler.write(json.dumps(data, indent=4))
