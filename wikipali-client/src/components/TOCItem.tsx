import { useState, useEffect } from 'react';
import axios from 'axios';
import ContentDisplay from '@/components/ContentDisplay';

type TOCItemProps = {
  item: {
    paragraph: number;
    chapter_len: number;
    level: number;
    toc: string;
  };
  channelId: string;
  channel2Id: string;
  bookId: string | number;
};

export default function TOCItem({ item, channelId, channel2Id, bookId }: TOCItemProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [content, setContent] = useState(null);

  const fetchContent = () => {
    const paragraphEnd = parseInt(String(item.paragraph)) + (item.chapter_len || 1) - 1;
    axios.get(`http://localhost:5000/api/toc/content/${bookId}/${channelId}`, {
      params: { paragraph_start: item.paragraph, paragraph_end: paragraphEnd, script: 'IAST', channel2: channel2Id },
    }).then(res => setContent(res.data));
  };

  return (
    <div className={`ml-${(item.level - 2) * 4}`}>
      <div className="flex justify-between p-2 cursor-pointer hover:bg-gray-100" onClick={() => { setIsOpen(!isOpen); if (!content) fetchContent(); }}>
        <span className="text-blue-600">{item.toc}</span>
        <span className="text-gray-600 text-sm">{item.chapter_len} paragraph{item.chapter_len > 1 ? 's' : ''}</span>
      </div>
      {isOpen && content && (
        <ContentDisplay content={content} />
      )}
    </div>
  );
}