/**
 * nav.js — Navbar style ummisco.fr (fond blanc, logo circulaire, liens caps)
 * Usage : initNav({ active: 'themes', base: '' })
 * active: 'themes' | 'centres' | 'projets' | 'logiciels' | 'membres' | 'publications' | 'actualite'
 */

function initNav({ active = '', base = '' } = {}) {
  const b = base;
  const lang = localStorage.getItem('lang') || 'fr';
  const isA = (id) => id === active ? 'style="color:#1a6faf"' : '';

  // Favicon
  if (!document.querySelector('link[rel="icon"]')) {
    const fav = document.createElement('link');
    fav.rel = 'icon'; fav.type = 'image/png';
    fav.href = b + 'images/logo-ummisco.png';
    document.head.appendChild(fav);
  }

  // Montserrat si pas chargée
  if (!document.querySelector('link[href*="Montserrat"]')) {
    const lp = document.createElement('link');
    lp.rel = 'preconnect'; lp.href = 'https://fonts.googleapis.com';
    document.head.appendChild(lp);
    const lf = document.createElement('link');
    lf.rel = 'stylesheet';
    lf.href = 'https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;1,700&display=swap';
    document.head.appendChild(lf);
  }

  const nav = document.createElement('nav');
  nav.className = 'site-nav';
  nav.style.cssText = `
    position:sticky;top:0;z-index:200;background:#fff;
    border-bottom:1px solid #e8e8e8;height:80px;
    display:flex;align-items:center;font-family:'Montserrat',sans-serif;
  `;
  nav.innerHTML = `
  <style>
    .snav-wrap{width:100%;max-width:1280px;margin:0 auto;padding:0 40px;display:flex;align-items:center;gap:0}
    .snav-logo{display:flex;align-items:center;gap:12px;text-decoration:none;flex-shrink:0;margin-right:40px}
    .snav-logo-mark{width:64px;height:64px;border-radius:50%;border:1.5px solid #d0d8e4;display:flex;align-items:center;justify-content:center;background:#fff}
    .snav-logo-name{font-size:14px;font-weight:700;letter-spacing:.08em;color:#1a1a1a;text-transform:uppercase}
    .snav-menu{display:flex;align-items:center;list-style:none;gap:2px;flex:1;padding:0;margin:0}
    .snav-menu li{position:relative}
    .snav-menu li>a,.snav-menu li>span{display:flex;align-items:center;gap:4px;padding:8px 11px;font-size:13.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#333;cursor:pointer;border-radius:6px;transition:color .15s,background .15s;white-space:nowrap;text-decoration:none}
    .snav-menu li>a:hover,.snav-menu li>span:hover{color:#1a6faf;background:#f0f6ff}
    .snav-chevron{font-size:8px;opacity:.55;transition:transform .15s}
    .snav-menu li:hover .snav-chevron{transform:rotate(180deg)}
    .snav-sub{position:absolute;top:calc(100% + 6px);left:0;min-width:300px;background:#fff;border:1px solid #e8e8e8;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.1);list-style:none;padding:6px 0;opacity:0;pointer-events:none;transform:translateY(-6px);transition:opacity .15s,transform .15s;z-index:300}
    .snav-menu li:hover .snav-sub{opacity:1;pointer-events:all;transform:none}
    .snav-sub li>a{display:block;padding:13px 20px;font-size:13px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#222;border-radius:0;background:none;white-space:normal;line-height:1.4}
    .snav-sub li>a:hover{background:#f0f6ff;color:#1a6faf}
    .snav-sub li+li{border-top:1px solid #f2f2f2}
    /* Mega-menu thèmes */
    .snav-mega{position:absolute;top:calc(100% + 8px);left:-60px;width:680px;background:#fff;border:1px solid #e8e8e8;border-radius:12px;box-shadow:0 12px 40px rgba(0,0,0,.12);padding:20px;opacity:0;pointer-events:none;transform:translateY(-8px);transition:opacity .15s,transform .15s;z-index:300;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
    .snav-menu li:hover .snav-mega{opacity:1;pointer-events:all;transform:none}
    .snav-theme-card{display:flex;flex-direction:column;border-radius:10px;overflow:hidden;border:1px solid #eee;text-decoration:none;transition:box-shadow .15s,transform .15s;background:#fff}
    .snav-theme-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.12);transform:translateY(-2px)}
    .snav-theme-img{width:100%;height:120px;object-fit:cover;display:block}
    .snav-theme-name{padding:10px 10px 12px;font-size:11.5px;font-weight:700;color:#222;text-align:center;line-height:1.4}
    .snav-intranet{display:flex;align-items:center;gap:6px;padding:7px 14px;background:transparent;color:#1a6faf !important;border:1.5px solid #1a6faf;border-radius:8px;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;flex-shrink:0;margin-left:12px;transition:all .15s}
    .snav-intranet:hover{background:#1a6faf;color:#fff !important}
    .snav-intranet svg{flex-shrink:0}
    .snav-lang{position:relative;flex-shrink:0;margin-left:12px}
    .snav-lang-btn{display:flex;align-items:center;gap:6px;padding:8px 14px;border:1px solid #d0d8e4;border-radius:8px;font-size:12.5px;font-weight:600;color:#333;cursor:pointer;background:#fff;font-family:'Montserrat',sans-serif;transition:border-color .15s}
    .snav-lang-btn:hover{border-color:#1a6faf}
    .snav-lang-menu{position:absolute;top:calc(100% + 6px);right:0;background:#fff;border:1px solid #e8e8e8;border-radius:8px;box-shadow:0 8px 20px rgba(0,0,0,.1);list-style:none;min-width:80px;padding:4px 0;opacity:0;pointer-events:none;transform:translateY(-6px);transition:opacity .15s,transform .15s;z-index:300}
    .snav-lang-menu.open{opacity:1;pointer-events:all;transform:none}
    .snav-lang-menu li>a{display:block;padding:9px 16px;font-size:13px;font-weight:600;color:#444;text-decoration:none;transition:background .12s}
    .snav-lang-menu li>a:hover{background:#f0f6ff;color:#1a6faf}
  </style>
  <div class="snav-wrap">
    <a href="${b}index.html" class="snav-logo">
      <div class="snav-logo-mark">
        <svg width="32" height="32" viewBox="0 0 48 48" fill="none">
          <rect x="6" y="6" width="13" height="13" rx="2" stroke="#1a6faf" stroke-width="2"/>
          <rect x="29" y="6" width="13" height="13" rx="2" stroke="#1a6faf" stroke-width="2"/>
          <rect x="6" y="29" width="13" height="13" rx="2" stroke="#1a6faf" stroke-width="2"/>
          <rect x="29" y="29" width="13" height="13" rx="2" stroke="#1a6faf" stroke-width="2"/>
          <circle cx="24" cy="24" r="3.5" fill="#4caf50"/>
          <circle cx="12.5" cy="12.5" r="2.5" fill="#1a6faf"/>
          <circle cx="35.5" cy="12.5" r="2.5" fill="#1a6faf"/>
          <circle cx="12.5" cy="35.5" r="2.5" fill="#1a6faf"/>
          <circle cx="35.5" cy="35.5" r="2.5" fill="#1a6faf"/>
        </svg>
      </div>
      <span class="snav-logo-name">UMMISCO</span>
    </a>
    <ul class="snav-menu">
      <li>
        <span ${isA('themes')}>Thèmes <span class="snav-chevron">▾</span></span>
        <div class="snav-mega">
          <a href="${b}pages/axes.html#modelisation" class="snav-theme-card">
            <img src="https://ummisco.fr/wp-content/uploads/2024/11/laptop-ejecting-graphics-arrows-scaled.jpg" class="snav-theme-img" alt="Modélisation" loading="lazy"/>
            <div class="snav-theme-name">Modélisation mathématique et informatique à base d'agents</div>
          </a>
          <a href="${b}pages/axes.html#ia" class="snav-theme-card">
            <img src="https://ummisco.fr/wp-content/uploads/elementor/thumbs/img-03-rg9fit1rrfviwafjte9juynm268xeqj2slorz1u5go.jpg" class="snav-theme-img" alt="Intelligence Artificielle" loading="lazy"/>
            <div class="snav-theme-name">Intelligence Artificielle et Apprentissage Profond</div>
          </a>
          <a href="${b}pages/axes.html#capteurs" class="snav-theme-card">
            <img src="https://ummisco.fr/wp-content/uploads/2018/08/1.png" class="snav-theme-img" alt="Capteurs" loading="lazy"/>
            <div class="snav-theme-name">Capteurs et collecte de données</div>
          </a>
          <a href="${b}pages/axes.html#participatif" class="snav-theme-card">
            <img src="https://ummisco.fr/wp-content/uploads/2018/06/app01.png" class="snav-theme-img" alt="Approches participatives" loading="lazy"/>
            <div class="snav-theme-name">Approches participatives et science citoyenne</div>
          </a>
        </div>
      </li>
      <li>
        <span ${isA('centres')}>Centres <span class="snav-chevron">▾</span></span>
        <ul class="snav-sub">
          <li><a href="${b}pages/partenaires.html">Centre France</a></li>
          <li><a href="${b}pages/partenaires.html">Centre Afrique de l'Ouest</a></li>
          <li><a href="${b}pages/partenaires.html">Centre Afrique centrale et de l'est</a></li>
          <li><a href="${b}pages/partenaires.html">Centre Méditerranée</a></li>
          <li><a href="${b}pages/partenaires.html">Centre Asie du Sud-Est</a></li>
        </ul>
      </li>
      <li><a href="${b}pages/projets.html" ${isA('projets')}>Projets</a></li>
      <li><a href="${b}pages/integrations.html" ${isA('logiciels')}>Logiciels</a></li>
      <li><a href="${b}pages/equipe.html" ${isA('membres')}>Membres</a></li>
      <li><a href="${b}pages/publications.html" ${isA('publications')}>Publications</a></li>
      <li><a href="${b}pages/actualites.html" ${isA('actualite')}>Actualité</a></li>
    </ul>
    <a href="${b}pages/login.html" class="snav-intranet">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      Intranet
    </a>
    <div class="snav-lang">
      <button class="snav-lang-btn" id="snav-lang-btn">
        ${lang.toUpperCase()} <span class="snav-chevron">▾</span>
      </button>
      <ul class="snav-lang-menu" id="snav-lang-menu">
        <li><a href="#" onclick="setLang && setLang('fr');return false">FR</a></li>
        <li><a href="#" onclick="setLang && setLang('en');return false">EN</a></li>
      </ul>
    </div>
  </div>`;

  document.body.prepend(nav);

  // Lang toggle
  document.getElementById('snav-lang-btn').addEventListener('click', () => {
    document.getElementById('snav-lang-menu').classList.toggle('open');
  });
  document.addEventListener('click', e => {
    const btn  = document.getElementById('snav-lang-btn');
    const menu = document.getElementById('snav-lang-menu');
    if (btn && menu && !btn.contains(e.target) && !menu.contains(e.target))
      menu.classList.remove('open');
  });

  // i18n
  if (typeof applyTranslations === 'function') applyTranslations();
}

// ── Footer minimaliste ──
function initFooter({ base = '' } = {}) {
  const b = base;
  const f = document.createElement('footer');
  f.style.cssText = 'border-top:1px solid #efefef;padding:22px 40px;display:flex;align-items:center;justify-content:space-between;font-family:Montserrat,sans-serif;font-size:13px;color:#888';
  f.innerHTML = `
    <span>© ${new Date().getFullYear()} UMMISCO &nbsp;·&nbsp; Tous droits réservés</span>
    <a href="${b}pages/contact.html" style="color:#333;font-weight:600;text-decoration:none">Contact</a>`;
  document.body.appendChild(f);
}
