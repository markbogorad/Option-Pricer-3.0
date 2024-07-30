# kdb_utils.py
from qpython import qconnection
import numpy as np
import pandas as pd

class KDBUtils:
    def __init__(self, host='localhost', port=5001):  # Adjust port if necessary
        self.q = qconnection.QConnection(host=host, port=port)
        try:
            self.q.open()
            print(f"Connected to KDB+ server version: {self.q.protocol_version}.")
            self.create_tables()
        except Exception as e:
            print(f"Error connecting to KDB+ server: {e}")

    def create_tables(self):
        self.q.sendSync("user_inputs: ([] id: `int$(); S: `float$(); K: `float$(); T: `float$(); sigma: `float$(); r: `float$(); purchase_price_call: `float$(); purchase_price_put: `float$())")

    def record_user_input(self, data):
        try:
            # Convert pandas DataFrame to dictionary
            data_dict = data.to_dict('list')
            # Extract values as lists
            values = [data_dict[col] for col in data_dict]
            # Insert data into KDB+ table
            self.q.sendSync("insert", 'user_inputs', values)
            print("User input recorded successfully.")
        except Exception as e:
            print(f"Error recording user input: {e}")

    def close(self):
        self.q.close()

