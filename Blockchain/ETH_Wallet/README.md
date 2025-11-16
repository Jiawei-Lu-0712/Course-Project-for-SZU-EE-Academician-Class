# Ethereum Wallet GUI

A desktop Ethereum wallet application built with Python and Tkinter. This wallet allows users to create new Ethereum accounts, manage existing ones, and send transactions on the Ethereum network. It also includes a feature to encrypt and store private keys locally using a short password for convenient access.

## Features

- **Create New Wallet**: Generate a new Ethereum account, including a private key, public address, and a mnemonic phrase.
- **QR Code Generation**: A QR code is generated upon wallet creation, containing the address, private key, and mnemonic phrase for easy backup.
- **Login Options**: Access your wallet using either your full private key or a previously set short password.
- **Account Dashboard**: View your wallet address, current balance in Ether, and the network you are connected to.
- **Send Transactions**: Send Ether to any other Ethereum address with the ability to include custom data.
- **Transaction History**: View a list of transactions made during the current session.
- **Export Transactions**: Export your session's transaction history as a PDF file.
- **Secure Short Password**: Set a short, memorable password that encrypts your private key for local storage. This allows for quicker logins without needing to enter the full private key each time.
- **Update Password**: Functionality to verify an old password and set a new one for your stored account.

## Screenshots

The application consists of three main windows:

1.  **Login Window**: The initial screen where you can enter a private key or a short password to access your wallet. It also provides options to create a new wallet or exit the application.
2.  **Create Wallet Window**: This window allows you to generate a new Ethereum account. It displays the new address and a QR code that contains the address, private key, and mnemonic phrase.
3.  **Account Information Window**: This is the main dashboard after logging in. It displays your account details (address, balance), provides fields to send a transaction, and shows a log of your transactions for the current session.

## Installation

1.  **Install the required libraries:**
    ```bash
    pip install web3 Pillow qrcode pycryptodome reportlab mnemonic