$(document).ready(function () {
    // Tab switching
    $('.selection-tabs .tab').click(function () {
        $('.selection-tabs .tab').removeClass('active');
        $(this).addClass('active');
        $('.tab-content').removeClass('active');
        $('#' + $(this).data('tab')).addClass('active');
    });

    // Load books when channel changes
    $('#channel-select').change(function () {
        var channelId = $(this).val();
        $('#loading-channel-books').show();
        $('#book-select-by-channel').empty().append('<option value="">Select a book</option>');
        if (channelId) {
            $.get('/api/books/' + channelId, function (data) {
                $('#book-select-by-channel').empty().append('<option value="">Select a book</option>');
                $.each(data, function (i, book) {
                    $('#book-select-by-channel').append(
                        '<option value="' + book.book + '">' + book.book + ' - ' + book.name + ' (' + book.lines_count + ' lines)</option>'
                    );
                });
                $('#loading-channel-books').hide();
            });
        } else {
            $('#loading-channel-books').hide();
        }
    });

    // Load channels when book changes
    $('#book-select').change(function () {
        var bookId = $(this).val();
        $('#loading-book-channels').show();
        $('#channel-select-by-book').empty().append('<option value="">Select a channel</option>');
        if (bookId) {
            $.get('/api/channels/' + bookId, function (data) {
                $.each(data, function (i, channel) {
                    $('#channel-select-by-book').append(
                        '<option value="' + channel.id + '">' + channel.name + '(' + channel.lines_count + 'lines)</option>'
                    );
                });
                $('#loading-book-channels').hide();
            });
        } else {
            $('#loading-book-channels').hide();
        }
    });

    // Sanitize TOC text for anchor IDs
    function sanitizeAnchor(text) {
        return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    }

    // Global TOC cache
    var tocCache = {};

    // Load TOC when book is selected
    function loadTOC(bookId) {
        if (!bookId) {
            $('#toc-content').empty();
            return;
        }
        if (tocCache[bookId]) {
            renderTOC(tocCache[bookId]);
        } else {
            $.get('/api/toc/' + bookId, function (data) {
                tocCache[bookId] = data;
                renderTOC(data);
            });
        }
    }

    // Render TOC
    function renderTOC(data) {
        $('#toc-content').empty();
        var tocTree = {};
        data.forEach(function (item) {
            if (!tocTree[item.level]) tocTree[item.level] = [];
            tocTree[item.level].push(item);
        });

        var $ul = $('<ul class="toc-list list-unstyled">');
        if (tocTree[2]) {
            tocTree[2].forEach(function (level2) {
                var anchor = sanitizeAnchor(level2.toc);
                var $li = $('<li class="toc-item level-' + level2.level + '">')
                    .append('<span class="toc-toggle" data-bs-toggle="collapse" data-bs-target="#toc-' + level2.id + '"><i class="bi bi-chevron-right"></i></span>')
                    .append('<a href="#para-' + level2.paragraph + '" class="toc-name">' + level2.toc + '</a>')
                    .append('<span class="toc-info"> (Len: ' + level2.chapter_len + ', Para: ' + level2.paragraph + ')</span>');
                var $subUl = $('<ul class="toc-list list-unstyled collapse" id="toc-' + level2.id + '">');
                if (tocTree[3]) {
                    tocTree[3].filter(function (item) { return item.parent == level2.paragraph; }).forEach(function (level3) {
                        var subAnchor = sanitizeAnchor(level3.toc);
                        var $subLi = $('<li class="toc-item level-' + level3.level + '">')
                            .append('<span class="toc-toggle" data-bs-toggle="collapse" data-bs-target="#toc-' + level3.id + '"><i class="bi bi-chevron-right"></i></span>')
                            .append('<a href="#para-' + level3.paragraph + '" class="toc-name">' + level3.toc + '</a>')
                            .append('<span class="toc-info"> (Len: ' + level3.chapter_len + ', Para: ' + level3.paragraph + ')</span>');
                        var $subSubUl = $('<ul class="toc-list list-unstyled collapse" id="toc-' + level3.id + '">');
                        if (tocTree[4]) {
                            tocTree[4].filter(function (item) { return item.parent == level3.paragraph; }).forEach(function (level4) {
                                var subSubAnchor = sanitizeAnchor(level4.toc);
                                $subSubUl.append(
                                    '<li class="toc-item level-' + level4.level + '">' +
                                    '<a href="#para-' + level4.paragraph + '" class="toc-name">' + level4.toc + '</a>' +
                                    '<span class="toc-info"> (Len: ' + level4.chapter_len + ', Para: ' + level4.paragraph + ')</span></li>'
                                );
                            });
                        }
                        $subLi.append($subSubUl);
                        $subUl.append($subLi);
                    });
                }
                $li.append($subUl);
                $ul.append($li);
            });
        }
        $('#toc-content').append($ul);

        $('.toc-toggle').click(function () {
            var $icon = $(this).find('i');
            $icon.toggleClass('bi-chevron-right bi-chevron-down');
        });

        $('.toc-name').click(function (e) {
            e.preventDefault();
            var anchorId = $(this).attr('href');
            $('html, body').animate({
                scrollTop: $(anchorId).offset().top - 70
            }, 500);
        });
    }
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            if (!timeout) { // Only execute if no pending timeout
                timeout = setTimeout(() => {
                    func.apply(this, args);
                    timeout = null; // Reset timeout after execution
                }, wait);
            }
        };
    }

    // Lazy loading for translations
    var currentPage = 1;
    var loading = false;
    var bookId = new URLSearchParams(window.location.search).get('book');
    var channelId = new URLSearchParams(window.location.search).get('channel');
    var lastParagraph = 0;

    function loadMoreTranslations() {
        if (loading || !bookId || !channelId) return;
        loading = true;
        $('#loading-translations').show();

        var paragraphStart = lastParagraph + 1;
        var paragraphEnd = paragraphStart + 9;

        $.get('/api/translations', paragraphStart < 10 ? {
            book: bookId,
            channel: channelId,
        } : {
            book: bookId,
            channel: channelId,
            paragraph_start: paragraphStart,
            paragraph_end: paragraphEnd
        }, function (data) {
            if ($.isEmptyObject(data)) {
                $('#loading-translations').text('No more translations available');
                loading = false;
                return;
            }

            var tocPromise = tocCache[bookId] ? $.Deferred().resolve(tocCache[bookId]) : $.get('/api/toc/' + bookId);
            tocPromise.done(function (tocData) {
                if (!tocCache[bookId]) tocCache[bookId] = tocData;

                $.each(data, function (paragraph, items) {
                    var $container = $('<div class="paragraph-container" data-paragraph="' + paragraph + '" id="para-' + paragraph + '">');
                    var first = true;
                    $.each(items, function (i, item) {
                        var tocText = '';
                        var tocItem = tocData.find(function (t) { return t.paragraph == paragraph; });
                        if (tocItem) tocText = sanitizeAnchor(tocItem.toc);

                        var paranum = first ? '<div class="position-absolute bottom-0 end-0 p-2 text-muted">' + paragraph + '</div>' : '';
                        first = false;
                        var $card = $('<div class="card mb-1 position-relative">').append(
                            '<div class="card-body">' +
                            '<p class="pali-text">' + item.sentence_content + '</p>' +
                            (item.translation_content ? '<p class="translation-text">' + item.translation_content + '</p>' : '') +
                            paranum +
                            '</div>'
                        );
                        $container.append($card);
                        $('#translations-container').append($container);
                        lastParagraph = Math.max(lastParagraph, parseInt(paragraph));
                    });
                });
                loading = false;
                $('#loading-translations').hide();
            });
        });
    }

    // Infinite scroll with debounced loadMoreTranslations
    $(window).on('scroll', debounce(function () {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            loadMoreTranslations();
        }
    }, 200));


    // Handle book and channel changes
    function handleSelectionChange(formId) {
        // var bookId = new URLSearchParams(window.location.search).get('book');
        // var channelId = new URLSearchParams(window.location.search).get('channel');


        if (formId == "channel-first-form") {
            var newBookId = $('#book-select-by-channel').val();
            var newChannelId = $('#channel-select').val();

        } else {
            var newBookId = $('#book-select').val();
            var newChannelId = $('#channel-select-by-book').val();

        }

        if (newBookId && newChannelId && (newBookId !== bookId || newChannelId !== channelId)) {
            bookId = newBookId;
            channelId = newChannelId;
            history.pushState({}, '', '/view?book=' + bookId + '&channel=' + channelId);
            lastParagraph = 0;
            $('#translations-container').empty();
            $('#loading-translations').text('Loading more...').show();
            loadTOC(bookId);
            loadMoreTranslations();
        }
    }

    // Initialize bookId and channelId from URL if present
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }
    if (!bookId) bookId = getUrlParameter('book');
    if (!channelId) channelId = getUrlParameter('channel');

    // Load initial TOC and translations if book and channel are selected
    if (bookId && channelId) {
        loadTOC(bookId);
        $('#translations-container').empty();
        $('#loading-translations').text('Loading more...').show();
        loadMoreTranslations();
    }

    // Handle form submission
    $('#channel-first-form, #book-first-form').submit(function (e) {
        e.preventDefault();
        handleSelectionChange(e.currentTarget.id);
    });

    // Handle select changes
    // $('#book-select-by-channel').change(function (e) {
    //     bookId = $('#book-select-by-channel').val();
    // });
    // $('#channel-select-by-book').change(function (e) {
    //     channelId = $('#channel-select-by-book').val();
    // });

    // Toggle sidebar
    $('#tocSidebar').on('show.bs.collapse', function () {
        $('.main-content').addClass('sidebar-open');
        var sidebarBookId = $('#book-select').val() || $('#book-select-by-channel').val();
        if (sidebarBookId && sidebarBookId !== bookId) {
            bookId = sidebarBookId;
            loadTOC(bookId);
        } else if (bookId) {
            loadTOC(bookId);
        }
    }).on('hide.bs.collapse', function () {
        $('.main-content').removeClass('sidebar-open');
    });
});