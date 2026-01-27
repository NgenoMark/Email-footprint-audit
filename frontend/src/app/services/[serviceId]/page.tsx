import ConfidenceBadge from "../../../components/ConfidenceBadge";
import EvidenceList from "../../../components/EvidenceList";

const evidenceItems = [
  {
    id: "1",
    subject: "Welcome to OPSWAT Academy!",
    from: "noreply@opswatacademy.com",
    date: "Jan 24, 2026",
    type: "welcome",
  },
  {
    id: "2",
    subject: "Verify your email",
    from: "security@opswatacademy.com",
    date: "Jan 24, 2026",
    type: "verify",
  },
];

export default function ServiceDetailPage({
  params,
}: {
  params: { serviceId: string };
}) {
  return (
    <section className="grid">
      <div className="panel service-detail">
        <p className="tag">Service</p>
        <h2>{params.serviceId}</h2>
        <p className="subtitle">
          Detected from official domain and verified emails.
        </p>
        <div className="service-detail__meta">
          <ConfidenceBadge level="high" />
          <span className="chip">First seen Jan 24, 2026</span>
          <span className="chip">4 evidence emails</span>
        </div>
      </div>
      <EvidenceList items={evidenceItems} />
    </section>
  );
}
