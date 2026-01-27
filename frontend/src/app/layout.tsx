import "../styles/globals.css";
import "../styles/theme.css";

import AppShell from "../components/AppShell";

export const metadata = {
  title: "Email Footprint Audit",
  description: "Discover services linked to your email with evidence and confidence.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
