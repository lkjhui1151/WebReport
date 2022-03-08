import React from 'react'
import '../../assets/css/layout.css'

import { AiOutlineSearch, AiOutlineMenu } from 'react-icons/ai';
import { GiHamburgerMenu } from 'react-icons/gi';
import Time from '../time/Time';
import Sidebar from '../sidebar/Sidebar';
import Dashboard from '../../pages/Dashboard';
import Vaiso from '../../pages/Vaiso';
import { BrowserRouter, Route, Link, Routes } from 'react-router-dom'
import Vanessus from '../../pages/Vanessus';



function Layout() {


    return (
        <div className='container'>
            <BrowserRouter>
                <div className="navigation">
                    <Sidebar />
                </div>
                <div className="main">
                    <div className="topbar">
                        <div className="toggle">
                            <GiHamburgerMenu style={{ color: "#5f68f9" }} />
                        </div>
                        <div className="navbar">
                            <ul className='item-list'>
                                <li><Link to="/">Dashboard</Link></li>
                                <div className="dropdown">
                                    <button className="dropbtn">VA SCAN
                                        <i className="fa-solid fa-circle-chevron-down"></i>
                                    </button>
                                    <div className="dropdown-content">
                                        <Link to="/iso">ISO</Link>
                                        <Link to="/nessus">NESSUS</Link>
                                        {/* <Link to="/burp">Burp</Link> */}
                                    </div>
                                </div>
                            </ul>
                        </div>

                        <div className="detail">
                            <Time />
                            <div className="divider"></div>
                            <div><a href="#">Log Out</a></div>
                        </div>
                    </div>
                    <div className="cardBox">
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/iso" element={<Vaiso />} />
                            <Route path="/nessus" element={<Vanessus />} />
                        </Routes>
                    </div>
                </div>
            </BrowserRouter>
        </div>
    )
}

export default Layout
