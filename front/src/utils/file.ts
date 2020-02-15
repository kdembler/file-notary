import { FileInfo } from '@/types/fileInfo'

export function saveFile(file: FileInfo) {
  if (!file.objectUrl) {
    console.warn('Tried saving file without objectUrl')
    return
  }

  const a = document.createElement('a')
  a.href = file.objectUrl
  a.download = file.name
  document.body.appendChild(a)
  a.click()
}
