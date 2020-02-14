// TODO: switch to SHA-3
export async function getFileHash(file: Blob | File): Promise<string> {
  const content = await file.arrayBuffer()
  const digest = await crypto.subtle.digest('SHA-256', content)
  const array = new Uint8Array(digest)
  const hash = array.reduce((acc, byte) => {
    const hex = byte.toString(16)
    const padded = hex.padStart(2, '0')
    return `${acc}${padded}`
  }, '0x')
  return hash
}
