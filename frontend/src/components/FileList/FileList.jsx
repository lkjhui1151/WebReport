import React, { useState } from 'react'
import '../../assets/css/fileList.css'
import FileItem from '../FileItem/FileItem'

const FileList = ({ files, removeFile }) => {
    const [status, setStatus] = useState("")

    const deleteFileHandler = ({ files, removeFile }) => {
        // axios.delete()
        // console.log(files);
    }

    return (
        <div className="file-card-container">
            <div className='file-card-list'>
                <ul className='file-list-upload'>
                    {
                        files &&
                        files.map(f => <FileItem key={f.name} file={f} deleteFile={deleteFileHandler} />)
                    }
                </ul>
            </div>
        </div>
    )
}

export default FileList
