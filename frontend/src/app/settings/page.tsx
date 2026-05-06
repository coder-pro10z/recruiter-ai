"use client";

import { useState, useEffect } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { settingsApi } from "@/lib/api";
import type { MatchingRules } from "@/lib/types";
import { Save, Plus, X } from "lucide-react";

function TagEditor({
  label,
  tags,
  onChange,
}: {
  label: string;
  tags: string[];
  onChange: (t: string[]) => void;
}) {
  const [input, setInput] = useState("");
  const add = () => {
    const v = input.trim().toLowerCase();
    if (v && !tags.includes(v)) onChange([...tags, v]);
    setInput("");
  };
  return (
    <div>
      <p className="text-xs text-gray-400 mb-2">{label}</p>
      <div className="flex flex-wrap gap-1 mb-2">
        {tags.map((t) => (
          <span key={t} className="flex items-center gap-1 px-2 py-0.5 bg-gray-800 text-gray-300 text-xs rounded">
            {t}
            <button onClick={() => onChange(tags.filter((x) => x !== t))} className="text-gray-500 hover:text-red-400">
              <X size={10} />
            </button>
          </span>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 max-w-xs px-3 py-1.5 bg-gray-900 border border-gray-700 rounded text-xs text-gray-100 focus:outline-none focus:border-brand-500"
          placeholder={`Add ${label.toLowerCase()}...`}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && add()}
        />
        <button onClick={add} className="p-1.5 bg-gray-700 hover:bg-gray-600 rounded text-gray-300">
          <Plus size={12} />
        </button>
      </div>
    </div>
  );
}

export default function SettingsPage() {
  const { data: rules } = useQuery({ queryKey: ["rules"], queryFn: settingsApi.getRules });
  const { data: feedsData } = useQuery({ queryKey: ["feeds"], queryFn: settingsApi.getFeeds });

  const [draft, setDraft] = useState<Partial<MatchingRules>>({});
  const [feeds, setFeeds] = useState<string[]>([]);
  const [feedInput, setFeedInput] = useState("");

  useEffect(() => { if (rules) setDraft(rules); }, [rules]);
  useEffect(() => { if (feedsData) setFeeds(feedsData.feeds); }, [feedsData]);

  const saveRules = useMutation({
    mutationFn: () => settingsApi.updateRules(draft),
  });
  const saveFeeds = useMutation({
    mutationFn: () => settingsApi.updateFeeds(feeds),
  });

  const update = (key: keyof MatchingRules, val: unknown) =>
    setDraft((d) => ({ ...d, [key]: val }));

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold text-white">Settings</h1>

      {/* Matching Rules */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-5">
        <h2 className="text-sm font-semibold text-gray-300">Matching Rules</h2>

        <TagEditor
          label="Required Skills (I have)"
          tags={draft.required_skills ?? []}
          onChange={(v) => update("required_skills", v)}
        />
        <TagEditor
          label="Preferred Skills"
          tags={draft.preferred_skills ?? []}
          onChange={(v) => update("preferred_skills", v)}
        />
        <TagEditor
          label="Blocked Companies"
          tags={draft.blocked_companies ?? []}
          onChange={(v) => update("blocked_companies", v)}
        />
        <TagEditor
          label="Blocked Keywords"
          tags={draft.blocked_keywords ?? []}
          onChange={(v) => update("blocked_keywords", v)}
        />

        <div>
          <p className="text-xs text-gray-400 mb-2">Min Match Score ({((draft.min_match_score ?? 0.4) * 100).toFixed(0)}%)</p>
          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={draft.min_match_score ?? 0.4}
            onChange={(e) => update("min_match_score", parseFloat(e.target.value))}
            className="w-full accent-brand-500"
          />
        </div>

        <button
          onClick={() => saveRules.mutate()}
          disabled={saveRules.isPending}
          className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg disabled:opacity-50"
        >
          <Save size={14} />
          {saveRules.isPending ? "Saving..." : saveRules.isSuccess ? "Saved!" : "Save Rules"}
        </button>
      </div>

      {/* RSS Feeds */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-semibold text-gray-300">RSS Feeds</h2>
        <div className="space-y-2">
          {feeds.map((f, i) => (
            <div key={i} className="flex items-center gap-2">
              <span className="flex-1 text-xs text-gray-400 font-mono bg-gray-800 px-3 py-1.5 rounded truncate">{f}</span>
              <button
                onClick={() => setFeeds(feeds.filter((_, j) => j !== i))}
                className="text-gray-600 hover:text-red-400"
              >
                <X size={12} />
              </button>
            </div>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            className="flex-1 px-3 py-1.5 bg-gray-800 border border-gray-700 rounded text-xs text-gray-100 focus:outline-none focus:border-brand-500"
            placeholder="https://... RSS feed URL"
            value={feedInput}
            onChange={(e) => setFeedInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && feedInput.trim()) {
                setFeeds([...feeds, feedInput.trim()]);
                setFeedInput("");
              }
            }}
          />
          <button
            onClick={() => {
              if (feedInput.trim()) {
                setFeeds([...feeds, feedInput.trim()]);
                setFeedInput("");
              }
            }}
            className="p-1.5 bg-gray-700 hover:bg-gray-600 rounded text-gray-300"
          >
            <Plus size={12} />
          </button>
        </div>
        <button
          onClick={() => saveFeeds.mutate()}
          disabled={saveFeeds.isPending}
          className="flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg disabled:opacity-50"
        >
          <Save size={14} />
          {saveFeeds.isPending ? "Saving..." : saveFeeds.isSuccess ? "Saved!" : "Save Feeds"}
        </button>
      </div>
    </div>
  );
}
