import EmptyState from "../../components/EmptyState";
import Filters from "../../components/Filters";
import ServiceCard from "../../components/ServiceCard";
import { fetchJson } from "../../lib/api";
import type {
  EvidenceListResponse,
  ScanListResponse,
  ServiceListResponse,
} from "../../types/api";

type DashboardProps = {
  searchParams?: {
    confidence?: string;
    category?: string;
  };
};

export default async function DashboardPage({ searchParams }: DashboardProps) {
  const confidence = searchParams?.confidence || "";
  const category = searchParams?.category || "";
  const query = new URLSearchParams();
  if (confidence) {
    query.set("confidence", confidence);
  }
  if (category) {
    query.set("category", category);
  }
  const servicesPath = query.toString() ? `/services?${query}` : "/services";

  const [servicesData, scansData, evidenceData] = await Promise.all([
    fetchJson<ServiceListResponse>(servicesPath),
    fetchJson<ScanListResponse>("/scans"),
    fetchJson<EvidenceListResponse>("/evidence"),
  ]);
  const services = servicesData.items;
  const lastScan = scansData.items[0];
  const highCount = services.filter((svc) => svc.confidence === "high").length;
  const grouped = services.reduce<Record<string, typeof services>>((acc, svc) => {
    const key = svc.category || "uncategorized";
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(svc);
    return acc;
  }, {});

  return (
    <section className="grid">
      <div className="panel dashboard__summary">
        <div>
          <p className="tag">Scan summary</p>
          <h2>{services.length} services discovered</h2>
          <p className="subtitle">
            {lastScan
              ? `Last scan ${new Date(lastScan.started_at || "").toLocaleString()} · ${highCount} high confidence services detected.`
              : "No scans yet. Run a scan to discover services."}
          </p>
        </div>
        <button className="btn secondary">Review changes</button>
      </div>

      <Filters confidence={confidence} category={category} />

      <div className="grid two">
        <div className="panel dashboard__history">
          <h3>Recent scans</h3>
          {scansData.items.length === 0 ? (
            <p className="subtitle">No scans yet.</p>
          ) : (
            <ul>
              {scansData.items.slice(0, 5).map((scan) => (
                <li key={scan.id}>
                  <strong>{scan.status}</strong>
                  <span>
                    {scan.started_at
                      ? new Date(scan.started_at).toLocaleString()
                      : "unknown"}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="panel dashboard__history">
          <h3>Recent evidence</h3>
          {evidenceData.items.length === 0 ? (
            <p className="subtitle">No evidence yet.</p>
          ) : (
            <ul>
              {evidenceData.items.slice(0, 5).map((item) => (
                <li key={item.id}>
                  <strong>{item.subject}</strong>
                  <span>
                    {new Date(item.sent_at).toLocaleDateString()} · {item.from_domain}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {services.length === 0 ? (
        <EmptyState
          title="No services yet"
          subtitle="Run your first scan to populate the dashboard."
        />
      ) : (
        <div className="category-groups">
          {Object.entries(grouped).map(([categoryName, items]) => (
            <details key={categoryName} className="category-group" open>
              <summary>
                <div>
                  <h3>{categoryName}</h3>
                  <p className="subtitle">{items.length} services</p>
                </div>
                <span className="chip">toggle</span>
              </summary>
              <div className="services-grid">
                {items.map((service) => (
                  <a key={service.id} href={`/services/${service.id}`}>
                    <ServiceCard
                      name={service.display_name}
                      domain={service.primary_domain}
                      confidence={service.confidence}
                      evidenceCount={service.evidence_count}
                      category={service.category}
                    />
                  </a>
                ))}
              </div>
            </details>
          ))}
        </div>
      )}
    </section>
  );
}
