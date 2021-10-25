import React, { useState, useEffect } from 'react'
import './pos.css'
import axios from 'axios';
import AddNode from './addNode'
import Node from '../../components/node/node'
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

function PoS() {

    const [nodes, setNodes] = useState([])
    const [selected, setSelected] = useState(0)
    const [stakeUpdates, setStakeUpdates] = useState([])

    useEffect(() => {
        getStakeUpdates()
    }, [nodes, selected])

    useEffect(() => {
        // first load of the app
        getNodes()
    }, []);

    const getNodes = () => {
        axios.get('/api/viewNodes')
            .then((res) => {
                console.log(res.data)
                setNodes(res.data)
            })
            .catch((err) => {

            })
    }

    const getChangeString = (initialStake, finalStake) => {
        const percentage = ((finalStake - initialStake) * 100) / initialStake
        const stringP = percentage > 0 ? "+" : ""
        const fString = (finalStake - initialStake).toFixed(4) + " (" + stringP + (percentage.toFixed(2)) + "%)"
        return fString
    }

    const getFinalStakeString = (stakeUpdates) => {
        if (stakeUpdates.length == 0) {
            return "-"
        }
        const percentage = ((stakeUpdates[stakeUpdates.length - 1].finalStake - stakeUpdates[0].initialStake) * 100) / stakeUpdates[0].initialStake
        const stringP = percentage > 0 ? "+" : ""
        const fString = stakeUpdates[stakeUpdates.length - 1].finalStake.toFixed(4) + " (" + stringP + (percentage.toFixed(2)) + "%)"
        return fString
    }
    const getDateString = (unixTimestamp) => {
        const date = new Date(unixTimestamp * 1000)
        return date.toLocaleString()
    }

    const getColorAttribute = (initialStake, finalStake) => {
        const percentage = ((finalStake - initialStake) * 100) / initialStake
        return percentage >= 0 ? "success" : "failure"
    }
    const getFinalColorAttribute = (stakeUpdates) => {
        if (stakeUpdates.length == 0) {
            return ""
        }
        const percentage = ((stakeUpdates[stakeUpdates.length - 1].finalStake - stakeUpdates[0].initialStake) * 100) / stakeUpdates[0].initialStake
        return percentage >= 0 ? "success" : "failure"
    }

    const getStakeUpdates = () => {
        if (nodes[0] == null) { return }
        axios.post('/api/viewStakeUpdates', {
            node_id: nodes[selected].node_id
        })
            .then((res) => {
                console.log(res)
                setStakeUpdates(res.data)
            })
    }

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


    const setIndex = (e) => {
        console.log('setting index to: ', e.target.name)
        console.log(e.target)
        setSelected(e.target.name)
    }
    return (
        <div className="pos-main-container">
            <div className="nodes-container">
                <h2>PoS Nodes</h2>
                <Carousel responsive={responsive} containerClass="pos-nodes-list-container">
                    {
                        nodes.map((node, index) => {
                            return (
                                <Node setSelected={setSelected} index={index} selected={index == selected} node={node} />
                            )
                        })
                    }
                </Carousel>
                <br />
                <div className="selected-node-details-container">
                    <h2 className="node-title">{nodes.length == 0 ? "" : nodes[selected].node_name}</h2>
                    <table className="node-stake-table">
                        <tr>
                            <th>Block Hash</th>
                            <th>Timestamp</th>
                            <th>Stake Before</th>
                            <th>Reward/Penalty</th>
                        </tr>
                        {stakeUpdates.map((stakeUpdate) => {
                            return (
                                <tr>
                                    <td className="block_hash_table">{stakeUpdate.block_hash}</td>
                                    <td>{getDateString(stakeUpdate.timestamp)}</td>
                                    <td>{stakeUpdate.initialStake.toFixed(4)}</td>
                                    <td><span className={getColorAttribute(stakeUpdate.initialStake, stakeUpdate.finalStake)}>{getChangeString(stakeUpdate.initialStake, stakeUpdate.finalStake)}</span></td>
                                </tr>
                            )
                        })}
                        <tr>
                            <td colSpan="3">Initial Stake</td>
                            <td>{stakeUpdates.length > 0 ? stakeUpdates[0].initialStake : "-"}</td>
                        </tr>
                        <tr>
                            <td colSpan="3">Final Stake</td>
                            <td className={getFinalColorAttribute(stakeUpdates)}>{getFinalStakeString(stakeUpdates)}</td>
                        </tr>

                    </table>
                </div>

            </div >
            <div className="add-node-container">
                <AddNode getNodes={getNodes} />
            </div>

        </div >
    )
}

export default PoS
