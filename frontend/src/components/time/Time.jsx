import React, { useState, useEffect } from 'react'
import './time.css'
import { AiOutlineClockCircle, AiOutlineCalendar } from 'react-icons/ai';
// import { BsFillCalendarEventFill } from 'react-icons/bs';


function Time() {
    const [dateState, setDateState] = useState(new Date())
    useEffect(() => {
        setInterval(() => setDateState(new Date()), 10000);
    }, []);

    return (
        <div className='TimeCalenda'>
            <AiOutlineClockCircle />
            <p>
                {dateState.toLocaleString('en-US', {
                    hour: 'numeric',
                    minute: 'numeric',
                    hour12: true,
                })}
            </p>

            <AiOutlineCalendar />
            <p>
                {' '}
                {dateState.toLocaleDateString('en-GB', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                })}
            </p>
        </div>
    )
}

export default Time
