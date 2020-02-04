import os
import logging
import json
import multiprocessing as mp
from hashlib import sha256
from web3 import Web3, HTTPProvider
from cobra_hdwallet import HDWallet
from utils import safe_getenv


def start_notary():
    notary_queue = mp.Queue()
    ethereum_handler = EthereumHandler(notary_queue)
    ethereum_handler.run()

    return notary_queue

class EthereumHandler():
    def __init__(self, notary_queue):
        self.notary_queue = notary_queue
        self.logger = logging.getLogger('eth')

        self._set_infura_web3()
        self._load_contract_info()
        self._load_account_info()

        self.logger.info('initalized web3 and loaded contract info')

    def run(self):
        p = mp.Process(target=self._process_queue)
        p.start()

    def _set_infura_web3(self):
        infura_endpoint = safe_getenv("ETH_INFURA_ENDPOINT")

        self.web3 = Web3(HTTPProvider(infura_endpoint))
        if not self.web3.isConnected():
            raise Exception('web3 did not connect')

    def _load_contract_info(self):
        with open('eth/fileNotary.json') as json_file:
            contract = json.load(json_file)
        self.notary_contract = self.web3.eth.contract(
            address=contract['address'],
            abi=contract['abi']
        )

    def _load_account_info(self):
        account_mnemonic = safe_getenv("ETH_ACCOUNT_MNEMONIC")
        hd_wallet = HDWallet()
        account = hd_wallet.create_hdwallet(account_mnemonic)
        self.address = account['address']
        self.private_key = bytearray.fromhex(account['private_key'])

    def _process_queue(self):
        self.logger.info('starting queue processing')
        while True:
            self.logger.info('waiting for data to process')
            file_name, file_bytes = self.notary_queue.get()

            digester = sha256()
            digester.update(file_bytes)
            file_hash = digester.hexdigest()

            try:
                nonce = self.web3.eth.getTransactionCount(self.address)
                self.logger.info(f'notarizing {file_name} with hash {file_hash} and nonce {nonce}')
                txn = self.notary_contract.functions.setFileHash(file_name, file_hash).buildTransaction({
                    'from': self.address,
                    'nonce': nonce
                })

                signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
                txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                self.logger.info(f'transaction {txn_hash.hex()} sent')
            except Exception as e:
                self.logger.error(f'failed to notarize {file_name}: {e}')
