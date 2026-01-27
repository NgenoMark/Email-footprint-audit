export default function Topbar() {
  return (
    <div className="topbar panel">
      <div>
        <p className="tag">Security / Audit</p>
        <h2 className="title">Your Email Footprint</h2>
      </div>
      <div className="topbar__actions">
        <input className="topbar__search" placeholder="Search services..." />
        <button className="btn">Run Scan</button>
      </div>
    </div>
  );
}
