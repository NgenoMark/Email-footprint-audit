"use client";

import { useState } from "react";

import { fetchJson } from "../lib/api";

export default function RebuildButton() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleRebuild = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await fetchJson("/services/rebuild", { method: "POST" });
      setSuccess("Services rebuilt.");
    } catch (error) {
      console.error(error);
      setError("Rebuild failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid">
      <button className="btn secondary" onClick={handleRebuild} disabled={loading}>
        {loading ? "Rebuilding..." : "Rebuild services"}
      </button>
      {success ? <p className="subtitle">{success}</p> : null}
      {error ? <p className="subtitle">{error}</p> : null}
    </div>
  );
}
