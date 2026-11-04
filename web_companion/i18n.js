/**
 * SQLiteViewer Web-Companion Internationalization (i18n)
 * Supports DE, EN, ES, ZH, JA, and RU with fallback chain: requested -> en -> de -> key
 */

export const SUPPORTED_LOCALES = ["de", "en", "es", "zh", "ja", "ru"];
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
    status_import_too_large: "Datei ist größer als das lokale Importlimit von {limit}.",
    status_import_too_many_columns: "Export enthält mehr als {limit} Spalten und wurde nicht geladen.",
    status_import_too_many_rows: "Export enthält mehr als {limit} Ergebniszeilen und wurde nicht geladen.",
    
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
    status_import_too_large: "File exceeds the local import limit of {limit}.",
    status_import_too_many_columns: "Export contains more than {limit} columns and was not loaded.",
    status_import_too_many_rows: "Export contains more than {limit} result rows and was not loaded.",
    
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
  },
  es: {
    doc_title: "SQLiteViewer Companion",
    meta_description: "Companion sin conexión para sqliteviewer-export-v1.json",
    eyebrow: "SQLiteViewer Companion",
    hero_title: "Inspecciona exportaciones locales sin subir la base de datos.",
    hero_lead: "Este companion abre `sqliteviewer-export-v1.json` directamente en el navegador, muestra metadatos, columnas y filas de resultados, manteniéndose estrictamente sin conexión.",
    action_load_json: "Cargar JSON",
    action_open_demo: "Abrir demo",
    action_reset: "Restablecer",
    action_export_csv: "Exportar CSV",
    status_ready: "Listo.",
    status_reset: "Companion local restablecido.",
    status_drag_idle_title: "Arrastra el archivo aquí",
    status_drag_idle_hint: "Actualmente compatible con la exportación de escritorio `sqliteviewer-export-v1.json`.",
    status_drag_active: "Suelta el archivo para cargar la exportación.",
    status_demo_loaded: "Exportación de demostración cargada.",
    status_restored: "Última exportación cargada restaurada.",
    status_export_loaded: "{label} cargado: {name} ({count} filas visibles).",
    status_storage_warn: "Exportación cargada, pero el navegador no pudo almacenar el estado localmente.",
    status_read_error: "No se pudo leer el archivo.",
    status_import_too_large: "El archivo supera el límite de importación local de {limit}.",
    status_import_too_many_columns: "La exportación contiene más de {limit} columnas y no se cargó.",
    status_import_too_many_rows: "La exportación contiene más de {limit} filas de resultados y no se cargó.",
    panel_source_eyebrow: "Origen",
    panel_source_title: "Metadatos de exportación",
    panel_source_empty: "Aún no se ha cargado ninguna exportación.",
    query_label: "Consulta SQL",
    meta_database: "Base de datos",
    meta_view: "Vista",
    meta_table: "Tabla",
    meta_rows: "Filas",
    meta_limit: "Límite",
    meta_sort: "Ordenación",
    meta_unknown: "Desconocido",
    panel_view_eyebrow: "Vista",
    panel_view_title: "Filas de resultados",
    results_count_zero: "0 filas visibles",
    results_count_one: "1 fila visible",
    results_count_other: "{count} filas visibles",
    search_label: "Buscar en filas visibles",
    search_placeholder: "Título, ID, consulta, notas BLOB …",
    empty_state_initial: "No hay datos visibles. Carga una exportación o abre la demo.",
    empty_state_filtered: "Ninguna fila coincide con el filtro »{query}«.",
    panel_notes_eyebrow: "Diseño deliberadamente ligero",
    panel_notes_title: "Límites del Companion",
    note_no_upload: "Sin cargas en servidores ni sincronización en la nube.",
    note_no_write: "Sin funciones de escritura en el escritorio ni en la base de datos.",
    note_raw_sqlite: "Los archivos `.sqlite` en bruto permanecen deliberadamente como vía de evaluación posterior.",
    sort_click_asc: "Clic para ordenar ascendente",
    sort_click_desc: "Clic para ordenar descendente",
    sort_click_clear: "Clic para eliminar ordenación",
    summary_path_hidden: "ruta local completa oculta en la exportación",
    summary_path_none: "sin ruta local en la exportación",
    summary_unknown_db: "base de datos desconocida",
    summary_source_prefix: "Origen:"
  },
  zh: {
    doc_title: "SQLiteViewer Companion",
    meta_description: "sqliteviewer-export-v1.json 离线助手",
    eyebrow: "SQLiteViewer Companion",
    hero_title: "在不上传数据库的情况下查看本地导出数据。",
    hero_lead: "本助手直接在浏览器中打开 `sqliteviewer-export-v1.json`，显示元数据、列和结果行，保持纯离线运行。",
    action_load_json: "加载 JSON",
    action_open_demo: "打开演示",
    action_reset: "重置",
    action_export_csv: "导出 CSV",
    status_ready: "就绪。",
    status_reset: "本地助手已重置。",
    status_drag_idle_title: "拖放文件到此处",
    status_drag_idle_hint: "目前支持桌面导出文件 `sqliteviewer-export-v1.json`。",
    status_drag_active: "释放文件以加载导出数据。",
    status_demo_loaded: "演示导出数据已加载。",
    status_restored: "已恢复上次加载的导出数据。",
    status_export_loaded: "已加载 {label}：{name}（{count} 个可见行）。",
    status_storage_warn: "已加载导出数据，但浏览器无法进行本地恢复存储。",
    status_read_error: "无法读取文件。",
    status_import_too_large: "文件大小超过本地导入限制 {limit}。",
    status_import_too_many_columns: "导出包含超过 {limit} 列，未予加载。",
    status_import_too_many_rows: "导出包含超过 {limit} 结果行，未予加载。",
    panel_source_eyebrow: "来源",
    panel_source_title: "导出元数据",
    panel_source_empty: "尚未加载导出数据。",
    query_label: "SQL 查询",
    meta_database: "数据库",
    meta_view: "视图",
    meta_table: "数据表",
    meta_rows: "行数",
    meta_limit: "限制",
    meta_sort: "排序",
    meta_unknown: "未知",
    panel_view_eyebrow: "视图",
    panel_view_title: "结果行",
    results_count_zero: "0 个可见行",
    results_count_one: "1 个可见行",
    results_count_other: "{count} 个可见行",
    search_label: "在可见行中搜索",
    search_placeholder: "标题、ID、查询、BLOB 说明 …",
    empty_state_initial: "暂无可见数据。请加载导出文件或打开演示。",
    empty_state_filtered: "没有匹配搜索条件“{query}”的行。",
    panel_notes_eyebrow: "轻量化设计",
    panel_notes_title: "助手边界",
    note_no_upload: "无服务器上传，无云端同步。",
    note_no_write: "不支持回写桌面程序或原始数据库。",
    note_raw_sqlite: "原始 `.sqlite` 文件明确作为后续评估路线。",
    sort_click_asc: "点击升序排列",
    sort_click_desc: "点击降序排列",
    sort_click_clear: "点击清除排序",
    summary_path_hidden: "导出中已隐藏完整的本地路径",
    summary_path_none: "导出中无本地路径",
    summary_unknown_db: "未知数据库",
    summary_source_prefix: "来源："
  },
  ja: {
    doc_title: "SQLiteViewer Companion",
    meta_description: "sqliteviewer-export-v1.json 用オフラインコンパニオン",
    eyebrow: "SQLiteViewer Companion",
    hero_title: "データベースをアップロードせずにローカルエクスポートを確認。",
    hero_lead: "このコンパニオンはブラウザ内で `sqliteviewer-export-v1.json` を直接開き、メタデータ、列、結果行を表示します。完全なオフラインファースト設計です。",
    action_load_json: "JSON 読み込み",
    action_open_demo: "デモを開く",
    action_reset: "リセット",
    action_export_csv: "CSV エクスポート",
    status_ready: "準備完了。",
    status_reset: "ローカルコンパニオンをリセットしました。",
    status_drag_idle_title: "ファイルをここにドロップ",
    status_drag_idle_hint: "現在デスクトップエクスポート `sqliteviewer-export-v1.json` に対応しています。",
    status_drag_active: "ファイルを離してエクスポートを読み込みます。",
    status_demo_loaded: "デモエクスポートを読み込みました。",
    status_restored: "最後に読み込んだエクスポートを復元しました。",
    status_export_loaded: "{label} を読み込みました: {name} ({count} 件の可視行)。",
    status_storage_warn: "エクスポートを読み込みましたが、ブラウザにローカル復元用データを保存できませんでした。",
    status_read_error: "ファイルを読み込めませんでした。",
    status_import_too_large: "ファイルサイズがローカルインポート制限 {limit} を超えています。",
    status_import_too_many_columns: "エクスポートの列数が {limit} を超えているため読み込まれませんでした。",
    status_import_too_many_rows: "エクスポートの結果行数が {limit} を超えているため読み込まれませんでした。",
    panel_source_eyebrow: "ソース",
    panel_source_title: "エクスポートメタデータ",
    panel_source_empty: "まだエクスポートが読み込まれていません。",
    query_label: "SQL クエリ",
    meta_database: "データベース",
    meta_view: "ビュー",
    meta_table: "テーブル",
    meta_rows: "行数",
    meta_limit: "上限",
    meta_sort: "並び順",
    meta_unknown: "不明",
    panel_view_eyebrow: "ビュー",
    panel_view_title: "結果行",
    results_count_zero: "0 件の可視行",
    results_count_one: "1 件の可視行",
    results_count_other: "{count} 件の可視行",
    search_label: "可視行内を検索",
    search_placeholder: "タイトル、ID、クエリ、BLOBメモ …",
    empty_state_initial: "表示可能なデータがありません。エクスポートを読み込むかデモを開いてください。",
    empty_state_filtered: "検索条件「{query}」に一致する行はありません。",
    panel_notes_eyebrow: "軽量性を最優先",
    panel_notes_title: "コンパニオンの範囲",
    note_no_upload: "サーバーアップロードおよびクラウド同期なし。",
    note_no_write: "デスクトップやデータベースへの書き戻し機能なし。",
    note_raw_sqlite: "生の `.sqlite` ファイル対応は将来的な検討事項です。",
    sort_click_asc: "クリックで昇順に並べ替え",
    sort_click_desc: "クリックで降順に並べ替え",
    sort_click_clear: "クリックで並べ替えを解除",
    summary_path_hidden: "エクスポート内で完全なローカルパスは非表示",
    summary_path_none: "エクスポート内にローカルパスなし",
    summary_unknown_db: "不明なデータベース",
    summary_source_prefix: "ソース:"
  },
  ru: {
    doc_title: "SQLiteViewer Companion",
    meta_description: "Автономный компаньон для sqliteviewer-export-v1.json",
    eyebrow: "SQLiteViewer Companion",
    hero_title: "Просмотр локального экспорта без загрузки базы данных в сеть.",
    hero_lead: "Этот компаньон открывает `sqliteviewer-export-v1.json` прямо в браузере, отображает метаданные, столбцы и строки результатов, работая строго автономно.",
    action_load_json: "Загрузить JSON",
    action_open_demo: "Открыть демо",
    action_reset: "Сбросить",
    action_export_csv: "Экспорт в CSV",
    status_ready: "Готово.",
    status_reset: "Локальный компаньон сброшен.",
    status_drag_idle_title: "Перетащите файл сюда",
    status_drag_idle_hint: "В настоящее время поддерживается экспорт приложения `sqliteviewer-export-v1.json`.",
    status_drag_active: "Отпустите файл для загрузки данных экспорта.",
    status_demo_loaded: "Демонстрационный экспорт загружен.",
    status_restored: "Восстановлен последний загруженный экспорт.",
    status_export_loaded: "{label} загружен: {name} ({count} видимых строк).",
    status_storage_warn: "Экспорт загружен, но браузер не смог сохранить состояние для локального восстановления.",
    status_read_error: "Не удалось прочитать файл.",
    status_import_too_large: "Размер файла превышает локальный лимит импорта {limit}.",
    status_import_too_many_columns: "Экспорт содержит более {limit} столбцов и не был загружен.",
    status_import_too_many_rows: "Экспорт содержит более {limit} строк результатов и не был загружен.",
    panel_source_eyebrow: "Источник",
    panel_source_title: "Метаданные экспорта",
    panel_source_empty: "Экспорт ещё не загружен.",
    query_label: "SQL-запрос",
    meta_database: "База данных",
    meta_view: "Вид",
    meta_table: "Таблица",
    meta_rows: "Строк",
    meta_limit: "Лимит",
    meta_sort: "Сортировка",
    meta_unknown: "Неизвестно",
    panel_view_eyebrow: "Вид",
    panel_view_title: "Строки результатов",
    results_count_zero: "0 видимых строк",
    results_count_one: "1 видимая строка",
    results_count_other: "{count} видимых строк",
    search_label: "Поиск по видимым строкам",
    search_placeholder: "Заголовок, ID, запрос, примечания BLOB …",
    empty_state_initial: "Данные пока не отображаются. Загрузите файл экспорта или откройте демо.",
    empty_state_filtered: "Нет строк, соответствующих фильтру поиска «{query}».",
    panel_notes_eyebrow: "Минималистичный дизайн",
    panel_notes_title: "Границы возможностей",
    note_no_upload: "Без передачи на сервер и облачной синхронизации.",
    note_no_write: "Без функций обратной записи в программу или базу данных.",
    note_raw_sqlite: "Прямая работа с файлами `.sqlite` осознанно оставлена на будущее.",
    sort_click_asc: "Нажмите для сортировки по возрастанию",
    sort_click_desc: "Нажмите для сортировки по убыванию",
    sort_click_clear: "Нажмите для сброса сортировки",
    summary_path_hidden: "полный локальный путь скрыт в экспорте",
    summary_path_none: "нет локального пути в экспорте",
    summary_unknown_db: "неизвестная база данных",
    summary_source_prefix: "Источник:"
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
