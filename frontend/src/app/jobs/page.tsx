"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { jobsApi, recruitersApi, outreachApi } from "@/lib/api";
import type { Job } from "@/lib/types";
import { ExternalLink, Zap, Search, Mail, Users } from "lucide-react";
import clsx from "clsx";

export default function JobsPage() {
  const qc = useQueryClient();
  const [filter, setFilter] = useState<"all" | "matched">("all");
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<Job | null>(null);

  const { data: jobs = [], isLoading } = useQuery({
    queryKey: ["jobs", filter],
    queryFn: () => jobsApi.list(filter === "matched" ? true : undefined),
  });

  const detect = useMutation({
    mutationFn: jobsApi.detect,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["jobs"] }),
  });

  const scrape = useMutation({
    mutationFn: ({ jobId, company, title }: { jobId: string; company: string; title: string }) =>
      recruitersApi.scrape(jobId, company, title),
  });

  const generate = useMutation({
    mutationFn: ({ jobId }: { jobId: string }) => outreachApi.generate(jobId),
  });

  const filtered = jobs.filter(
    (j) =>
      j.title.toLowerCase().includes(search.toLowerCase()) ||
      j.company.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Jobs</h1>
        <button
          onClick={() => detect.mutate()}
          disabled={detect.isPending}
          className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg disabled:opacity-50"
        >
          <Zap size={14} />
          {detect.isPending ? "Detecting..." : "Detect Now"}
        </button>
      </div>

      <div className="flex items-center gap-3">
        <div className="relative flex-1 max-w-xs">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input
            className="w-full pl-9 pr-3 py-2 bg-gray-900 border border-gray-800 rounded-lg text-sm text-gray-100 placeholder:text-gray-600 focus:outline-none focus:border-brand-500"
            placeholder="Search jobs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex gap-1 bg-gray-900 rounded-lg p-1 border border-gray-800">
          {(["all", "matched"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={clsx(
                "px-3 py-1 text-xs font-medium rounded transition-colors capitalize",
                filter === f ? "bg-brand-600 text-white" : "text-gray-400 hover:text-gray-100"
              )}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {isLoading ? (
        <p className="text-gray-500 text-sm">Loading...</p>
      ) : filtered.length === 0 ? (
        <p className="text-gray-500 text-sm">No jobs found. Click "Detect Now" to pull new listings.</p>
      ) : (
        <div className="space-y-2">
          {filtered.map((job) => (
            <div
              key={job.id}
              onClick={() => setSelected(selected?.id === job.id ? null : job)}
              className={clsx(
                "bg-gray-900 border rounded-xl p-4 cursor-pointer transition-colors",
                selected?.id === job.id ? "border-brand-500" : "border-gray-800 hover:border-gray-700"
              )}
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-medium text-white text-sm">{job.title}</p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {job.company} · {job.location ?? "Remote"} · {job.employment_type ?? "—"}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  {job.is_match && (
                    <span className="px-2 py-0.5 bg-green-900/40 text-green-400 text-xs rounded-full font-medium">
                      {((job.match_score ?? 0) * 100).toFixed(0)}% match
                    </span>
                  )}
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="text-gray-500 hover:text-gray-300"
                  >
                    <ExternalLink size={14} />
                  </a>
                </div>
              </div>

              {selected?.id === job.id && (
                <div className="mt-4 space-y-3">
                  {job.required_skills.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Required Skills</p>
                      <div className="flex flex-wrap gap-1">
                        {job.required_skills.map((s) => (
                          <span key={s} className="px-2 py-0.5 bg-gray-800 text-gray-300 text-xs rounded">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {job.match_reasons.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Match Reasons</p>
                      {job.match_reasons.map((r, i) => (
                        <p key={i} className="text-xs text-gray-400">• {r}</p>
                      ))}
                    </div>
                  )}
                  <div className="flex gap-2 pt-1">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        scrape.mutate({ jobId: job.id, company: job.company, title: job.title });
                      }}
                      disabled={scrape.isPending}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-700 hover:bg-gray-600 text-xs text-white rounded-lg disabled:opacity-50"
                    >
                      <Users size={12} /> Find Recruiters
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        generate.mutate({ jobId: job.id });
                      }}
                      disabled={generate.isPending}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-brand-600 hover:bg-brand-700 text-xs text-white rounded-lg disabled:opacity-50"
                    >
                      <Mail size={12} /> Generate Outreach
                    </button>
                  </div>
                  {generate.isSuccess && (
                    <p className="text-xs text-green-400">Outreach generated. Check Applications.</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
