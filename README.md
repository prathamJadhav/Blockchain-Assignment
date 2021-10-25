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

## New in Assignment 2 (Implementation of PoS consensus algorithm)
### Changes in Frontend and codebase
#### Backend
- Routes for adding, getting nodes and recieving stake updates have been added to `app.py`
- The lot selection process for PoS has been done in `Proof of Stake.py` and `Lot.py`
- The validation functions for nodes have been added to `node.py`
#### Frontend
- A new page has been created for PoS, the code for which is in the `frontend/src/pages/pos` folder
- A screenshot of the new page on the web portal is given below:

![PoS](/documentation/resources/pos.png)


### Basic Overview
In the Proof of Stake consensus algorithm, several nodes participate in the block forging and validation process by putting down a stake as collateral during the validation process. This incentivizes the nodes to correctly forge and validate blocks, on doing which they recieve a reward or are penalized when doing so incorrectly. 
### Adding a new node
Since we are not dealing with a cryptocurrency, but using a blockchain for the purpose of storing transactions for Dexter's coffee shop, it is assumed that the stake is paid to Dexter in fiat currency.   
In the PoS section of the web portal, an option exists for Dexter to add a new node to the Blockchain. Here, he can input the node name and stake that they have put down. To make sure that it is Dexter who is adding these new nodes, the data is signed with his private key and then verified at the server. To prevent duplicating nodes by sending the same request as Dexter, a unique ID is generated for each node, so that the signature is different every time. 
Once verified, the node details are stored in the database.
We can see the 'Add Node' option on the right in the image given above.

### Simulating Node Behaviour
Since it is not possible for us to run nodes in a P2P network due to time constraint and complexity, we decided to simulate node behaviour in the backend itself. 

### Simulating Byzantine Behaviour
In order to show that byzantine nodes that validate blocks incorrectly are punished, we simulate incorrect results for some nodes. Every node has a 1/15 chance of displaying byzantine behaviour. When this behaviour is identified by other nodes during validation, a small fee is cut from the stake of this node.

### Forging and validating a block
When a new block needs to be created, a node is selected with probability proportionate to its stake in the system. This node forges the new block (creates merkle root, sets previous block hash, etc.). The other blocks then validate this newly created block. Once consensus is reached, the forgers and validators who took the right decision are rewarded, and those who displayed byzantine behaviour are punished. 

### Viewing the stake details
In the main section in the PoS tab, we can see a list of nodes that have participated in the PoS consensus mechanism. On selecting a node, we can see a table displaying the stake history for that node. Columns include the block hash (for the block for which the reward/penalty was generated), timestamp, initial stake and net profit/loss. The nodes that are in consensus have profit hightlighted in green and byzantine nodes have loss highlighted in red. the last two rows indicate the initial stake that was put down as well as the stake at the moment.

The above image of the PoS tab shows the stake history for one of the nodes.

A block diagram of the PoS process is given below:


![PoS Diagram](/documentation/resources/pos_diagram.png)

Note: In an actual PoS system, each node must have its own copy of transactions. However, since we are simulating nodes through software, the nodes will use a shared pool of unverified transactions for forging and validation. Any inconsistencies in transactions between nodes is simulated using the byzantine nodes as mentioned above.

## Installation

### Backend:

Use a virtual environment to set up the python modules.
```sh
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Frontend:
```sh
cd frontend/
npm install
npm run build
cd ..
```
After the installation is complete, run the project:
```
python app.py
```
The app will start on port `9000` by default, it should be running at localhost:9000



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

The private key for testing purposes can be found at:
https://drive.google.com/file/d/1Y6I3l-4CrExcwah7JW82Ic6PeImKOmO_/view?usp=sharing

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
