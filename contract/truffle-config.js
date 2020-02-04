const HDWalletProvider = require("@truffle/hdwallet-provider");

const fs = require("fs");
const mnemonic = fs
  .readFileSync(".secret")
  .toString()
  .trim();

module.exports = {
  networks: {
    kovan: {
      provider: () =>
        new HDWalletProvider(
          mnemonic,
          `https://kovan.infura.io/v3/d94c6d05fdac485d8e50a77ff1ff6793`
        ),
      network_id: 42,
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: true
    }
  }
};
