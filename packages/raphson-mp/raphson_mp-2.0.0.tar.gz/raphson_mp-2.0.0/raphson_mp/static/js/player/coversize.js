// Ensures combined height of album cover and lyrics box never exceed 100vh

class CoverSize {
    #lyricsBox;
    #coverBox;
    #body;
    #timeoutId;

    constructor() {
        document.addEventListener('DOMContentLoaded', () => {
            this.#lyricsBox = document.getElementById('lyrics-box');
            this.#coverBox = document.getElementById('album-cover-box');
            this.#body = document.getElementsByTagName("body")[0];

            const resizeObserver = new ResizeObserver(() => this.#observerCallback());
            resizeObserver.observe(this.#lyricsBox);
            resizeObserver.observe(this.#body);
        });
    }

    #setMaxHeight(value) {
        this.#coverBox.style.maxHeight = value;
        this.#coverBox.style.maxWidth = value;
        this.#lyricsBox.style.maxWidth = value;
        console.debug('coversize: max height changed:', value);
    }

    resizeCover() {
        // Do not set max height in single column interface
        if (this.#body.clientWidth <= 950) {
            this.#setMaxHeight('none');
            return;
        }

        if (this.#lyricsBox.hidden) {
            // No lyrics
            this.#setMaxHeight(`calc(100vh - 2*var(--gap))`);
            return;
        }

        this.#setMaxHeight(`calc(100vh - 3*var(--gap) - ${this.#lyricsBox.clientHeight}px)`);
    }

    #observerCallback() {
        // Throttle function calls
        if (this.#timeoutId) {
            clearTimeout(this.#timeoutId);
        }

        this.#timeoutId = setTimeout(() => this.resizeCover(), 100);
    }
}

const coverSize = new CoverSize();
