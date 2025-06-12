import React, { useState, useEffect } from 'react';
import { Menu } from 'antd';
import TocList from './TocList.jsx';

const Sidebar = () => {
    const [bookId, setBookId] = useState(null);
    const [toc, setToc] = useState([]);

    useEffect(() => {
        if (bookId) {
            fetch(`/api/toc/${bookId}`)
                .then(res => res.json())
                .then(data => setToc(data));
        } else {
            setToc([]);
        }
    }, [bookId]);

    const handleBookChange = (newBookId) => {
        setBookId(newBookId);
    };

    return (
        <div style={{ padding: '16px' }}>
            <h4>Table of Contents</h4>
            <TocList toc={toc} />
        </div>
    );
};

export default Sidebar;
