import React, { useState, useEffect } from 'react'
import './node.css'
import axios from 'axios';

function Node() {

    const clickBtn = (e) => {
        e.preventDefault()
    }

    const updateVal = (e) => {
        setName(e.target.name == "name" ? e.target.value : name)
        setStake(e.target.name == "stake" ? e.target.value : stake)
        setPrivateKey(e.target.name == "privateKey" ? e.target.value : privateKey)
    }

    const uploadFile = async (e) => {
        e.preventDefault()
        const reader = new FileReader()
        reader.onload = async (e) => {
            const text = e.target.result
            setPrivateKey(text)
        };
        reader.readAsText(e.target.files[0])
    }

    const [name, setName] = useState("")
    const [stake, setStake] = useState(0)
    const [privateKey, setPrivateKey] = useState("")
    const [inProgess, setInProgress] = useState(false)
    const [status, setStatus] = useState("")
    const [success, setSuccess] = useState(false)
    return (
        <div className="node-container">
            <form onSubmit={clickBtn}>
                <h2>Add A Validator Node (PoS)</h2>
                <br />
                <div className="node-header">NODE NAME</div>
                <div className="node-input-container">
                    <input width="pixels" className="node-input" value={name} onChange={updateVal} name="name"></input>
                </div>
                <br /><br />
                <div className="node-header">STAKE</div>
                <div className="node-input-container">
                    <input width="pixels" className="node-input" value={stake} onChange={updateVal} name="stake"></input>
                </div>
                <br /><br />
                <div className="node-header">YOUR PRIVATE KEY</div>
                <input type="file" onChange={uploadFile}></input>
                <br /><br /><br /><br />
                <div className="node-button-container">
                    <button className="submit-button" type="submit">{inProgess ? "Submitting..." : "Submit"}</button>
                </div>
                <br />
                <div className={"status-indicator " + (success ? "success" : "failure")}>{inProgess ? "" : status}</div>
            </form>
            <br />
            <div>
                A node will add and verify new blocks onto the blockchain. A node is chosen to do so with a probability proportionate to the stake (security deposit) that the node has put down. On successfully forging/verification of a block, the node will recieve a reward, which will be added to its stake balance.
            </div>
        </div>
    )
}

export default Node
