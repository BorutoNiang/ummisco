/**
 * nav.js — Injecte le header + navbar institutionnels dans toutes les pages publiques.
 * Usage : <script src="../js/nav.js"></script> (ou "js/nav.js" depuis index.html)
 * Puis appeler : initNav({ active: 'actualites' })
 *
 * active values: 'accueil' | 'unite' | 'recherches' | 'productions' | 'actualites' | 'contact'
 */

function initNav({ active = '', base = '' } = {}) {

  /* base = '' depuis index.html, base = '../' depuis pages/ */
  const b = base;

  // ── Favicon ──
  if (!document.querySelector('link[rel="icon"]')) {
    const favicon = document.createElement('link');
    favicon.rel = 'icon';
    favicon.type = 'image/png';
    favicon.href = b + 'images/logo-ummisco.png';
    document.head.appendChild(favicon);
  }

  // ── Topbar ──
  const topbar = document.createElement('div');
  topbar.className = 'topbar-inst';
  topbar.innerHTML = `
    <div class="container">
      <div class="topbar-inst-left">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>
        Université Cheikh Anta Diop de Dakar &nbsp;|&nbsp; École Supérieure Polytechnique
      </div>
      <div class="topbar-inst-right">
        <a href="${b}pages/login.html">ENT</a>
        <span class="topbar-inst-sep">|</span>
        <a href="#" onclick="setLang('fr');return false" id="btn-fr" style="font-weight:${localStorage.getItem('lang')==='en'?'400':'700'}">FR</a>
        <span class="topbar-inst-sep">|</span>
        <a href="#" onclick="setLang('en');return false" id="btn-en" style="font-weight:${localStorage.getItem('lang')==='en'?'700':'400'}">EN</a>
      </div>
    </div>`;

  // ── Header logos ──
  // Chemin absolu depuis la racine du serveur pour éviter les problèmes de chemins relatifs
  const imgBase = (() => {
    // Trouve la racine du site (dossier contenant index.html)
    const path = window.location.pathname;
    const parts = path.split('/').filter(Boolean);
    // Si on est dans pages/ ou pages/admin/, remonter
    const depth = parts.length - 1; // -1 pour le fichier html
    return depth === 0 ? '' : '../'.repeat(depth);
  })();

  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <div class="container">
      <div class="header-logos">
        <a href="${b}index.html" style="display:flex;align-items:center;gap:14px;text-decoration:none">
          <img src="${imgBase}images/logo-ucad.png"    alt="UCAD"    class="header-logo-img" style="height:54px;width:auto;object-fit:contain"/>
          <div class="header-logo-sep"></div>
          <img src="${imgBase}images/logo-ummisco.png" alt="UMMISCO" class="header-logo-img" style="height:54px;width:auto;object-fit:contain;max-width:160px"/>
        </a>
        <div class="header-logo-sep"></div>
        <div class="header-brand">
          <div class="header-brand-name">UMMISCO</div>
          <div class="header-brand-sub">Unité Mixte Internationale de Modélisation Mathématique<br>et Informatique des Systèmes Complexes · ESP/UCAD · Dakar</div>
        </div>
      </div>
      <div class="header-right">
        <a href="${b}pages/login.html" class="btn btn--primary btn--sm" id="hdr-login-btn">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
          Espace membres
        </a>
      </div>
    </div>`;

  // ── Navbar ──
  const isA = (id) => id === active ? 'class="active"' : '';
  const nav = document.createElement('nav');
  nav.className = 'main-nav';
  nav.innerHTML = `
    <div class="container">
      <ul class="nav-menu">
        <li class="nav-item"><a href="${b}index.html" ${isA('accueil')} data-i18n="nav.home">Accueil</a></li>
        <li class="nav-item">
          <span ${isA('unite')}><span data-i18n="nav.unite">Unité</span> <span class="nav-arrow">▾</span></span>
          <ul class="nav-dropdown">
            <li><a href="${b}pages/presentation.html" data-i18n="nav.presentation">Présentation</a></li>
            <li><a href="${b}pages/equipe.html" data-i18n="nav.equipe">Équipe</a></li>
            <li><a href="${b}pages/partenaires.html" data-i18n="nav.partenaires">Partenaires</a></li>
            <li><a href="${b}pages/contact.html" data-i18n="nav.contact">Contact</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <span ${isA('recherches')}><span data-i18n="nav.recherches">Recherches</span> <span class="nav-arrow">▾</span></span>
          <ul class="nav-dropdown">
            <li><a href="${b}pages/axes.html" data-i18n="nav.axes">Axes thématiques</a></li>
            <li><a href="${b}pages/projets.html" data-i18n="nav.projets">Projets</a></li>
            <li><a href="${b}pages/publications.html" data-i18n="nav.publications">Publications</a></li>
            <li><a href="${b}pages/datasets.html" data-i18n="nav.datasets">Datasets</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <span ${isA('productions')}><span data-i18n="nav.productions">Productions</span> <span class="nav-arrow">▾</span></span>
          <ul class="nav-dropdown">
            <li><a href="${b}pages/publications.html" data-i18n="nav.articles">Articles &amp; Thèses</a></li>
            <li><a href="${b}pages/datasets.html" data-i18n="nav.donnees">Données ouvertes</a></li>
            <li><a href="${b}pages/integrations.html" data-i18n="nav.outils">Outils &amp; Simulations</a></li>
          </ul>
        </li>
        <li class="nav-item"><a href="${b}pages/actualites.html" ${isA('actualites')} data-i18n="nav.actualites">Actualités</a></li>
        <li class="nav-item"><a href="${b}pages/contact.html" ${isA('contact')} data-i18n="nav.contact">Contact</a></li>
      </ul>
      <div class="nav-actions">
        <a href="${b}pages/login.html" class="nav-login-btn" id="nav-login-btn">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          <span data-i18n="nav.connexion">Connexion</span>
        </a>
      </div>
    </div>`;

  // Prepend to body
  document.body.prepend(nav);
  document.body.prepend(header);
  document.body.prepend(topbar);

  // Charger i18n si pas déjà chargé
  if (!window._i18nLoaded) {
    window._i18nLoaded = true;
    const s = document.createElement('script');
    s.src = b + 'js/i18n.js';
    s.onload = () => applyTranslations();
    document.head.appendChild(s);
  } else {
    applyTranslations();
  }

  // Update login btn if already connected
  if (typeof Auth !== 'undefined' && Auth.isLoggedIn()) {
    ['hdr-login-btn', 'nav-login-btn'].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      if (id === 'hdr-login-btn') { el.textContent = 'Back-office'; el.href = b + 'pages/admin/dashboard.html'; }
      if (id === 'nav-login-btn') { el.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg> Mon espace`; el.href = b + 'pages/admin/dashboard.html'; }
    });
  }
}

