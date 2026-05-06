export interface Job {
  id: string;
  title: string;
  company: string;
  location: string | null;
  url: string;
  source: string;
  match_score: number | null;
  is_match: boolean;
  experience_level: string | null;
  employment_type: string | null;
  required_skills: string[];
  preferred_skills: string[];
  match_reasons: string[];
}

export type ApplicationStatus =
  | "detected"
  | "matched"
  | "outreach_sent"
  | "applied"
  | "interviewing"
  | "offer"
  | "rejected"
  | "ghosted";

export interface Application {
  id: string;
  job_id: string;
  status: ApplicationStatus;
  applied_at: string | null;
  last_followup_at: string | null;
  next_followup_at: string | null;
  followup_count: number;
  notion_page_id: string | null;
  notes: string | null;
  timeline: Array<{ event: string; at: string }>;
  created_at: string;
  updated_at: string;
}

export interface Recruiter {
  id: string;
  job_id: string | null;
  name: string | null;
  title: string | null;
  company: string;
  email: string | null;
  linkedin_url: string | null;
  email_verified: boolean;
  email_confidence: number;
  source: string | null;
}

export interface OutreachMessage {
  id: string;
  job_id: string;
  recruiter_id: string | null;
  channel: string;
  subject: string | null;
  body: string;
  sent: boolean;
  sent_at: string | null;
  opened: boolean;
  opened_at: string | null;
}

export interface Funnel {
  detected: number;
  matched: number;
  outreach_sent: number;
  applied: number;
  interviewing: number;
  offer: number;
  rejected: number;
  ghosted: number;
}

export interface AnalyticsSummary {
  funnel: Funnel;
  rates: {
    total_applied: number;
    total_responded: number;
    response_rate: number;
    emails_sent: number;
    emails_opened: number;
    email_open_rate: number;
  };
  top_matched_companies: Array<{ company: string; avg_score: number; job_count: number }>;
  generated_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
}

export interface MatchingRules {
  required_skills: string[];
  preferred_skills: string[];
  blocked_companies: string[];
  blocked_keywords: string[];
  min_match_score: number;
  target_levels: string[];
  target_employment: string[];
}
