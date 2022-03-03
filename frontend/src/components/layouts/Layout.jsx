import React from 'react'
import '../../assets/css/layout.css'

import { AiOutlineSearch, AiOutlineMenu } from 'react-icons/ai';
import { GiHamburgerMenu } from 'react-icons/gi';
import Time from '../time/Time';
import Sidebar from '../sidebar/Sidebar';
import Dashboard from '../../pages/Dashboard';
import { Route } from 'react-router-dom'


function Layout() {

    return (
        <div className='container'>
            <div className="navigation">
                <Sidebar />
            </div>
            <div className="main">
                <div className="topbar">
                    <div className="toggle">
                        <GiHamburgerMenu style={{ color: "#5f68f9" }} />
                    </div>
                    <div className="navbar">
                        <a href="#">Dashboard</a>
                        <a href="#">VA SCAN</a>
                    </div>
                    <div className="detail">
                        <Time />
                        <div className="divider"></div>
                        <div><a href="#">Log Out</a></div>
                    </div>
                </div>
                <div className="cardBox">
                    <Dashboard />
                </div>
            </div>
        </div>
    )
}

export default Layout
