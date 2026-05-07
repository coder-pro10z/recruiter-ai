import axios from "axios";
import type {
  ApiResponse,
  Job,
  Application,
  Recruiter,
  OutreachMessage,
  AnalyticsSummary,
  MatchingRules,
} from "./types";

const client = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000"}/api/v1`,
  timeout: 30_000,
});

async function get<T>(path: string): Promise<T> {
  const { data } = await client.get<ApiResponse<T>>(path);
  if (!data.success) throw new Error(data.error ?? "Unknown error");
  return data.data as T;
}

async function post<T>(path: string, body?: unknown): Promise<T> {
  const { data } = await client.post<ApiResponse<T>>(path, body);
  if (!data.success) throw new Error(data.error ?? "Unknown error");
  return data.data as T;
}

async function patch<T>(path: string, body?: unknown): Promise<T> {
  const { data } = await client.patch<ApiResponse<T>>(path, body);
  if (!data.success) throw new Error(data.error ?? "Unknown error");
  return data.data as T;
}

async function put<T>(path: string, body?: unknown): Promise<T> {
  const { data } = await client.put<ApiResponse<T>>(path, body);
  if (!data.success) throw new Error(data.error ?? "Unknown error");
  return data.data as T;
}

// Jobs
export const jobsApi = {
  list: (isMatch?: boolean) =>
    get<Job[]>(`/jobs${isMatch !== undefined ? `?is_match=${isMatch}` : ""}`),
  get: (id: string) => get<Job>(`/jobs/${id}`),
  detect: () => post<{ detected: number }>("/jobs/detect"),
  delete: (id: string) => client.delete(`/jobs/${id}`),
};

// Applications
export const applicationsApi = {
  list: (status?: string) =>
    get<Application[]>(`/applications${status ? `?status=${status}` : ""}`),
  get: (id: string) => get<Application>(`/applications/${id}`),
  updateStatus: (id: string, status: string, notes?: string) =>
    patch<Application>(`/applications/${id}/status`, { status, notes }),
  triggerFollowups: () => post<{ sent_count: number }>("/applications/trigger-followups"),
};

// Recruiters
export const recruitersApi = {
  list: (jobId?: string) =>
    get<Recruiter[]>(`/recruiters${jobId ? `?job_id=${jobId}` : ""}`),
  scrape: (jobId: string, company: string, jobTitle: string) =>
    post<{ found: number }>("/recruiters/scrape", {
      job_id: jobId,
      company,
      job_title: jobTitle,
    }),
};

// Outreach
export const outreachApi = {
  list: (jobId?: string) =>
    get<OutreachMessage[]>(`/outreach${jobId ? `?job_id=${jobId}` : ""}`),
  generate: (jobId: string, recruiterId?: string, myName?: string) =>
    post<OutreachMessage>("/outreach/generate", {
      job_id: jobId,
      recruiter_id: recruiterId,
      my_name: myName ?? "Your Name",
    }),
  send: (outreachId: string) =>
    post<{ sent: boolean; gmail_message_id: string | null }>(`/outreach/send/${outreachId}`),
};

// Analytics
export const analyticsApi = {
  summary: () => get<AnalyticsSummary>("/analytics/summary"),
  funnel: () => get<Record<string, number>>("/analytics/funnel"),
};

// Settings
export const settingsApi = {
  getRules: () => get<MatchingRules>("/settings/rules"),
  updateRules: (rules: Partial<MatchingRules>) => patch<MatchingRules>("/settings/rules", rules),
  getFeeds: () => get<{ feeds: string[] }>("/settings/feeds"),
  updateFeeds: (feeds: string[]) => put<{ feeds: string[] }>("/settings/feeds", { feeds }),
  getProfiles: () => get<Array<{id: string, name: string, is_active: boolean}>>("/settings/profiles"),
  createProfile: (profile: any) => post<{id: string, name: string}>("/settings/profiles", profile),
  activateProfile: (id: string) => put<{active_profile_id: string}>(`/settings/profiles/${id}/activate`),
};
