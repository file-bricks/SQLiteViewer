/**
 * SQLiteViewer Web-Companion Internationalization (i18n)
 * Supports DE and EN with fallback chain: requested -> en -> de -> key
 */

export const SUPPORTED_LOCALES = ["de", "en"];
export const DEFAULT_LOCALE = "de";
export const STORAGE_KEY = "sqliteviewer-web-companion:language";

export const TRANSLATIONS = {
  de: {
    // Meta / Doc
    doc_title: "SQLiteViewer Companion",
    meta_description: "Offline-Companion für sqliteviewer-export-v1.json",
    
    // Hero
    eyebrow: "SQLiteViewer Companion",
    hero_title: "Lokale Exporte prüfen, ohne die Datenbank hochzuladen.",
    hero_lead: "Dieser Companion öffnet `sqliteviewer-export-v1.json` direkt im Browser, zeigt Metadaten, Spalten und Ergebniszeilen an und bleibt bewusst offline-first.",
    
    // Actions
    action_load_json: "JSON laden",
    action_open_demo: "Demo öffnen",
    action_reset: "Zurücksetzen",
    action_export_csv: "CSV exportieren",
    
    // Status
    status_ready: "Bereit.",
    status_reset: "Lokaler Companion zurückgesetzt.",
    status_drag_idle_title: "Datei hier ablegen",
    status_drag_idle_hint: "Unterstützt wird aktuell der Desktop-Export `sqliteviewer-export-v1.json`.",
    status_drag_active: "Datei loslassen, um den Export zu laden.",
    status_demo_loaded: "Demo-Export geladen.",
    status_restored: "Zuletzt geladener Export wiederhergestellt.",
    status_export_loaded: "{label} geladen: {name} ({count} sichtbare Zeilen).",
    status_storage_warn: "Export geladen, aber der Browser konnte keine lokale Wiederherstellung speichern.",
    status_read_error: "Datei konnte nicht gelesen werden.",
    
    // Panel 1: Source & Metadata
    panel_source_eyebrow: "Quelle",
    panel_source_title: "Export-Metadaten",
    panel_source_empty: "Noch kein Export geladen.",
    query_label: "SQL-Query",
    
    // Meta Cards
    meta_database: "Datenbank",
    meta_view: "Ansicht",
    meta_table: "Tabelle",
    meta_rows: "Zeilen",
    meta_limit: "Limit",
    meta_sort: "Sortierung",
    meta_unknown: "Unbekannt",
    
    // Panel 2: Result Rows
    panel_view_eyebrow: "Ansicht",
    panel_view_title: "Ergebniszeilen",
    results_count_zero: "0 sichtbare Zeilen",
    results_count_one: "1 sichtbare Zeile",
    results_count_other: "{count} sichtbare Zeilen",
    search_label: "Suche in sichtbaren Zeilen",
    search_placeholder: "Titel, ID, Query, BLOB-Hinweise …",
    empty_state_initial: "Noch keine Daten sichtbar. Lade einen Export oder öffne die Demo.",
    empty_state_filtered: "Keine Zeilen passen zum Suchfilter »{query}«.",
    
    // Panel 3: Limitations
    panel_notes_eyebrow: "Bewusst klein gehalten",
    panel_notes_title: "Companion-Grenzen",
    note_no_upload: "Keine Server-Uploads und kein Cloud-Sync.",
    note_no_write: "Keine Schreibfunktionen zurück in Desktop oder Datenbank.",
    note_raw_sqlite: "Rohe `.sqlite`-Dateien bleiben bewusst ein späterer Evaluationspfad.",
    
    // Table sorting
    sort_click_asc: "Klicken für aufsteigende Sortierung",
    sort_click_desc: "Klicken für absteigende Sortierung",
    sort_click_clear: "Klicken zum Aufheben der Sortierung",
    
    // Summary
    summary_path_hidden: "voller lokaler Pfad im Export ausgeblendet",
    summary_path_none: "kein lokaler Pfad im Export",
    summary_unknown_db: "unbekannte Datenbank",
    summary_source_prefix: "Quelle:"
  },
  en: {
    // Meta / Doc
    doc_title: "SQLiteViewer Companion",
    meta_description: "Offline companion for sqliteviewer-export-v1.json",
    
    // Hero
    eyebrow: "SQLiteViewer Companion",
    hero_title: "Inspect local exports without uploading the database.",
    hero_lead: "This companion opens `sqliteviewer-export-v1.json` directly in your browser, displays metadata, columns, and result rows, and remains strictly offline-first.",
    
    // Actions
    action_load_json: "Load JSON",
    action_open_demo: "Open Demo",
    action_reset: "Reset",
    action_export_csv: "Export CSV",
    
    // Status
    status_ready: "Ready.",
    status_reset: "Local companion reset.",
    status_drag_idle_title: "Drop file here",
    status_drag_idle_hint: "Currently supports the desktop export `sqliteviewer-export-v1.json`.",
    status_drag_active: "Release file to load export.",
    status_demo_loaded: "Demo export loaded.",
    status_restored: "Last loaded export restored.",
    status_export_loaded: "{label} loaded: {name} ({count} visible rows).",
    status_storage_warn: "Export loaded, but the browser could not store local restoration.",
    status_read_error: "File could not be read.",
    
    // Panel 1: Source & Metadata
    panel_source_eyebrow: "Source",
    panel_source_title: "Export Metadata",
    panel_source_empty: "No export loaded yet.",
    query_label: "SQL Query",
    
    // Meta Cards
    meta_database: "Database",
    meta_view: "View",
    meta_table: "Table",
    meta_rows: "Rows",
    meta_limit: "Limit",
    meta_sort: "Sort",
    meta_unknown: "Unknown",
    
    // Panel 2: Result Rows
    panel_view_eyebrow: "View",
    panel_view_title: "Result Rows",
    results_count_zero: "0 visible rows",
    results_count_one: "1 visible row",
    results_count_other: "{count} visible rows",
    search_label: "Search visible rows",
    search_placeholder: "Title, ID, query, BLOB notes …",
    empty_state_initial: "No data visible yet. Load an export or open the demo.",
    empty_state_filtered: "No rows match search filter \"{query}\".",
    
    // Panel 3: Limitations
    panel_notes_eyebrow: "Deliberately lightweight",
    panel_notes_title: "Companion Scope",
    note_no_upload: "No server uploads and no cloud sync.",
    note_no_write: "No write-back functionality to desktop or database.",
    note_raw_sqlite: "Raw `.sqlite` files intentionally remain a later evaluation path.",
    
    // Table sorting
    sort_click_asc: "Click to sort ascending",
    sort_click_desc: "Click to sort descending",
    sort_click_clear: "Click to clear sorting",
    
    // Summary
    summary_path_hidden: "full local path hidden in export",
    summary_path_none: "no local path in export",
    summary_unknown_db: "unknown database",
    summary_source_prefix: "Source:"
  }
};

