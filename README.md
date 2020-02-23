# FileNotary

File Notary is a simple blockchain-based notarization service letting you verify the authenticity of your files.

## Overview

File Notary consists of a frontend app for managing your files and a backend that processes these files. Each file is uploaded to Amazon S3 for storage. At the same time, the hash of the file is calculated with SHA-3 and saved in a Smart Contract on Ethereum Blockchain. Upon downloading, the hash is calculated once again and compared with the one saved in the Ethereum. After that verification, you can tell with a certainty that the file wasn't modified after the upload.

## Usage

1. Clone the repo

```sh
https://github.com/kdembler/file-notary
cd file-notary/
```

2. Copy `.env.example` file as `.env` and provide needed env variables

3. Install contract deployment dependencies

```sh
cd contract/
yarn # or npm install
```

4. Deploy the contract

```sh
yarn migrate:kovan # or npm run migrate:kovan
```

5. Build Docker containers

```sh
cd ..
docker build -t file-notary-frontend front
docker build -t file-notary-backend notary
```

6. Start the `docker-compose`

```sh
docker-compose up
```

7. After the compose starts, the frontend will be available at `localhost:80`

## License

MIT © Klaudiusz Dembler
