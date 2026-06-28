import { buildDemoExport, exportToCsv, filterRows, formatCellValue, parseExport } from "./library.js";

const STORAGE_KEY = "sqliteviewer-web-companion:last-export";

const state = {
  exportData: null,
  visibleRows: [],
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
};

function setStatus(message, tone = "neutral") {
  elements.status.textContent = message;
  elements.status.dataset.tone = tone;
}

function persistExport(rawPayload) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(rawPayload));
  } catch (_error) {
    setStatus("Export geladen, aber der Browser konnte keine lokale Wiederherstellung speichern.", "warn");
  }
}

function restoreExport() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return false;
    }
    loadPayload(JSON.parse(raw), { persist: false, sourceLabel: "Zuletzt geladener Export wiederhergestellt." });
    return true;
  } catch (_error) {
    return false;
  }
}

function clearExport() {
  state.exportData = null;
  state.visibleRows = [];
  elements.filterInput.value = "";
  elements.metaCards.innerHTML = "";
  elements.queryText.textContent = "";
  elements.queryBox.hidden = true;
  elements.tableHead.innerHTML = "";
  elements.tableBody.innerHTML = "";
  elements.resultsCount.textContent = "0 sichtbare Zeilen";
  elements.emptyState.hidden = false;
  elements.shellState.textContent = "Noch kein Export geladen.";
  elements.csvExportButton.disabled = true;
  localStorage.removeItem(STORAGE_KEY);
  setStatus("Lokaler Companion zurückgesetzt.", "neutral");
}

function renderMeta(exportData) {
  const cards = [
    ["Datenbank", exportData.source.databaseName ?? "Unbekannt"],
    ["Ansicht", exportData.source.view],
    ["Tabelle", exportData.source.table ?? "—"],
    ["Zeilen", `${exportData.rowCount}`],
    ["Limit", exportData.source.rowLimit ?? "—"],
    ["Sortierung", exportData.source.sortColumn
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

  const exportedAt = exportData.exportedAt ?? "unbekannt";
  const dbPath = exportData.source.databasePath ?? "nicht mitgegeben";
  elements.shellState.textContent = `${exportData.appName} ${exportData.appVersion} · Export: ${exportedAt} · Quelle: ${dbPath}`;
}

function renderTable(exportData, rows) {
  elements.tableHead.innerHTML = "";
  elements.tableBody.innerHTML = "";

  const headerRow = document.createElement("tr");
  for (const column of exportData.columns) {
    const th = document.createElement("th");
    th.textContent = column;
    headerRow.appendChild(th);
  }
  elements.tableHead.appendChild(headerRow);

  if (rows.length === 0) {
    elements.emptyState.hidden = false;
    elements.resultsCount.textContent = "0 sichtbare Zeilen";
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
  elements.resultsCount.textContent = `${rows.length} sichtbare Zeilen`;
}

function applyFilter() {
  if (!state.exportData) {
    return;
  }
  state.visibleRows = filterRows(state.exportData, { query: elements.filterInput.value });
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
  setStatus(options.sourceLabel ?? "Export lokal geladen.", "success");
}

function loadDemo() {
  const demo = buildDemoExport();
  loadPayload(demo.raw, { sourceLabel: "Demo-Export geladen." });
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result ?? ""));
    reader.onerror = () => reject(new Error("Die Datei konnte nicht gelesen werden."));
    reader.readAsText(file, "utf-8");
  });
}

async function handleFile(file) {
  if (!file) {
    return;
  }
  try {
    const text = await readFileAsText(file);
    loadPayload(JSON.parse(text), { sourceLabel: `Export geladen: ${file.name}` });
  } catch (error) {
    setStatus(error instanceof Error ? error.message : "Unbekannter Ladefehler.", "error");
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
  setStatus(`CSV exportiert: ${state.visibleRows.length} sichtbare Zeilen.`, "success");
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

const params = new URLSearchParams(window.location.search);
if (params.get("demo") === "1") {
  loadDemo();
} else if (!restoreExport()) {
  setStatus("Bereit für lokale JSON-Exporte. Keine Server-Uploads.", "neutral");
}
