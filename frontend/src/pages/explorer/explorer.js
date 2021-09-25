import React, { useState, useEffect } from 'react'
import './explorer.css'
import Block from '../../components/block/block'
import axios from 'axios';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

function Explorer() {

    const responsive = {
        superLargeDesktop: {
            // the naming can be any, depends on you.
            breakpoint: { max: 4000, min: 3000 },
            items: 5
        },
        desktop: {
            breakpoint: { max: 3000, min: 1024 },
            items: 3
        },
        tablet: {
            breakpoint: { max: 1024, min: 464 },
            items: 2
        },
        mobile: {
            breakpoint: { max: 464, min: 0 },
            items: 1
        }
    };

    const [blocks, setBlocks] = useState([])
    const [selected, setSelected] = useState(0)
    const [transactions, setTransactions] = useState([])
    const [creationInProgess, setCreationInProgress] = useState(false)
    const [verificationInProgress, setVerificationInProgress] = useState(false)

    useEffect(() => {
        getTransactions()
    }, [blocks, selected])

    useEffect(() => {
        // first load of the app
        getBlocks()
    }, []);

    const getBlocks = () => {
        axios.get('/api/viewBlocks')
            .then((res) => {
                console.log(res.data)
                setBlocks(res.data)
            })
            .catch((err) => {

            })
    }
    const getDateString = (unixTimestamp) => {
        const date = new Date(unixTimestamp * 1000)
        return date.toLocaleString()
    }


    const verifyTransactions = (e) => {
        if (creationInProgess) { return }
        e.preventDefault()
        setCreationInProgress(true)
        console.log('verify clicked')
        axios.get('/api/verifyTransaction')
            .then((res) => {
                console.log(res)
                getBlocks()
                setCreationInProgress(false)
            })
            .catch((err) => {
                console.log(err)
                setCreationInProgress(false)
            })
    }

    const verifyBlockchain = (e) => {
        e.preventDefault()
        setVerificationInProgress(true)
        axios.get('/api/verifyBlocks')
            .then((res) => {
                setVerificationInProgress(false)
                if (!res.data.error) {
                    alert("Success")
                }
            })
            .catch((err) => {
                setVerificationInProgress(false)
                alert("Error")
            })
    }

    const getTransactions = () => {
        if (blocks[0] == null) { return }
        axios.post('/api/viewTransactions', {
            block_hash: blocks[selected].block_hash
        })
            .then((res) => {
                setTransactions(res.data)
            })
    }

    return (
        <div className="explorer-container">
            <div className="verify-button-label">
                <h4 onClick={verifyBlockchain}>{!verificationInProgress ? "Verify Blockchain" : "Verifying..."}</h4>
                <h4 onClick={verifyTransactions}>{!creationInProgess ? "+ Create Block" : "Creating..."}</h4>
            </div>

            <Carousel responsive={responsive} containerClass="main-blocks-container">
                {blocks.map((block, index) => {
                    return (
                        <div className="main-block-container"><Block block={block} selected={index == selected} index={index} setSelected={setSelected} /></div>
                    )
                })}
                {/* <div className="main-block-container-verify">
                    <h3>Unverified Transactions</h3>
                    <p>Some transactions many have not been verified yet. Click verify to create a new block and view its transactions.</p>
                    <button onClick={verifyTransactions}>Verify</button>
                </div> */}
            </Carousel>
            <br />
            <br />
            <div className="main-block-content">
                <div className="main-block-header">{blocks[selected] == null || blocks[selected].block_height == 0 ? "GENESIS BLOCK" : "BLOCK"}</div>
                <div className="main-block-title">{"Block #" + (blocks[selected] == null ? "1" : blocks[selected].block_height)}</div>
                <br />
                <div className="main-block-content-label height">{"Height: " + (blocks[selected] == null ? "1" : blocks[selected].block_height)}</div>
                <div className="main-block-content-label hash">{"Hash: " + (blocks[selected] == null ? "2" : blocks[selected].block_hash)}</div>
                <div className="main-block-content-label prev">{"Previous Hash: " + (blocks[selected] == null ? "2" : blocks[selected].previous_block_hash)}</div>
                <div className="main-block-content-label time">{"Time: " + (blocks[selected] == null ? "0" : getDateString(blocks[selected].timestamp))}</div>
                <br />
                <div className="main-block-title">Transactions</div>

                <table className="main-block-transactions-table">
                    <tr>
                        <th>Transaction ID</th>
                        <th>Customer Name</th>
                        <th>Amount</th>
                        <th>Time</th>
                    </tr>
                    {
                        transactions.map((transaction) => {
                            return (
                                <tr>
                                    <td>{transaction.tid}</td>
                                    <td>{transaction.customer}</td>
                                    <td>{transaction.amount}</td>
                                    <td>{getDateString(transaction.timestamp)}</td>
                                </tr>
                            )
                        })}
                </table>
            </div>

        </div >
    )
}

export default Explorer
