import React, { useState } from 'react'
import axios from 'axios';
import './fileUpload.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import Alert, { ModalHeader, ModalBody, ModalFooter } from '../Alert/Alert';
import Button from '../Button/Button';

const FileList = []
let state = false

const FileUpload = ({ files, type, setFiles, removeFile, addFile }) => {
    const [showModal, setShowModal] = useState(false)
    // console.log(type);
    const uploadHandler = (event) => {
        for (let i = 0; i < event.target.files.length; i++) {
            const file = event.target.files[i]

            const fileType = file.name.split(".");

            for (let i = 0; i < FileList.length; i++) {
                if (FileList[i] == fileType[0]) {
                    FileList.splice(i, 1);
                    file.isUploading = false
                    break;
                }
                else {
                    state = true
                }
            }
            // state = true
            FileList.push(fileType[0])
            if (fileType[fileType.length - 1] == "csv") {
                state = true
            }
            else {
                setShowModal(true)
                for (let i = 0; i < FileList.length; i++) {
                    if (FileList[i] == fileType[0]) {
                        FileList.splice(i, 1);
                    }
                }
                state = false
            }

            if (state == true) {
                file.isUploading = true
                setFiles([...files, file])
                const formData = new FormData()
                formData.append('file', file);
                formData.append('fileName', file.name);
                formData.append('type', type);
                const config = {
                    headers: {
                        'content-type': 'multipart/form-data',
                    },
                };
                addFile(formData, config, file)
            }
        }
    }
    return (
        <div className='file-card'>
            <div className="file-inputs">
                <input type="file" onChange={uploadHandler} value="" />
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
            <Alert show={showModal}>
                <ModalHeader>
                    <h2>Notifications</h2>
                </ModalHeader>
                <ModalBody>
                    <p style={{ textAlign: 'justify' }}>
                        Please input file type CSV only EiEi
                    </p>
                </ModalBody>
                <ModalFooter>
                    <Button onClick={() => setShowModal(false)}>
                        Close
                    </Button>
                </ModalFooter>
            </Alert>
        </div>
    )
}

export default FileUpload
