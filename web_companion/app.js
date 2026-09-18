import {
  buildDemoExport,
  exportToCsv,
  filterRows,
  formatCellValue,
  formatSourceSummary,
  parseExport,
  sortRows,
} from "./library.js";
import {
  detectLocale,
  getLocale,
  setLocale,
  t,
  translateDocument,
} from "./i18n.js";

const STORAGE_KEY = "sqliteviewer-web-companion:last-export";

const state = {
  exportData: null,
  visibleRows: [],
  sortKey: null,
  sortDescending: false,
};

const elements = {
  status: document.querySelector("[data-status]"),
  fileInput: document.querySelector("[data-file-input]"),
  dropZone: document.querySelector("[data-drop-zone]"),
  filterInput: document.querySelector("[data-filter-input]"),
  importButton: document.querySelector("[data-import-button]"),
  demoButton: document.querySelector("[data-demo-button]"),
  clearButton: document.querySelector("[data-clear-button]"),
  shellState: document.querySelector("[data-shell-state]"),
  metaCards: document.querySelector("[data-meta-cards]"),
  queryBox: document.querySelector("[data-query-box]"),
  queryText: document.querySelector("[data-query-text]"),
  resultsCount: document.querySelector("[data-results-count]"),
  csvExportButton: document.querySelector("[data-csv-export-button]"),
  tableHead: document.querySelector("[data-table-head]"),
  tableBody: document.querySelector("[data-table-body]"),
  emptyState: document.querySelector("[data-empty-state]"),
  langButtons: document.querySelectorAll("[data-lang-btn]"),
};

function setStatus(message, tone = "neutral") {
  elements.status.textContent = message;
  elements.status.dataset.tone = tone;
}

function persistExport(rawPayload) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(rawPayload));
  } catch (_error) {
    setStatus(t("status_storage_warn"), "warn");
  }
}

function restoreExport() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return false;
    }
    loadPayload(JSON.parse(raw), { persist: false, sourceLabel: t("status_restored") });
    return true;
  } catch (_error) {
    return false;
  }
}

function clearExport() {
  const loc = getLocale();
  state.exportData = null;
  state.visibleRows = [];
  state.sortKey = null;
  state.sortDescending = false;
  elements.filterInput.value = "";
  elements.metaCards.innerHTML = "";
  elements.queryText.textContent = "";
  elements.queryBox.hidden = true;
  elements.tableHead.innerHTML = "";
  elements.tableBody.innerHTML = "";
  elements.resultsCount.textContent = t("results_count_zero", {}, loc);
  elements.emptyState.textContent = t("empty_state_initial", {}, loc);
  elements.emptyState.hidden = false;
  elements.shellState.textContent = t("panel_source_empty", {}, loc);
  elements.csvExportButton.disabled = true;
  localStorage.removeItem(STORAGE_KEY);
  setStatus(t("status_reset", {}, loc), "neutral");
}

function renderMeta(exportData) {
  const loc = getLocale();
  const cards = [
    [t("meta_database", {}, loc), exportData.source.databaseName ?? t("meta_unknown", {}, loc)],
    [t("meta_view", {}, loc), exportData.source.view],
    [t("meta_table", {}, loc), exportData.source.table ?? "—"],
    [t("meta_rows", {}, loc), `${exportData.rowCount}`],
    [t("meta_limit", {}, loc), exportData.source.rowLimit ?? "—"],
    [t("meta_sort", {}, loc), exportData.source.sortColumn
      ? `${exportData.source.sortColumn}${exportData.source.sortDescending ? " ↓" : " ↑"}`
      : "—"],
  ];

  elements.metaCards.innerHTML = "";
  const fragment = document.createDocumentFragment();
  for (const [label, value] of cards) {
    const article = document.createElement("article");
    article.className = "meta-card";

    const labelNode = document.createElement("span");
    labelNode.className = "meta-card__label";
    labelNode.textContent = label;

    const valueNode = document.createElement("strong");
    valueNode.className = "meta-card__value";
    valueNode.textContent = String(value);

    article.append(labelNode, valueNode);
    fragment.appendChild(article);
  }
  elements.metaCards.appendChild(fragment);

  if (exportData.source.query) {
    elements.queryText.textContent = exportData.source.query;
    elements.queryBox.hidden = false;
  } else {
    elements.queryText.textContent = "";
    elements.queryBox.hidden = true;
  }

  elements.shellState.textContent = formatSourceSummary(exportData, { locale: loc });
}

