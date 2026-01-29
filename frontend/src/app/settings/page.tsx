"use client";

import { useState } from "react";

import { fetchJson } from "../../lib/api";

export default function SettingsPage() {
  const [exporting, setExporting] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleExport = async (format: "csv" | "json") => {
    setExporting(true);
    try {
      const data = await fetchJson<{ url: string }>("/exports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ format }),
      });
      window.open(data.url, "_blank");
    } catch (error) {
      console.error(error);
      alert("Export failed.");
    } finally {
      setExporting(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Delete all local data? This cannot be undone.")) {
      return;
    }
    setDeleting(true);
    try {
      await fetchJson("/settings/delete-data", { method: "POST" });
      alert("All data deleted.");
    } catch (error) {
      console.error(error);
      alert("Delete failed.");
    } finally {
      setDeleting(false);
    }
  };

  return (
    <section className="grid">
      <div className="panel settings">
        <p className="tag">Settings</p>
        <h2>Privacy controls</h2>
        <p className="subtitle">
          Manage your data locally and remove everything at any time.
        </p>
        <div className="settings__actions">
          <button
            className="btn secondary"
            onClick={() => handleExport("json")}
            disabled={exporting}
          >
            {exporting ? "Exporting..." : "Export JSON"}
          </button>
          <button className="btn" onClick={handleDelete} disabled={deleting}>
            {deleting ? "Deleting..." : "Delete all data"}
          </button>
        </div>
      </div>
      <div className="panel settings__info">
        <h3>Connected inbox</h3>
        <p>Gmail · last scan 2 minutes ago</p>
        <p className="subtitle">
          Tokens are encrypted at rest and never leave this machine.
        </p>
      </div>
    </section>
  );
}
