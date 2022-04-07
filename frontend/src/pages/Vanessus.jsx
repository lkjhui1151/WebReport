import React from 'react'
import '../assets/css/dashboard.css'
import { AiOutlineSecurityScan } from 'react-icons/ai';
import FileUpload from '../components/FileUpload/FileUpload';
import FileList from '../components/FileList/FileList';
import Table from '../components/table/Table';

function Vanessus() {
    return (
        <div>
            <div className='title'>
                <div className="card">
                    <AiOutlineSecurityScan style={{ color: "#ffffff", fontSize: "35px" }} />
                </div>
                <h2>VA SCAN NESSUS</h2>
            </div>
            <div className="iso-container">
                <FileUpload />
                <FileList />
            </div>
            <Table />
        </div>
    )
}


export default Vanessus
