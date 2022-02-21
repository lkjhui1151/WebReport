import React from 'react'
import './sidebars.css'
import { Link } from 'react-router-dom'
import { MdDashboard } from "@react-icons/all-files/md/MdDashboard";
import { AiFillSecurityScan } from "@react-icons/all-files/ai/AiFillSecurityScan"

const sidebarNavItems = [
    {
        display: 'Dashboard',
        icon: <MdDashboard />,
        to: '/',
        section: ''
    },
    {
        display: 'Vulnerability Analysis',
        icon: <AiFillSecurityScan />,
        to: '/va-scan',
        section: 'va-scan'
    },
]

const Sidebar = () => {
    return (
        <div className='sidebar'>
            <div className="sidebar_menu">
                <div className="sidebar_menu_indicator">
                    {
                        sidebarNavItems.map((item, index) => (
                            <Link to={item.to} key={index}>
                                <div className="sidebar_menu_item">
                                    <div className="sidebar_menu_item_icon">
                                        {item.icon}
                                    </div>
                                    <div className="sidebar_menu_item_text">
                                        {item.display}
                                    </div>
                                </div>
                            </Link>
                        ))
                    }
                </div>
            </div>
        </div>
    )
}

export default Sidebar
