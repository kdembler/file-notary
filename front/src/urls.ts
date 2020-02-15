const apiUrl = 'http://localhost:5000'

export const loginUrl = `${apiUrl}/login`
export const registerUrl = `${apiUrl}/register`
export const filesUrl = `${apiUrl}/files`
export const fileDetailsUrl = (fileId: string) => `${filesUrl}/${fileId}`
