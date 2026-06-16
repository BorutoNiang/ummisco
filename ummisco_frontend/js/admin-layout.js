/* admin-layout.js — Sidebar + topbar professionnels, sans emojis */

const ADMIN_NAV = [
  {
    id:'dashboard', label:'Tableau de bord', href:'dashboard.html',
    svg:'<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>'
  },
  {
    id:'publications', label:'Publications', href:'publications.html',
    svg:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>'
  },
  {
    id:'datasets', label:'Datasets', href:'datasets.html',
    svg:'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'
  },
  {
    id:'projets', label:'Projets', href:'projets.html',
    svg:'<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'
  },
  {
    id:'actualites', label:'Actualités', href:'actualites.html',
    svg:'<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v2"/><path d="M15 2v4M8 2v4M3 10h13"/><rect x="2" y="14" width="6" height="6" rx="1"/>'
  },
  {
    id:'bailleurs', label:'Bailleurs', href:'bailleurs.html', roles:['super_admin','admin_axe','chercheur'],
    svg:'<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'
  },
  {
    id:'integrations', label:'Intégrations', href:'integrations.html',
    svg:'<rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>'
  },
  {
    id:'utilisateurs', label:'Utilisateurs', href:'utilisateurs.html', roles:['super_admin'],
    svg:'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
  },
  {
    id:'roles', label:'Rôles & Permissions', href:'roles.html', roles:['super_admin'],
    svg:'<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
  },
  {
    id:'bon-achat', label:"Bon d'achat", href:'bon-achat.html', roles:['super_admin'],
    svg:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/>'
  },
  {
    id:'convention-stage', label:'Convention de stage', href:'convention-stage.html', roles:['super_admin'],
    svg:'<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>'
  },
  {
    id:'prestation-service', label:'Prestation de service', href:'prestation-service.html', roles:['super_admin'],
    svg:'<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>'
  },
];

