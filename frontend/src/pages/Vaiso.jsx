import React, { useState, useEffect } from 'react'
import '../assets/css/iso.css'
import { AiOutlineSecurityScan } from 'react-icons/ai';
import FileUpload from '../components/FileUpload/FileUpload';
import FileList from '../components/FileList/FileList';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid'

import Table from '../components/table/Table';


function Vaiso() {

    const [files, setFiles] = useState([])
    const [data, setGET] = useState([]);

    async function getUser() {
        try {
            const response = await axios.get('http://localhost:8000/web/report/report-detail/iso');
            console.log(response.data);
            setGET(response.data)
        } catch (error) {
            console.error(error);
        }
    }

    const removeFile = (filename) => {
        setFiles(files.filter(file => file.name !== filename))
    }

    const addFile = (formData, config, file) => {
        axios.post('http://localhost:8000/web/report/company-add/', formData, config)
            .then((res) => {
                console.log(res);
                file.isUploading = false
                setFiles([...files, file])
                getUser()
            })
            .catch((err) => {
                console.log(err);
                removeFile(file.name)
            })
    }

    const deleteFile = (id, name) => {
        axios.delete('http://localhost:8000/web/report/report-delete/' + id)
            .then(res => {
                console.log(res.data);
                getUser()
            })
    }
    // getUser()

    useEffect(() => {
        getUser()
    }, [])

    return (
        <div>
            <div className='title'>
                <div className="card">
                    <AiOutlineSecurityScan style={{ color: "#ffffff", fontSize: "35px" }} />
                </div>
                <h2>VA SCAN ISO</h2>
            </div>
            <div className="iso-container">
                <FileUpload files={files} type={"iso"} setFiles={setFiles} removeFile={removeFile} key={uuidv4()} addFile={addFile} />
                <FileList files={files} removeFile={removeFile} key={uuidv4()} />
            </div>
            <Table data={data} deleteFile={deleteFile} key={uuidv4()} />
        </div>
    )
}

export default Vaiso
