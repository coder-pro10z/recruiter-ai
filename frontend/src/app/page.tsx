"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { jobsApi, applicationsApi, analyticsApi } from "@/lib/api";
import { Briefcase, Send, BarChart2, RefreshCw, Zap } from "lucide-react";

export default function Dashboard() {
  const qc = useQueryClient();
  const { data: summary } = useQuery({ queryKey: ["analytics-summary"], queryFn: analyticsApi.summary });
  const { data: jobs } = useQuery({ queryKey: ["jobs"], queryFn: () => jobsApi.list() });
  const { data: matchedJobs } = useQuery({ queryKey: ["jobs-matched"], queryFn: () => jobsApi.list(true) });

  const detect = useMutation({
    mutationFn: jobsApi.detect,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["jobs"] }),
  });
  const followup = useMutation({
    mutationFn: applicationsApi.triggerFollowups,
  });

  const funnel = summary?.funnel;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 text-sm mt-1">AI-powered job hunting overview</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => detect.mutate()}
            disabled={detect.isPending}
            className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <Zap size={14} />
            {detect.isPending ? "Detecting..." : "Detect Jobs"}
          </button>
          <button
            onClick={() => followup.mutate()}
            disabled={followup.isPending}
            className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <Send size={14} />
            Run Follow-ups
          </button>
        </div>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total Jobs", value: jobs?.length ?? 0, icon: Briefcase, color: "text-blue-400" },
          { label: "Matched", value: matchedJobs?.length ?? 0, icon: Zap, color: "text-green-400" },
          { label: "Applied", value: funnel?.applied ?? 0, icon: Send, color: "text-yellow-400" },
          { label: "Interviews", value: funnel?.interviewing ?? 0, icon: BarChart2, color: "text-purple-400" },
        ].map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="bg-gray-900 rounded-xl p-4 border border-gray-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400 text-sm">{label}</span>
              <Icon size={16} className={color} />
            </div>
            <p className="text-2xl font-bold text-white">{value}</p>
          </div>
        ))}
      </div>

      {/* Funnel */}
      {funnel && (
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Application Funnel</h2>
          <div className="grid grid-cols-8 gap-2">
            {Object.entries(funnel).map(([stage, count]) => (
              <div key={stage} className="text-center">
                <p className="text-xl font-bold text-white">{count}</p>
                <p className="text-xs text-gray-500 mt-1 capitalize">{stage.replace("_", " ")}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent matched jobs */}
      <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Recent Matches</h2>
        {matchedJobs?.length === 0 ? (
          <p className="text-gray-500 text-sm">No matches yet. Click "Detect Jobs" to start.</p>
        ) : (
          <div className="space-y-3">
            {matchedJobs?.slice(0, 5).map((job) => (
              <div key={job.id} className="flex items-center justify-between py-2 border-b border-gray-800 last:border-0">
                <div>
                  <p className="text-sm font-medium text-white">{job.title}</p>
                  <p className="text-xs text-gray-400">{job.company} · {job.location ?? "Remote"}</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-medium text-green-400">
                    {((job.match_score ?? 0) * 100).toFixed(0)}%
                  </span>
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-brand-500 hover:underline"
                  >
                    View
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Rate summary */}
      {summary?.rates && (
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
            <p className="text-gray-400 text-sm mb-1">Email Open Rate</p>
            <p className="text-2xl font-bold text-white">
              {(summary.rates.email_open_rate * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-gray-500 mt-1">{summary.rates.emails_opened} / {summary.rates.emails_sent} emails</p>
          </div>
          <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
            <p className="text-gray-400 text-sm mb-1">Response Rate</p>
            <p className="text-2xl font-bold text-white">
              {(summary.rates.response_rate * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-gray-500 mt-1">{summary.rates.total_responded} / {summary.rates.total_applied} applications</p>
          </div>
        </div>
      )}
    </div>
  );
}
