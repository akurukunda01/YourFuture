// Central API configuration.
// In development the Vite dev server proxies /api -> Flask (see vite.config.js).
// In production the SPA is served same-origin behind /api, so the default works
// without any env var. Override with VITE_API_URL only for split deployments.
export const API = import.meta.env.VITE_API_URL ?? "/api";

// Resolve a media reference to a usable URL.
// - Absolute http(s) URLs (admin-entered logos, etc.) are used as-is.
// - Falsy values return "" so <img> can fall back gracefully.
export function mediaUrl(value) {
  if (!value) return "";
  if (/^https?:\/\//i.test(value)) return value;
  return `${API}/${value}`;
}
