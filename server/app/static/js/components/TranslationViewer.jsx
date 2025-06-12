import React, { useState, useEffect, useCallback } from 'react';
import { Card, Spin, Alert, Typography } from 'antd';
import SelectionControls from './SelectionControls.jsx';

const { Title, Text } = Typography;

const TranslationViewer = () => {
    const [translations, setTranslations] = useState({});
    const [bookId, setBookId] = useState(null);
    const [channelId, setChannelId] = useState(null);
    const [lastParagraph, setLastParagraph] = useState(0);
    const [loading, setLoading] = useState(false);
    const [bookName, setBookName] = useState('');
    const [channelName, setChannelName] = useState('');

    const loadMoreTranslations = useCallback(async () => {
        if (loading || !bookId || !channelId) return;
        setLoading(true);
        const paragraphStart = lastParagraph + 1;
        const paragraphEnd = paragraphStart + 9;

        try {
            const res = await fetch(`/api/translations?book=${bookId}&channel=${channelId}&paragraph_start=${paragraphStart}&paragraph_end=${paragraphEnd}`);
            const data = await res.json();
            if (Object.keys(data).length === 0) {
                setLoading(false);
                return;
            }
            setTranslations(prev => ({ ...prev, ...data }));
            setLastParagraph(Math.max(lastParagraph, ...Object.keys(data).map(Number)));
        } catch (error) {
            console.error('Error loading translations:', error);
        } finally {
            setLoading(false);
        }
    }, [bookId, channelId, lastParagraph, loading]);

    useEffect(() => {
        const handleScroll = () => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
                loadMoreTranslations();
            }
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [loadMoreTranslations]);

    const handleSelectionChange = async ({ bookId: newBookId, channelId: newChannelId }) => {
        setBookId(newBookId);
        setChannelId(newChannelId);
        setTranslations({});
        setLastParagraph(0);
        setLoading(true);

        try {
            const bookRes = await fetch(`/api/books/${newChannelId}`);
            const books = await bookRes.json();
            const book = books.find(b => b.book === newBookId);
            setBookName(book ? book.name : newBookId);

            const channelRes = await fetch(`/api/channels/${newBookId}`);
            const channels = await channelRes.json();
            const channel = channels.find(c => c.id === newChannelId);
            setChannelName(channel ? channel.name : newChannelId);

            await loadMoreTranslations();
        } catch (error) {
            console.error('Error fetching metadata:', error);
        }
    };

    return (
        <div>
            <SelectionControls onSelectionChange={handleSelectionChange} />
            {bookId && channelId && (
                <div className="book-info">
                    <Title level={4}>
                        <Text strong>Book: </Text>
                        <Text>{bookName || bookId}</Text>
                    </Title>
                    <Title level={4}>
                        <Text strong>Channel: </Text>
                        <Text>{channelName}</Text>
                    </Title>
                </div>
            )}
            {Object.keys(translations).length > 0 ? (
                Object.entries(translations).map(([paragraph, items]) => (
                    <div key={paragraph} className="paragraph-container" id={`para-${paragraph}`}>
                        {items
                            .sort((a, b) => a.word_start - b.word_start)
                            .map((item, index) => (
                                <Card key={index} style={{ marginBottom: '8px' }}>
                                    <p className="pali-text">{item.sentence_content}</p>
                                    {item.translation_content && <p className="translation-text">{item.translation_content}</p>}
                                </Card>
                            ))}
                    </div>
                ))
            ) : bookId && channelId ? (
                <Alert message="No translation data found for the selected book and channel" type="info" />
            ) : (
                <div style={{ textAlign: 'center' }}>
                    <Title level={3}>Welcome to the Nissaya Translation Viewer</Title>
                    <Text>Please select a book and channel to view translations</Text>
                </div>
            )}
            {loading && <Spin style={{ display: 'block', textAlign: 'center', margin: '16px 0' }} />}
        </div>
    );
};

export default TranslationViewer;
