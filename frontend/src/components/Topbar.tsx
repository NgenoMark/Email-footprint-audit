"use client";

import { useState } from "react";

import { fetchJson } from "../lib/api";

const defaultQuery =
  'subject:(welcome OR verify OR "confirm your email" OR "password reset" OR receipt OR invoice OR security OR login OR "new login" OR "verification code" OR "one-time" OR "two-factor" OR account)';

export default function Topbar() {
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState(defaultQuery);
  const [search, setSearch] = useState("");

  const runScan = async () => {
    setLoading(true);
    try {
      await fetchJson("/scans", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider: "gmail", query }),
      });
      alert("Scan started.");
    } catch (error) {
      console.error(error);
      alert("Failed to start scan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="topbar panel">
      <div>
        <p className="tag">Security / Audit</p>
        <h2 className="title">Your Email Footprint</h2>
      </div>
      <div className="topbar__actions">
        <input
          className="topbar__search"
          placeholder="Search services..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <input
          className="topbar__search"
          placeholder="Scan query..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <a
          className="btn secondary"
          href={search ? `/dashboard?q=${encodeURIComponent(search)}` : "/dashboard"}
        >
          Search
        </a>
        <button className="btn" onClick={runScan} disabled={loading}>
          {loading ? "Scanning..." : "Run Scan"}
        </button>
      </div>
    </div>
  );
}
