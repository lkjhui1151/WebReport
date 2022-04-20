import { useEffect, useRef } from 'react';
import './model.css'

const Model = (props) => {
    const modelRef = useRef();

    useEffect(() => {
        const clickOutsideContent = (e) => {
            if (e.target === modelRef.current) {
                props.setShow(false);
            }
        };
        window.addEventListener('click', clickOutsideContent);
        return () => {
            window.removeEventListener('click', clickOutsideContent);
        };
    }, [props]);

    return (
        <div className={`model ${props.show ? 'active' : ''}`}>
            <div className="model-content">
                {/* {
                    !props.hideCloseButton && <span onClick={() => props.setShow(false)} className="model-close">
                        &times;
                    </span>
                } */}
                {props.children}
            </div>
        </div>
    )
}

export default Model

export const ModelHeader = (props) => {
    return <div className="model-header">
        {
            props.children
        }
    </div>
}

export const ModelBody = (props) => {
    return <div className="model-body">
        {
            props.children
        }
    </div>
}

export const ModelFooter = (props) => {
    return <div className="model-footer">
        {
            props.children
        }
    </div>
}