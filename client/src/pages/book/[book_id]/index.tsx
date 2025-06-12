import Layout from '@/components/Layout';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import axios from 'axios';
import ContentDisplay from '@/components/ContentDisplay';

export default function BookContentPage() {
    const router = useRouter();
    const { book_id } = router.query;
    const paragraph = parseInt(router.query.paragraph as string);
    const length = parseInt(router.query.length as string);
    const [content, setContent] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (book_id && paragraph && length) {
            const paragraph_end = paragraph + length;
            const url = `http://localhost:5000/api/toc/content/${book_id}/7a9b2e4f-6d8c-4b1a-9e3f-82c4d7f105a9?paragraph_start=${paragraph}&paragraph_end=${paragraph_end}&script=Latn&channel2=`;

            axios.get(url)
                .then(res => {
                    setContent(res.data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error('Error loading content:', err);
                    setLoading(false);
                });
        }
    }, [book_id, paragraph, length]);

    return (
        <Layout>
            <h1 className="text-2xl font-bold text-center mb-6">Book {book_id}</h1>
            {loading ? (
                <p className="text-center">Loading content...</p>
            ) : (
                <div className="bg-white p-6 rounded shadow whitespace-pre-line">
                    <ContentDisplay content={content} />
                </div>
            )}
        </Layout>
    );
}
