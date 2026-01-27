type ConfidenceBadgeProps = {
  level: "high" | "medium" | "low";
};

export default function ConfidenceBadge({ level }: ConfidenceBadgeProps) {
  return <span className={`badge ${level}`}>{level} confidence</span>;
}
