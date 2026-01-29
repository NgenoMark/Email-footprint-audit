"use client";

import { useState } from "react";

import { fetchJson } from "../lib/api";

export default function ConnectButton() {
  const [loading, setLoading] = useState(false);

  const handleConnect = async () => {
    setLoading(true);
    try {
      const data = await fetchJson<{ url: string }>("/auth/gmail/start");
      window.location.href = data.url;
    } catch (error) {
      console.error(error);
      alert("Failed to start Gmail OAuth.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button className="btn" onClick={handleConnect} disabled={loading}>
      {loading ? "Connecting..." : "Connect Gmail"}
      <span aria-hidden>→</span>
    </button>
  );
}
