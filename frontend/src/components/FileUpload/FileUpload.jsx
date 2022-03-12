import React, { useState } from 'react'
import axios from 'axios';
import '../../assets/css/fileUpload.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import Alert, { ModalHeader, ModalBody, ModalFooter } from '../Alert/Alert';
import Button from '../Button/Button';

const FileList = []
let state = false

const FileUpload = ({ files, setFiles, removeFile }) => {
    const [showModal, setShowModal] = useState(false)

    const uploadHandler = (event) => {
        console.log(FileList);
        const file = event.target.files[0]
        const fileType = file.name.split(".");

        for (let i = 0; i < FileList.length; i++) {
            if (FileList[i] == fileType[0]) {
                FileList.splice(i, 1);
                console.log("state 0s");
                break;
            }
            else {
                console.log("state 0");
                state = true
            }
        }
        // state = true
        FileList.push(fileType[0])
        // state = 1
        console.log(FileList);
        console.log(state);

        if (fileType[fileType.length - 1] === "csv" && state === true) {
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
            console.log("File is : " + formData);
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
        else {
            setShowModal(true)
            // for (let i = 0; i < FileList.length; i++) {
            //     if (FileList[i] == fileType[0]) {
            //         FileList.splice(i, 1);
            //     }
            // }
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
                        Please input file type CSV only
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
