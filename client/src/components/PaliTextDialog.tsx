import { useState, useEffect, JSX } from 'react';
import { useRouter } from 'next/router'; // ✅ Add this
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

interface PaliTextItem {
    book: number;
    chapter_len: number;
    id: string;
    level: number;
    paragraph: number;
    parent: number;
    title: string;
}

interface PaliTextDialogProps {
    tagKey: string | null;
    isOpen: boolean;
    onClose: () => void;
}

export default function PaliTextDialog({ tagKey, isOpen, onClose }: PaliTextDialogProps) {
    const [paliTextData, setPaliTextData] = useState<PaliTextItem[]>([]);
    const router = useRouter();

    useEffect(() => {
        if (tagKey && isOpen) {
            const url = `http://localhost:5000/api/palitext?view=palitext&tags=${encodeURIComponent(tagKey)}`;
            console.log("Fetching:", url);
            fetch(url)
                .then(response => response.json())
                .then(data => setPaliTextData(data.data))
                .catch(error => console.error('Error fetching pali text:', error));
        }
    }, [tagKey, isOpen]);

    const handleItemClick = (item: PaliTextItem) => {
        const url = `/book/${item.book}?paragraph=${item.paragraph}&length=${item.chapter_len}`;
        router.push(url);
    };

    const renderPaliTextItems = (items: PaliTextItem[], level: number = 0): JSX.Element[] => {
        return items.map(item => {
            const childItems = paliTextData.filter(child => child.parent === item.paragraph && child.book === item.book);
            return (
                <div key={item.id} className={`pl-${level * 4}`}>
                    <div
                        className="py-1 px-2 hover:bg-gray-100 cursor-pointer rounded"
                        onClick={() => handleItemClick(item)}
                    >
                        {item.title}
                    </div>
                    {childItems.length > 0 && (
                        <div className="ml-2">
                            {renderPaliTextItems(childItems, level + 1)}
                        </div>
                    )}
                </div>
            );
        });
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="bg-white text-gray-900 max-w-3xl w-full">
                <DialogHeader>
                    <DialogTitle>Select Pali Text</DialogTitle>
                </DialogHeader>
                <div className="max-h-[400px] overflow-y-auto">
                    {renderPaliTextItems(paliTextData.filter(item => item.parent === -1))}
                </div>
            </DialogContent>
        </Dialog>
    );
}
