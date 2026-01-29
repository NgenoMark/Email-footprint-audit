"use client";

import { useEffect, useState } from "react";

import { fetchJson, resolveApiUrl } from "../../lib/api";
import type { DomainMapResponse } from "../../types/api";

export default function SettingsPage() {
  const [exporting, setExporting] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [format, setFormat] = useState<"csv" | "json">("csv");
  const [lastExportUrl, setLastExportUrl] = useState<string | null>(null);
  const [domain, setDomain] = useState("");
  const [serviceName, setServiceName] = useState("");
  const [category, setCategory] = useState("");
  const [overrides, setOverrides] = useState<DomainMapResponse["items"]>([]);

  const handleExport = async () => {
    setExporting(true);
    try {
      const data = await fetchJson<{ url: string }>("/exports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ format }),
      });
      setLastExportUrl(resolveApiUrl(data.url));
      window.open(resolveApiUrl(data.url), "_blank");
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

  const loadOverrides = async () => {
    try {
      const data = await fetchJson<DomainMapResponse>("/domain-map");
      setOverrides(data.items);
    } catch (error) {
      console.error(error);
    }
  };

  const handleOverrideSave = async () => {
    if (!domain || !serviceName) {
      alert("Domain and service name are required.");
      return;
    }
    try {
      await fetchJson("/domain-map", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          domain,
          service_name: serviceName,
          category: category || null,
        }),
      });
      setDomain("");
      setServiceName("");
      setCategory("");
      loadOverrides();
    } catch (error) {
      console.error(error);
      alert("Failed to save mapping.");
    }
  };

  useEffect(() => {
    loadOverrides();
  }, []);

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
            onClick={handleExport}
            disabled={exporting}
          >
            {exporting ? "Exporting..." : `Export ${format.toUpperCase()}`}
          </button>
          <select
            value={format}
            onChange={(event) => setFormat(event.target.value as "csv" | "json")}
          >
            <option value="csv">CSV</option>
            <option value="json">JSON</option>
          </select>
          <button className="btn" onClick={handleDelete} disabled={deleting}>
            {deleting ? "Deleting..." : "Delete all data"}
          </button>
        </div>
        {lastExportUrl ? (
          <div className="settings__export">
            <p className="subtitle">Last export:</p>
            <a href={lastExportUrl} className="chip">
              {lastExportUrl}
            </a>
          </div>
        ) : null}
      </div>
      <div className="panel settings__info">
        <h3>Connected inbox</h3>
        <p>Gmail · last scan 2 minutes ago</p>
        <p className="subtitle">
          Tokens are encrypted at rest and never leave this machine.
        </p>
      </div>
      <div className="panel settings__map">
        <h3>Domain map overrides</h3>
        <p className="subtitle">
          Add or fix service mappings without editing CSV files.
        </p>
        <div className="settings__map-form">
          <input
            placeholder="domain.com"
            value={domain}
            onChange={(event) => setDomain(event.target.value)}
          />
          <input
            placeholder="Service name"
            value={serviceName}
            onChange={(event) => setServiceName(event.target.value)}
          />
          <input
            placeholder="Category"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
          />
          <button className="btn secondary" onClick={handleOverrideSave}>
            Save mapping
          </button>
        </div>
        {overrides.length === 0 ? (
          <p className="subtitle">No overrides yet.</p>
        ) : (
          <ul className="settings__map-list">
            {overrides.map((item) => (
              <li key={item.domain}>
                <strong>{item.domain}</strong>
                <span>{item.service_name}</span>
                <span className="chip">{item.category || "uncategorized"}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
