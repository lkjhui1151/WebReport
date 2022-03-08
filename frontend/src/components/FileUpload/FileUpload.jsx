import React from 'react'
import axios from 'axios';
import '../../assets/css/fileUpload.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'


const FileUpload = ({ files, setFiles, removeFile }) => {
    const uploadHandler = (event) => {
        const file = event.target.files[0]

        // const fileType = file.name.split(".");
        // console.log(fileType[fileType.length - 1])

        file.isUploading = true
        setFiles([...files, file])
        const formData = new FormData()
        formData.append('file', file);
        formData.append('fileName', file.name);
        const config = {
            headers: {
                'content-type': 'multipart/form-data',
            },
        };
        axios.post('http://localhost:8000/ReportVA/company-add/', formData, config)
            .then((res) => {
                file.isUploading = false
                setFiles([...files, file])
            })
            .catch((err) => {
                console.log(err);
                removeFile(file.name)
            })
    }
    return (
        <div className='file-card'>
            <div className="file-inputs">
                <input type="file" onChange={uploadHandler} />
                <button>
                    <i>
                        <FontAwesomeIcon icon={faPlus} />
                    </i>
                    Upload
                </button>
            </div>
            <div className='file-title'>
                <p className="file-main">Support files :</p>
                <p className="info">CSV</p>
            </div>
        </div>
    )
}

export default FileUpload
