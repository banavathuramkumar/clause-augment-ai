import React from 'react';
import {
  FileText,
  Sparkles,
  ShieldCheck,
  Cpu,
  BarChart2,
  TrendingUp,
  Layers,
  ArrowRight
} from 'lucide-react';
import StatCard from '../components/StatCard';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell
} from 'recharts';

export default function Overview({ dataset, expansion, experiments, onNavigate }) {
  const totalClauses = dataset?.total_clauses || 0;
  const numCategories = dataset?.num_categories || 0;
  const generatedVariations = expansion?.augmented_count || 0;
  const acceptedVariations = expansion?.accepted_count || 0;
  const expansionRate = expansion?.expansion_percentage || 0;

  // Best experiment
  let bestExp = null;
  if (experiments && experiments.length > 0) {
    bestExp = [...experiments].sort(
      (a, b) => (b.metrics?.Augmented?.macro_f1 || 0) - (a.metrics?.Augmented?.macro_f1 || 0)
    )[0];
  }

  // Distribution chart data
  const distData = Object.entries(dataset?.stats?.category_distribution || {}).map(
    ([name, count]) => ({
      name: name.length > 12 ? name.substring(0, 11) + '..' : name,
      fullName: name,
      count
    })
  );

  const COLORS = ['#2563eb', '#3b82f6', '#60a5fa', '#10b981', '#06b6d4', '#8b5cf6', '#f59e0b', '#ec4899', '#64748b', '#14b8a6'];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-navy-950 via-navy-900 to-slate-900 rounded-2xl p-6 text-white shadow-xl border border-navy-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <span className="px-3 py-1 bg-brand-600/30 text-brand-400 border border-brand-500/40 rounded-full text-xs font-semibold uppercase tracking-wider">
            Academic Research Pipeline
          </span>
          <h2 className="text-2xl font-bold mt-2">ClauseAugment AI: Legal Text Augmentation</h2>
          <p className="text-slate-400 text-sm mt-1 max-w-2xl">
            Controlled NLP data augmentation algorithms and traditional ML classification benchmark.
            Evaluates generalization and semantic preservation without data leakage or paid APIs.
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => onNavigate('augmentation')}
            className="flex items-center space-x-2 px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-sm font-semibold shadow-lg transition"
          >
            <Sparkles className="w-4 h-4" />
            <span>Launch Studio</span>
          </button>
          <button
            onClick={() => onNavigate('training')}
            className="flex items-center space-x-2 px-4 py-2 bg-navy-800 hover:bg-navy-700 text-slate-200 border border-navy-700 rounded-lg text-sm font-semibold transition"
          >
            <Cpu className="w-4 h-4" />
            <span>Train Models</span>
          </button>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Benchmark Clauses"
          value={totalClauses}
          subtitle={`${numCategories} legal categories`}
          icon={FileText}
          color="blue"
        />
        <StatCard
          title="Generated Variations"
          value={generatedVariations}
          subtitle={`${acceptedVariations} verified / accepted`}
          icon={Sparkles}
          color="indigo"
        />
        <StatCard
          title="Dataset Expansion"
          value={`${expansionRate}%`}
          subtitle="Validated expansion ratio"
          icon={TrendingUp}
          color="emerald"
        />
        <StatCard
          title="Best Model Macro F1"
          value={bestExp ? (bestExp.metrics?.Augmented?.macro_f1 || 0).toFixed(4) : 'N/A'}
          subtitle={bestExp ? `${bestExp.model_name} (${bestExp.feature_type})` : 'Run training experiment'}
          icon={BarChart2}
          color="purple"
        />
      </div>

      {/* Two Column Layout: Class Distribution & Pipeline Stages */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Class distribution chart */}
        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-800 text-base">Class Distribution</h3>
              <p className="text-xs text-slate-500">Distribution of legal clauses across categories</p>
            </div>
            <span className="text-xs font-mono text-slate-500">
              Imbalance Ratio: {dataset?.stats?.imbalance_ratio || 1.0}
            </span>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={distData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                <XAxis dataKey="name" angle={-30} textAnchor="end" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip
                  formatter={(val, name, props) => [val, props.payload.fullName]}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff' }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {distData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Guided Pipeline Walkthrough */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-slate-800 text-base mb-1">Pipeline Workflow</h3>
            <p className="text-xs text-slate-500 mb-4">6-phase reproducible legal NLP architecture</p>

            <div className="space-y-3">
              {[
                { title: '1. Dataset Ingestion', desc: 'Standard contract clause corpus', tab: 'dataset' },
                { title: '2. Preprocessing', desc: 'Legal modal & negation preservation', tab: 'preprocessing' },
                { title: '3. Augmentation Studio', desc: '6 controlled perturbation algorithms', tab: 'augmentation' },
                { title: '4. Semantic Guardrails', desc: 'Cosine similarity & entity verification', tab: 'validation' },
                { title: '5. Model Training', desc: 'Zero-leakage split & TF-IDF classifiers', tab: 'training' },
                { title: '6. Robustness Stress', desc: 'Evaluation under style shift & noise', tab: 'robustness' }
              ].map((step, idx) => (
                <button
                  key={idx}
                  onClick={() => onNavigate(step.tab)}
                  className="w-full text-left p-2.5 rounded-lg border border-slate-100 hover:border-brand-200 hover:bg-brand-50/40 transition group flex items-center justify-between"
                >
                  <div>
                    <h4 className="text-xs font-semibold text-slate-800 group-hover:text-brand-600 transition">
                      {step.title}
                    </h4>
                    <p className="text-[11px] text-slate-500">{step.desc}</p>
                  </div>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-brand-600 group-hover:translate-x-0.5 transition" />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
