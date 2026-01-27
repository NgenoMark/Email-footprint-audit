export default function SettingsPage() {
  return (
    <section className="grid">
      <div className="panel settings">
        <p className="tag">Settings</p>
        <h2>Privacy controls</h2>
        <p className="subtitle">
          Manage your data locally and remove everything at any time.
        </p>
        <div className="settings__actions">
          <button className="btn secondary">Export JSON</button>
          <button className="btn">Delete all data</button>
        </div>
      </div>
      <div className="panel settings__info">
        <h3>Connected inbox</h3>
        <p>Gmail · last scan 2 minutes ago</p>
        <p className="subtitle">
          Tokens are encrypted at rest and never leave this machine.
        </p>
      </div>
    </section>
  );
}
