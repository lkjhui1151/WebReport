import React from 'react'
import './fileList.css'
import FileItem from '../FileItem/FileItem'

import { v4 as uuidv4 } from 'uuid'

const FileList = ({ files, removeFile }) => {

    const deleteFileHandler = (_name) => {
        removeFile(_name)
        // axios.post("http://localhost:8000/ReportVA/company-add/", _name)
        //     .then((res) => removeFile(_name))
        //     .catch((err) => console.error(err));
    }

    return (
        <div className="file-card-container">
            <div className='file-card-list'>
                <ul className='file-list-upload'>
                    {
                        files &&
                        files.map(f => <FileItem key={uuidv4()} file={f} deleteFile={deleteFileHandler} />)
                    }
                </ul>
            </div>
        </div>
    )
}

export default FileList
