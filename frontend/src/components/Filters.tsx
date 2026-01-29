"use client";

import { useState } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

import { fetchJson } from "../lib/api";

type FiltersProps = {
  confidence?: string;
  category?: string;
};

export default function Filters({ confidence, category }: FiltersProps) {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const updateParam = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    const next = params.toString();
    router.push(next ? `${pathname}?${next}` : pathname);
  };

  const handleExport = async () => {
    setLoading(true);
    try {
      const data = await fetchJson<{ url: string }>("/exports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ format: "csv" }),
      });
      window.open(data.url, "_blank");
    } catch (error) {
      console.error(error);
      alert("Export failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="filters panel">
      <div>
        <label>Confidence</label>
        <select
          value={confidence || ""}
          onChange={(event) => updateParam("confidence", event.target.value)}
        >
          <option value="">All</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>
      <div>
        <label>Category</label>
        <select
          value={category || ""}
          onChange={(event) => updateParam("category", event.target.value)}
        >
          <option value="">All</option>
          <option value="streaming">Streaming</option>
          <option value="newsletters">Newsletters</option>
          <option value="finance">Finance</option>
          <option value="developer">Developer</option>
          <option value="productivity">Productivity</option>
          <option value="gaming">Gaming</option>
          <option value="education">Education</option>
        </select>
      </div>
      <button className="btn secondary" onClick={handleExport} disabled={loading}>
        {loading ? "Exporting..." : "Export CSV"}
      </button>
    </div>
  );
}
