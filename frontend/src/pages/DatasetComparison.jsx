import React from 'react';
import { Scale, TrendingUp, Layers, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';

export default function DatasetComparison({ dataset, expansion }) {
  const origDist = expansion?.original_distribution || {};
  const augDist = expansion?.augmented_distribution || {};

  const categories = Array.from(new Set([...Object.keys(origDist), ...Object.keys(augDist)]));

  const chartData = categories.map((cat) => ({
    name: cat.length > 12 ? cat.substring(0, 11) + '..' : cat,
    fullName: cat,
    Original: origDist[cat] || 0,
    Augmented: augDist[cat] || 0,
    NetAdded: (augDist[cat] || 0) - (origDist[cat] || 0)
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <h2 className="text-xl font-bold text-slate-900">Dataset Comparison & Expansion Analytics</h2>
        <p className="text-xs text-slate-500 mt-1">
          Comparative analysis between original benchmark corpus and expanded, validated dataset.
        </p>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Original Corpus</p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{expansion?.original_count || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Synthesized</p>
          <p className="text-2xl font-bold text-indigo-600 mt-1">{expansion?.augmented_count || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Accepted</p>
          <p className="text-2xl font-bold text-emerald-600 mt-1">{expansion?.accepted_count || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Needs Review</p>
          <p className="text-2xl font-bold text-amber-600 mt-1">{expansion?.needs_review_count || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Dataset Expansion</p>
          <p className="text-2xl font-bold text-brand-600 mt-1">+{expansion?.expansion_percentage || 0}%</p>
        </div>
      </div>

      {/* Class Distribution Comparison Chart */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-slate-900 text-base">Class Distribution: Original vs Augmented</h3>
            <p className="text-xs text-slate-500">Compares clause density before and after verified data augmentation</p>
          </div>
        </div>

        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 20, left: -10, bottom: 30 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="name" angle={-30} textAnchor="end" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip
                formatter={(val, name, props) => [val, `${name} (${props.payload.fullName})`]}
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff' }}
              />
              <Legend verticalAlign="top" height={36} />
              <Bar dataKey="Original" fill="#64748b" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Augmented" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Traceability Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <h3 className="font-bold text-slate-900 text-base mb-2">Category-Wise Expansion Audit</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">Category</th>
                <th className="p-3 text-center">Original Count</th>
                <th className="p-3 text-center">Augmented Count</th>
                <th className="p-3 text-center">Net Added</th>
                <th className="p-3 text-center">Category Expansion %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {chartData.map((row) => {
                const growth = row.Original > 0 ? (((row.Augmented - row.Original) / row.Original) * 100).toFixed(1) : 0;
                return (
                  <tr key={row.fullName} className="hover:bg-slate-50">
                    <td className="p-3 font-medium text-slate-800">{row.fullName}</td>
                    <td className="p-3 text-center text-slate-600">{row.Original}</td>
                    <td className="p-3 text-center font-bold text-brand-600">{row.Augmented}</td>
                    <td className="p-3 text-center text-emerald-600 font-medium">+{row.NetAdded}</td>
                    <td className="p-3 text-center font-mono font-medium text-slate-700">+{growth}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
