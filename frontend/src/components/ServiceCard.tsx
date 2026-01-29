type ServiceCardProps = {
  name: string;
  domain: string;
  confidence: "high" | "medium" | "low";
  evidenceCount: number;
  category?: string | null;
};

export default function ServiceCard({
  name,
  domain,
  confidence,
  evidenceCount,
  category,
}: ServiceCardProps) {
  return (
    <div className="service-card panel">
      <div className="service-card__header">
        <p className="service-card__label">{domain}</p>
        <h3>{name}</h3>
      </div>
      <div className="service-card__meta">
        <span className={`badge ${confidence}`}>{confidence}</span>
        {category ? <span className="chip">{category}</span> : null}
        <span>{evidenceCount} signals</span>
      </div>
    </div>
  );
}
