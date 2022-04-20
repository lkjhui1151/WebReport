import React, { useState } from 'react'
import './fileUpload.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import Alert, { ModalHeader, ModalBody, ModalFooter } from '../Alert/Alert';
import Button from '../Button/Button';

const FileList = []
let state = false
let count = 0

const FileUpload = ({ files, type, setFiles, removeFile, addFile }) => {
    const [showModal, setShowModal] = useState(false)
    const [fileArr, setFileArr] = useState([])
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
                if (type == 'iso') {
                    file.isUploading = true
                    // console.log(files);
                    // console.log(file);
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
                if (type == 'nessus') {
                    // file.isUploading = true
                    const formData = { file: '', fileName: '', type: '', config: '' }
                    formData.file = file
                    formData.fileName = file.name
                    formData.type = type

                    fileArr.push(formData)
                    count += 1
                    if (count >= event.target.files.length) {
                        setFiles([...files, ...fileArr])
                        count = 0
                    }
                    if (event.target.files.length == 1) {
                        setFiles([...files, ...fileArr])
                    }
                }
                if (type == 'web') {
                    // file.isUploading = true
                    const formData = { file: '', fileName: '', type: '', config: '' }
                    formData.file = file
                    formData.fileName = file.name
                    formData.type = type

                    fileArr.push(formData)
                    count += 1
                    if (count >= event.target.files.length) {
                        setFiles([...files, ...fileArr])
                        count = 0
                    }
                    if (event.target.files.length == 1) {
                        setFiles([...files, ...fileArr])
                    }
                }
                if (type == 'infra') {
                    // file.isUploading = true
                    const formData = { file: '', fileName: '', type: '', config: '' }
                    formData.file = file
                    formData.fileName = file.name
                    formData.type = type

                    fileArr.push(formData)
                    count += 1
                    if (count >= event.target.files.length) {
                        setFiles([...files, ...fileArr])
                        count = 0
                    }
                    if (event.target.files.length == 1) {
                        setFiles([...files, ...fileArr])
                    }
                }
            }
        }
    }
    return (
        <div className='file-card'>
            <div className="file-inputs">
                {
                    type == 'iso' &&
                    <input type="file" onChange={uploadHandler} value="" />
                }
                {
                    type == 'nessus' &&
                    <input type="file" onChange={uploadHandler} value="" multiple />
                }
                {
                    type == 'web' &&
                    <input type="file" onChange={uploadHandler} value="" multiple />
                }
                {
                    type == 'infra' &&
                    <input type="file" onChange={uploadHandler} value="" multiple />
                }
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
