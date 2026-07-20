window.FlashPageState = {
    _state: {},
    _listeners: {},

    get: function(key, fallback = null) {
        return this._state[key] !== undefined ? this._state[key] : fallback;
    },

    set: function(key, value) {
        this._state[key] = value;
        if (this._listeners[key]) {
            this._listeners[key].forEach(callback => callback(value));
        }
    },

    onChange: function(key, callback) {
        if (!this._listeners[key]) {
            this._listeners[key] = [];
        }
        this._listeners[key].push(callback);
    }
};

window.fpBindWidgets = function() {
    const widgets = document.querySelectorAll('[data-fp-widget]');
    widgets.forEach(widget => {
        // Prevent rebinding
        if (widget.hasAttribute('data-fp-bound')) return;
        widget.setAttribute('data-fp-bound', 'true');

        const widgetType = widget.getAttribute('data-fp-widget');
        const id = widget.id;

        if (widgetType === 'text_input') {
            // Set initial state
            FlashPageState.set(id, widget.value);
            
            // Listen for changes
            widget.addEventListener('input', (e) => {
                FlashPageState.set(id, e.target.value);
            });
        }
        // Additional widget types (select, checkbox, etc.) can be handled here.
    });
};

document.addEventListener("DOMContentLoaded", function() {
    window.fpBindWidgets();
});
