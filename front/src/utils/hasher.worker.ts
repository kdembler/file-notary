import { sha3_256 } from 'js-sha3'

const worker: Worker = self as any

worker.addEventListener('message', async ({ data }) => {
  const file = data as File | Blob

  const fileContent = await readFileContent(file)

  const hash = sha3_256(fileContent)
  worker.postMessage(`0x${hash}`)

  // Worker type doesn't contain 'close' fn
  ;(worker as any).close()
})

const readFileContent = async (file: File | Blob): Promise<ArrayBuffer> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => {
      if (reader.readyState !== reader.DONE || !reader.result) {
        reject()
        return
      }
      resolve(reader.result as ArrayBuffer)
    }
    reader.readAsArrayBuffer(file)
  })
}
