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
    console.log(files);
    async function getUser() {
        try {
            const response = await axios.get('http://10.11.101.32/web/report/report-detail/iso');
            setGET(response.data)
        } catch (error) {
        }
    }

    const removeFile = (filename) => {
        setFiles(files.filter(file => file.name !== filename))
    }

    const addFile = (formData, config, file) => {
        axios.post('http://10.11.101.32/web/report/reportiso-add/', formData, config)
            .then((res) => {
                file.isUploading = false
                setFiles([...files, file])
                getUser()
            })
            .catch((err) => {
                removeFile(file.name)
                alert(err)
            })
    }

    const deleteFile = (id) => {
        axios.delete('http://10.11.101.32/web/report/report-delete/' + id)
            .then(res => {
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
                <FileList files={files} type={"iso"} removeFile={removeFile} key={uuidv4()} />
            </div>
            <Table data={data} deleteFile={deleteFile} key={uuidv4()} />
        </div>
    )
}

export default Vaiso
