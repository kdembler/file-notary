const FileNotary = artifacts.require("FileNotary");
const fs = require("fs");

const artifcatsDir = "artifacts";

module.exports = async function(deployer) {
  await deployer.deploy(FileNotary);
  const instance = await FileNotary.deployed();
  const contract = { address: instance.address, abi: instance.abi };
  if (!fs.existsSync(artifcatsDir)) {
    fs.mkdirSync(artifcatsDir);
  }
  fs.writeFileSync(`${artifcatsDir}/fileNotary.json`, JSON.stringify(contract));
};
