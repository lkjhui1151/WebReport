import React from 'react'
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom'
import '../../assets/css/navigatebar.css'
import { NavigateItem } from './NavigateItem';

function Navigatebar() {
    let list = document.querySelectorAll('.navigation li');
    function activeLink() {
        list.forEach((item) =>
            item.classList.remove(''))
        this.classList.add('hovered')
    }
    list.forEach((item) =>
        item.addEventListener('mouseover', activeLink))

    return (
        <div className='container'>
            <div className="navigation">
                <BrowserRouter>
                    <ul >
                        <li>
                            <Link to="/VA-SCAN/profile">
                                <span className='title'>Profile</span>
                            </Link>
                        </li>
                        <li className={list}>
                            <Link to="/VA-SCAN/iso">
                                <span className='title'>ISO</span>
                            </Link>
                        </li>
                        <li className={list}>
                            <Link to="/VA-SCAN/nessus">
                                <span className='title'>NESSUS</span>
                            </Link>
                        </li>
                    </ul>
                    <Switch>
                        <Route path='/VA-SCAN/iso' exact>
                            {/* <h1>ISO</h1> */}
                        </Route>
                        <Route path='/VA-SCAN/nessus' exact>
                            {/* <h1>NUSSES</h1> */}
                        </Route>
                        <Route path='/VA-SCAN/profile' exact>
                            {/* <h1>NUSSES</h1> */}
                        </Route>
                    </Switch>
                </BrowserRouter>
            </div>
        </div>
    )
}

export default Navigatebar
