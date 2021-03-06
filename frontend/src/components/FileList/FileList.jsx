import React from 'react'
import './fileList.css'
import FileItem from '../FileItem/FileItem'

import { v4 as uuidv4 } from 'uuid'

const FileList = ({ files, removeFile, type }) => {
    const deleteFileHandler = (_name) => {
        removeFile(_name)
        // axios.post("http://localhost:8000/ReportVA/company-add/", _name)
        //     .then((res) => removeFile(_name))
        //     .catch((err) => console.error(err));
    }

    return (
        <div className="file-card-container">

            <ul className='file-list'>
                {
                    type == 'iso' &&
                    files.map(f => <FileItem key={uuidv4()} file={f} deleteFile={deleteFileHandler} />)
                }
                {
                    type == 'nessus' &&
                    files.map(f => {
                        if (f.file) {
                            return <FileItem key={uuidv4()} file={f.file} deleteFile={deleteFileHandler} />
                        }
                        else {
                            return <FileItem key={uuidv4()} file={f} deleteFile={deleteFileHandler} />
                        }
                    })
                }
                {
                    type == 'web' &&
                    files.map(f => {
                        if (f.file) {
                            return <FileItem key={uuidv4()} file={f.file} deleteFile={deleteFileHandler} />
                        }
                        else {
                            return <FileItem key={uuidv4()} file={f} deleteFile={deleteFileHandler} />
                        }
                    })
                }
                {
                    type == 'infra' &&
                    files.map(f => {
                        if (f.file) {
                            return <FileItem key={uuidv4()} file={f.file} deleteFile={deleteFileHandler} />
                        }
                        else {
                            return <FileItem key={uuidv4()} file={f} deleteFile={deleteFileHandler} />
                        }
                    })
                }
            </ul>

        </div>
    )
}

export default FileList
