import Layout from '@/components/Layout';
import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import axios from 'axios';
import TOCItem from '@/components/TOCItem';
import { useSearchParams } from 'next/navigation';

export default function BookView() {
  const router = useRouter();
  const { book_id, channel_id } = router.query;
  const [toc, setToc] = useState([]);
  const searchParams = useSearchParams()
  const channel2_id = searchParams.get('channel2');

  useEffect(() => {
    if (book_id) axios.get(`http://localhost:5000/api/toc/${book_id}`).then(res => setToc(res.data));
  }, [book_id]);

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-center mb-6">Book View</h1>
      <div className="bg-white p-6 rounded shadow">
        {toc.map((item: any) => (
          <TOCItem
            key={item.paragraph}
            item={item}
            channelId={channel_id as string}
            channel2Id={channel2_id as string}
            bookId={book_id as string}
          />
        ))}
      </div>
    </Layout>
  );
}
