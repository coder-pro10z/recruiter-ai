"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { applicationsApi } from "@/lib/api";
import type { Application, ApplicationStatus } from "@/lib/types";
import { format } from "date-fns";
import clsx from "clsx";

const STATUSES: ApplicationStatus[] = [
  "detected", "matched", "outreach_sent", "applied",
  "interviewing", "offer", "rejected", "ghosted",
];

const STATUS_COLORS: Record<ApplicationStatus, string> = {
  detected: "bg-gray-700 text-gray-300",
  matched: "bg-blue-900/40 text-blue-400",
  outreach_sent: "bg-yellow-900/40 text-yellow-400",
  applied: "bg-orange-900/40 text-orange-400",
  interviewing: "bg-purple-900/40 text-purple-400",
  offer: "bg-green-900/40 text-green-400",
  rejected: "bg-red-900/40 text-red-400",
  ghosted: "bg-gray-800 text-gray-500",
};

export default function ApplicationsPage() {
  const qc = useQueryClient();
  const [statusFilter, setStatusFilter] = useState<ApplicationStatus | "all">("all");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const { data: applications = [], isLoading } = useQuery({
    queryKey: ["applications", statusFilter],
    queryFn: () => applicationsApi.list(statusFilter === "all" ? undefined : statusFilter),
  });

  const updateStatus = useMutation({
    mutationFn: ({ id, status }: { id: string; status: ApplicationStatus }) =>
      applicationsApi.updateStatus(id, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["applications"] }),
  });

  const followups = useMutation({
    mutationFn: applicationsApi.triggerFollowups,
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Applications</h1>
        <button
          onClick={() => followups.mutate()}
          disabled={followups.isPending}
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm font-medium rounded-lg disabled:opacity-50"
        >
          {followups.isPending ? "Sending..." : `Run Follow-ups ${followups.data ? `(${followups.data.sent_count} sent)` : ""}`}
        </button>
      </div>

      {/* Status filter pills */}
      <div className="flex gap-1 flex-wrap">
        {(["all", ...STATUSES] as const).map((s) => (
          <button
            key={s}
            onClick={() => setStatusFilter(s)}
            className={clsx(
              "px-3 py-1 text-xs font-medium rounded-full capitalize transition-colors",
              statusFilter === s
                ? "bg-brand-600 text-white"
                : "bg-gray-800 text-gray-400 hover:text-gray-200"
            )}
          >
            {s.replace("_", " ")}
          </button>
        ))}
      </div>

      {isLoading ? (
        <p className="text-gray-500 text-sm">Loading...</p>
      ) : applications.length === 0 ? (
        <p className="text-gray-500 text-sm">No applications found.</p>
      ) : (
        <div className="space-y-2">
          {applications.map((app) => (
            <div
              key={app.id}
              className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden"
            >
              <div
                className="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-800/50"
                onClick={() => setExpandedId(expandedId === app.id ? null : app.id)}
              >
                <div className="flex items-center gap-3">
                  <span className={clsx("px-2 py-0.5 text-xs rounded-full font-medium capitalize", STATUS_COLORS[app.status])}>
                    {app.status.replace("_", " ")}
                  </span>
                  <div>
                    <p className="text-sm text-white font-medium">Application #{app.id.slice(-6)}</p>
                    <p className="text-xs text-gray-500">
                      Created {format(new Date(app.created_at), "MMM d, yyyy")}
                      {app.applied_at && ` · Applied ${format(new Date(app.applied_at), "MMM d")}`}
                      {app.followup_count > 0 && ` · ${app.followup_count} follow-up${app.followup_count > 1 ? "s" : ""}`}
                    </p>
                  </div>
                </div>
                <div className="text-gray-600 text-xs">{expandedId === app.id ? "▲" : "▼"}</div>
              </div>

              {expandedId === app.id && (
                <div className="px-4 pb-4 border-t border-gray-800 space-y-4">
                  {/* Status update */}
                  <div>
                    <p className="text-xs text-gray-500 mb-2">Update Status</p>
                    <div className="flex flex-wrap gap-1">
                      {STATUSES.map((s) => (
                        <button
                          key={s}
                          onClick={() => updateStatus.mutate({ id: app.id, status: s })}
                          disabled={app.status === s || updateStatus.isPending}
                          className={clsx(
                            "px-2 py-1 text-xs rounded capitalize transition-colors",
                            app.status === s
                              ? "bg-brand-600 text-white"
                              : "bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200 disabled:opacity-50"
                          )}
                        >
                          {s.replace("_", " ")}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Timeline */}
                  {app.timeline.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-500 mb-2">Timeline</p>
                      <div className="space-y-1">
                        {app.timeline.map((e, i) => (
                          <p key={i} className="text-xs text-gray-400">
                            {format(new Date(e.at), "MMM d HH:mm")} — {e.event.replace(/_/g, " ")}
                          </p>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Next followup */}
                  {app.next_followup_at && (
                    <p className="text-xs text-yellow-400">
                      Next follow-up: {format(new Date(app.next_followup_at), "MMM d, yyyy")}
                    </p>
                  )}
                  {app.notes && <p className="text-xs text-gray-400 italic">Notes: {app.notes}</p>}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
