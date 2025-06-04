<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Calendar Assistant</title>
</head>
<body>
    <div id="login-form">
        <button id="ms-login">Sign in with Microsoft</button>
    </div>

    <div id="dashboard" style="display:none;">
        <button id="events-btn">Manage Events</button>
        <button id="pdf-btn">Parse PDF</button>
        <button id="chat-btn">AI Chatbot</button>
        <button id="logout-btn">Logout</button>
    </div>

    <div id="events-section" style="display:none;">
        <!-- TODO: plug in event CRUD UI here -->
        <p>Event management section</p>
    </div>

    <div id="pdf-section" style="display:none;">
        <!-- TODO: plug in PDF parsing interface here -->
        <p>PDF parser section</p>
    </div>

    <div id="chat-section" style="display:none;">
        <!-- TODO: plug in AI chatbot UI here -->
        <p>AI Chatbot section</p>
    </div>

    <script>
    const loginButton = document.getElementById('ms-login');
    const dashboard = document.getElementById('dashboard');
    const loginView = document.getElementById('login-view');

    const eventsBtn = document.getElementById('events-btn');
    const pdfBtn = document.getElementById('pdf-btn');
    const chatBtn = document.getElementById('chat-btn');
    const logoutBtn = document.getElementById('logout-btn');

    const eventsSection = document.getElementById('events-section');
    const pdfSection = document.getElementById('pdf-section');
    const chatSection = document.getElementById('chat-section');

    function showSection(section) {
        eventsSection.style.display = 'none';
        pdfSection.style.display = 'none';
        chatSection.style.display = 'none';
        if (section) {
            section.style.display = 'block';
        }
    }

    function checkAuth() {
        const token = localStorage.getItem('access_token');
        const userId = localStorage.getItem('user_id');
        if (token && userId) {
            loginView.style.display = 'none';
            dashboard.style.display = 'block';
        } else {
            loginView.style.display = 'block';
            dashboard.style.display = 'none';
            showSection(null);
        }
    }

    loginButton.addEventListener('click', () => {
        window.location.href = '/oauth/login';
    });

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_id');
        checkAuth();
    });

    eventsBtn.addEventListener('click', () => {
        showSection(eventsSection); // attach CRUD logic here
    });

    pdfBtn.addEventListener('click', () => {
        showSection(pdfSection); // attach PDF parser logic here
    });

    chatBtn.addEventListener('click', () => {
        showSection(chatSection); // attach chatbot integration here
    });

    window.addEventListener('load', checkAuth);
    </script>
    <div id="status"></div>

    <div id="login-form">
        <input id="username" placeholder="Username">
        <input id="password" placeholder="Password" type="password">
        <button id="login">Log In</button>
    </div>

    <div id="events"></div>

    <div id="create-form">
        <input id="create-subject" placeholder="Subject">
        <input id="create-start" placeholder="Start (ISO)">
        <button id="create-event">Create Event</button>
    </div>

    <div id="update-form">
        <input id="update-id" placeholder="Event ID">
        <input id="update-subject" placeholder="Subject (optional)">
        <input id="update-start" placeholder="Start (ISO optional)">
        <button id="update-event">Update Event</button>
    </div>

    <div id="delete-form">
        <input id="delete-id" placeholder="Event ID">
        <button id="delete-event">Delete Event</button>
    </div>

    <button id="logout">Log Out</button>

    <script src="main.js"></script>
</body>
</html>












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
