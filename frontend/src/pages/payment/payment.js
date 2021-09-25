import React, { useState } from 'react'
import { v4 as uuidv4 } from 'uuid';
import './payment.css'
import axios from 'axios';

function str2ab(str) {
    const buf = new ArrayBuffer(str.length);
    const bufView = new Uint8Array(buf);
    for (let i = 0, strLen = str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}


async function importRsaPrivateKey(pem) {
    const pemHeader = "-----BEGIN PRIVATE KEY-----";
    const pemFooter = "-----END PRIVATE KEY-----";

    var pemContents = pem.replace(pemHeader, "").replace(pemFooter, "")
    pemContents = pemContents.replace(/(\r\n|\n|\r)/gm, "");
    const binaryDerString = window.atob(pemContents);
    const binaryDer = str2ab(binaryDerString);
    return await window.crypto.subtle.importKey(
        "pkcs8",
        binaryDer,
        {
            name: "RSASSA-PKCS1-v1_5",
            hash: "SHA-256"
        },
        true,
        ["sign"]
    );
}

function Payment() {
    const [name, setName] = useState("")
    const [amount, setAmount] = useState("")
    const [privateKey, setPrivateKey] = useState("")
    const [inProgess, setInProgress] = useState(false)
    const [status, setStatus] = useState("")
    const [success, setSuccess] = useState(false)
    const updateVal = (e) => {
        setName(e.target.name == "name" ? e.target.value : name)
        setAmount(e.target.name == "amount" ? e.target.value : amount)
        setPrivateKey(e.target.name == "privateKey" ? e.target.value : privateKey)
    }
    const clickBtn = (e) => {
        e.preventDefault()
        if (inProgess) { return }
        // validate data
        if ((isNaN(amount) || isNaN(parseFloat(amount))) || name.trim() == "") {
            alert('Invalid format')
            return
        }
        const tid = uuidv4()
        const payload = {
            name: name,
            amount: amount,
            tid: tid
        }
        importRsaPrivateKey(privateKey)
            .then((privateKeyObj) => {
                setInProgress(true)
                const stringifiedPayload = JSON.stringify(payload)
                console.log(stringifiedPayload)
                window.crypto.subtle.sign({ "name": "RSASSA-PKCS1-v1_5" }, privateKeyObj, Buffer.from(stringifiedPayload))
                    .then((signature) => {
                        const signFinal = btoa(String.fromCharCode.apply(null, new Uint8Array(signature)));
                        console.log("Final Signature:", signFinal)
                        // send the network request
                        const data = {
                            "customer": name,
                            "tid": tid,
                            "amount": amount,
                            "message": stringifiedPayload,
                            "signature": signFinal
                        }
                        axios.post('/api/addTransaction', data)

                            .then((res) => {
                                console.log(res)
                                setName('')
                                setAmount(0)
                                setInProgress(false)
                                setStatus(res.data.message)
                                setSuccess(!res.data.error || true)
                            })
                            .catch((err) => {
                                console.log(err)
                                setInProgress(false)
                                setStatus('An error occurred')
                                setSuccess(false)
                            })

                    })
                    .catch((err) => {
                        alert('Error in reading private key file. Please make sure that the file is in the proper format.')
                    })

            })
            .catch((err) => {
                alert('Error in reading private key file. Please make sure that the file is in the proper format.')
            })
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

    return (
        <div className="payment-container">
            <form onSubmit={clickBtn}>
                <h2>Add a Transaction</h2>
                <br />
                <div className="payment-header">CUSTOMER NAME</div>
                <div className="payment-input-container">
                    <input width="pixels" className="payment-input" value={name} onChange={updateVal} name="name"></input>
                </div>
                <br /><br />
                <div className="payment-header">AMOUNT</div>
                <div className="payment-input-container">
                    <input width="pixels" className="payment-input" value={amount} onChange={updateVal} name="amount"></input>
                </div>
                <br /><br />
                <div className="payment-header">YOUR PRIVATE KEY</div>
                <input type="file" onChange={uploadFile}></input>
                <br /><br /><br /><br />
                <div className="payment-button-container">
                    <button className="submit-button" type="submit">{inProgess ? "Submitting..." : "Submit"}</button>
                </div>
                <br />
                <div className={"status-indicator " + (success ? "success" : "failure")}>{inProgess ? "" : status}</div>
            </form>
        </div>
    )
}

export default Payment
