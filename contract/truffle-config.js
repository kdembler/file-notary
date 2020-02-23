const path = require("path");
const HDWalletProvider = require("@truffle/hdwallet-provider");
const dotenv = require("dotenv");

const dotenvFilePath = path.resolve(__dirname, "..", ".env");
dotenv.config({ path: dotenvFilePath });

const getEnv = key => {
  const value = process.env[key];
  if (!value) {
    throw Error(`Env variable ${key} not found`);
  }
  return value;
};

const privateKey = getEnv("ETH_PRIVATE_KEY");
const web3Uri = getEnv("ETH_NODE_ENDPOINT");

module.exports = {
  networks: {
    kovan: {
      provider: () => new HDWalletProvider(privateKey, web3Uri),
      network_id: 42,
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: true
    }
  }
};
