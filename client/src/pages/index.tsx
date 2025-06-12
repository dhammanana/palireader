
import Layout from '@/components/Layout';
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState('');
  const [channels, setChannels] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/books').then(res => setBooks(res.data));
  }, []);

  const handleBookSelect = (bookId: string) => {
    setSelectedBook(bookId);
    axios.get(`http://localhost:5000/api/channels/${bookId}`).then(res => setChannels(res.data));
  };

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-center mb-6">Chattha Samgāyana Tipitaka</h1>
      <div className="bg-white p-6 rounded shadow mb-6">
        <div className="flex space-x-4">
          <select className="p-2 border rounded" onChange={e => handleBookSelect(e.target.value)}>
            <option value="">Select Book</option>
            {books.map((book: any) => (
              <option key={book.book_id} value={book.book_id}>
                {book.book_name} - {book.lines_count} lines
              </option>
            ))}
          </select>
          <select className="p-2 border rounded" disabled={!selectedBook}>
            <option value="">Select Channel</option>
            {channels.map((channel: any) => (
              <option key={channel.id} value={channel.id}>{channel.name} - {channel.lines_count} lines</option>
            ))}
          </select>
        </div>
      </div>
    </Layout>
  );
}