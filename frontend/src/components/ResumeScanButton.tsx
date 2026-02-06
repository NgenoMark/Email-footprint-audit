"use client";

import { useState } from "react";

import { fetchJson } from "../lib/api";

export default function ResumeScanButton({ scanId }: { scanId: string }) {
  const [loading, setLoading] = useState(false);

  const handleResume = async () => {
    setLoading(true);
    try {
      await fetchJson(`/scans/${scanId}/resume`, { method: "POST" });
    } catch (error) {
      console.error(error);
      alert("Resume failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button className="btn secondary" onClick={handleResume} disabled={loading}>
      {loading ? "Resuming..." : "Resume"}
    </button>
  );
}
