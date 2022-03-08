import React from 'react'
import '../assets/css/dashboard.css'
import { AiOutlineSecurityScan } from 'react-icons/ai';

function Vanessus() {
    return (
        <div className='title'>
            <div className="card">
                <AiOutlineSecurityScan style={{ color: "#ffffff", fontSize: "35px" }} />
            </div>
            <h2>VA SCAN NESSUS</h2>
        </div>
    )
}


export default Vanessus
