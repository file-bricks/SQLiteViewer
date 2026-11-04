import { test, describe } from "node:test";
import assert from "node:assert/strict";

import {
  SUPPORTED_LOCALES,
  DEFAULT_LOCALE,
  STORAGE_KEY,
  TRANSLATIONS,
  getLocale,
  setLocale,
  normalizeLocale,
  detectLocale,
  t,
  translateDocument,
} from "../i18n.js";

describe("i18n Core Contract (Tier-2 6-Languages)", () => {
  test("supported locales include de, en, es, zh, ja, ru with de as default", () => {
    assert.deepEqual(SUPPORTED_LOCALES, ["de", "en", "es", "zh", "ja", "ru"]);
    assert.equal(DEFAULT_LOCALE, "de");
    assert.equal(STORAGE_KEY, "sqliteviewer-web-companion:language");
  });

  test("translations dictionary contains all 54 required keys with 100% parity across all 6 languages", () => {
    const deKeys = Object.keys(TRANSLATIONS.de).sort();
    assert.equal(deKeys.length, 54, "DE should contain exactly 54 keys");

    for (const lang of ["en", "es", "zh", "ja", "ru"]) {
      const langKeys = Object.keys(TRANSLATIONS[lang]).sort();
      assert.deepEqual(langKeys, deKeys, `${lang.toUpperCase()} keys should be identical to DE keys`);
    }
  });

  test("t() returns accurate translations for all 6 languages", () => {
    assert.equal(t("action_load_json", {}, "de"), "JSON laden");
    assert.equal(t("action_load_json", {}, "en"), "Load JSON");
    assert.equal(t("action_load_json", {}, "es"), "Cargar JSON");
    assert.equal(t("action_load_json", {}, "zh"), "加载 JSON");
    assert.equal(t("action_load_json", {}, "ja"), "JSON 読み込み");
    assert.equal(t("action_load_json", {}, "ru"), "Загрузить JSON");

    assert.equal(t("panel_source_title", {}, "de"), "Export-Metadaten");
    assert.equal(t("panel_source_title", {}, "en"), "Export Metadata");
    assert.equal(t("panel_source_title", {}, "es"), "Metadatos de exportación");
    assert.equal(t("panel_source_title", {}, "zh"), "导出元数据");
    assert.equal(t("panel_source_title", {}, "ja"), "エクスポートメタデータ");
    assert.equal(t("panel_source_title", {}, "ru"), "Метаданные экспорта");
  });

  test("t() interpolates parameters properly across languages", () => {
    const formattedDe = t("status_export_loaded", {
      label: "Demo",
      name: "test.sqlite",
      count: 42,
    }, "de");
    assert.equal(formattedDe, "Demo geladen: test.sqlite (42 sichtbare Zeilen).");

    const formattedEn = t("status_export_loaded", {
      label: "Demo",
      name: "test.sqlite",
      count: 42,
    }, "en");
    assert.equal(formattedEn, "Demo loaded: test.sqlite (42 visible rows).");

    const formattedEs = t("status_export_loaded", {
      label: "Demo",
      name: "test.sqlite",
      count: 42,
    }, "es");
    assert.equal(formattedEs, "Demo cargado: test.sqlite (42 filas visibles).");

    const emptyFiltered = t("empty_state_filtered", { query: "orders" }, "en");
    assert.equal(emptyFiltered, 'No rows match search filter "orders".');
  });

  test("t() falls back gracefully for unknown keys or unsupported locales", () => {
    // Nonexistent key returns key itself
    assert.equal(t("non_existent_key_xyz", {}, "de"), "non_existent_key_xyz");
    assert.equal(t("non_existent_key_xyz", {}, "en"), "non_existent_key_xyz");
    assert.equal(t("non_existent_key_xyz", {}, "es"), "non_existent_key_xyz");

    // Unsupported locale defaults to de fallback
    assert.equal(t("action_load_json", {}, "fr"), "JSON laden");
  });

  test("normalizeLocale handles full codes and case variations for all 6 languages", () => {
    assert.equal(normalizeLocale("de-DE"), "de");
    assert.equal(normalizeLocale("EN_US"), "en");
    assert.equal(normalizeLocale("es-ES"), "es");
    assert.equal(normalizeLocale("zh-CN"), "zh");
    assert.equal(normalizeLocale("ja-JP"), "ja");
    assert.equal(normalizeLocale("ru-RU"), "ru");
    assert.equal(normalizeLocale("fr-FR"), "de"); // unsupported falls back to default
    assert.equal(normalizeLocale(null), "de");
  });

  test("setLocale and getLocale update the active language", () => {
    setLocale("en");
    assert.equal(getLocale(), "en");
    assert.equal(t("action_open_demo"), "Open Demo");

    setLocale("es");
    assert.equal(getLocale(), "es");
    assert.equal(t("action_open_demo"), "Abrir demo");

    setLocale("zh");
    assert.equal(getLocale(), "zh");
    assert.equal(t("action_open_demo"), "打开演示");

    setLocale("ja");
    assert.equal(getLocale(), "ja");
    assert.equal(t("action_open_demo"), "デモを開く");

    setLocale("ru");
    assert.equal(getLocale(), "ru");
    assert.equal(t("action_open_demo"), "Открыть демо");

    setLocale("de");
    assert.equal(getLocale(), "de");
    assert.equal(t("action_open_demo"), "Demo öffnen");
  });

  test("detectLocale falls back to DEFAULT_LOCALE in node environment without storage/navigator", () => {
    const loc = detectLocale();
    assert.ok(SUPPORTED_LOCALES.includes(loc));
  });

  test("translateDocument updates mock DOM nodes with data-i18n attributes", () => {
    const mockNodes = [
      { dataset: { i18n: "action_load_json" }, textContent: "Alt" },
      { dataset: { i18n: "action_reset" }, textContent: "Alt" },
    ];
    const mockPlaceholders = [
      { dataset: { i18nPlaceholder: "search_placeholder" }, placeholder: "Alt" },
    ];
    const mockTitles = [
      { dataset: { i18nTitle: "sort_click_asc" }, title: "Alt" },
    ];
    const mockAriaLabels = [
      {
        dataset: { i18nAriaLabel: "search_label" },
        setAttribute(attr, val) { this[attr] = val; }
      }
    ];

    const mockRoot = {
      documentElement: { lang: "de" },
      querySelectorAll(selector) {
        if (selector === "[data-i18n]") return mockNodes;
        if (selector === "[data-i18n-placeholder]") return mockPlaceholders;
        if (selector === "[data-i18n-title]") return mockTitles;
        if (selector === "[data-i18nAriaLabel]" || selector === "[data-i18n-aria-label]") return mockAriaLabels;
        return [];
      }
    };

    translateDocument(mockRoot, "es");

    assert.equal(mockRoot.documentElement.lang, "es");
    assert.equal(mockNodes[0].textContent, "Cargar JSON");
    assert.equal(mockNodes[1].textContent, "Restablecer");
    assert.equal(mockPlaceholders[0].placeholder, "Título, ID, consulta, notas BLOB …");
    assert.equal(mockTitles[0].title, "Clic para ordenar ascendente");
    assert.equal(mockAriaLabels[0]["aria-label"], "Buscar en filas visibles");
  });
});
