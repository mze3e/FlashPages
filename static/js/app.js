// Content CMS JavaScript functionality
(function($) {
    'use strict';

    // Initialize when DOM is ready
    $(document).ready(function() {
        initSearch();
        initTooltips();
        initScrollSpy();
        initCodeBlocks();
        initTables();
        initForms();
    });

    // Search functionality
    function initSearch() {
        const searchInput = $('#search-input');
        const searchResults = $('#search-results');
        let searchTimeout;

        if (searchInput.length === 0) return;

        searchInput.on('input', function() {
            const query = $(this).val().trim();
            
            clearTimeout(searchTimeout);
            
            if (query.length < 2) {
                searchResults.addClass('d-none').empty();
                return;
            }

            // Debounce search requests
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });

        // Hide search results when clicking outside
        $(document).on('click', function(e) {
            if (!$(e.target).closest('#search-form').length) {
                searchResults.addClass('d-none');
            }
        });

        function performSearch(query) {
            searchResults.removeClass('d-none').html('<div class="p-2 text-muted">Searching...</div>');

            $.get('/api/search', { query: query, limit: 5 })
                .done(function(data) {
                    displaySearchResults(data.results);
                })
                .fail(function() {
                    searchResults.html('<div class="p-2 text-danger">Search failed</div>');
                });
        }

        function displaySearchResults(results) {
            if (results.length === 0) {
                searchResults.html('<div class="p-2 text-muted">No results found</div>');
                return;
            }

            let html = '';
            results.forEach(function(result) {
                html += `
                    <div class="search-result-item" onclick="window.location.href='${result.slug}'">
                        <div class="search-result-title">${result.title}</div>
                        <div class="search-result-snippet">${result.snippet}</div>
                    </div>
                `;
            });

            searchResults.html(html);
        }
    }

    // Initialize Bootstrap tooltips
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Initialize ScrollSpy for docs navigation
    function initScrollSpy() {
        if ($('body').hasClass('docs-page')) {
            new bootstrap.ScrollSpy(document.body, {
                target: '#docs-nav',
                offset: 100
            });
        }
    }

    // Enhance code blocks
    function initCodeBlocks() {
        $('pre code').each(function() {
            const $code = $(this);
            const $pre = $code.parent();

            // Add copy button
            const $copyBtn = $('<button class="btn btn-sm btn-outline-secondary copy-btn">Copy</button>');
            $pre.css('position', 'relative').append($copyBtn);

            $copyBtn.on('click', function(e) {
                e.preventDefault();
                
                // Copy to clipboard
                const textArea = document.createElement('textarea');
                textArea.value = $code.text();
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);

                // Show feedback
                const originalText = $copyBtn.text();
                $copyBtn.text('Copied!').addClass('btn-success');
                setTimeout(() => {
                    $copyBtn.text(originalText).removeClass('btn-success');
                }, 1000);
            });
        });
    }

    // Enhance tables
    function initTables() {
        $('.content table').each(function() {
            const $table = $(this);
            
            // Make tables responsive if not already
            if (!$table.parent().hasClass('table-responsive')) {
                $table.wrap('<div class="table-responsive"></div>');
            }
            
            // Add Bootstrap table classes
            $table.addClass('table table-striped table-hover');
        });
    }

    // Form submission handling for component modals
    function initForms() {
        // Make submitForm available globally
        window.submitForm = async function(formId) {
            const form = document.getElementById(formId);
            if (!form) return;
            
            const formData = new FormData(form);
            const modalElement = form.closest('.modal');
            const modal = modalElement ? bootstrap.Modal.getInstance(modalElement) : null;
            
            // Add current page URL
            formData.append('page_url', window.location.pathname);
            
            try {
                const response = await fetch('/api/forms/submit', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    showAlert('success', result.message || 'Form submitted successfully!');
                    form.reset();
                    if (modal) modal.hide();
                } else {
                    throw new Error(result.message || 'Failed to submit form');
                }
            } catch (error) {
                showAlert('danger', 'Error submitting form: ' + error.message);
            }
        };
        
        // Alert display function
        window.showAlert = function(type, message) {
            const alertDiv = $(`
                <div class="alert alert-${type} alert-dismissible fade show" style="position: fixed; top: 20px; right: 20px; z-index: 9999; max-width: 350px;">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `);
            
            $('body').append(alertDiv);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                alertDiv.alert('close');
            }, 5000);
        };

        window.saveData = async function(source) {
            const table = document.getElementById('data-editor-' + source);
            if (!table) {
                showAlert('danger', 'Data table not found.');
                return;
            }

            const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
            const data = [];

            table.querySelectorAll('tbody tr').forEach(row => {
                const rowData = {};
                row.querySelectorAll('td').forEach((cell, index) => {
                    const field = cell.dataset.field || headers[index];
                    rowData[field] = cell.textContent;
                });
                data.push(rowData);
            });

            try {
                const response = await fetch('/api/forms/data/' + source, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                const result = await response.json();

                if (response.ok) {
                    showAlert('success', result.message || 'Data saved successfully!');
                } else {
                    throw new Error(result.detail || 'Failed to save data');
                }
            } catch (error) {
                showAlert('danger', 'Error saving data: ' + error.message);
            }
        };
    }

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(e) {
        const target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 600, 'swing');
        }
    });

    // Auto-resize textareas
    function autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    }

    $('textarea.auto-resize').each(function() {
        autoResizeTextarea(this);
    }).on('input', function() {
        autoResizeTextarea(this);
    });

    // Form validation enhancement
    $('.needs-validation').on('submit', function(e) {
        const form = this;
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        $(form).addClass('was-validated');
    });

    // Loading states for buttons
    $('.btn[data-loading]').on('click', function() {
        const $btn = $(this);
        const originalText = $btn.html();
        const loadingText = $btn.data('loading') || 'Loading...';
        
        $btn.html(`<span class="spinner-border spinner-border-sm me-2"></span>${loadingText}`)
            .prop('disabled', true);
        
        // Reset after form submission or timeout
        setTimeout(() => {
            $btn.html(originalText).prop('disabled', false);
        }, 5000);
    });

    // Keyboard shortcuts
    $(document).on('keydown', function(e) {
        // Ctrl/Cmd + S to save (in editor)
        if ((e.ctrlKey || e.metaKey) && e.keyCode === 83) {
            const $form = $('#editor-form');
            if ($form.length) {
                e.preventDefault();
                $form.submit();
            }
        }
        
        // Ctrl/Cmd + / for search
        if ((e.ctrlKey || e.metaKey) && e.keyCode === 191) {
            e.preventDefault();
            $('#search-input').focus();
        }
        
        // Escape to close modals/search
        if (e.keyCode === 27) {
            $('#search-results').addClass('d-none');
            $('.modal').modal('hide');
        }
    });

    // Theme switcher (if implemented)
    $('.theme-switcher').on('change', function() {
        const theme = $(this).val();
        // This would require backend implementation
        $.post('/cms/theme', { theme: theme })
            .done(() => location.reload())
            .fail(() => alert('Theme change failed'));
    });

    // Auto-save functionality for editors
    let autoSaveTimer;
    let hasUnsavedChanges = false;

    $('#content').on('input', function() {
        hasUnsavedChanges = true;
        clearTimeout(autoSaveTimer);
        
        // Auto-save to localStorage after 2 seconds of inactivity
        autoSaveTimer = setTimeout(function() {
            const content = $('#content').val();
            const path = $('input[name="path"]').val();
            
            if (path && content) {
                localStorage.setItem(`cms_draft_${path}`, content);
                console.log('Auto-saved draft to localStorage');
            }
        }, 2000);
    });

    // Warn about unsaved changes
    $(window).on('beforeunload', function(e) {
        if (hasUnsavedChanges) {
            const message = 'You have unsaved changes. Are you sure you want to leave?';
            e.returnValue = message;
            return message;
        }
    });

    // Mark changes as saved when form is submitted
    $('#editor-form').on('submit', function() {
        hasUnsavedChanges = false;
    });

    // Load draft from localStorage if available
    $(window).on('load', function() {
        const path = $('input[name="path"]').val();
        if (path) {
            const draft = localStorage.getItem(`cms_draft_${path}`);
            if (draft && draft !== $('#content').val()) {
                if (confirm('A draft was found in local storage. Do you want to load it?')) {
                    $('#content').val(draft);
                    hasUnsavedChanges = true;
                }
            }
        }
    });

})(jQuery);

// Global utility functions
window.CMS = {
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toast = $(`
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `);
        
        $('.toast-container').append(toast);
        new bootstrap.Toast(toast[0]).show();
        
        // Remove from DOM after hiding
        toast.on('hidden.bs.toast', function() {
            $(this).remove();
        });
    },

    // Confirm action
    confirm: function(message, callback) {
        if (window.confirm(message)) {
            callback();
        }
    },

    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
};
