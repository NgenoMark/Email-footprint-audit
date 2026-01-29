"use client";

import { useState } from "react";

import { fetchJson } from "../lib/api";

export default function RebuildButton() {
  const [loading, setLoading] = useState(false);

  const handleRebuild = async () => {
    setLoading(true);
    try {
      await fetchJson("/services/rebuild", { method: "POST" });
      alert("Services rebuilt.");
    } catch (error) {
      console.error(error);
      alert("Rebuild failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button className="btn secondary" onClick={handleRebuild} disabled={loading}>
      {loading ? "Rebuilding..." : "Rebuild services"}
    </button>
  );
}