let currentLocale = DEFAULT_LOCALE;

/**
 * Returns the currently active locale.
 */
export function getLocale() {
  return currentLocale;
}

/**
 * Normalizes a locale code to supported languages (e.g. 'de-DE' -> 'de').
 */
export function normalizeLocale(locale) {
  if (!locale || typeof locale !== "string") {
    return DEFAULT_LOCALE;
  }
  const code = locale.toLowerCase().split("-")[0].split("_")[0];
  return SUPPORTED_LOCALES.includes(code) ? code : DEFAULT_LOCALE;
}

/**
 * Sets the active locale if supported and saves to localStorage if available.
 */
export function setLocale(locale) {
  const norm = normalizeLocale(locale);
  currentLocale = norm;
  try {
    if (typeof localStorage !== "undefined") {
      localStorage.setItem(STORAGE_KEY, norm);
    }
  } catch (_e) {
    // ignore storage restrictions
  }
  return currentLocale;
}

/**
 * Detects the best matching locale from localStorage or browser language.
 */
export function detectLocale() {
  try {
    if (typeof localStorage !== "undefined") {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored && SUPPORTED_LOCALES.includes(stored)) {
        return stored;
      }
    }
  } catch (_e) {
    // ignore storage restrictions
  }

  if (typeof navigator !== "undefined" && navigator.language) {
    const navCode = navigator.language.toLowerCase().split("-")[0].split("_")[0];
    if (SUPPORTED_LOCALES.includes(navCode)) {
      return navCode;
    }
  }

  return DEFAULT_LOCALE;
}

/**
 * Translates a key for a given locale with fallback:
 * locale -> en -> de -> key.
 * Interpolates {param} placeholders if params object is provided.
 */
export function t(key, params = {}, locale = currentLocale) {
  const loc = normalizeLocale(locale);
  let text = TRANSLATIONS[loc]?.[key];

  if (text === undefined && loc !== "en") {
    text = TRANSLATIONS["en"]?.[key];
  }
  if (text === undefined && loc !== "de") {
    text = TRANSLATIONS["de"]?.[key];
  }
  if (text === undefined) {
    return String(key);
  }

  if (params && typeof params === "object") {
    for (const [k, v] of Object.entries(params)) {
      text = text.replace(new RegExp(`\\{${k}\\}`, "g"), String(v));
    }
  }

  return text;
}

/**
 * Retranslates all DOM elements matching data-i18n attributes in the given root element or document.
 */
export function translateDocument(root = typeof document !== "undefined" ? document : null, locale = currentLocale) {
  if (!root) return;

  if (root.documentElement) {
    root.documentElement.lang = locale;
  }

  const textNodes = root.querySelectorAll("[data-i18n]");
  for (const node of textNodes) {
    const key = node.dataset.i18n;
    if (key) {
      node.textContent = t(key, {}, locale);
    }
  }

  const placeholders = root.querySelectorAll("[data-i18n-placeholder]");
  for (const node of placeholders) {
    const key = node.dataset.i18nPlaceholder;
    if (key) {
      node.placeholder = t(key, {}, locale);
    }
  }

  const titles = root.querySelectorAll("[data-i18n-title]");
  for (const node of titles) {
    const key = node.dataset.i18nTitle;
    if (key) {
      node.title = t(key, {}, locale);
    }
  }

  const ariaLabels = root.querySelectorAll("[data-i18n-aria-label]");
  for (const node of ariaLabels) {
    const key = node.dataset.i18nAriaLabel;
    if (key) {
      node.setAttribute("aria-label", t(key, {}, locale));
    }
  }
}
