import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import React from 'react'
import { faFileAlt, faSpinner, faTrash } from '@fortawesome/free-solid-svg-icons'
import '../../assets/css/fileItem.css'

const FileItem = ({ file, deleteFile }) => {
    return (
        <li className='file-item' key={file.name}>
            <FontAwesomeIcon icon={faFileAlt} />
            <p>{file.name}</p>
            <div className="file-item-actions">
                {file.isUpload && <FontAwesomeIcon icon={faSpinner} className="fa-spin" />}
                {!file.isUpload && <FontAwesomeIcon icon={faTrash} onClick={() => deleteFile(file.name)} />}
            </div>
        </li>
    )
}

export default FileItem
