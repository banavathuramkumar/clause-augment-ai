import React from 'react';
import {
  LayoutDashboard,
  Database,
  FileText,
  Sparkles,
  ShieldCheck,
  Scale,
  Cpu,
  BarChart3,
  Activity,
  Download,
  BookOpen
} from 'lucide-react';

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview Dashboard', icon: LayoutDashboard },
  { id: 'dataset', label: 'Dataset Management', icon: Database },
  { id: 'preprocessing', label: 'Text Preprocessing', icon: FileText },
  { id: 'augmentation', label: 'Augmentation Studio', icon: Sparkles },
  { id: 'validation', label: 'Semantic Validation', icon: ShieldCheck },
  { id: 'comparison', label: 'Dataset Comparison', icon: Scale },
  { id: 'training', label: 'Model Training', icon: Cpu },
  { id: 'evaluation', label: 'Evaluation Results', icon: BarChart3 },
  { id: 'robustness', label: 'Robustness Testing', icon: Activity },
  { id: 'export', label: 'Export Center', icon: Download },
  { id: 'docs', label: 'Project Documentation', icon: BookOpen },
];

export default function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="w-64 bg-navy-950 text-slate-300 flex flex-col shrink-0 border-r border-navy-800 shadow-xl min-h-screen">
      {/* Brand header */}
      <div className="p-5 border-b border-navy-800 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-brand-500/20 font-bold text-lg">
          CA
        </div>
        <div>
          <h1 className="font-bold text-slate-100 tracking-tight leading-none text-base">
            ClauseAugment <span className="text-brand-500">AI</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1 font-mono">v1.0.0 Enterprise NLP</p>
        </div>
      </div>

      {/* Nav items */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[11px] font-semibold uppercase tracking-wider text-slate-400">
          Main Pipeline
        </div>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-600/30'
                  : 'text-slate-300 hover:text-white hover:bg-navy-800/80'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span className="truncate">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Status footer */}
      <div className="p-4 border-t border-navy-800 text-xs text-slate-400 bg-navy-900/40">
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="font-medium text-slate-300">FastAPI ML Core Active</span>
        </div>
        <p className="text-[11px] text-slate-500 mt-1">Zero Leakage Architecture</p>
      </div>
    </aside>
  );
}
