import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { readFile, access } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

async function read(relativePath) {
  return readFile(path.join(ROOT, relativePath), "utf8");
}

test("manifest exposes installable metadata and icons", async () => {
  const manifest = JSON.parse(await read("manifest.webmanifest"));

  assert.equal(manifest.lang, "de");
  assert.equal(manifest.display, "standalone");
  assert.equal(manifest.start_url, "./");
  assert.equal(manifest.scope, "./");
  assert.ok(Array.isArray(manifest.display_override));
  assert.ok(manifest.display_override.includes("standalone"));

  const sizes = manifest.icons.map((icon) => icon.sizes);
  assert.ok(sizes.includes("192x192"));
  assert.ok(sizes.includes("512x512"));
  assert.ok(manifest.icons.some((icon) => icon.purpose === "maskable"));

  for (const icon of manifest.icons) {
    await access(path.join(ROOT, icon.src));
  }
});

test("index wires mobile shell metadata", async () => {
  const html = await read("index.html");

  assert.match(html, /viewport-fit=cover/);
  assert.doesNotMatch(html, /apple-mobile-web-app-capable/, "apple-mobile-web-app-capable ist deprecated seit iOS 11.3 — darf nicht gesetzt sein");
  assert.match(html, /apple-touch-icon/);
  assert.match(html, /manifest\.webmanifest/);
});

test("service worker caches the offline shell including icons", async () => {
  const sw = await read("sw.js");

  for (const asset of [
    "./index.html",
    "./style.css",
    "./app.js",
    "./library.js",
    "./manifest.webmanifest",
    "./icons/sqliteviewer-companion-180.png",
    "./icons/Icon-192.png",
    "./icons/Icon-maskable-192.png",
    "./icons/Icon-512.png",
    "./icons/Icon-maskable-512.png"
  ]) {
    assert.match(sw, new RegExp(asset.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  }

  assert.ok(
    /caches\.match\([^)]*ignoreSearch\s*:\s*true/.test(sw),
    "caches.match muss { ignoreSearch: true } für ?demo=1 nutzen"
  );

  assert.ok(
    /self\.skipWaiting\(\)/.test(sw),
    "install-Handler muss self.skipWaiting() aufrufen, damit der neue SW sofort aktiviert wird"
  );

  assert.ok(
    /self\.clients\.claim\(\)/.test(sw),
    "activate-Handler muss clients.claim() aufrufen, damit bestehende Seiten sofort übernommen werden"
  );

  // BUG-W1 Regressionstest
  assert.ok(
    /fetch\(event\.request\)[\s\S]{0,100}\.catch\(/.test(sw),
    "BUG-W1: sw.js fetch muss .catch() für Offline-Fallback haben — sonst unhandled rejection wenn Ressource nicht gecacht und Netz offline"
  );

  assert.ok(
    sw.includes("503"),
    "BUG-W1: Offline-Fallback muss HTTP 503 zurückgeben"
  );

  // CACHE-Version v3+ sicherstellen (nach W1-Fix gebumpt)
  const cacheMatch = sw.match(/CACHE_NAME\s*=\s*["']sqliteviewer-companion-v(\d+)["']/);
  assert.ok(cacheMatch && parseInt(cacheMatch[1]) >= 3, "CACHE_NAME muss auf v3+ gebumpt sein (nach BUG-W1-Fix)");
});

// --- iOS PWA-Härtung (P4b, 2026-06-16) ---
describe("iOS PWA-Härtung", () => {
  test("iOS: viewport enthält viewport-fit=cover (Notch/Dynamic Island)", async () => {
    const html = await read("index.html");
    assert.match(html, /viewport-fit=cover/, "viewport-fit=cover fehlt im viewport-Meta-Tag");
  });

  test("iOS: apple-touch-icon zeigt auf sqliteviewer-companion-180.png (opak)", async () => {
    const html = await read("index.html");
    assert.match(html, /sqliteviewer-companion-180\.png/, "sqliteviewer-companion-180.png fehlt als Linkziel");
  });

  test("iOS: apple-mobile-web-app-title ist vorhanden", async () => {
    const html = await read("index.html");
    assert.match(html, /apple-mobile-web-app-title/, "apple-mobile-web-app-title Meta-Tag fehlt");
  });

  test("iOS: apple-mobile-web-app-status-bar-style ist vorhanden", async () => {
    const html = await read("index.html");
    assert.match(html, /apple-mobile-web-app-status-bar-style/, "apple-mobile-web-app-status-bar-style Meta-Tag fehlt");
  });

  test("iOS: KEIN apple-mobile-web-app-capable (deprecated seit iOS 11.3)", async () => {
    const html = await read("index.html");
    assert.doesNotMatch(html, /apple-mobile-web-app-capable/, "apple-mobile-web-app-capable ist deprecated und darf nicht gesetzt sein");
  });

  test("iOS: sqliteviewer-companion-180.png existiert physisch in icons/", async () => {
    await access(path.join(ROOT, "icons", "sqliteviewer-companion-180.png"));
  });

  test("iOS: style.css enthält safe-area-inset", async () => {
    const css = await read("style.css");
    assert.match(css, /safe-area-inset/, "safe-area-inset CSS fehlt in style.css");
  });

  test("iOS: style.css hat .shell mit env(safe-area-inset-top)", async () => {
    const css = await read("style.css");
    assert.match(css, /\.shell/, ".shell Klasse fehlt in style.css");
    assert.match(css, /env\(safe-area-inset-top\)/, "env(safe-area-inset-top) fehlt in .shell");
  });

  test("iOS: style.css hat safe-area-inset-bottom", async () => {
    const css = await read("style.css");
    assert.match(css, /safe-area-inset-bottom/, "safe-area-inset-bottom fehlt in style.css");
  });
});
