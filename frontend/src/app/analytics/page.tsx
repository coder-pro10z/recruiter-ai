"use client";

import { useQuery } from "@tanstack/react-query";
import { analyticsApi } from "@/lib/api";
import { TrendingUp, Mail, Users, Trophy } from "lucide-react";

export default function AnalyticsPage() {
  const { data: summary, isLoading } = useQuery({
    queryKey: ["analytics-summary"],
    queryFn: analyticsApi.summary,
  });

  if (isLoading) return <p className="text-gray-500 text-sm">Loading analytics...</p>;
  if (!summary) return <p className="text-gray-500 text-sm">No data available yet.</p>;

  const { funnel, rates, top_matched_companies } = summary;
  const funnelStages = Object.entries(funnel);
  const maxFunnelVal = Math.max(...funnelStages.map(([, v]) => v), 1);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Analytics</h1>

      {/* Key metrics */}
      <div className="grid grid-cols-3 gap-4">
        {[
          {
            icon: Mail,
            label: "Email Open Rate",
            value: `${(rates.email_open_rate * 100).toFixed(1)}%`,
            sub: `${rates.emails_opened} / ${rates.emails_sent}`,
            color: "text-yellow-400",
          },
          {
            icon: TrendingUp,
            label: "Response Rate",
            value: `${(rates.response_rate * 100).toFixed(1)}%`,
            sub: `${rates.total_responded} / ${rates.total_applied}`,
            color: "text-green-400",
          },
          {
            icon: Users,
            label: "Interviews",
            value: funnel.interviewing,
            sub: `${funnel.offer} offers`,
            color: "text-purple-400",
          },
        ].map(({ icon: Icon, label, value, sub, color }) => (
          <div key={label} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <p className="text-sm text-gray-400">{label}</p>
              <Icon size={16} className={color} />
            </div>
            <p className="text-3xl font-bold text-white">{value}</p>
            <p className="text-xs text-gray-500 mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Visual funnel */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-5">Application Funnel</h2>
        <div className="space-y-2">
          {funnelStages.map(([stage, count]) => (
            <div key={stage} className="flex items-center gap-3">
              <p className="text-xs text-gray-400 w-24 capitalize shrink-0">{stage.replace("_", " ")}</p>
              <div className="flex-1 bg-gray-800 rounded-full h-2">
                <div
                  className="bg-brand-500 h-2 rounded-full transition-all"
                  style={{ width: `${(count / maxFunnelVal) * 100}%` }}
                />
              </div>
              <p className="text-xs text-white w-6 text-right shrink-0">{count}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Top matched companies */}
      {top_matched_companies.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4 flex items-center gap-2">
            <Trophy size={14} /> Top Matched Companies
          </h2>
          <div className="space-y-2">
            {top_matched_companies.map((co, i) => (
              <div key={co.company} className="flex items-center justify-between py-1">
                <div className="flex items-center gap-3">
                  <span className="text-xs text-gray-600 w-4">{i + 1}</span>
                  <p className="text-sm text-white">{co.company}</p>
                  <span className="text-xs text-gray-500">{co.job_count} job{co.job_count > 1 ? "s" : ""}</span>
                </div>
                <span className="text-sm font-medium text-green-400">{(co.avg_score * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
