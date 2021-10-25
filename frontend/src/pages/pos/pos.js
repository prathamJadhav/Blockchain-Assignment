import React, { useState, useEffect } from 'react'
import './pos.css'
import axios from 'axios';
import AddNode from './addNode'
import Node from '../../components/node/node'
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';

function PoS() {

    const [nodes, setNodes] = useState([
        {
            node_name: "Test Node 1",
            stake: 32,
            node_id: 1
        },
        {
            node_name: "Test Node 2",
            stake: 64,
            node_id: 1
        },
        {
            node_name: "Test Node 3",
            stake: 128,
            node_id: 1
        },
        {
            node_name: "Test Node 4",
            stake: 128,
            node_id: 1
        },
        {
            node_name: "Test Node 5",
            stake: 128,
            node_id: 1
        }
    ])
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

    const getStakeUpdates = () => {
        if (nodes[0] == null) { return }
        axios.post('/api/viewStakeUpdates', {
            node_id: nodes[selected].node_id
        })
            .then((res) => {
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
                    <h2 className="node-title">Test Node 1</h2>
                    <table className="node-stake-table">
                        <tr>
                            <th>Block Hash</th>
                            <th>Timestamp</th>
                            <th>Stake Before</th>
                            <th>Reward/Penalty</th>
                        </tr>
                        <tr>
                            <td>asfsdf</td>
                            <td>12th October, 2021</td>
                            <td>32</td>
                            <td><span className="success"> +1.4 (+4.3%)</span></td>
                        </tr>
                        <tr>
                            <td>gdffd</td>
                            <td>13th October, 2021</td>
                            <td>32</td>
                            <td><span className="failure">-1.4 (-4.2%)</span></td>
                        </tr>
                        <tr>
                            <td>gdd</td>
                            <td>14th October, 2021</td>
                            <td>32</td>
                            <td><span className="success">+3 (+9.4%)</span></td>
                        </tr>
                        <tr>
                            <td>asfsdf</td>
                            <td>12th October, 2021</td>
                            <td>32</td>
                            <td><span className="success"> +1.4 (+4.3%)</span></td>
                        </tr>
                        <tr>
                            <td>gdffd</td>
                            <td>13th October, 2021</td>
                            <td>32</td>
                            <td><span className="failure">-1.4 (-4.2%)</span></td>
                        </tr>
                        <tr>
                            <td>gdd</td>
                            <td>14th October, 2021</td>
                            <td>32</td>
                            <td><span className="success">+3 (+9.4%)</span></td>
                        </tr>
                        <tr>
                            <td colSpan="3">Initial Stake</td>
                            <td>32</td>
                        </tr>
                        <tr>
                            <td colSpan="3">Final Stake</td>
                            <td>35 <span className="success">(+9.3%)</span></td>
                        </tr>

                    </table>
                </div>

            </div >
            <div className="add-node-container">
                <AddNode />
            </div>

        </div >
    )
}

export default PoS
