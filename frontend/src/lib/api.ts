import { DEFAULT_API_URL } from "./constants";

export function getApiBase(): string {
  return process.env.NEXT_PUBLIC_API_URL || DEFAULT_API_URL;
}

function joinUrl(base: string, path: string): string {
  if (base.endsWith("/") && path.startsWith("/")) {
    return base.slice(0, -1) + path;
  }
  if (!base.endsWith("/") && !path.startsWith("/")) {
    return `${base}/${path}`;
  }
  return base + path;
}

export async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const url = joinUrl(getApiBase(), path);
  const response = await fetch(url, {
    ...init,
    cache: "no-store",
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function resolveApiUrl(pathOrUrl: string): string {
  if (pathOrUrl.startsWith("http://") || pathOrUrl.startsWith("https://")) {
    return pathOrUrl;
  }
  return joinUrl(getApiBase(), pathOrUrl);
}
