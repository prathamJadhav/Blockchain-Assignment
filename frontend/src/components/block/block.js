import React from 'react'
import './block.css'

function Block(props) {

    const getDateString = (unixTimestamp) => {
        const date = new Date(unixTimestamp * 1000)
        return date.toLocaleString()
    }

    const setBlock = (e) => {
        console.log('block clicked')
        props.setSelected(props.index)
    }

    return (
        <div className={"block-container " + (props.selected ? "selected" : "")} onClick={setBlock}>
            <div className="title-header">{props.block.block_height == 0 ? 'GENESIS BLOCK' : 'BLOCK'}</div>
            <div className="title">{"Block #" + props.block.block_height}</div>
            <div className="content">Hash: <span>{props.block.block_hash}</span><br /></div>
            <div className="content">Prev: <span>{props.block.previous_block_hash || "N/A"}</span><br /></div>
            <div className="content">Merkle: <span>{props.block.merkleRoot || "asdf"}</span><br /></div>
            <div className="content">Time: {getDateString(props.block.timestamp)}<br /></div>
        </div>

    )
}

export default Block
