import React, { useState } from 'react'
import '../assets/css/iso.css'
import { AiOutlineSecurityScan } from 'react-icons/ai';
import FileUpload from '../components/FileUpload/FileUpload';
import FileList from '../components/FileList/FileList';

function Vaiso() {

    const [files, setFiles] = useState([])
    const [status, setStatus] = useState("")

    const removeFile = (filename) => {
        setFiles(files.filter(file => file.name !== filename))
    }

    function handleSubmit(e) {
        e.preventDefault();
        setStatus("POST")
    }


    console.log(status);

    return (
        <div>
            <div className='title'>
                <div className="card">
                    <AiOutlineSecurityScan style={{ color: "#ffffff", fontSize: "35px" }} />
                </div>
                <h2>VA SCAN ISO</h2>
            </div>
            <div className="iso-container">
                <FileUpload files={files} setFiles={setFiles} removeFile={removeFile} status={status} />
                <div className='vertical-line'></div>
                <FileList files={files} removeFile={removeFile} />
            </div>
            <form onSubmit={handleSubmit}>
                <button type="submit">Submit</button>
            </form>
        </div>
    )
}

export default Vaiso
