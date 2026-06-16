/* ── api.js — Client HTTP vers le backend FastAPI ───────────── */

const API_BASE = 'http://localhost:8000/api/v1';

// ── Tokens ───────────────────────────────────────────────────

const Auth = {
  getToken()  { return localStorage.getItem('access_token'); },
  getRefresh(){ return localStorage.getItem('refresh_token'); },
  setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  },
  clear() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
  },
  isLoggedIn() { return !!this.getToken(); },
  getUser() {
    const u = localStorage.getItem('current_user');
    return u ? JSON.parse(u) : null;
  },
  setUser(u) { localStorage.setItem('current_user', JSON.stringify(u)); },
  getRole() { return this.getUser()?.role?.libelle || 'visiteur'; },
  can(...roles) { return roles.includes(this.getRole()); },
};

// ── Fetch wrapper ─────────────────────────────────────────────

async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (Auth.isLoggedIn()) headers['Authorization'] = `Bearer ${Auth.getToken()}`;

  let res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  // Auto-refresh si 401
  if (res.status === 401 && Auth.getRefresh()) {
    const r = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: Auth.getRefresh() }),
    });
    if (r.ok) {
      const data = await r.json();
      Auth.setTokens(data.access_token, data.refresh_token);
      headers['Authorization'] = `Bearer ${data.access_token}`;
      res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    } else {
      Auth.clear();
      window.location.href = '/pages/login.html';
      return;
    }
  }

  if (!res.ok) {
    let err;
    try { err = await res.json(); } catch { err = { detail: 'Erreur réseau' }; }
    throw new Error(err.detail || `Erreur ${res.status}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

const api = {
  get:    (path, opts={}) => apiFetch(path, { method: 'GET',    ...opts }),
  post:   (path, body, opts={}) => apiFetch(path, { method: 'POST',   body: JSON.stringify(body), ...opts }),
  patch:  (path, body, opts={}) => apiFetch(path, { method: 'PATCH',  body: JSON.stringify(body), ...opts }),
  put:    (path, body, opts={}) => apiFetch(path, { method: 'PUT',    body: JSON.stringify(body), ...opts }),
  delete: (path, opts={}) => apiFetch(path, { method: 'DELETE', ...opts }),

  // Upload multipart
  upload: async (path, formData) => {
    const headers = {};
    if (Auth.isLoggedIn()) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    const res = await fetch(`${API_BASE}${path}`, { method: 'POST', headers, body: formData });
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail); }
    return res.json();
  },

  // Téléchargement binaire (docx, xlsx, pdf, etc.)
  download: async (path, body, filename) => {
    const headers = { 'Content-Type': 'application/json' };
    if (Auth.isLoggedIn()) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    let res = await fetch(`${API_BASE}${path}`, {
      method: 'POST', headers, body: JSON.stringify(body)
    });
    if (res.status === 401 && Auth.getRefresh()) {
      const r = await fetch(`${API_BASE}/auth/refresh`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: Auth.getRefresh() }),
      });
      if (r.ok) {
        const data = await r.json();
        Auth.setTokens(data.access_token, data.refresh_token);
        headers['Authorization'] = `Bearer ${data.access_token}`;
        res = await fetch(`${API_BASE}${path}`, { method: 'POST', headers, body: JSON.stringify(body) });
      } else {
        Auth.clear();
        window.location.href = '../login.html';
        return;
      }
    }
    if (!res.ok) {
      let err; try { err = await res.json(); } catch { err = { detail: 'Erreur réseau' }; }
      throw new Error(err.detail || `Erreur ${res.status}`);
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  },
};

// ── Toast notifications ───────────────────────────────────────

const Toast = {
  container: null,
  init() {
    if (this.container) return;
    this.container = document.createElement('div');
    this.container.style.cssText = `
      position:fixed; bottom:24px; right:24px; z-index:9999;
      display:flex; flex-direction:column; gap:10px; pointer-events:none;
    `;
    document.body.appendChild(this.container);
  },
  show(msg, type = 'info', duration = 4000) {
    this.init();
    const colors = { info:'#3b82f6', success:'#06d6a0', error:'#ef4444', warn:'#f59e0b' };
    const icons  = { info:'ℹ', success:'✓', error:'✕', warn:'⚠' };
    const t = document.createElement('div');
    t.style.cssText = `
      background:#1a2235; border:1px solid ${colors[type]}44;
      border-left: 3px solid ${colors[type]};
      color:#e8eaf0; padding:12px 16px; border-radius:10px;
      font-family:'DM Sans',sans-serif; font-size:14px;
      display:flex; align-items:center; gap:10px;
      box-shadow:0 8px 24px rgba(0,0,0,.5);
      pointer-events:all; max-width:320px;
      animation: toastIn .3s cubic-bezier(.4,0,.2,1);
    `;
    t.innerHTML = `<span style="color:${colors[type]};font-weight:600">${icons[type]}</span><span>${msg}</span>`;
    if (!document.getElementById('toast-style')) {
      const s = document.createElement('style');
      s.id = 'toast-style';
      s.textContent = `@keyframes toastIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:none}}@keyframes toastOut{to{opacity:0;transform:translateX(16px)}}`;
      document.head.appendChild(s);
    }
    this.container.appendChild(t);
    setTimeout(() => {
      t.style.animation = 'toastOut .3s forwards';
      setTimeout(() => t.remove(), 300);
    }, duration);
  },
  success: (m) => Toast.show(m, 'success'),
  error:   (m) => Toast.show(m, 'error'),
  info:    (m) => Toast.show(m, 'info'),
  warn:    (m) => Toast.show(m, 'warn'),
};

// ── Helpers ───────────────────────────────────────────────────

function formatDate(d) {
  if (!d) return '—';
  return new Date(d).toLocaleDateString('fr-FR', { day:'2-digit', month:'short', year:'numeric' });
}

function formatDateTime(d) {
  if (!d) return '—';
  return new Date(d).toLocaleString('fr-FR', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
}

function truncate(str, n = 100) {
  if (!str) return '';
  return str.length > n ? str.slice(0, n) + '…' : str;
}

function badgeHtml(visibilite) {
  const map = { public:'badge--public', prive:'badge--prive', protege:'badge--protege' };
  const label = { public:'Public', prive:'Privé', protege:'Protégé' };
  return `<span class="badge ${map[visibilite]||''}">${label[visibilite]||visibilite}</span>`;
}

function statutBadge(statut) {
  const map = {
    publie:'badge--publie', en_attente:'badge--attente',
    rejete:'badge--rejete', brouillon:'badge--brouillon',
  };
  const label = { publie:'Publié', en_attente:'En attente', rejete:'Rejeté', brouillon:'Brouillon' };
  return `<span class="badge ${map[statut]||''}">${label[statut]||statut}</span>`;
}

function avatarInitials(nom, prenom) {
  return `${(prenom||'')[0]||''}${(nom||'')[0]||''}`.toUpperCase();
}

// ── Guard pages protégées ─────────────────────────────────────

function requireAuth(roles = []) {
  if (!Auth.isLoggedIn()) {
    // Chemin relatif depuis pages/ ou pages/admin/
    const depth = window.location.pathname.split('/').filter(Boolean).length;
    const prefix = depth >= 3 ? '../../' : '../';
    window.location.href = prefix + 'pages/login.html';
    return false;
  }
  if (roles.length && !Auth.can(...roles)) {
    Toast.error('Accès refusé');
    setTimeout(() => history.back(), 1500);
    return false;
  }
  return true;
}

// Rediriger si déjà connecté (page login)
function redirectIfAuth() {
  if (Auth.isLoggedIn()) {
    window.location.href = 'admin/dashboard.html';
  }
}
