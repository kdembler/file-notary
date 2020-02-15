import Web3 from 'web3'
import { web3Url } from '@/urls'
import FileNotary from './fileNotary.json'
import { Contract } from 'web3-eth-contract'

const NO_HASH = '0x0000000000000000000000000000000000000000000000000000000000000000'
const EVENT_NAME = 'HashSet'
const EVENT_SIG = FileNotary.abi.find(a => a.type === 'event' && a.name === EVENT_NAME)!.signature

export default class Web3Service {
  notary: Contract
  constructor() {
    const web3 = new Web3(web3Url)

    this.notary = new web3.eth.Contract(FileNotary.abi as any, FileNotary.address)
  }

  async getFileBlockchainHash(fileId: string): Promise<string> {
    const hash = await this.notary.methods.getFileHash(fileId).call()
    if (hash === NO_HASH) {
      return this.listenForFileEvents(fileId)
    }
    return hash
  }

  private async listenForFileEvents(fileId: string): Promise<string> {
    return new Promise((resolve, reject) => {
      const fileIndex = Web3.utils.keccak256(fileId)
      this.notary.once(EVENT_NAME, { topics: [EVENT_SIG, fileIndex] }, (err: any, event: any) => {
        if (err) {
          reject(err)
          return
        }

        const hash = event.raw.data as string
        resolve(hash)
      })
    })
  }
}