function initAdminLayout(activeId) {
  if (!requireAuth()) return;

  const user = Auth.getUser();
  const role = Auth.getRole();

  /* ── Styles injectés ── */
  const style = document.createElement('style');
  style.textContent = `
    *, *::before, *::after { box-sizing: border-box; }

    body {
      display: flex;
      min-height: 100vh;
      background: #f0f2f5;
      font-family: 'Open Sans', sans-serif;
      color: #1a1e2d;
      margin: 0;
    }

    /* ─── Sidebar ─── */
    .sidebar {
      width: 240px;
      min-width: 240px;
      background: #fff;
      border-right: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      position: fixed;
      top: 0; left: 0; bottom: 0;
      z-index: 100;
      overflow-y: auto;
    }

    .sidebar-brand {
      padding: 20px 20px 16px;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .sidebar-brand-logo {
      width: 36px; height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .sidebar-brand-logo svg { color: #fff; }
    .sidebar-brand-name {
      font-size: 15px;
      font-weight: 700;
      color: #003f87;
      line-height: 1.1;
    }
    .sidebar-brand-sub {
      font-size: 10px;
      color: #94a3b8;
      margin-top: 1px;
    }

    .sidebar-section-label {
      padding: 16px 20px 6px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: #94a3b8;
    }

    .sidebar-nav { flex: 1; padding: 8px 12px; }

    .sidebar-link {
      display: flex;
      align-items: center;
      gap: 11px;
      padding: 9px 12px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      color: #475569;
      cursor: pointer;
      transition: background .15s, color .15s;
      margin-bottom: 2px;
      text-decoration: none;
    }
    .sidebar-link:hover { background: #f1f5f9; color: #003f87; }
    .sidebar-link.active {
      background: #eff6ff;
      color: #003f87;
      font-weight: 600;
      border-left: 3px solid #003f87;
      padding-left: 9px;
    }
    .sidebar-link svg { flex-shrink: 0; opacity: .7; }
    .sidebar-link.active svg { opacity: 1; }

    .sidebar-divider {
      height: 1px;
      background: #e2e8f0;
      margin: 8px 12px;
    }

    /* User card en bas */
    .sidebar-user {
      padding: 14px 16px;
      border-top: 1px solid #e2e8f0;
      background: #fafafa;
    }
    .sidebar-user-row {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .sidebar-avatar {
      width: 34px; height: 34px;
      border-radius: 50%;
      background: #003f87;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 700;
      flex-shrink: 0;
    }
    .sidebar-user-name  { font-size: 13px; font-weight: 600; color: #1e293b; }
    .sidebar-user-role  { font-size: 11px; color: #94a3b8; }
    .sidebar-logout-btn {
      width: 100%;
      margin-top: 10px;
      padding: 7px 12px;
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;
      color: #64748b;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all .15s;
    }
    .sidebar-logout-btn:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

    /* ─── Main area ─── */
    .main-area {
      margin-left: 240px;
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    /* ─── Topbar ─── */
    .topbar {
      background: #fff;
      border-bottom: 1px solid #e2e8f0;
      height: 56px;
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .topbar-left { display: flex; align-items: center; gap: 16px; }
    .topbar-page-title {
      font-size: 15px;
      font-weight: 700;
      color: #1e293b;
    }
    .topbar-breadcrumb {
      font-size: 12px;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .topbar-breadcrumb::before {
      content: '/';
      color: #cbd5e1;
    }
    .topbar-right { display: flex; align-items: center; gap: 10px; }
    .topbar-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all .15s;
      text-decoration: none;
    }
    .topbar-btn-outline {
      border: 1px solid #e2e8f0;
      color: #475569;
      background: #fff;
    }
    .topbar-btn-outline:hover { background: #f8fafc; border-color: #003f87; color: #003f87; }
    .topbar-user-chip {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 5px 10px;
      border-radius: 20px;
      background: #f1f5f9;
      font-size: 12px;
      font-weight: 600;
      color: #475569;
      cursor: pointer;
    }
    .topbar-avatar {
      width: 28px; height: 28px;
      border-radius: 50%;
      background: #003f87;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 700;
      flex-shrink: 0;
    }

    /* ─── Page content ─── */
    .page-content { flex: 1; padding: 24px; }

    /* ─── Cards admin ─── */
    .card {
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 20px;
      transition: box-shadow .15s;
    }
    .card:hover { box-shadow: 0 2px 8px rgba(0,0,0,.06); }

    /* ─── Tables admin ─── */
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th {
      text-align: left; padding: 10px 14px;
      font-size: 11px; font-weight: 700; text-transform: uppercase;
      letter-spacing: .05em; color: #64748b;
      background: #f8fafc; border-bottom: 1px solid #e2e8f0;
    }
    td { padding: 12px 14px; border-bottom: 1px solid #f1f5f9; color: #475569; vertical-align: middle; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #fafbfc; }
    .table-wrap { overflow-x: auto; border-radius: 8px; }

    /* ─── Boutons admin ─── */
    .btn {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 8px 16px; border-radius: 6px;
      font-size: 13px; font-weight: 600;
      cursor: pointer; transition: all .15s; white-space: nowrap; border: none;
    }
    .btn--primary  { background: #003f87; color: #fff; }
    .btn--primary:hover  { background: #002a5c; }
    .btn--accent   { background: #e8001d; color: #fff; }
    .btn--accent:hover   { background: #c0001a; }
    .btn--ghost    { background: #fff; border: 1px solid #e2e8f0; color: #475569; }
    .btn--ghost:hover    { background: #f8fafc; border-color: #003f87; color: #003f87; }
    .btn--danger   { background: #dc2626; color: #fff; }
    .btn--danger:hover   { background: #b91c1c; }
    .btn--sm { padding: 5px 10px; font-size: 12px; }

    /* ─── Badges admin ─── */
    .badge {
      display: inline-block; padding: 3px 8px;
      border-radius: 4px; font-size: 11px; font-weight: 600;
      letter-spacing: .03em;
    }
    .badge--publie   { background: #d1fae5; color: #065f46; }
    .badge--attente  { background: #fef3c7; color: #92400e; }
    .badge--rejete   { background: #fee2e2; color: #991b1b; }
    .badge--brouillon{ background: #f1f5f9; color: #475569; }
    .badge--public   { background: #dbeafe; color: #1e40af; }
    .badge--prive    { background: #fef3c7; color: #92400e; }
    .badge--protege  { background: #ede9fe; color: #5b21b6; }

    /* ─── Forms admin ─── */
    .form-group { display: flex; flex-direction: column; gap: 5px; }
    .form-label  { font-size: 12px; font-weight: 600; color: #374151; }
    .form-input {
      background: #fff; border: 1px solid #d1d5db;
      border-radius: 6px; padding: 8px 12px;
      font-size: 13px; color: #1f2937;
      transition: border-color .15s, box-shadow .15s;
      font-family: inherit;
    }
    .form-input:focus { border-color: #003f87; box-shadow: 0 0 0 3px rgba(0,63,135,.08); outline: none; }
    .form-input::placeholder { color: #9ca3af; }
    textarea.form-input { resize: vertical; min-height: 90px; }
    select.form-input { cursor: pointer; }

    /* ─── Modals admin ─── */
    .modal-overlay {
      position: fixed; inset: 0;
      background: rgba(0,0,0,.45);
      display: flex; align-items: center; justify-content: center;
      z-index: 1000;
      opacity: 0; pointer-events: none;
      transition: opacity .15s;
    }
    .modal-overlay.open { opacity: 1; pointer-events: all; }
    .modal {
      background: #fff; border-radius: 10px; padding: 24px;
      max-width: 580px; width: calc(100% - 40px);
      max-height: 90vh; overflow-y: auto;
      box-shadow: 0 20px 60px rgba(0,0,0,.15);
      transform: translateY(10px);
      transition: transform .15s;
    }
    .modal-overlay.open .modal { transform: none; }
    .modal-header {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 18px; padding-bottom: 14px;
      border-bottom: 1px solid #e2e8f0;
    }
    .modal-title { font-size: 15px; font-weight: 700; color: #1e293b; }
    .modal-close {
      width: 28px; height: 28px; border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer; color: #94a3b8; background: none; border: none;
      transition: background .15s;
    }
    .modal-close:hover { background: #f1f5f9; color: #1e293b; }

    /* ─── Alerts ─── */
    .alert { padding: 10px 14px; border-radius: 6px; font-size: 13px; border-left: 3px solid; }
    .alert--error   { background: #fef2f2; border-color: #dc2626; color: #991b1b; }
    .alert--success { background: #f0fdf4; border-color: #16a34a; color: #166534; }
    .alert--info    { background: #eff6ff; border-color: #003f87; color: #1e40af; }

    /* ─── Utilitaires ─── */
    .flex         { display: flex; }
    .flex-between { display: flex; align-items: center; justify-content: space-between; }
    .flex-center  { display: flex; align-items: center; justify-content: center; }
    .gap-form     { display: flex; flex-direction: column; gap: 14px; }
    .grid-2       { display: grid; grid-template-columns: repeat(2,1fr); gap: 14px; }
    .mt-md  { margin-top: 16px; }
    .mb-md  { margin-bottom: 16px; }
    .mb-lg  { margin-bottom: 28px; }
    .w-full { width: 100%; }
    .text-muted { color: #94a3b8; font-size: 13px; }
    .font-mono  { font-family: 'Courier New', monospace; }
    .spinner {
      width: 18px; height: 18px;
      border: 2px solid #e2e8f0; border-top-color: #003f87;
      border-radius: 50%; animation: spin .6s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .skeleton {
      background: linear-gradient(90deg,#f1f5f9 25%,#e2e8f0 50%,#f1f5f9 75%);
      background-size: 200% 100%; animation: shimmer 1.4s infinite;
      border-radius: 6px;
    }
    @keyframes shimmer { to { background-position: -200% 0; } }

    @media(max-width:768px) {
      .sidebar { transform: translateX(-100%); }
      .main-area { margin-left: 0; }
    }
  `;
  document.head.appendChild(style);

  /* ── Construction sidebar ── */
  const navItems = ADMIN_NAV
    .filter(item => !item.roles || item.roles.includes(role))
    .map(item => `
      <a class="sidebar-link ${item.id === activeId ? 'active' : ''}" href="${item.href}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${item.svg}</svg>
        ${item.label}
      </a>`).join('');

  const sidebar = document.createElement('aside');
  sidebar.className = 'sidebar';
  sidebar.innerHTML = `
    <div class="sidebar-brand">
      <div class="sidebar-brand-logo">
        <img src="../../images/logo-ummisco-officiel.webp" alt="UMMISCO" style="width:36px;height:36px;object-fit:contain;border-radius:8px"/>
      </div>
      <div>
        <div class="sidebar-brand-name">UMMISCO</div>
        <div class="sidebar-brand-sub">Administration · ESP/UCAD</div>
      </div>
    </div>
    <nav class="sidebar-nav">
      <div class="sidebar-section-label">Navigation</div>
      ${navItems}
    </nav>
    <div class="sidebar-user">
      <div class="sidebar-user-row">
        <img src="../../images/logo-ummisco-officiel.webp" alt="UMMISCO" style="width:34px;height:34px;border-radius:50%;object-fit:contain;flex-shrink:0;border:1px solid #e2e8f0"/>
        <div>
          <div class="sidebar-user-name">${user?.prenom || ''} ${user?.nom || ''}</div>
          <div class="sidebar-user-role">${role === 'super_admin' ? 'Directeur' : role}</div>
        </div>
      </div>
      <button class="sidebar-logout-btn" onclick="logout()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        Déconnexion
      </button>
    </div>`;

  /* ── Construction topbar ── */
  const pageLabel = ADMIN_NAV.find(i => i.id === activeId)?.label || 'Administration';
  const topbar = document.createElement('header');
  topbar.className = 'topbar';
  topbar.innerHTML = `
    <div class="topbar-left">
      <span class="topbar-page-title">${pageLabel}</span>
      <span class="topbar-breadcrumb">${pageLabel}</span>
    </div>
    <div class="topbar-right">
      <a href="../../index.html" class="topbar-btn topbar-btn-outline" target="_blank">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        Portail public
      </a>
      <div class="topbar-user-chip">
        <img src="../../images/logo-ummisco-officiel.webp" alt="UMMISCO" style="width:28px;height:28px;border-radius:50%;object-fit:contain;border:1px solid #e2e8f0"/>
        ${user?.prenom || ''} ${user?.nom || ''}
      </div>
    </div>`;

  /* ── Injection dans le DOM ── */
  const existing = Array.from(document.body.children);
  const mainArea = document.createElement('div');
  mainArea.className = 'main-area';
  const pageContent = document.createElement('main');
  pageContent.className = 'page-content';
  existing.forEach(el => pageContent.appendChild(el));
  mainArea.appendChild(topbar);
  mainArea.appendChild(pageContent);
  document.body.appendChild(sidebar);
  document.body.appendChild(mainArea);
}

function logout() {
  Auth.clear();
  window.location.href = '../login.html';
}
