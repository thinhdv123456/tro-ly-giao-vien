// Service Worker tối giản cho Cổng Lớp Học — chỉ để "cài như app" (PWA).
// An toàn: KHÔNG can thiệp các yêu cầu tới Firebase/CDN (khác origin) — để chúng đi thẳng.
const CACHE = 'cong-v1';
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.add('/cong')).catch(() => {}));
  self.skipWaiting();
});
self.addEventListener('activate', (e) => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', (e) => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const u = new URL(r.url);
  if (u.origin !== location.origin) return;            // Firebase/Google/CDN → đi thẳng
  if (r.mode === 'navigate') {                          // mở trang: ưu tiên mạng, offline thì lấy bản đã lưu
    e.respondWith(
      fetch(r).then((res) => { const cp = res.clone(); caches.open(CACHE).then((c) => c.put('/cong', cp)); return res; })
        .catch(() => caches.match('/cong'))
    );
  }
});
