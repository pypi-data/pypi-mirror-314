document.addEventListener('DOMContentLoaded', () => {
    /** @type {HTMLButtonElement} */
    const syncButton = document.getElementById('sync-button');
    /** @type {HTMLButtonElement} */
    const stopButton = document.getElementById('stop-button');
    /** @type {HTMLTableElement} */
    const table = document.getElementById('table');
    /** @type {HTMLTableSectionElement} */
    const log = document.getElementById('log');
    /** @type {HTMLParagraphElement} */
    const wait = document.getElementById('wait');

    const decoder = new TextDecoder();

    function createRow(entry) {
        const tdTask = document.createElement('td');
        tdTask.textContent = entry.task;
        const tdIcon = document.createElement('td');
        if (entry.done) {
            tdIcon.classList.add('icon', 'icon-check', 'icon-col');
        } else {
            tdIcon.classList.add('icon', 'icon-loading', 'spinning', 'icon-col');
        }
        const row = document.createElement('tr');
        row.dataset.task = entry.task;
        row.append(tdTask, tdIcon);
        return row
    }

    function handleEntry(entry) {
        if (entry.done) {
            for (const row of log.children) {
                if (row.dataset.task == entry.task) {
                    row.replaceWith(createRow(entry));
                    return;
                }
            }
            log.append(createRow(entry));
        } else {
            log.append(createRow(entry));
        }

        if (log.children.length > 10) {
            log.children[0].remove();
        }
    }

    function handleResponse(result) {
        const values = decoder.decode(result.value);
        for (const value of values.split('\n')) {
            if (value) {
                console.debug('received value', value);
                handleEntry(JSON.parse(value))
            }
        }
        return result
    }

    syncButton.addEventListener('click', async () => {
        const response = await fetch('/offline/start', {method: 'POST'});
        checkResponseCode(response);
        wait.hidden = false;
    });

    stopButton.addEventListener('click', async () => {
        const response = await fetch('/offline/stop', {method: 'POST'});
        checkResponseCode(response);
    });

    async function monitor() {
        try {
            const response = await fetch('/offline/monitor', {method: 'GET'});
            checkResponseCode(response);
            if (response.status == 204) {
                // not running yet
            } else {
                syncButton.hidden = true;
                stopButton.hidden = false;
                const reader = response.body.getReader();
                await reader.read().then(function process(result) {
                    table.hidden = false;
                    wait.hidden = true;
                    if (result.done) {
                        return reader.closed;
                    }
                    return reader.read().then(handleResponse).then(process)
                });
            }
        } catch (err) {
            console.error(err);
            alert('error, check console');
        } finally {
            syncButton.hidden = false;
            stopButton.hidden = true;
            wait.hidden = true;
        }

        setTimeout(monitor, document.visibilityState == 'visible' ? 500 : 2000);
    }

    monitor();

});
