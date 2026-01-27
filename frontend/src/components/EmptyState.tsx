export default function EmptyState({
  title,
  subtitle,
  action,
}: {
  title: string;
  subtitle: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="empty panel">
      <h3>{title}</h3>
      <p>{subtitle}</p>
      {action}
    </div>
  );
}
