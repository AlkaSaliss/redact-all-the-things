const LOCALHOST_ALIASES = new Set(["127.0.0.1", "0.0.0.0", "[::1]", "::1"]);

export function canonicalLocalUrl(location: Location): string | null {
  if (location.protocol !== "http:" || !LOCALHOST_ALIASES.has(location.hostname)) {
    return null;
  }

  const next = new URL(location.href);
  next.hostname = "localhost";
  return next.toString();
}
