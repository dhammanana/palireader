import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:5000/api' });

export const getBooks = () => api.get('/books');
export const getChannels = (bookId: string) => api.get(`/channels/${bookId}`);
export const getTOC = (bookId: string) => api.get(`/toc/${bookId}`);
export const getTOCContent = (bookId: string, channelId: string, params: any) => api.get(`/toc/content/${bookId}/${channelId}`, { params });
