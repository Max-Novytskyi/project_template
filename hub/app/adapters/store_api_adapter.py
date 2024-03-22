import json
import logging

from typing import List
import requests
import pydantic_core

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway

from config import BATCH_SIZE

class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url
        self.data_batch = []

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        # Add processed data to the batch
        self.data_batch.extend([item.dict() for item in processed_agent_data_batch])

        if len(self.data_batch) >= BATCH_SIZE:
            print(f"The batch size is: {len(self.data_batch)}")
            # Send the data batch for saving
            return self._save_batch()

        return True

    def _save_batch(self):
        try:
            # Form the endpoint URL
            endpoint = f"{self.api_base_url}/processed_agent_data"
            
            # Convert the data batch to JSON
            json_data = json.dumps(self.data_batch, default=pydantic_core.to_jsonable_python)

            # Send a POST request to the Store API with the data batch
            response = requests.post(endpoint, data=json_data)

            # Check the response status
            if response.status_code == 200:
                logging.info("Data batch saved successfully.")
                return True
            else:
                logging.error(f"Failed to save data batch. Status code: {response.status_code}")
                return False

        except Exception as e:
            logging.error(f"An error occurred while saving data batch: {str(e)}")
            return False 

        finally:
            # Clear the batch after sending
            self.data_batch.clear()

    def __del__(self):
        # Send any remaining data when the object is destroyed
        if self.data_batch:
            self._save_batch()