// ── Footer partagé ──
function initFooter({ base = '' } = {}) {
  const b = base;
  const footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.innerHTML = `
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand-name">UMMISCO</div>
          <div class="footer-brand-sub" style="margin-top:8px">
            Unité Mixte Internationale de Modélisation Mathématique<br>
            et Informatique des Systèmes Complexes<br><br>
            École Supérieure Polytechnique<br>
            Université Cheikh Anta Diop · Dakar, Sénégal
          </div>
          <div style="margin-top:16px;font-size:12px;color:rgba(255,255,255,.5);display:flex;flex-direction:column;gap:4px">
            <span>✉ ummisco@ucad.edu.sn</span>
            <span>📍 Campus UCAD — Dakar Fann</span>
            <span>📍 Campus UCAD-IRD — Dakar Hann Maristes</span>
          </div>
        </div>
        <div>
          <div class="footer-col-title">Navigation</div>
          <div class="footer-links">
            <a href="${b}index.html">Accueil</a>
            <a href="${b}pages/axes.html">Axes de recherche</a>
            <a href="${b}pages/publications.html">Publications</a>
            <a href="${b}pages/datasets.html">Datasets</a>
            <a href="${b}pages/actualites.html">Actualités</a>
          </div>
        </div>
        <div>
          <div class="footer-col-title">L'unité</div>
          <div class="footer-links">
            <a href="${b}pages/presentation.html">Présentation</a>
            <a href="${b}pages/equipe.html">Équipe</a>
            <a href="${b}pages/partenaires.html">Partenaires</a>
            <a href="${b}pages/contact.html">Contact</a>
          </div>
        </div>
        <div>
          <div class="footer-col-title">Espace membres</div>
          <div class="footer-links">
            <a href="${b}pages/login.html">Connexion</a>
            <a href="${b}pages/admin/dashboard.html">Back-office</a>
            <a href="${b}pages/publications.html">Déposer une publication</a>
            <a href="${b}pages/datasets.html">Soumettre un dataset</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2025 UMMISCO — ESP/UCAD · Tous droits réservés</span>
        <span>Projet IPDL DIC1 · École Supérieure Polytechnique</span>
      </div>
    </div>`;
  document.body.appendChild(footer);
}
