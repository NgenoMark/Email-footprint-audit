const navItems = [
  { label: "Overview", href: "/" },
  { label: "Dashboard", href: "/dashboard" },
  { label: "Connect", href: "/connect" },
  { label: "Services", href: "/dashboard" },
  { label: "Settings", href: "/settings" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar panel">
      <div className="sidebar__brand">
        <span className="chip">Audit</span>
        <h1>Email Footprint</h1>
        <p>Personal account discovery</p>
      </div>
      <nav className="sidebar__nav">
        {navItems.map((item) => (
          <a key={item.label} href={item.href} className="sidebar__link">
            {item.label}
          </a>
        ))}
      </nav>
      <div className="sidebar__footer">
        <div className="chip">Local-first</div>
        <p>Encrypted tokens. Evidence only.</p>
      </div>
    </aside>
  );
}
