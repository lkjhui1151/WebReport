import React, { useState } from 'react'
import '../assets/css/iso.css'
import { AiOutlineSecurityScan } from 'react-icons/ai';
import FileUpload from '../components/FileUpload/FileUpload';
import FileList from '../components/FileList/FileList';

function Vaiso() {

    const [files, setFiles] = useState([])


    const removeFile = (filename) => {
        setFiles(files.filter(file => file.name !== filename))
    }

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

        </div>
    )
}

export default Vaiso
