"use client";

import "./globals.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Briefcase, LayoutDashboard, FileText, Settings, BarChart2 } from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/jobs", label: "Jobs", icon: Briefcase },
  { href: "/applications", label: "Applications", icon: FileText },
  { href: "/analytics", label: "Analytics", icon: BarChart2 },
  { href: "/settings", label: "Settings", icon: Settings },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const pathname = usePathname();

  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen">
        <QueryClientProvider client={queryClient}>
          <div className="flex h-screen overflow-hidden">
            <aside className="w-56 bg-gray-900 border-r border-gray-800 flex flex-col">
              <div className="px-5 py-4 border-b border-gray-800">
                <span className="text-brand-500 font-bold text-lg tracking-tight">JobFinder</span>
                <p className="text-gray-500 text-xs mt-0.5">AI Recruiting Platform</p>
              </div>
              <nav className="flex-1 px-3 py-4 space-y-1">
                {navItems.map(({ href, label, icon: Icon }) => (
                  <Link
                    key={href}
                    href={href}
                    className={clsx(
                      "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                      pathname === href
                        ? "bg-brand-600 text-white"
                        : "text-gray-400 hover:bg-gray-800 hover:text-gray-100"
                    )}
                  >
                    <Icon size={16} />
                    {label}
                  </Link>
                ))}
              </nav>
            </aside>
            <main className="flex-1 overflow-y-auto p-6">{children}</main>
          </div>
        </QueryClientProvider>
      </body>
    </html>
  );
}
