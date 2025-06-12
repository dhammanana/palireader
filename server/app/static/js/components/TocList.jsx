import React from 'react';
import { Menu } from 'antd';

const TocList = ({ toc }) => {
    const sanitizeAnchor = (text) => {
        return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    };

    const buildTocTree = () => {
        const tocTree = {};
        toc.forEach(item => {
            if (!tocTree[item.level]) tocTree[item.level] = [];
            tocTree[item.level].push(item);
        });

        const items = [];
        if (tocTree[2]) {
            tocTree[2].forEach(level2 => {
                const anchor = sanitizeAnchor(level2.toc);
                const subItems = [];
                if (tocTree[3]) {
                    tocTree[3].filter(item => item.parent === level2.paragraph).forEach(level3 => {
                        const subAnchor = sanitizeAnchor(level3.toc);
                        const subSubItems = [];
                        if (tocTree[4]) {
                            tocTree[4].filter(item => item.parent === level3.paragraph).forEach(level4 => {
                                subSubItems.push({
                                    key: `toc-${level4.id}`,
                                    label: (
                                        <span>
                                            <a href={`#para-${level4.paragraph}`} className="toc-name">{level4.toc}</a>
                                            <span className="toc-info"> (Len: {level4.chapter_len}, Para: {level4.paragraph})</span>
                                        </span>
                                    ),
                                });
                            });
                        }
                        subItems.push({
                            key: `toc-${level3.id}`,
                            label: (
                                <span>
                                    <a href={`#para-${level3.paragraph}`} className="toc-name">{level3.toc}</a>
                                    <span className="toc-info"> (Len: {level3.chapter_len}, Para: {level3.paragraph})</span>
                                </span>
                            ),
                            children: subSubItems,
                        });
                    });
                }
                items.push({
                    key: `toc-${level2.id}`,
                    label: (
                        <span>
                            <a href={`#para-${level2.paragraph}`} className="toc-name">{level2.toc}</a>
                            <span className="toc-info"> (Len: {level2.chapter_len}, Para: {level2.paragraph})</span>
                        </span>
                    ),
                    children: subItems,
                });
            });
        }
        return items;
    };

    return (
        <Menu
            mode="inline"
            items={buildTocTree()}
            style={{ border: 'none' }}
            onClick={(e) => {
                e.domEvent.preventDefault();
                const anchorId = e.domEvent.target.getAttribute('href');
                if (anchorId) {
                    const element = document.querySelector(anchorId);
                    if (element) {
                        window.scrollTo({
                            top: element.offsetTop - 64,
                            behavior: 'smooth',
                        });
                    }
                }
            }}
        />
    );
};

export default TocList;
