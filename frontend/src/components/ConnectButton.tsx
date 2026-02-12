"use client";

import { useState } from "react";

import { fetchJson } from "../lib/api";

export default function ConnectButton() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleConnect = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchJson<{ url: string }>("/auth/gmail/start");
      window.location.href = data.url;
    } catch (err) {
      console.error(err);
      setError("Failed to start Gmail OAuth.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid">
      <button className="btn" onClick={handleConnect} disabled={loading}>
        {loading ? "Connecting..." : "Connect Gmail"}
        <span aria-hidden>{"->"}</span>
      </button>
      {error ? <p className="subtitle">{error}</p> : null}
    </div>
  );
}
