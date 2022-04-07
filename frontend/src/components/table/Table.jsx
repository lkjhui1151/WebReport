import React from 'react'
import ReactFlexyTable from "react-flexy-table"
import "./table.css"
import { MdDelete } from 'react-icons/md';
import { AiOutlineDownload } from 'react-icons/ai';

const Table = (props) => {

    const additionalCols = [{
        header: "Actions",
        td: (data) => {
            return <div>
                <MdDelete className='icon' onClick={() => props.deleteFile(data.id, data.name)} />
                <AiOutlineDownload className='icon' onClick={() => alert("this is download for id " + data.id)} />
            </div>
        }
    }]
    return (
        <div>
            <ReactFlexyTable data={props.data} filterable nonFilterCols={["id", "file", "type"]} additionalCols={additionalCols} />
        </div>
    )
}

export default Table
