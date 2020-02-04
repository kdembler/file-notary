export interface File {
  name: string
  localHash: string | null
  blockchainHash: string | null
  saveName: string | null
  objectUrl: string | null
}

export function createFile(name: string): File {
  return {
    name,
    localHash: null,
    blockchainHash: null,
    saveName: null,
    objectUrl: null,
  }
}
