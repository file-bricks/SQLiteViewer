const CACHE_NAME = "sqliteviewer-companion-v2";
const OFFLINE_ASSETS = [
  "./",
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
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(OFFLINE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") {
    return;
  }

  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then((cached) => {
      if (cached) {
        return cached;
      }
      return fetch(event.request);
    })
  );
});
