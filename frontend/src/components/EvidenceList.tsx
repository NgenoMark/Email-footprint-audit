export type EvidenceItem = {
  id: string;
  subject: string;
  from: string;
  date: string;
  type: string;
};

export default function EvidenceList({ items }: { items: EvidenceItem[] }) {
  return (
    <div className="evidence panel">
      <h3>Evidence</h3>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <div>
              <p className="evidence__subject">{item.subject}</p>
              <p className="evidence__meta">
                {item.from} · {item.date}
              </p>
            </div>
            <span className="chip">{item.type}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
