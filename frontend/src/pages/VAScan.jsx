import React, { useState, useEffect } from 'react'
import axios from 'axios';
import '../assets/css/vascan.css'
import { saveAs } from "file-saver";

const CompanyTableHead = [
    'name',
    'File',
    'Action',
]

function VAScan() {


    const [file, setFile] = useState(null)

    function handleChange(event) {
        setFile(event.target.files[0])
    }

    function handleSubmit(event) {
        event.preventDefault()
        const url = 'http://localhost:8000/ReportVA/company-add/';
        const formData = new FormData();
        formData.append('file', file);
        formData.append('fileName', file.name);
        const config = {
            headers: {
                'content-type': 'multipart/form-data',
            },
        };
        // console.log(formData);
        axios.post(url, formData, config).then((response) => {
            console.log(response.data);
        });
    }

    const [data, setData] = useState([])


    useEffect(() => {
        const doFetch = async () => {
            const response = await fetch("http://localhost:8000/ReportVA/company-list/")
            const body = await response.json()
            const contacts = body
            // console.log(contacts)
            setData(contacts)
        }
        doFetch()
    }, [])
    // console.log(data);

    const saveFile = (name) => {
        name = name + ".docx"
        saveAs(
            "http://localhost:8000/ReportVA/uploads/" + name,
            name
        );
    };

    const deleteFile = (id) => {
        // Simple POST request with a JSON body using fetch
        const requestOptions = {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: 'delete file docx' })
        };

        fetch("http://localhost:8000/ReportVA/company-delete/" + id, requestOptions)
            .then(response => response.json())
            .then(data => this.useState({ postId: data.id }))

    }


    return (
        <div>
            <h2 className="page-header">Vulnerability SCAN</h2>
            <div className="row">
                <div className="col-8">
                    <div className="form-upload" >
                        <div className="card">
                            <div>
                                <table>
                                    <tr>
                                        <th>{CompanyTableHead[0]}</th>
                                        <th>{CompanyTableHead[1]}</th>
                                        <th>{CompanyTableHead[2]}</th>
                                    </tr>
                                    {data.map(item => (
                                        <tr>
                                            <th>{item.name}</th>
                                            <th>{item.file}</th>
                                            <button onClick={() => saveFile(item.name)}>download</button>
                                            <button onClick={() => deleteFile(item.id)}>delete</button>
                                        </tr>
                                    ))}
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-4">
                    <div className="card">
                        <form onSubmit={handleSubmit} className="form-upload">
                            <h1>CSV File Upload</h1>
                            <div className="row">
                                <div className="col-9">
                                    <input type="file" onChange={handleChange} />
                                </div>
                                <div className="col-3"><button type="submit" onChange={handleChange}>Upload</button></div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div >
    );
}

export default VAScan
