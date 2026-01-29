export type ServiceListItem = {
  id: string;
  display_name: string;
  primary_domain: string;
  category: string | null;
  confidence: "high" | "medium" | "low";
  confidence_reason: string;
  first_seen_at: string | null;
  last_seen_at: string | null;
  evidence_count: number;
};

export type ServiceListResponse = {
  items: ServiceListItem[];
  total: number;
  page: number;
  page_size: number;
};

export type ServiceEvidenceItem = {
  id: string;
  from_address: string;
  subject: string;
  sent_at: string;
  evidence_type: string;
  match_reason: string;
};

export type ServiceDetailResponse = {
  id: string;
  display_name: string;
  primary_domain: string;
  category: string | null;
  confidence: "high" | "medium" | "low";
  confidence_reason: string;
  first_seen_at: string | null;
  last_seen_at: string | null;
  evidence: ServiceEvidenceItem[];
};

export type EvidenceItem = {
  id: string;
  from_address: string;
  from_domain: string;
  subject: string;
  sent_at: string;
  evidence_type: string;
  snippet: string | null;
};

export type EvidenceListResponse = {
  items: EvidenceItem[];
  total: number;
  page: number;
  page_size: number;
};

export type ScanItem = {
  id: string;
  status: string;
  query: string;
  started_at: string | null;
  finished_at: string | null;
};

export type ScanListResponse = {
  items: ScanItem[];
};

export type ExportResponse = {
  url: string;
};

export type DomainMapItem = {
  domain: string;
  service_name: string;
  category: string;
};

export type DomainMapResponse = {
  items: DomainMapItem[];
};
