import React from 'react'

import { Route, Switch } from 'react-router-dom'

import Dashboard from '../pages/Dashboard'
import Customers from '../pages/Customers'
import Calendars from '../pages/Calendars'
import VAScan from '../pages/VAScan'

const Routes = () => {
    return (
        <Switch>
            <Route path='/' exact component={Dashboard} />
            <Route path='/calendar' component={Calendars} />
            <Route path='/vulnerability-scan' component={VAScan} />
            <Route path='/customers' component={Customers} />
        </Switch>
    )
}

export default Routes