function renderTable(exportData, rows) {
  const loc = getLocale();
  elements.tableHead.innerHTML = "";
  elements.tableBody.innerHTML = "";

  const headerRow = document.createElement("tr");
  for (const column of exportData.columns) {
    const th = document.createElement("th");
    th.dataset.col = column;
    th.tabIndex = 0;
    th.title = t("sort_click_asc", {}, loc);

    const label = document.createElement("span");
    label.textContent = column;
    th.appendChild(label);

    if (state.sortKey === column) {
      const indicator = document.createElement("span");
      indicator.className = "sort-indicator";
      indicator.setAttribute("aria-hidden", "true");
      indicator.textContent = state.sortDescending ? " ↓" : " ↑";
      th.appendChild(indicator);
      th.setAttribute("aria-sort", state.sortDescending ? "descending" : "ascending");
    } else {
      th.setAttribute("aria-sort", "none");
    }

    headerRow.appendChild(th);
  }
  elements.tableHead.appendChild(headerRow);

  if (rows.length === 0) {
    elements.emptyState.hidden = false;
    elements.resultsCount.textContent = t("results_count_zero", {}, loc);
    const query = elements.filterInput.value.trim();
    if (query) {
      elements.emptyState.textContent = t("empty_state_filtered", { query }, loc);
    } else {
      elements.emptyState.textContent = t("empty_state_initial", {}, loc);
    }
    return;
  }

  const fragment = document.createDocumentFragment();

  for (const row of rows) {
    const tr = document.createElement("tr");
    row.cells.forEach((value) => {
      const td = document.createElement("td");
      const text = formatCellValue(value);
      td.textContent = text || "∅";
      if (value !== null && typeof value === "object") {
        td.dataset.kind = "structured";
      }
      if (text.length > 96) {
        td.title = text;
      }
      tr.appendChild(td);
    });
    fragment.appendChild(tr);
  }

  elements.tableBody.appendChild(fragment);
  elements.emptyState.hidden = true;
  const count = rows.length;
  const countText = count === 1
    ? t("results_count_one", {}, loc)
    : t("results_count_other", { count }, loc);
  elements.resultsCount.textContent = countText;
}

function applyFilter() {
  if (!state.exportData) {
    return;
  }
  const filtered = filterRows(state.exportData, { query: elements.filterInput.value });
  state.visibleRows = sortRows(filtered, state.exportData.columns, {
    sortKey: state.sortKey,
    sortDescending: state.sortDescending,
  });
  renderTable(state.exportData, state.visibleRows);
}

function loadPayload(rawPayload, options = {}) {
  const exportData = parseExport(rawPayload);
  state.exportData = exportData;
  elements.filterInput.value = exportData.source.searchTerm ?? "";
  renderMeta(exportData);
  applyFilter();
  if (options.persist !== false) {
    persistExport(rawPayload);
  }
  elements.csvExportButton.disabled = false;
  setStatus(options.sourceLabel ?? t("status_export_loaded", {
    label: "Export",
    name: exportData.source.databaseName ?? "export",
    count: state.visibleRows.length
  }), "success");
}

function loadDemo() {
  const demo = buildDemoExport();
  loadPayload(demo.raw, { sourceLabel: t("status_demo_loaded") });
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result ?? ""));
    reader.onerror = () => reject(new Error(t("status_read_error")));
    reader.readAsText(file, "utf-8");
  });
}

