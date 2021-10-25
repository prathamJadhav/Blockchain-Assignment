import React from 'react'
import './node.css'

function Node(props) {
    const nodeSelected = () => {
        props.setSelected(props.index)
    }
    return (
        <div className={"pos-node-container " + (props.selected ? "selected" : "")} onClick={nodeSelected}>
            <h3>{props.node.node_name}</h3>
            <p>Stake: {props.node.stake}</p>
        </div>
    )
}

export default Node
