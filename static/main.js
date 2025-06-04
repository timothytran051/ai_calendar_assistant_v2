(function() {
    const statusDiv = document.getElementById('status');
    const logoutBtn = document.getElementById('logout');
    const loginBtn = document.getElementById('login');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const eventsDiv = document.getElementById('events');

    const createSubject = document.getElementById('create-subject');
    const createStart = document.getElementById('create-start');
    const createBtn = document.getElementById('create-event');

    const updateId = document.getElementById('update-id');
    const updateSubject = document.getElementById('update-subject');
    const updateStart = document.getElementById('update-start');
    const updateBtn = document.getElementById('update-event');

    const deleteId = document.getElementById('delete-id');
    const deleteBtn = document.getElementById('delete-event');

    const accessToken = localStorage.getItem('access_token');
    const userId = localStorage.getItem('user_id');

    async function authorizedFetch(url, options = {}) {
        const token = localStorage.getItem('access_token');
        const uid = localStorage.getItem('user_id');
        options.headers = options.headers || {};
        options.headers['Authorization'] = 'Bearer ' + token;
        options.headers['X-User-ID'] = uid;
        return fetch(url, options);
    }

    function maybeUpdateToken(data) {
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
        }
    }

    async function fetchEvents() {
        try {
            const res = await authorizedFetch('/events');
            const data = await res.json();
            maybeUpdateToken(data);
            eventsDiv.textContent = JSON.stringify(data, null, 2);
        } catch (err) {
            console.error('Failed to fetch events', err);
        }
    }

    async function login(username, password) {
        try {
            const res = await fetch('/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            if (data.access_token && data.user_id) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('user_id', data.user_id);
                statusDiv.textContent = 'User is logged in';
                fetchEvents();
            } else {
                statusDiv.textContent = 'Login failed';
            }
        } catch (err) {
            statusDiv.textContent = 'Login request failed';
            console.error(err);
        }
    }

    async function createEvent() {
        const body = {
            subject: createSubject.value,
            start: createStart.value
        };
        try {
            const res = await authorizedFetch('/events', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await res.json();
            maybeUpdateToken(data);
            fetchEvents();
        } catch (err) {
            console.error('Failed to create event', err);
        }
    }

    async function updateEvent() {
        const body = {};
        if (updateSubject.value) body.subject = updateSubject.value;
        if (updateStart.value) body.start = updateStart.value;
        const id = updateId.value;
        if (!id) return;
        try {
            const res = await authorizedFetch(`/events/${id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await res.json();
            maybeUpdateToken(data);
            fetchEvents();
        } catch (err) {
            console.error('Failed to update event', err);
        }
    }

    async function deleteEvent() {
        const id = deleteId.value;
        if (!id) return;
        try {
            const res = await authorizedFetch(`/events/${id}`, {
                method: 'DELETE'
            });
            const data = await res.json();
            maybeUpdateToken(data);
            fetchEvents();
        } catch (err) {
            console.error('Failed to delete event', err);
        }
    }

    if (accessToken && userId) {
        statusDiv.textContent = 'User is logged in';
        fetchEvents();
    } else {
        statusDiv.textContent = 'User is not logged in';
    }

    logoutBtn.addEventListener('click', function() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_id');
        location.reload();
    });

    loginBtn.addEventListener('click', function() {
        login(usernameInput.value, passwordInput.value);
    });

    createBtn.addEventListener('click', function() {
        createEvent();
    });

    updateBtn.addEventListener('click', function() {
        updateEvent();
    });

    deleteBtn.addEventListener('click', function() {
        deleteEvent();
    });
})();
