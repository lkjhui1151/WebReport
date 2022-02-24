import React, { useState } from 'react'
import Calendar from 'react-calendar';
import '../assets/css/calendar.css'


function Calendars() {
    const [value, onChange] = useState(new Date());
    return (
        <div className='card'>
            <h2 className="page-header">Calendar</h2>
            <div className='calendar-container'>
                <Calendar
                    onChange={onChange}
                    value={value}
                    selectRange={true}
                />
            </div>
            {value.length > 0 ? (
                <p className='text-center'>
                    <span className='bold'>Start:</span>{' '}
                    {value[0].toDateString()}
                    &nbsp;|&nbsp;
                    <span className='bold'>End:</span> {value[1].toDateString()}
                </p>
            ) : (
                <p className='text-center'></p>
            )}
        </div>

    )
}

export default Calendars
