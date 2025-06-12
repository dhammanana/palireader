import { useRouter } from 'next/router';

export default function BookView() {
    const router = useRouter();
    const { id, channel } = router.query;
    console.log(router.query)


    return (
        <>id: {id}, channel: {channel}
            <br />
        </>
    );
}
