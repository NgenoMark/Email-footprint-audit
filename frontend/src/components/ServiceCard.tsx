type ServiceCardProps = {
  name: string;
  domain: string;
  confidence: "high" | "medium" | "low";
  evidenceCount: number;
};

export default function ServiceCard({
  name,
  domain,
  confidence,
  evidenceCount,
}: ServiceCardProps) {
  return (
    <div className="service-card panel">
      <div>
        <p className="service-card__label">{domain}</p>
        <h3>{name}</h3>
      </div>
      <div className="service-card__meta">
        <span className={`badge ${confidence}`}>{confidence}</span>
        <span>{evidenceCount} signals</span>
      </div>
    </div>
  );
}
