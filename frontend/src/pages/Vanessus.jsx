import React, { useState, useEffect } from 'react'
import '../assets/css/dashboard.css'
import axios from 'axios';
import { AiOutlineSecurityScan } from 'react-icons/ai';
import FileUpload from '../components/FileUpload/FileUpload';
import FileList from '../components/FileList/FileList';
import Table from '../components/table/Table';
import { v4 as uuidv4 } from 'uuid'

function Vanessus() {

    const [files, setFiles] = useState([])
    const [data, setGET] = useState([]);
    const list = []
    // console.log(files);
    const uploadFile = (filesList) => {
        const formData = new FormData
        for (let i = 0; i < filesList.length; i++) {
            const file = filesList[i].file
            const fileName = filesList[i].fileName
            const type = filesList[i].type
            formData.append('file', file);
            formData.append('fileName', fileName);
            formData.append('type', type);
            file.isUploading = true
            list.push(file)
        }
        setGET([])
        setFiles([...list])
        // list = []

        const config = {
            headers: {
                'content-type': 'multipart/form-data',
            },
        }
        console.log(formData);
        axios.post('http://10.11.101.32/web/report/reportnessus-add/', formData, config)
            .then((res) => {
                // console.log(res);
                const list2 = []
                for (let i = 0; i < filesList.length; i++) {
                    const file = filesList[i].file
                    file.isUploading = false
                    list2.push(file)
                }
                setGET([])
                setFiles([...list2])
                getUser()
                alert("Success")
            })
            .catch((err) => {
                alert(err)
            })
    }

    async function getUser() {
        try {
            const response = await axios.get('http://10.11.101.32/web/report/report-detail/nessus');
            setGET(response.data)
        } catch (error) {
        }
    }

    const removeFile = (filename) => {
        console.log(filename);
        console.log(files);
        files.map(item => {
            if (item.fileName) {
                if (item.fileName == filename) {
                    setFiles(files.filter(file => file.fileName !== filename))
                }
            }
            else {
                if (item.name == filename) {
                    setFiles(files.filter(file => file.name !== filename))
                }
            }
        })
    }

    const deleteFile = (id) => {
        axios.delete('http://10.11.101.32/web/report/report-delete/' + id)
            .then(res => {
                getUser()
            })
    }
    useEffect(() => {
        getUser()
    }, [])

    return (
        <div>
            <div className='title'>
                <div className="card">
                    <AiOutlineSecurityScan style={{ color: "#ffffff", fontSize: "35px" }} />
                </div>
                <h2>VA SCAN NESSUS</h2>
            </div>
            <div className="iso-container">
                <FileUpload files={files} type={"nessus"} setFiles={setFiles} removeFile={removeFile} key={uuidv4()} />
                <FileList files={files} type={"nessus"} removeFile={removeFile} key={uuidv4()} />
                <button className='upload-file' onClick={() => uploadFile(files)}>
                    Upload
                </button>
            </div>
            <Table data={data} deleteFile={deleteFile} key={uuidv4()} />
        </div>
    )
}


export default Vanessus
