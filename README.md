# Dexter's Coffee
## Group Details
Dexter's Coffee portal is our blockchain group assignment (Group 48).
The group members include:
- Aryan Chaubal (2019A7PS0130H)
- Harsh Gupta (2019A7PS0103H)
- Prathamesh Jadhav (2019A7PS0084H)

## Project Details
Dexter's Coffee is an online portal for Dexter to add transactions in a secure tamper-proof way. The transactions he creates are stored in a blockchain and are publicly viewable.

The online portal is hosted here: https://dexters-coffee.herokuapp.com


### Authentication
In order to make sure that Dexter is the one creating new transactions, he uses his private key to sign the transaction. The signature is then verified using the corresponding public key at the backend. If the signature matches, the transaction is created, otherwise, it fails.

An 2048-bit RSA keypair is used for this purpose. The shell script used to generate the RSA keypair is as follows:
```sh
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private.pem -out private2.pem
rm private.pem
mv private2.pem private.pem
```
This outputs two files: `private.pem` and `public.pem` which are the required keys.

The private key is stored securely with Dexter and the public key is stored at the backend for verification. 

Here is a screenshot of the payment page on the website.

![Payment](/documentation/resources/payment.png)

**Note**: Since a transaction having the same customer name and amount will have the same signature, an attacker can just intercept the request and keep sending them. To counter this, a UUID is bundled in the signed payload data which results in a different signature every time. The backend checks whether a transaction already exists with the given UUID. 

### Transaction Process
The backend recieves transactions and stores them in an unverified transactions table. When someone clicks on "Create new Block" on the Blockchain Explorer, a new block is created using these unverified transactions and the transactions are then stored as a part of that block.

### Blockchain Explorer
The website offers a user-friendly look at the blockchain though the Explorer tab. The top row contains the blockchain where the blocks are placed in order, starting from the Genesis block. 

A block can be selected from Blockchain Explorer. On selection of a block, its details like block hash, previous block hash, merkle root, timestamp, etc. are shown. A list of transactions is also shown, each consisting of the customer name, amount, timestamp and transaction ID.

A screenshot of the blockchain explorer page is shown below:

![Explorer](/documentation/resources/explorer.png)

## Tech Stack
### Backend
The backend (consisting of most of the blockchain code) is created in Python. The Flask framework is used for the REST API to interact with the frontend.

### Frontend
The frontend is created in React using JavaScript. The static build folder is served by the Flask App.

### Contributions
- Aryan Chaubal (Frontend, UI Design)
- Harsh Gupta (Backend, Database management)
- Prathamesh Jadhav (Backend, Testing)