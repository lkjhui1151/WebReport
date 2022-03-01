import React from 'react'
import '../assets/css/dashboard.css'
import { MdOutlineSpaceDashboard } from 'react-icons/md';

function Dashboard() {
    return (
        <div className='title'>
            <div className="card">
                <MdOutlineSpaceDashboard style={{ color: "#ffffff", fontSize: "35px" }} />
            </div>
            <h2>DASHBOARD</h2>
        </div>
    )
}

export default Dashboard
