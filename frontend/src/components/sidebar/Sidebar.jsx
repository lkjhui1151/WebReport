import React from 'react'
import '../../assets/css/sidebar.css'
import dog from '../../assets/dog.jpg'

function Sidebar() {
    return (
        <div>
            <ul>
                <li>
                    <img src={dog} />
                    <p>Dog Hong_Hong</p>
                </li>
                <div className='horizontal'></div>
            </ul>
        </div>
    )
}

export default Sidebar
