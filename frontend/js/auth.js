// JWT helpers
function setToken(token) { localStorage.setItem('token', token); }
function getToken() { return localStorage.getItem('token'); }
function removeToken() { localStorage.removeItem('token'); }
function isLoggedIn() { return !!getToken(); }