async function handleFile(file) {
  if (!file) {
    return;
  }
  try {
    const text = await readFileAsText(file);
    const parsed = JSON.parse(text);
    const count = parsed.result_rows?.length ?? 0;
    const msg = t("status_export_loaded", {
      label: "Export",
      name: file.name,
      count
    });
    loadPayload(parsed, { sourceLabel: msg });
  } catch (error) {
    setStatus(error instanceof Error ? error.message : t("status_read_error"), "error");
  }
}

function handleCsvExport() {
  if (!state.exportData) {
    return;
  }
  const csv = exportToCsv(state.exportData.columns, state.visibleRows);
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  const dbName = state.exportData.source.databaseName ?? "export";
  link.href = url;
  link.download = `${dbName}.csv`;
  link.click();
  URL.revokeObjectURL(url);
  const loc = getLocale();
  const count = state.visibleRows.length;
  const countStr = count === 1 ? t("results_count_one", {}, loc) : t("results_count_other", { count }, loc);
  setStatus(`CSV export: ${countStr}.`, "success");
}

function updateLanguageButtons(locale) {
  for (const btn of elements.langButtons) {
    btn.classList.toggle("active", btn.dataset.langBtn === locale);
  }
}

function changeLanguage(locale) {
  const norm = setLocale(locale);
  updateLanguageButtons(norm);
  translateDocument(document, norm);
  if (state.exportData) {
    renderMeta(state.exportData);
    applyFilter();
  } else {
    elements.shellState.textContent = t("panel_source_empty", {}, norm);
    elements.resultsCount.textContent = t("results_count_zero", {}, norm);
    elements.emptyState.textContent = t("empty_state_initial", {}, norm);
    setStatus(t("status_ready", {}, norm), "neutral");
  }
}

for (const btn of elements.langButtons) {
  btn.addEventListener("click", () => {
    changeLanguage(btn.dataset.langBtn);
  });
}

elements.importButton.addEventListener("click", () => elements.fileInput.click());
elements.fileInput.addEventListener("change", async (event) => {
  const file = event.target.files?.[0];
  await handleFile(file);
  event.target.value = "";
});
elements.demoButton.addEventListener("click", loadDemo);
elements.clearButton.addEventListener("click", clearExport);
elements.csvExportButton.addEventListener("click", handleCsvExport);
elements.filterInput.addEventListener("input", applyFilter);

// Spaltensortierung per Klick auf Tabellenkopf (Event-Delegation)
elements.tableHead.addEventListener("click", (event) => {
  const th = event.target.closest("th[data-col]");
  if (!th || !state.exportData) {
    return;
  }
  const col = th.dataset.col;
  if (state.sortKey === col) {
    state.sortDescending = !state.sortDescending;
  } else {
    state.sortKey = col;
    state.sortDescending = false;
  }
  applyFilter();
});

elements.tableHead.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" && event.key !== " ") {
    return;
  }
  const th = event.target.closest("th[data-col]");
  if (!th || !state.exportData) {
    return;
  }
  event.preventDefault();
  th.click();
});

["dragenter", "dragover"].forEach((eventName) => {
  elements.dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropZone.dataset.drag = "active";
  });
});

["dragleave", "drop"].forEach((eventName) => {
  elements.dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropZone.dataset.drag = "idle";
  });
});

elements.dropZone.addEventListener("drop", async (event) => {
  const file = event.dataTransfer?.files?.[0];
  await handleFile(file);
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch(() => {
      setStatus("Offline-Shell konnte nicht registriert werden.", "warn");
    });
  });
}

// Initialize i18n
const initialLocale = detectLocale();
setLocale(initialLocale);
updateLanguageButtons(initialLocale);
translateDocument(document, initialLocale);

const params = new URLSearchParams(window.location.search);
if (params.get("demo") === "1") {
  loadDemo();
} else if (!restoreExport()) {
  setStatus(t("status_ready"), "neutral");
}
