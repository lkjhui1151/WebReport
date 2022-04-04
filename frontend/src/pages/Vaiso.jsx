import React, { useState, useEffect } from 'react'
import ReactFlexyTable from "react-flexy-table"
import "react-flexy-table/dist/index.css"
import '../assets/css/iso.css'
import { AiOutlineSecurityScan } from 'react-icons/ai';
import FileUpload from '../components/FileUpload/FileUpload';
import FileList from '../components/FileList/FileList';
// import axios from 'axios';
import { MdDelete } from 'react-icons/md';
import { AiOutlineDownload } from 'react-icons/ai';



function Vaiso() {

    const [files, setFiles] = useState([])
    const [data, setGET] = useState([]);
    
    const removeFile = (filename) => {
        setFiles(files.filter(file => file.name !== filename))
    }

    // console.log(api);
    useEffect(() => {
        const doFetch = async () => {
            const response = await fetch("http://localhost:8000/ReportVA/company-detail/iso")
            const body = await response.json()
            const contacts = body
            // console.log(contacts)
            setGET(contacts)
        }
        doFetch()
    }, [])

    const additionalCols = [{
        header: "Actions",
        td: (data) => {
            return <div>
                <MdDelete className='icon' onClick={() => alert("this is delete for id " + data.id)} />
                <AiOutlineDownload className='icon' onClick={() => alert("this is download for id " + data.id)} />
            </div>
        }
    }]

    return (
        <div>
            <div className='title'>
                <div className="card">
                    <AiOutlineSecurityScan style={{ color: "#ffffff", fontSize: "35px" }} />
                </div>
                <h2>VA SCAN ISO</h2>
            </div>
            <div className="iso-container">
                <FileUpload files={files} setFiles={setFiles} removeFile={removeFile} />
                <FileList files={files} removeFile={removeFile} />
            </div>
            <ReactFlexyTable data={data} filterable nonFilterCols={["id", "file", "type"]} additionalCols={additionalCols} />
        </div>
    )
}

export default Vaiso
