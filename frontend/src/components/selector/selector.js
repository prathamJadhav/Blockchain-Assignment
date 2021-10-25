import React, { useState } from 'react'
import './selector.css'

function Selector(props) {
    const [selected, setSelected] = useState(0)
    const getSelectedClassName = (s) => {
        return "selector-item " + (s == selected ? "selected" : "")
    }
    const setSelectedPayment = () => {
        setSelected(0)
        props.setSelected(0)
    }
    const setSelectedExplorer = () => {
        setSelected(2)
        props.setSelected(2)
    }
    const setSelectedNode = () => {
        setSelected(1)
        props.setSelected(1)
    }

    return (
        <div className="selector-container">
            <div className={getSelectedClassName(0)} onClick={setSelectedPayment}>
                PAYMENT
            </div>
            <div className={getSelectedClassName(1)} onClick={setSelectedNode}>
                PoS
            </div>
            <div className={getSelectedClassName(2)} onClick={setSelectedExplorer}>
                EXPLORER
            </div>
        </div>
    )
}

export default Selector
