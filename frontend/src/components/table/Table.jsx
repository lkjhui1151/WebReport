import React, { useState } from 'react'
import ReactFlexyTable from "react-flexy-table"
import "./table.css"
import { MdDelete } from 'react-icons/md';
import { AiOutlineDownload } from 'react-icons/ai';
import Model from '../models/Model';

const Table = (props) => {

    const [openModel, setOpenModel] = useState(false)
    const saveFile = (name) => {

    }
    const additionalCols = [{
        header: "Actions",
        td: (data) => {
            return <div>
                <MdDelete className='icon' onClick={() => props.deleteFile(data.id, data.name)} />
                {/* <AiOutlineDownload className='icon' onClick={() => alert("this is download for id " + data.id)} /> */}
                <AiOutlineDownload className='icon' onClick={() => saveFile(data.name)} />
            </div>
        }
    }]
    return (
        <>
            {openModel && <Model closeModel={setOpenModel} />}
            <div>
                <ReactFlexyTable data={props.data} filterable nonFilterCols={["id", "file", "type"]} additionalCols={additionalCols} />
            </div>
        </>

    )
}

export default Table
