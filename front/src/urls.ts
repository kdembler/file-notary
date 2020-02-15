const apiUrl = 'http://localhost:5000'

export const loginUrl = `${apiUrl}/login`
export const registerUrl = `${apiUrl}/register`
export const filesUrl = `${apiUrl}/files`
export const fileDetailsUrl = (fileId: string) => `${filesUrl}/${fileId}`

export const web3Url = 'wss://kovan.infura.io/ws/v3/d94c6d05fdac485d8e50a77ff1ff6793'
