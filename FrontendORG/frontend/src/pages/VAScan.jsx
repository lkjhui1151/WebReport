import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import axios from 'axios';
import '../assets/css/vascan.css'
import { saveAs } from "file-saver";
import topForm from '../components/topForm/topForm'

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
            <div className="col-12">
                <topForm />
                <div className="form-upload">
                    <form onSubmit={handleSubmit}>
                        <h1>CSV File Upload</h1>
                        <div className="row">
                            <div className="col-6">
                                <input type="file" onChange={handleChange} />
                            </div>
                            <div className="col-6"><button type="submit" className="upload" onChange={handleChange}>Upload</button></div>
                        </div>
                    </form>
                </div>
            </div>
            <div className="col-12">
                <div className="form-table" >
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
                                    <th>
                                        <button className='download' onClick={() => saveFile(item.name)}>Download</button>
                                        <button className='delete' onClick={() => deleteFile(item.id)}>Delete</button>
                                    </th>
                                </tr>
                            ))}
                        </table>
                    </div>
                </div>
            </div>
        </div >
    );
}

export default VAScan
