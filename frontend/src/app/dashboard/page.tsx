import EmptyState from "../../components/EmptyState";
import Filters from "../../components/Filters";
import RebuildButton from "../../components/RebuildButton";
import ResumeScanButton from "../../components/ResumeScanButton";
import ServiceCard from "../../components/ServiceCard";
import { fetchJson } from "../../lib/api";
import type {
  EvidenceListResponse,
  ScanListResponse,
  ServiceListResponse,
} from "../../types/api";

type DashboardProps = {
  searchParams?: {
    q?: string;
    page?: string;
    confidence?: string;
    category?: string;
    scan_page?: string;
    evidence_page?: string;
  };
};

function buildDashboardUrl(params: {
  q?: string;
  confidence?: string;
  category?: string;
  page: number;
  scanPage: number;
  evidencePage: number;
}): string {
  const query = new URLSearchParams({
    page: String(params.page),
    scan_page: String(params.scanPage),
    evidence_page: String(params.evidencePage),
  });
  if (params.q) {
    query.set("q", params.q);
  }
  if (params.confidence) {
    query.set("confidence", params.confidence);
  }
  if (params.category) {
    query.set("category", params.category);
  }
  return `/dashboard?${query.toString()}`;
}

export default async function DashboardPage({ searchParams }: DashboardProps) {
  const confidence = searchParams?.confidence || "";
  const category = searchParams?.category || "";
  const search = searchParams?.q || "";
  const page = Number(searchParams?.page || 1);
  const scanPage = Number(searchParams?.scan_page || 1);
  const evidencePage = Number(searchParams?.evidence_page || 1);
  const pageSize = 24;
  const miniPageSize = 5;

  const query = new URLSearchParams();
  if (search) {
    query.set("q", search);
  }
  if (confidence) {
    query.set("confidence", confidence);
  }
  if (category) {
    query.set("category", category);
  }
  query.set("page", String(page));
  query.set("page_size", String(pageSize));
  const servicesPath = `/services?${query.toString()}`;

  const [servicesData, scansData, evidenceData] = await Promise.all([
    fetchJson<ServiceListResponse>(servicesPath),
    fetchJson<ScanListResponse>(`/scans?page=${scanPage}&page_size=${miniPageSize}`),
    fetchJson<EvidenceListResponse>(
      `/evidence?page=${evidencePage}&page_size=${miniPageSize}`
    ),
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
          <h2>{servicesData.total} services discovered</h2>
          <p className="subtitle">
            {lastScan
              ? `Last scan ${new Date(lastScan.started_at || "").toLocaleString()} - ${highCount} high confidence services detected.`
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
              {scansData.items.map((scan) => (
                <li key={scan.id}>
                  <strong>{scan.status}</strong>
                  <span>
                    {scan.started_at
                      ? new Date(scan.started_at).toLocaleString()
                      : "unknown"}
                  </span>
                  {scan.progress_pct != null ? (
                    <span>{Math.round(scan.progress_pct)}%</span>
                  ) : null}
                  {scan.status === "failed" && scan.id ? (
                    <ResumeScanButton scanId={scan.id} />
                  ) : null}
                </li>
              ))}
            </ul>
          )}
          <div className="pagination compact">
            <a
              className={`btn secondary ${scanPage <= 1 ? "disabled" : ""}`}
              href={
                scanPage > 1
                  ? buildDashboardUrl({
                      q: search,
                      confidence,
                      category,
                      page,
                      scanPage: scanPage - 1,
                      evidencePage,
                    })
                  : "#"
              }
            >
              Prev
            </a>
            <span className="chip">
              {scansData.page}/{Math.max(1, Math.ceil(scansData.total / scansData.page_size))}
            </span>
            <a
              className={`btn secondary ${
                scansData.page * scansData.page_size >= scansData.total ? "disabled" : ""
              }`}
              href={
                scansData.page * scansData.page_size < scansData.total
                  ? buildDashboardUrl({
                      q: search,
                      confidence,
                      category,
                      page,
                      scanPage: scanPage + 1,
                      evidencePage,
                    })
                  : "#"
              }
            >
              Next
            </a>
          </div>
        </div>

        <div className="panel dashboard__history">
          <h3>Recent evidence</h3>
          {evidenceData.items.length === 0 ? (
            <p className="subtitle">No evidence yet.</p>
          ) : (
            <ul>
              {evidenceData.items.map((item) => (
                <li key={item.id}>
                  <strong>{item.subject}</strong>
                  <span>
                    {new Date(item.sent_at).toLocaleDateString()} - {item.from_domain}
                  </span>
                </li>
              ))}
            </ul>
          )}
          <div className="pagination compact">
            <a
              className={`btn secondary ${evidencePage <= 1 ? "disabled" : ""}`}
              href={
                evidencePage > 1
                  ? buildDashboardUrl({
                      q: search,
                      confidence,
                      category,
                      page,
                      scanPage,
                      evidencePage: evidencePage - 1,
                    })
                  : "#"
              }
            >
              Prev
            </a>
            <span className="chip">
              {evidenceData.page}/{Math.max(1, Math.ceil(evidenceData.total / evidenceData.page_size))}
            </span>
            <a
              className={`btn secondary ${
                evidenceData.page * evidenceData.page_size >= evidenceData.total
                  ? "disabled"
                  : ""
              }`}
              href={
                evidenceData.page * evidenceData.page_size < evidenceData.total
                  ? buildDashboardUrl({
                      q: search,
                      confidence,
                      category,
                      page,
                      scanPage,
                      evidencePage: evidencePage + 1,
                    })
                  : "#"
              }
            >
              Next
            </a>
          </div>
        </div>

        <div className="panel dashboard__history">
          <h3>Maintenance</h3>
          <p className="subtitle">
            If you update the domain map, rebuild services to merge duplicates.
          </p>
          <RebuildButton />
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
          <div className="pagination">
            <a
              className={`btn secondary ${page <= 1 ? "disabled" : ""}`}
              href={
                page > 1
                  ? buildDashboardUrl({
                      q: search,
                      confidence,
                      category,
                      page: page - 1,
                      scanPage,
                      evidencePage,
                    })
                  : "#"
              }
            >
              Previous
            </a>
            <span className="chip">
              Page {servicesData.page} of{" "}
              {Math.max(1, Math.ceil(servicesData.total / servicesData.page_size))}
            </span>
            <a
              className={`btn secondary ${
                servicesData.page * servicesData.page_size >= servicesData.total
                  ? "disabled"
                  : ""
              }`}
              href={
                servicesData.page * servicesData.page_size < servicesData.total
                  ? buildDashboardUrl({
                      q: search,
                      confidence,
                      category,
                      page: page + 1,
                      scanPage,
                      evidencePage,
                    })
                  : "#"
              }
            >
              Next
            </a>
          </div>
        </div>
      )}
    </section>
  );
}
