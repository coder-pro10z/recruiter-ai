"use client";

import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
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
    const values = input
      .split(/[\n,]+/) // Split by comma or newline
      .map(v => v.trim().toLowerCase())
      .filter(v => v.length > 0);

    if (values.length > 0) {
      const newTags = [...tags];
      values.forEach(v => {
        if (!newTags.includes(v)) newTags.push(v);
      });
      onChange(newTags);
    }
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
  const queryClient = useQueryClient();
  const { data: profiles } = useQuery({ queryKey: ["profiles"], queryFn: settingsApi.getProfiles });
  const { data: rules } = useQuery({ queryKey: ["rules"], queryFn: settingsApi.getRules });
  const { data: feedsData } = useQuery({ queryKey: ["feeds"], queryFn: settingsApi.getFeeds });

  const [draft, setDraft] = useState<Partial<MatchingRules>>({});
  const [feeds, setFeeds] = useState<string[]>([]);
  const [feedInput, setFeedInput] = useState("");
  const [profileName, setProfileName] = useState("");

  useEffect(() => { if (rules) setDraft(rules); }, [rules]);
  useEffect(() => { if (feedsData) setFeeds(feedsData.feeds); }, [feedsData]);

  const saveRules = useMutation({
    mutationFn: () => settingsApi.updateRules(draft),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["rules"] })
  });
  
  const createProfile = useMutation({
    mutationFn: () => settingsApi.createProfile({
      name: profileName || "Custom Profile",
      ...draft,
      is_active: true
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["profiles"] });
      queryClient.invalidateQueries({ queryKey: ["rules"] });
      setProfileName("");
    }
  });

  const activateProfile = useMutation({
    mutationFn: (id: string) => settingsApi.activateProfile(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["profiles"] });
      queryClient.invalidateQueries({ queryKey: ["rules"] });
    }
  });

  const saveFeeds = useMutation({
    mutationFn: () => settingsApi.updateFeeds(feeds),
  });

  const update = (key: keyof MatchingRules, val: unknown) =>
    setDraft((d) => ({ ...d, [key]: val }));

  return (
    <div className="space-y-6 max-w-2xl pb-20">
      <h1 className="text-2xl font-bold text-white">Settings</h1>

      {/* Profile Selector */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-semibold text-gray-300">Active Search Profile</h2>
        <div className="flex gap-4">
          <select 
            className="flex-1 bg-gray-800 border border-gray-700 rounded text-sm text-gray-200 px-3 py-2 focus:outline-none focus:border-brand-500"
            value={profiles?.find(p => p.is_active)?.id || ""}
            onChange={(e) => {
              if (e.target.value) activateProfile.mutate(e.target.value);
            }}
          >
            <option value="" disabled>Select a profile...</option>
            {profiles?.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Matching Rules */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-5">
        <h2 className="text-sm font-semibold text-gray-300">Matching Rules Configuration</h2>

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

        <div className="flex flex-col gap-3 pt-4 border-t border-gray-800">
          <button
            onClick={() => saveRules.mutate()}
            disabled={saveRules.isPending}
            className="flex items-center justify-center gap-2 w-full py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg disabled:opacity-50 transition-colors"
          >
            <Save size={14} />
            {saveRules.isPending ? "Saving..." : saveRules.isSuccess ? "Updated!" : "Update Current Profile"}
          </button>
          
          <div className="flex items-center gap-2">
             <input 
               className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-sm text-gray-200 focus:outline-none focus:border-brand-500"
               placeholder="New Profile Name (e.g. Senior .NET)"
               value={profileName}
               onChange={(e) => setProfileName(e.target.value)}
             />
             <button
               onClick={() => createProfile.mutate()}
               disabled={createProfile.isPending || !profileName.trim()}
               className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm font-medium rounded-lg disabled:opacity-50 transition-colors whitespace-nowrap"
             >
                Save as New Profile
             </button>
          </div>
        </div>
      </div>

      {/* RSS Feeds */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-semibold text-gray-300">Active RSS Feeds</h2>
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
