"use client";

import { useEffect } from "react";
import { useSearchParams } from "next/navigation";

import ConnectButton from "../../components/ConnectButton";
import { setUserEmail } from "../../lib/api";

export default function ConnectPage() {
  const searchParams = useSearchParams();

  useEffect(() => {
    const email = searchParams.get("email");
    if (email) {
      setUserEmail(email);
    }
  }, [searchParams]);

  return (
    <section className="grid">
      <div className="panel connect">
        <p className="tag">Connect inbox</p>
        <h2>Secure Gmail access</h2>
        <p className="subtitle">
          We only read metadata needed to detect account creation signals. Your
          email content never leaves your machine.
        </p>
        <ConnectButton />
      </div>
      <div className="panel connect__steps">
        <h3>What happens next</h3>
        <ol>
          <li>Google consent screen opens.</li>
          <li>We scan for welcome, verify, and receipt emails.</li>
          <li>Services are deduplicated and scored.</li>
        </ol>
      </div>
    </section>
  );
}
