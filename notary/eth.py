import json
import logging
import multiprocessing as mp
import os

from hashlib import sha3_256
from utils import safe_getenv
from web3 import Web3, HTTPProvider


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
        web3_endpoint = safe_getenv("ETH_NODE_ENDPOINT")

        self.web3 = Web3(HTTPProvider(web3_endpoint))
        if not self.web3.isConnected():
            raise Exception('web3 did not connect')

    def _load_contract_info(self):
        with open('artifacts/fileNotary.json') as json_file:
            contract = json.load(json_file)
        self.notary_contract = self.web3.eth.contract(
            address=contract['address'],
            abi=contract['abi']
        )

    def _load_account_info(self):
        private_key = safe_getenv("ETH_PRIVATE_KEY").strip()
        account = self.web3.eth.account.privateKeyToAccount(private_key)

        self.private_key = bytearray.fromhex(private_key)
        self.address = account.address

    def _process_queue(self):
        self.logger.info('starting queue processing')
        while True:
            self.logger.info('waiting for data to process')

            try:
                file_id, file_bytes = self.notary_queue.get()
            except KeyboardInterrupt:
                self.logger.info('exitting')
                break

            digester = sha3_256()
            digester.update(file_bytes)
            file_hash = digester.hexdigest()

            try:
                nonce = self.web3.eth.getTransactionCount(self.address)
                self.logger.info(f'notarizing {file_id} with hash {file_hash} and nonce {nonce}')
                txn = self.notary_contract.functions.setFileHash(file_id, file_hash).buildTransaction({
                    'from': self.address,
                    'nonce': nonce
                })

                signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
                txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                self.logger.info(f'transaction {txn_hash.hex()} sent')
            except Exception as e:
                self.logger.error(f'failed to notarize {file_id}: {e}')
