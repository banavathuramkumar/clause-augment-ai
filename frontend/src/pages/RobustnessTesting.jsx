import React, { useState } from 'react';
import { Activity, Play, ShieldAlert, CheckCircle2, TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

const PERTURBATIONS = [
  { id: 'drafting_style_shift', name: 'Drafting Style Shift', desc: 'Converts formulaic clauses to alternative legal boilerplate phrasing' },
  { id: 'paraphrase_stress', name: 'Paraphrase Stress Test', desc: 'Applies formal synonym substitutions on peripheral predicates' },
  { id: 'punctuation_spacing', name: 'Scanned / OCR Spacing Noise', desc: 'Introduces irregular punctuation spacing common in scanned filings' },
  { id: 'case_typo', name: 'Transcription / Casing Permutation', desc: 'Simulates casing anomalies across non-defined words' },
];

export default function RobustnessTesting({ experiments, selectedExperiment }) {
  const exp = selectedExperiment || (experiments && experiments.length > 0 ? experiments[0] : null);

  const [selectedTypes, setSelectedTypes] = useState([
    'drafting_style_shift',
    'paraphrase_stress',
    'punctuation_spacing',
    'case_typo'
  ]);
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');

  const handleToggle = (id) => {
    setSelectedTypes((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const handleRunStressTest = async () => {
    if (!exp?.id) return;
    if (selectedTypes.length === 0) {
      setError('Please select at least one stress test perturbation type.');
      return;
    }

    setRunning(true);
    setError('');
    try {
      const res = await api.runRobustness({
        experiment_id: exp.id,
        perturbation_types: selectedTypes,
      });
      setResults(res);
    } catch (err) {
      setError(err.message || 'Robustness evaluation failed.');
    } finally {
      setRunning(false);
    }
  };

  if (!exp) {
    return (
      <div className="bg-white p-12 rounded-xl border border-slate-200 text-center">
        <Activity className="w-12 h-12 text-slate-300 mx-auto mb-3" />
        <h3 className="font-bold text-slate-800 text-base">No Trained Model Available</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Please run a training experiment first before executing out-of-distribution robustness stress tests.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Out-of-Distribution Robustness Stress Testing</h2>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl">
            Examines whether data augmentation actually improves model resilience against alternate legal drafting styles,
            unseen syntax inversions, and document transcription noise.
          </p>
        </div>
        <button
          onClick={handleRunStressTest}
          disabled={running}
          className="flex items-center space-x-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-brand-600/20 disabled:opacity-50 transition shrink-0"
        >
          <Play className="w-4 h-4 fill-current" />
          <span>{running ? 'Running Perturbation Suite...' : 'Execute Robustness Stress Test'}</span>
        </button>
      </div>

      {error && (
        <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg">
          {error}
        </div>
      )}

      {/* Perturbation Type Selection */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-4">
        <h3 className="font-bold text-slate-900 text-sm">Target Stress Perturbations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {PERTURBATIONS.map((p) => {
            const active = selectedTypes.includes(p.id);
            return (
              <div
                key={p.id}
                onClick={() => handleToggle(p.id)}
                className={`p-3.5 rounded-lg border cursor-pointer transition ${
                  active
                    ? 'border-brand-600 bg-brand-50/40 shadow-sm'
                    : 'border-slate-200 bg-slate-50/40 hover:bg-slate-100/50'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className={`text-xs font-bold ${active ? 'text-brand-700' : 'text-slate-800'}`}>
                    {p.name}
                  </span>
                  <input
                    type="checkbox"
                    checked={active}
                    onChange={() => {}}
                    className="rounded text-brand-600 focus:ring-brand-500 pointer-events-none"
                  />
                </div>
                <p className="text-[11px] text-slate-500 leading-normal">{p.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Results Section */}
      {results.length > 0 && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {results.map((res) => {
              const improved = res.f1_delta >= 0;
              return (
                <div key={res.perturbation_type} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                  <p className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
                    {res.perturbation_type.replace(/_/g, ' ')}
                  </p>
                  <div className="flex items-baseline justify-between mb-1">
                    <span className="text-xs text-slate-500">Augmented F1:</span>
                    <span className="text-sm font-bold text-brand-600">{res.augmented_model_f1.toFixed(4)}</span>
                  </div>
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-xs text-slate-500">Original Baseline:</span>
                    <span className="text-sm font-semibold text-slate-600">{res.original_model_f1.toFixed(4)}</span>
                  </div>
                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-[11px] font-semibold text-slate-600">Resilience Shift:</span>
                    <span className={`text-xs font-bold font-mono ${improved ? 'text-emerald-600' : 'text-rose-600'}`}>
                      {improved ? `+${res.f1_delta.toFixed(4)}` : res.f1_delta.toFixed(4)}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Sample Perturbations Inspection Table */}
          <div className="bg-white rounded-xl border border-slate-200/80 shadow-sm overflow-hidden">
            <div className="p-4 border-b border-slate-200 bg-slate-50/50">
              <h3 className="font-bold text-slate-800 text-sm">Perturbation Traceability Samples</h3>
              <p className="text-xs text-slate-500">Inspect actual test clauses transformed under controlled stress</p>
            </div>
            <div className="divide-y divide-slate-100 text-xs">
              {results.map((res) => (
                <div key={res.perturbation_type} className="p-4 space-y-3">
                  <span className="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-700">
                    {res.perturbation_type.replace(/_/g, ' ')}
                  </span>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {res.sample_perturbations.map((sample, sIdx) => (
                      <div key={sIdx} className="p-3 bg-slate-50 rounded-lg border border-slate-200 space-y-1.5">
                        <div className="text-[11px] text-slate-600">
                          <span className="font-semibold text-slate-800 block text-[10px] uppercase">Unseen Test Clause:</span>
                          {sample.original}
                        </div>
                        <div className="text-[11px] text-brand-900 font-medium">
                          <span className="font-semibold text-brand-700 block text-[10px] uppercase">Perturbed Form:</span>
                          {sample.perturbed}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
