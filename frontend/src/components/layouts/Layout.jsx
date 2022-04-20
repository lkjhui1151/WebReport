import React from 'react'
import './layout.css'
import Time from '../time/Time';
import Dashboard from '../../pages/Dashboard';
import Vaiso from '../../pages/Vaiso';
import { BrowserRouter, Route, Link, Routes } from 'react-router-dom'
import Vanessus from '../../pages/Vanessus';
import VanessusWeb from '../../pages/VanessusWeb';
import VanessusInfra from '../../pages/VanessusInfra';



function Layout() {
    return (
        <div className='container'>
            <BrowserRouter>
                <div className="main">
                    <div className="topbar">
                        <div className="navbar">
                            <ul className='item-list'>
                                <li><Link to="/">Monthly Report</Link></li>
                                <div className="dropdown">
                                    <button className="dropbtn">VA SCAN
                                        <i className="fa-solid fa-circle-chevron-down"></i>
                                    </button>
                                    <div className="dropdown-content">
                                        <Link to="/iso">ISO</Link>
                                        <Link to="/nessus">NESSUS</Link>
                                        <Link to="/nessus-web">WEB</Link>
                                        <Link to="/nessus-infra">INFRA</Link>
                                    </div>
                                </div>
                            </ul>
                        </div>

                        <div className="detail">
                            <Time />
                        </div>
                    </div>
                    <div className="cardBox">
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/iso" element={<Vaiso />} />
                            <Route path="/nessus" element={<Vanessus />} />
                            <Route path="/nessus-web" element={<VanessusWeb />} />
                            <Route path="/nessus-infra" element={<VanessusInfra />} />
                        </Routes>
                    </div>
                </div>
            </BrowserRouter>
        </div>
    )
}

export default Layout
