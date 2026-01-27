import ConnectButton from "../components/ConnectButton";

export default function Home() {
  return (
    <div className="hero panel">
      <p className="tag">Email Footprint Audit</p>
      <h1 className="title">Find every service your email touched.</h1>
      <p className="subtitle">
        A privacy-first audit that scans your inbox for account signals and
        turns them into a clean, evidence-backed service list.
      </p>
      <div className="hero__actions">
        <ConnectButton />
        <a className="btn secondary" href="/dashboard">
          View dashboard
        </a>
      </div>
      <div className="hero__stats">
        <div>
          <h3>200+</h3>
          <p>Possible services</p>
        </div>
        <div>
          <h3>High</h3>
          <p>Confidence scoring</p>
        </div>
        <div>
          <h3>Local</h3>
          <p>Runs on your machine</p>
        </div>
      </div>
    </div>
  );
}
