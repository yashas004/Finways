from web3 import Web3
import json
import requests
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Connecting to Ethereum blockchain node
web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  

# Loading ABI and contract address
with open('contract_abi.json', 'r') as f:
    contract_abi = json.load(f)

contract_address = '25435263'  

# Loading contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to fetch data from sidechain
def fetch_data_from_sidechain():
    # Making API call for interacting with sidechain to fetch data
    data = requests.get('http://sidechain.api/data').json()
    return data

# Function to preprocess data
def preprocess_data(data):
    # Preprocess data here
    processed_data = data
    return processed_data

# Function to train AI model
def train_model(data):
   
    model = Sequential([
        Dense(64, activation='relu', input_shape=(len(data[0]),)),
        Dense(64, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(data, epochs=10, batch_size=32)
    return model

# Main function
def main():
    # Fetching data from sidechain
    sidechain_data = fetch_data_from_sidechain()
    
    # Preprocess data
    preprocessed_data = preprocess_data(sidechain_data)
    
    # Training AI model
    model = train_model(preprocessed_data)
    
    # Converting model to JSON format
    model_json = model.to_json()
    
    # Deploying AI model to blockchain
    contract.functions.deployModel(model_json).transact()

if __name__ == "__main__":
    main()


