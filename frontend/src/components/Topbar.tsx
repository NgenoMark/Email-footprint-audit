"use client";

import { useEffect, useState } from "react";

import { fetchJson } from "../lib/api";
import type { QueueHealthResponse, ScanListResponse } from "../types/api";

const defaultQuery =
  'subject:(welcome OR verify OR "confirm your email" OR "password reset" OR receipt OR invoice OR security OR login OR "new login" OR "verification code" OR "one-time" OR "two-factor" OR account)';

export default function Topbar() {
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState(defaultQuery);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [queueInfo, setQueueInfo] = useState<string | null>(null);

  const runScan = async () => {
    setLoading(true);
    setStatus("Starting scan...");
    try {
      await fetchJson("/scans", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider: "gmail", query }),
      });
      setStatus("Scan queued. It will update shortly.");
    } catch (error) {
      console.error(error);
      setStatus("Failed to start scan.");
    } finally {
      setLoading(false);
    }
  };

  const pollScans = async () => {
    try {
      const [data, queue] = await Promise.all([
        fetchJson<ScanListResponse>("/scans"),
        fetchJson<QueueHealthResponse>("/queue/health"),
      ]);
      const latest = data.items[0];
      if (queue.use_rq) {
        if (queue.healthy) {
          setQueueInfo(`Queue depth: ${queue.queue_depth}`);
        } else {
          setQueueInfo("Queue unavailable");
        }
      } else {
        setQueueInfo("Inline background mode");
      }
      if (!latest) {
        setStatus(null);
        return;
      }
      if (latest.status === "running") {
        const pct =
          latest.progress_pct != null ? ` ${latest.progress_pct.toFixed(0)}%` : "";
        setStatus(`Scan running${pct}...`);
      } else if (latest.status === "success") {
        setStatus("Scan complete.");
      } else if (latest.status === "failed") {
        setStatus("Scan failed.");
      } else if (latest.status === "queued") {
        setStatus("Scan queued.");
      }
    } catch (error) {
      console.error(error);
      setQueueInfo("Queue status unavailable");
    }
  };

  useEffect(() => {
    pollScans();
    const id = setInterval(pollScans, 5000);
    return () => clearInterval(id);
  }, []);

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
      <div>
        {status ? <p className="topbar__status">{status}</p> : null}
        {queueInfo ? <p className="topbar__status">{queueInfo}</p> : null}
      </div>
    </div>
  );
}
