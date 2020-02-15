export interface FileInfo {
  id: string
  name: string
  created: string
  localHash?: string
}

export function createFile(name: string): FileInfo {
  return {
    id: '',
    name,
    localHash: '',
    // localHash: null,
    // blockchainHash: null,
    // saveName: null,
    // objectUrl: null,
  }
}
