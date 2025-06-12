const tocCache = {};

async function loadTOC(bookId) {
    const response = await fetch(`/api/toc/${bookId}`);
    const toc = await response.json();
    tocCache[bookId] = toc;
    const tocList = document.getElementById('toc-list');
    tocList.innerHTML = '';

    toc.forEach(item => {
        const div = document.createElement('div');
        div.className = 'toc-item';
        div.style = `--level: ${item.level - 2}`;
        div.innerHTML = `
            <a class="toc-link collapsed" data-paragraph="${item.paragraph}" data-chapter-len="${item.chapter_len}">
                ${item.toc}
                <span class="paragraph-count">${item.chapter_len} paragraph${item.chapter_len > 1 ? 's' : ''}</span>
            </a>
            <div class="content-container" id="content-${item.paragraph}"></div>`;
        tocList.appendChild(div);
    });

    document.querySelectorAll('.toc-link').forEach(link => {
        link.addEventListener('click', async () => {
            const paragraph = link.getAttribute('data-paragraph');
            const chapterLen = parseInt(link.getAttribute('data-chapter-len')) || 1;
            const contentDiv = document.getElementById(`content-${paragraph}`);
            const isActive = contentDiv.classList.contains('active');

            if (isActive) {
                contentDiv.classList.remove('active');
                link.classList.add('collapsed');
                return;
            }

            // Check if content is already loaded
            if (contentDiv.hasAttribute('data-loaded')) {
                contentDiv.classList.add('active');
                link.classList.remove('collapsed');
                return;
            }

            const paragraphEnd = parseInt(paragraph) + chapterLen - 1;
            const response = await fetch(`/api/toc/content/${bookId}/${channelId}?paragraph_start=${paragraph}&paragraph_end=${paragraphEnd}&script=${scriptLang}&channel2=${channel2Id}`);
            const data = await response.json();
            contentDiv.innerHTML = '';

            $.each(data, function (paragraph, items) {
                const $container = $(`<div class="paragraph-container" data-paragraph="${paragraph}" id="para-${paragraph}">`);
                let first = true;
                $.each(items, function (i, item) {
                    const tocText = tocCache[bookId].find(t => t.paragraph == paragraph)?.toc || '';
                    const paranum = first ? `<div class="position-absolute bottom-0 end-0 p-2 text-muted">${paragraph}</div>` : '';
                    first = false;
                    const $card = $(`
                        <div class="card">
                            <div class="card-body">
                                <p class="pali-text">${item.sentence_content}</p>
                                ${item.translation_content_2 ? `<p class="translation2-text">${item.translation_content_2}</p>` : ''}
                                ${item.translation_content ? `<p class="translation-text">${item.translation_content}</p>` : ''}
                                ${paranum}
                            </div>
                        </div>
                    `);
                    $container.append($card);
                });
                $(contentDiv).append($container);
            });

            // Mark content as loaded
            contentDiv.setAttribute('data-loaded', 'true');
            contentDiv.classList.add('active');
            link.classList.remove('collapsed');
        });
    });
}