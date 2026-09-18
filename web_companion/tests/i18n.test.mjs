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

describe("i18n Core Contract", () => {
  test("supported locales include de and en with de as default", () => {
    assert.deepEqual(SUPPORTED_LOCALES, ["de", "en"]);
    assert.equal(DEFAULT_LOCALE, "de");
    assert.equal(STORAGE_KEY, "sqliteviewer-web-companion:language");
  });

  test("translations dictionary contains all required keys for both de and en", () => {
    const deKeys = Object.keys(TRANSLATIONS.de);
    const enKeys = Object.keys(TRANSLATIONS.en);

    assert.ok(deKeys.length > 25, "DE should contain 25+ keys");
    assert.deepEqual(deKeys.sort(), enKeys.sort(), "DE and EN should have identical key sets");
  });

  test("t() returns accurate translations for DE and EN", () => {
    assert.equal(t("action_load_json", {}, "de"), "JSON laden");
    assert.equal(t("action_load_json", {}, "en"), "Load JSON");

    assert.equal(t("panel_source_title", {}, "de"), "Export-Metadaten");
    assert.equal(t("panel_source_title", {}, "en"), "Export Metadata");
  });

  test("t() interpolates parameters properly", () => {
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

    const emptyFiltered = t("empty_state_filtered", { query: "orders" }, "en");
    assert.equal(emptyFiltered, 'No rows match search filter "orders".');
  });

  test("t() falls back gracefully for unknown keys or unsupported locales", () => {
    // Nonexistent key returns key itself
    assert.equal(t("non_existent_key_xyz", {}, "de"), "non_existent_key_xyz");
    assert.equal(t("non_existent_key_xyz", {}, "en"), "non_existent_key_xyz");

    // Unsupported locale defaults to de/en fallback
    assert.equal(t("action_load_json", {}, "fr"), "JSON laden");
  });

  test("normalizeLocale handles full codes and case variations", () => {
    assert.equal(normalizeLocale("de-DE"), "de");
    assert.equal(normalizeLocale("EN_US"), "en");
    assert.equal(normalizeLocale("es-ES"), "de"); // unsupported falls back to default
    assert.equal(normalizeLocale(null), "de");
  });

  test("setLocale and getLocale update the active language", () => {
    setLocale("en");
    assert.equal(getLocale(), "en");
    assert.equal(t("action_open_demo"), "Open Demo");

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

    translateDocument(mockRoot, "en");

    assert.equal(mockRoot.documentElement.lang, "en");
    assert.equal(mockNodes[0].textContent, "Load JSON");
    assert.equal(mockNodes[1].textContent, "Reset");
    assert.equal(mockPlaceholders[0].placeholder, "Title, ID, query, BLOB notes …");
    assert.equal(mockTitles[0].title, "Click to sort ascending");
    assert.equal(mockAriaLabels[0]["aria-label"], "Search visible rows");
  });
});
