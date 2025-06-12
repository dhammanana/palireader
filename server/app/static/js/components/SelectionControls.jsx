import React, { useState, useEffect } from 'react';
import { Tabs, Select, Button, Spin } from 'antd';

const { TabPane } = Tabs;

const SelectionControls = ({ onSelectionChange }) => {
    const [activeTab, setActiveTab] = useState('channel-first');
    const [channels, setChannels] = useState([]);
    const [books, setBooks] = useState([]);
    const [channelBooks, setChannelBooks] = useState([]);
    const [bookChannels, setBookChannels] = useState([]);
    const [selectedChannel, setSelectedChannel] = useState('');
    const [selectedBook, setSelectedBook] = useState('');
    const [loadingBooks, setLoadingBooks] = useState(false);
    const [loadingChannels, setLoadingChannels] = useState(false);

    useEffect(() => {
        fetch('/api/books')
            .then(res => res.json())
            .then(data => setBooks(data));
        fetch('/api/channels/0')
            .then(res => res.json())
            .then(data => setChannels(data));
    }, []);

    useEffect(() => {
        if (selectedChannel) {
            setLoadingBooks(true);
            fetch(`/api/books/${selectedChannel}`)
                .then(res => res.json())
                .then(data => {
                    setChannelBooks(data);
                    setLoadingBooks(false);
                });
        } else {
            setChannelBooks([]);
        }
    }, [selectedChannel]);

    useEffect(() => {
        if (selectedBook) {
            setLoadingChannels(true);
            fetch(`/api/channels/${selectedBook}`)
                .then(res => res.json())
                .then(data => {
                    setBookChannels(data);
                    setLoadingChannels(false);
                });
        } else {
            setBookChannels([]);
        }
    }, [selectedBook]);

    const handleSubmit = () => {
        onSelectionChange({ bookId: selectedBook, channelId: selectedChannel });
    };

    return (
        <div style={{ background: '#fff', padding: '16px', borderRadius: '8px', marginBottom: '16px' }}>
            <Tabs activeKey={activeTab} onChange={setActiveTab}>
                <TabPane tab="Select Channel First" key="channel-first">
                    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                        <div style={{ flex: 1, minWidth: '200px' }}>
                            <label>Select Channel:</label>
                            <Select
                                style={{ width: '100%' }}
                                value={selectedChannel}
                                onChange={setSelectedChannel}
                                placeholder="Select a channel"
                            >
                                {channels.map(channel => (
                                    <Select.Option key={channel.id} value={channel.id}>
                                        {channel.name}
                                    </Select.Option>
                                ))}
                            </Select>
                        </div>
                        <div style={{ flex: 1, minWidth: '200px' }}>
                            <label>Select Book:</label>
                            <Select
                                style={{ width: '100%' }}
                                value={selectedBook}
                                onChange={setSelectedBook}
                                placeholder="Select a book"
                                loading={loadingBooks}
                            >
                                {channelBooks.map(book => (
                                    <Select.Option key={book.book} value={book.book}>
                                        {`${book.book} - ${book.name} (${book.lines_count} lines)`}
                                    </Select.Option>
                                ))}
                            </Select>
                            {loadingBooks && <Spin />}
                        </div>
                    </div>
                    <div style={{ textAlign: 'right', marginTop: '16px' }}>
                        <Button type="primary" onClick={handleSubmit} disabled={!selectedBook || !selectedChannel}>
                            View Translations
                        </Button>
                    </div>
                </TabPane>
                <TabPane tab="Select Book First" key="book-first">
                    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                        <div style={{ flex: 1, minWidth: '200px' }}>
                            <label>Select Book:</label>
                            <Select
                                style={{ width: '100%' }}
                                value={selectedBook}
                                onChange={setSelectedBook}
                                placeholder="Select a book"
                            >
                                {books.map(book => (
                                    <Select.Option key={book.book_id} value={book.book_id}>
                                        {`${book.book_id} - ${book.book_name} (${book.lines_count} lines)`}
                                    </Select.Option>
                                ))}
                            </Select>
                        </div>
                        <div style={{ flex: 1, minWidth: '200px' }}>
                            <label>Select Channel:</label>
                            <Select
                                style={{ width: '100%' }}
                                value={selectedChannel}
                                onChange={setSelectedChannel}
                                placeholder="Select a channel"
                                loading={loadingChannels}
                            >
                                {bookChannels.map(channel => (
                                    <Select.Option key={channel.id} value={channel.id}>
                                        {channel.name}
                                    </Select.Option>
                                ))}
                            </Select>
                            {loadingChannels && <Spin />}
                        </div>
                    </div>
                    <div style={{ textAlign: 'right', marginTop: '16px' }}>
                        <Button type="primary" onClick={handleSubmit} disabled={!selectedBook || !selectedChannel}>
                            View Translations
                        </Button>
                    </div>
                </TabPane>
            </Tabs>
        </div>
    );
};

export default SelectionControls;
