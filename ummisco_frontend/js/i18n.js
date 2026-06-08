/**
 * i18n.js — Système de traduction FR/EN
 * Usage : appeler applyTranslations() après le DOM chargé
 * Marquer les éléments avec data-i18n="clé"
 */

const TRANSLATIONS = {
  fr: {
    // Nav
    'nav.home':         'Accueil',
    'nav.unite':        'Unité',
    'nav.presentation': 'Présentation',
    'nav.equipe':       'Équipe',
    'nav.partenaires':  'Partenaires',
    'nav.contact':      'Contact',
    'nav.recherches':   'Recherches',
    'nav.axes':         'Axes thématiques',
    'nav.projets':      'Projets',
    'nav.publications': 'Publications',
    'nav.datasets':     'Datasets',
    'nav.productions':  'Productions',
    'nav.articles':     'Articles & Thèses',
    'nav.donnees':      'Données ouvertes',
    'nav.outils':       'Outils & Simulations',
    'nav.actualites':   'Actualités',
    'nav.connexion':    'Connexion',
    'nav.membres':      'Espace membres',

    // Header
    'header.sub': 'Unité Mixte Internationale de Modélisation Mathématique<br>et Informatique des Systèmes Complexes · ESP/UCAD · Dakar',

    // Index
    'home.actus.title':   'Actualités',
    'home.actus.more':    'voir plus >>',
    'home.partners':      'Nos partenaires',
    'home.events.title':  'Evénements',
    'home.events.more':   "voir plus d'évènements >>",
    'home.axes.title':    'Axes de recherche',
    'home.axes.explore':  'Explorer',
    'home.pubs.title':    'Publications récentes',
    'home.pubs.all':      'Toutes les publications',
    'home.read_more':     'Lire la suite >>',

    // Chiffres
    'chiffres.title':        'UMMISCO en chiffres',
    'chiffres.doctorants':   'Doctorants',
    'chiffres.international':'Internationaux',
    'chiffres.nationalites': 'Nationalités',
    'chiffres.cotutelle':    'En Cotutelle',
    'chiffres.partenariat':  'Partenariat',

    // Footer
    'footer.nav':       'Navigation',
    'footer.unite':     "L'unité",
    'footer.members':   'Espace membres',
    'footer.address1':  'Campus UCAD — Dakar Fann',
    'footer.address2':  'Campus UCAD-IRD — Dakar Hann Maristes',
    'footer.copy':      '© 2025 UMMISCO — ESP/UCAD · Tous droits réservés',
    'footer.projet':    'Projet IPDL DIC1 · École Supérieure Polytechnique',

    // Pages
    'page.actualites.title': 'Actualités',
    'page.actualites.sub':   'Vie du laboratoire, conférences, séminaires et publications récentes',
    'page.equipe.title':     'L\'équipe',
    'page.equipe.sub':       'Chercheurs permanents, doctorants et membres associés de l\'UMMISCO',
    'page.pubs.title':       'Publications',
    'page.pubs.sub':         'Travaux de recherche publiés par les membres de l\'UMMISCO',
    'page.datasets.title':   'Datasets',
    'page.datasets.sub':     'Données de recherche produites par les chercheurs UMMISCO',
    'page.axes.title':       'Axes thématiques',
    'page.axes.sub':         'Cinq domaines structurant la recherche de l\'UMMISCO',
    'page.projets.title':    'Projets de recherche',
    'page.projets.sub':      'Projets en cours, planifiés et terminés',
    'page.contact.title':    'Contact',
    'page.contact.sub':      'Nous contacter · ESP/UCAD · Dakar, Sénégal',
    'page.presentation.title': 'Présentation de l\'UMMISCO',

    // Boutons communs
    'btn.search':    'Rechercher',
    'btn.load_more': 'Charger plus',
    'btn.all_axes':  'Tous les axes',
    'btn.login':     'Se connecter',
    'btn.back':      '← Retour au portail',
  },

  en: {
    // Nav
    'nav.home':         'Home',
    'nav.unite':        'Unit',
    'nav.presentation': 'About',
    'nav.equipe':       'Team',
    'nav.partenaires':  'Partners',
    'nav.contact':      'Contact',
    'nav.recherches':   'Research',
    'nav.axes':         'Research Areas',
    'nav.projets':      'Projects',
    'nav.publications': 'Publications',
    'nav.datasets':     'Datasets',
    'nav.productions':  'Productions',
    'nav.articles':     'Articles & Theses',
    'nav.donnees':      'Open Data',
    'nav.outils':       'Tools & Simulations',
    'nav.actualites':   'News',
    'nav.connexion':    'Login',
    'nav.membres':      'Member Space',

    // Header
    'header.sub': 'International Joint Unit for Mathematical and Computer Modelling<br>of Complex Systems · ESP/UCAD · Dakar',

    // Index
    'home.actus.title':   'News',
    'home.actus.more':    'see more >>',
    'home.partners':      'Our partners',
    'home.events.title':  'Events',
    'home.events.more':   'see more events >>',
    'home.axes.title':    'Research Areas',
    'home.axes.explore':  'Explore',
    'home.pubs.title':    'Recent Publications',
    'home.pubs.all':      'All publications',
    'home.read_more':     'Read more >>',

    // Chiffres
    'chiffres.title':        'UMMISCO in Numbers',
    'chiffres.doctorants':   'PhD Students',
    'chiffres.international':'International',
    'chiffres.nationalites': 'Nationalities',
    'chiffres.cotutelle':    'Co-supervision',
    'chiffres.partenariat':  'Partnerships',

    // Footer
    'footer.nav':       'Navigation',
    'footer.unite':     'The Unit',
    'footer.members':   'Member Space',
    'footer.address1':  'UCAD Campus — Dakar Fann',
    'footer.address2':  'UCAD-IRD Campus — Dakar Hann Maristes',
    'footer.copy':      '© 2025 UMMISCO — ESP/UCAD · All rights reserved',
    'footer.projet':    'IPDL DIC1 Project · École Supérieure Polytechnique',

    // Pages
    'page.actualites.title': 'News',
    'page.actualites.sub':   'Lab life, conferences, seminars and recent publications',
    'page.equipe.title':     'The Team',
    'page.equipe.sub':       'Permanent researchers, PhD students and associate members of UMMISCO',
    'page.pubs.title':       'Publications',
    'page.pubs.sub':         'Research work published by UMMISCO members',
    'page.datasets.title':   'Datasets',
    'page.datasets.sub':     'Research data produced by UMMISCO researchers',
    'page.axes.title':       'Research Areas',
    'page.axes.sub':         'Five areas structuring UMMISCO research',
    'page.projets.title':    'Research Projects',
    'page.projets.sub':      'Ongoing, planned and completed projects',
    'page.contact.title':    'Contact',
    'page.contact.sub':      'Contact us · ESP/UCAD · Dakar, Senegal',
    'page.presentation.title': 'About UMMISCO',

    // Boutons communs
    'btn.search':    'Search',
    'btn.load_more': 'Load more',
    'btn.all_axes':  'All areas',
    'btn.login':     'Sign in',
    'btn.back':      '← Back to portal',
  }
};

/** Retourne la langue courante (stockée en localStorage) */
function getLang() {
  return localStorage.getItem('lang') || 'fr';
}

/** Traduit une clé */
function t(key) {
  const lang = getLang();
  return TRANSLATIONS[lang]?.[key] || TRANSLATIONS['fr']?.[key] || key;
}

/** Applique les traductions sur tous les éléments data-i18n dans le DOM */
function applyTranslations() {
  const lang = getLang();
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = TRANSLATIONS[lang]?.[key] || TRANSLATIONS['fr']?.[key];
    if (!val) return;
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.placeholder = val;
    } else {
      el.innerHTML = val;
    }
  });
  // Mettre à jour l'attribut lang du <html>
  document.documentElement.lang = lang;
  // Mettre en gras le bouton actif
  ['fr','en'].forEach(l => {
    const btn = document.getElementById('btn-' + l);
    if (btn) btn.style.fontWeight = lang === l ? '700' : '400';
  });
}

/** Change la langue et recharge la page */
function setLang(lang) {
  localStorage.setItem('lang', lang);
  location.reload();
}

// Appliquer automatiquement au chargement
document.addEventListener('DOMContentLoaded', applyTranslations);
