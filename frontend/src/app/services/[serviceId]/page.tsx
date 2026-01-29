import ConfidenceBadge from "../../../components/ConfidenceBadge";
import EvidenceList, { EvidenceItem } from "../../../components/EvidenceList";
import { fetchJson } from "../../../lib/api";
import type { ServiceDetailResponse } from "../../../types/api";

export default async function ServiceDetailPage({
  params,
}: {
  params: { serviceId: string };
}) {
  const service = await fetchJson<ServiceDetailResponse>(
    `/services/${params.serviceId}`
  );
  const evidenceItems: EvidenceItem[] = service.evidence.map((item) => ({
    id: item.id,
    subject: item.subject,
    from: item.from_address,
    date: new Date(item.sent_at).toLocaleString(),
    type: item.evidence_type,
  }));
  return (
    <section className="grid">
      <div className="panel service-detail">
        <p className="tag">Service</p>
        <h2>{service.display_name}</h2>
        <p className="subtitle">
          {service.confidence_reason}
        </p>
        <div className="service-detail__meta">
          <ConfidenceBadge level={service.confidence} />
          <span className="chip">
            First seen{" "}
            {service.first_seen_at
              ? new Date(service.first_seen_at).toLocaleDateString()
              : "unknown"}
          </span>
          <span className="chip">{service.evidence.length} evidence emails</span>
        </div>
      </div>
      <EvidenceList items={evidenceItems} />
    </section>
  );
}
