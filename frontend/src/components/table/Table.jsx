import React, { useState } from 'react'
import ReactFlexyTable from "react-flexy-table"
import "./table.css"
import { MdDelete } from 'react-icons/md';
import { AiOutlineDownload } from 'react-icons/ai';
import Model, { ModelBody, ModelFooter, ModelHeader } from '../models/Model';
import { saveAs } from "file-saver";
import Button from '../Button/Button';

const Table = (props) => {

    const [showModel, setShowModel] = useState(false)
    const [stateID, setStateID] = useState([])
    const [stateName, setStateName] = useState([])
    const saveFile = (name) => {
        name = name + ".docx"
        saveAs(
            "http://10.11.101.32/web/report/media/report/" + name,
            name
        );
    }
    const additionalCols = [{
        header: "Actions",
        td: (data) => {
            return <div>
                <MdDelete className='icon' onClick={() => { setStateID(data.id); setStateName(data.name); setShowModel(true) }} />
                <Model show={showModel}>
                    <ModelHeader>
                        <h2>Delete File</h2>
                    </ModelHeader>
                    <ModelBody >
                        <p style={{ textAlign: 'justify' }}>Do you want to delete the file <b>{stateName}</b>?</p>
                    </ModelBody>
                    <ModelFooter>
                        <Button onClick={() => setShowModel(false)}>
                            Close
                        </Button>
                        <button className='file-delete' onClick={() => props.deleteFile(stateID)}>
                            Confirm
                        </button>
                    </ModelFooter>
                </Model>
                <AiOutlineDownload className='icon' onClick={() => saveFile(data.name)} />
            </div>
        }
    }]
    return (
        <>
            <div>
                <ReactFlexyTable data={props.data} filterable nonFilterCols={["id", "file", "type"]} additionalCols={additionalCols} />
            </div>

        </>
    )
}

export default Table
