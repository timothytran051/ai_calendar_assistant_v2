(function() {
    // Section elements
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const eventsSection = document.getElementById('events-section');
    const pdfSection = document.getElementById('pdf-section');
    const chatSection = document.getElementById('chat-section');
    const statusDiv = document.getElementById('status');

    // Dashboard navigation buttons
    const msLoginBtn = document.getElementById('ms-login');
    const eventsBtn = document.getElementById('events-btn');
    const pdfBtn = document.getElementById('pdf-btn');
    const chatBtn = document.getElementById('chat-btn');
    const logoutBtn = document.getElementById('logout-btn');

    // Event CRUD UI elements
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

    const API_BASE = "http://localhost:8000"; 

    // Helper: show only the given section
    function showSection(section) {
        eventsSection.style.display = 'none';
        pdfSection.style.display = 'none';
        chatSection.style.display = 'none';
        if (section) section.style.display = 'block';
    }

    window.onload = function() {
    // Parse query params for access_token and user_id
    const params = new URLSearchParams(window.location.search);
    const token = params.get("access_token");
    const userId = params.get("user_id");
    if (token && userId) {
        localStorage.setItem("access_token", token);
        localStorage.setItem("user_id", userId);
        // Remove tokens from URL (so refresh is clean)
        window.history.replaceState({}, document.title, "/");
    }
    // Now call your existing checkAuth or init logic
    checkAuth();
};


    // Auth state: update UI
    function checkAuth() {
        const token = localStorage.getItem('access_token');
        const userId = localStorage.getItem('user_id');
        if (token && userId) {
            loginSection.style.display = 'none';
            dashboardSection.style.display = 'block';
            statusDiv.textContent = 'User is logged in';
        } else {
            loginSection.style.display = 'block';
            dashboardSection.style.display = 'none';
            showSection(null);
            statusDiv.textContent = 'User is not logged in';
        }
    }

    // Microsoft OAuth login
if (msLoginBtn) {
    msLoginBtn.addEventListener('click', function() {
        window.location.href = 'http://127.0.0.1:8000/oauth/login';
    });
}

    // Dashboard navigation
    eventsBtn.addEventListener('click', function() {
        showSection(eventsSection);
        fetchEvents();
    });
    pdfBtn.addEventListener('click', function() { showSection(pdfSection); });
    chatBtn.addEventListener('click', function() { showSection(chatSection); });

    logoutBtn.addEventListener('click', function() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_id');
        location.reload();
    });

    // -----------------------
    // Event CRUD logic below:
    // -----------------------

    // Helper for authorized API requests
    async function authorizedFetch(url, options = {}) {
        const token = localStorage.getItem('access_token');
        const uid = localStorage.getItem('user_id');
        options.headers = options.headers || {};
        options.headers['Authorization'] = 'Bearer ' + token;
        options.headers['User-ID'] = uid;
        return fetch(url, options);
    }

    function maybeUpdateToken(data) {
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
        }
    }

    async function fetchEvents() {
        try {
            const res = await authorizedFetch(`${API_BASE}/events`);
            const data = await res.json();
            maybeUpdateToken(data);
            eventsDiv.textContent = JSON.stringify(data, null, 2);
        } catch (err) {
            console.error('Failed to fetch events', err);
        }
    }

    async function createEvent() {
        const body = {
            subject: createSubject.value,
            start: createStart.value
        };
        try {
            const res = await authorizedFetch(`${API_BASE}/events`, {
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
            const res = await authorizedFetch(`${API_BASE}/events`, {
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
            const res = await authorizedFetch(`${API_BASE}/events`, {
                method: 'DELETE'
            });
            const data = await res.json();
            maybeUpdateToken(data);
            fetchEvents();
        } catch (err) {
            console.error('Failed to delete event', err);
        }
    }

    createBtn.addEventListener('click', createEvent);
    updateBtn.addEventListener('click', updateEvent);
    deleteBtn.addEventListener('click', deleteEvent);

    // On load, show correct view
    window.addEventListener('load', checkAuth);
})();
