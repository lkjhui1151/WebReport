import React from 'react'
import FileUpload from '../components/FileUpload/FileUpload';
import FileList from '../components/FileList/FileList';
import Table from '../components/table/Table'
import { AiOutlineSecurityScan } from 'react-icons/ai';

const VanessusInfra = () => {
    return (
        <div>
            <div className='title'>
                <div className="card">
                    <AiOutlineSecurityScan style={{ color: "#ffffff", fontSize: "35px" }} />
                </div>
                <h2>VA SCAN NESSUS INFRA</h2>
            </div>
            <div className="iso-container">
                <FileUpload />
                <FileList />
            </div>
            <Table />
        </div>
    )
}

export default VanessusInfra
