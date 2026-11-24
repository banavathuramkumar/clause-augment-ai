import React from 'react';
import { Database, RefreshCw, CheckCircle2 } from 'lucide-react';

export default function Header({ datasets, selectedDataset, onSelectDataset, onRefresh, loading }) {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between shadow-sm sticky top-0 z-20">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 text-sm text-slate-600">
          <Database className="w-4 h-4 text-brand-600" />
          <span className="font-medium text-slate-700">Active Legal Dataset:</span>
        </div>
        <select
          value={selectedDataset?.id || ''}
          onChange={(e) => {
            const found = datasets.find((d) => d.id === e.target.value);
            if (found) onSelectDataset(found);
          }}
          className="bg-slate-50 border border-slate-300 text-slate-800 text-sm rounded-lg focus:ring-brand-500 focus:border-brand-500 block p-2 font-medium"
        >
          {datasets.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name} ({d.total_clauses} clauses)
            </option>
          ))}
        </select>
      </div>

      <div className="flex items-center space-x-3">
        <button
          onClick={onRefresh}
          disabled={loading}
          className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition border border-slate-200 disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-brand-600' : ''}`} />
          <span>Sync State</span>
        </button>

        <div className="flex items-center space-x-1 px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-full text-xs font-medium border border-emerald-200">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
          <span>Local Engine Verified</span>
        </div>
      </div>
    </header>
  );
}
