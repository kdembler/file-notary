import HasherWorker from 'worker-loader!./hasher.worker'

export async function getFileHash(file: File): Promise<string> {
  return new Promise(resolve => {
    const worker = new HasherWorker()
    worker.postMessage(file)
    worker.onmessage = msg => resolve(msg.data)
  })
}
