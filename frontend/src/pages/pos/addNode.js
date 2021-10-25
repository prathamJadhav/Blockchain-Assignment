import React, { useState, useEffect } from 'react'
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';


function AddNode() {

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
    const [name, setName] = useState("")
    const [stake, setStake] = useState(0)
    const [privateKey, setPrivateKey] = useState("")
    const [inProgess, setInProgress] = useState(false)
    const [status, setStatus] = useState("")
    const [success, setSuccess] = useState(false)

    const clickBtn = (e) => {
        e.preventDefault()
        if (inProgess) { return }
        // validate data
        if ((isNaN(stake) || isNaN(parseFloat(stake))) || name.trim() == "") {
            alert('Invalid format')
            return
        }
        const nid = uuidv4()
        const payload = {
            node_name: name,
            stake: stake,
            node_id: nid
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
                            "node_name": name,
                            "stake": stake,
                            "message": stringifiedPayload,
                            "node_id": nid,
                            "signature": signFinal
                        }
                        axios.post('/api/addNode', data)
                            .then((res) => {
                                console.log(res)
                                setName('')
                                setStake(0)
                                setInProgress(false)
                                setStatus(res.data.message)
                                setSuccess(!res.data.error || true)
                            })
                            .catch((err) => {
                                console.log(err.response)
                                setInProgress(false)
                                setStatus(err.response.data.message || 'An error occurred')
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

    return (
        <div>
            <form onSubmit={clickBtn}>
                <h2>Add a Node</h2>
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
        </div>
    )
}

export default AddNode
