"use client";

import { useState } from "react";

import { fetchJson } from "../lib/api";

export default function ResumeScanButton({ scanId }: { scanId: string }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleResume = async () => {
    setLoading(true);
    setError(null);
    try {
      await fetchJson(`/scans/${scanId}/resume`, { method: "POST" });
    } catch (error) {
      console.error(error);
      setError("Resume failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button className="btn secondary" onClick={handleResume} disabled={loading}>
        {loading ? "Resuming..." : "Resume"}
      </button>
      {error ? <p className="subtitle">{error}</p> : null}
    </div>
  );
}
