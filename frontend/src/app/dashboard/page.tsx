import Filters from "../../components/Filters";
import ServiceCard from "../../components/ServiceCard";

const services = [
  { name: "OPSWAT Academy", domain: "opswatacademy.com", confidence: "high", evidenceCount: 4 },
  { name: "Substack", domain: "substack.com", confidence: "medium", evidenceCount: 2 },
  { name: "Activision", domain: "activision.com", confidence: "medium", evidenceCount: 3 },
  { name: "GitHub", domain: "github.com", confidence: "high", evidenceCount: 7 },
  { name: "Notion", domain: "notion.so", confidence: "low", evidenceCount: 1 },
  { name: "Stripe", domain: "stripe.com", confidence: "high", evidenceCount: 4 },
];

export default function DashboardPage() {
  return (
    <section className="grid">
      <div className="panel dashboard__summary">
        <div>
          <p className="tag">Scan summary</p>
          <h2>142 services discovered</h2>
          <p className="subtitle">
            Last scan 2 minutes ago. 39 high confidence services detected.
          </p>
        </div>
        <button className="btn secondary">Review changes</button>
      </div>

      <Filters />

      <div className="grid three">
        {services.map((service) => (
          <a key={service.domain} href={`/services/${service.domain}`}>
            <ServiceCard {...service} />
          </a>
        ))}
      </div>
    </section>
  );
}
