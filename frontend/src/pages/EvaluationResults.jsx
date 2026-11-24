import React, { useState } from 'react';
import { BarChart3, TrendingUp, TrendingDown, Layers, FileDown, ShieldCheck } from 'lucide-react';
import { api } from '../services/api';
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

export default function EvaluationResults({ experiments, selectedExperiment, onSelectExperiment }) {
  const exp = selectedExperiment || (experiments && experiments.length > 0 ? experiments[0] : null);

  const [activeMatrixTab, setActiveMatrixTab] = useState('Augmented');

  if (!exp) {
    return (
      <div className="bg-white p-12 rounded-xl border border-slate-200 text-center">
        <BarChart3 className="w-12 h-12 text-slate-300 mx-auto mb-3" />
        <h3 className="font-bold text-slate-800 text-base">No Evaluation Experiments Yet</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Navigate to the "Model Training" tab to train your first comparative baseline and augmented classifier.
        </p>
      </div>
    );
  }

  const origMetrics = exp.metrics?.Original || {};
  const augMetrics = exp.metrics?.Augmented || {};

  const accDelta = exp.comparison?.accuracy_delta || 0;
  const f1Delta = exp.comparison?.macro_f1_delta || 0;
  const relF1 = exp.comparison?.relative_f1_improvement_pct || 0;

  // Overview metrics chart data
  const metricsComparisonData = [
    { metric: 'Accuracy', Original: Math.round((origMetrics.accuracy || 0) * 1000) / 10, Augmented: Math.round((augMetrics.accuracy || 0) * 1000) / 10 },
    { metric: 'Macro F1', Original: Math.round((origMetrics.macro_f1 || 0) * 1000) / 10, Augmented: Math.round((augMetrics.macro_f1 || 0) * 1000) / 10 },
    { metric: 'Weighted F1', Original: Math.round((origMetrics.weighted_f1 || 0) * 1000) / 10, Augmented: Math.round((augMetrics.weighted_f1 || 0) * 1000) / 10 },
    { metric: 'Macro Precision', Original: Math.round((origMetrics.macro_precision || 0) * 1000) / 10, Augmented: Math.round((augMetrics.macro_precision || 0) * 1000) / 10 },
    { metric: 'Macro Recall', Original: Math.round((origMetrics.macro_recall || 0) * 1000) / 10, Augmented: Math.round((augMetrics.macro_recall || 0) * 1000) / 10 },
  ];

  // Class-wise report breakdown
  const origClf = origMetrics.classification_report || {};
  const augClf = augMetrics.classification_report || {};
  const labels = origMetrics.labels || Object.keys(origClf).filter((k) => !['accuracy', 'macro avg', 'weighted avg'].includes(k));

  const activeMatrix = activeMatrixTab === 'Original' ? origMetrics.confusion_matrix : augMetrics.confusion_matrix;

  return (
    <div className="space-y-6">
      {/* Experiment Selector & Export */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Selected Experiment:</span>
            <select
              value={exp.id}
              onChange={(e) => {
                const found = experiments.find((x) => x.id === e.target.value);
                if (found) onSelectExperiment(found);
              }}
              className="text-xs font-bold text-slate-800 bg-slate-50 border border-slate-300 rounded-lg p-1.5 focus:ring-brand-500 focus:border-brand-500"
            >
              {experiments.map((x) => (
                <option key={x.id} value={x.id}>
                  {x.name} ({x.model_name})
                </option>
              ))}
            </select>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Test Partition: {exp.test_size} clauses (unseen held-out test split) | Train: {exp.original_train_size} original, {exp.augmented_train_size} augmented
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <a
            href={api.getExportUrl('evaluation_pdf', '', exp.id)}
            download
            className="flex items-center space-x-1.5 px-3.5 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold shadow transition"
          >
            <FileDown className="w-4 h-4" />
            <span>Export Report PDF</span>
          </a>
          <a
            href={api.getExportUrl('classification_report_csv', '', exp.id)}
            download
            className="flex items-center space-x-1.5 px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-200 transition"
          >
            <span>Report CSV</span>
          </a>
        </div>
      </div>

      {/* KPI Delta Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Test Accuracy Delta</p>
          <div className="flex items-center justify-center space-x-1 mt-1">
            {accDelta >= 0 ? <TrendingUp className="w-4 h-4 text-emerald-600" /> : <TrendingDown className="w-4 h-4 text-rose-600" />}
            <span className={`text-2xl font-bold ${accDelta >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
              {(accDelta * 100).toFixed(1)}%
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-0.5">
            Original {(origMetrics.accuracy * 100).toFixed(1)}% &rarr; Augmented {(augMetrics.accuracy * 100).toFixed(1)}%
          </p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Macro F1 Score Delta</p>
          <div className="flex items-center justify-center space-x-1 mt-1">
            {f1Delta >= 0 ? <TrendingUp className="w-4 h-4 text-emerald-600" /> : <TrendingDown className="w-4 h-4 text-rose-600" />}
            <span className={`text-2xl font-bold ${f1Delta >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
              {f1Delta >= 0 ? `+${f1Delta.toFixed(4)}` : f1Delta.toFixed(4)}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-0.5">
            Original {origMetrics.macro_f1?.toFixed(4)} &rarr; Augmented {augMetrics.macro_f1?.toFixed(4)}
          </p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Relative F1 Improvement</p>
          <p className={`text-2xl font-bold mt-1 ${relF1 >= 0 ? 'text-brand-600' : 'text-rose-600'}`}>
            {relF1 >= 0 ? `+${relF1}%` : `${relF1}%`}
          </p>
          <p className="text-[11px] text-slate-400 mt-0.5">Scientific relative delta</p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Generalization Outcome</p>
          <p className={`text-xl font-bold mt-1.5 ${f1Delta >= 0 ? 'text-emerald-600' : 'text-amber-600'}`}>
            {f1Delta >= 0 ? 'Robust Gain' : 'Honest Baseline Shift'}
          </p>
          <p className="text-[11px] text-slate-400 mt-0.5">Zero hardcoding guarantee</p>
        </div>
      </div>

      {/* Metrics Comparison Chart */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <h3 className="font-bold text-slate-900 text-base mb-1">Comparative Metrics (%) on Held-Out Test Set</h3>
        <p className="text-xs text-slate-500 mb-4">
          Direct comparison between baseline trained on original data vs classifier trained on augmented data.
        </p>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={metricsComparisonData} margin={{ top: 20, right: 20, left: -10, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="metric" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
              <Tooltip
                formatter={(val, name) => [`${val}%`, name]}
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff' }}
              />
              <Legend verticalAlign="top" height={36} />
              <Bar dataKey="Original" fill="#64748b" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Augmented" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Confusion Matrix Heatmap Representation */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
          <div>
            <h3 className="font-bold text-slate-900 text-base">Confusion Matrix Analysis</h3>
            <p className="text-xs text-slate-500">True Label (rows) vs Predicted Label (columns)</p>
          </div>
          <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-lg text-xs font-semibold">
            <button
              onClick={() => setActiveMatrixTab('Augmented')}
              className={`px-3 py-1 rounded-md transition ${activeMatrixTab === 'Augmented' ? 'bg-brand-600 text-white shadow-sm' : 'text-slate-600'}`}
            >
              Experiment B: Augmented
            </button>
            <button
              onClick={() => setActiveMatrixTab('Original')}
              className={`px-3 py-1 rounded-md transition ${activeMatrixTab === 'Original' ? 'bg-brand-600 text-white shadow-sm' : 'text-slate-600'}`}
            >
              Experiment A: Original
            </button>
          </div>
        </div>

        {activeMatrix && activeMatrix.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="border-collapse text-[11px] font-mono text-center mx-auto">
              <thead>
                <tr>
                  <th className="p-2 text-slate-400 font-sans text-xs">True \ Pred</th>
                  {labels.map((l, idx) => (
                    <th key={idx} className="p-2 w-12 text-slate-700 truncate font-semibold" title={l}>
                      {l.substring(0, 4)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {activeMatrix.map((row, rIdx) => (
                  <tr key={rIdx}>
                    <td className="p-2 font-sans font-semibold text-slate-700 text-left truncate max-w-[120px]" title={labels[rIdx]}>
                      {labels[rIdx]}
                    </td>
                    {row.map((val, cIdx) => {
                      const isDiag = rIdx === cIdx;
                      let bg = 'bg-slate-50 text-slate-400';
                      if (val > 0) {
                        bg = isDiag ? 'bg-blue-600 text-white font-bold' : 'bg-rose-100 text-rose-800 font-bold';
                      }
                      return (
                        <td key={cIdx} className={`p-2 border border-white rounded ${bg}`}>
                          {val}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-xs text-slate-400 text-center py-6">No matrix data available.</p>
        )}
      </div>

      {/* Class-wise Performance Breakdown */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <h3 className="font-bold text-slate-900 text-base mb-2">Class-Wise Precision, Recall, and F1 Breakdown</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3">Legal Category</th>
                <th className="p-3 text-center">Orig Precision</th>
                <th className="p-3 text-center">Aug Precision</th>
                <th className="p-3 text-center">Orig Recall</th>
                <th className="p-3 text-center">Aug Recall</th>
                <th className="p-3 text-center">Orig F1</th>
                <th className="p-3 text-center">Aug F1</th>
                <th className="p-3 text-center">F1 Delta</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {labels.map((lbl) => {
                const oData = origClf[lbl] || {};
                const aData = augClf[lbl] || {};
                const f1Diff = (aData['f1-score'] || 0) - (oData['f1-score'] || 0);
                return (
                  <tr key={lbl} className="hover:bg-slate-50">
                    <td className="p-3 font-medium text-slate-800">{lbl}</td>
                    <td className="p-3 text-center text-slate-600">{(oData['precision'] || 0).toFixed(3)}</td>
                    <td className="p-3 text-center font-medium text-slate-800">{(aData['precision'] || 0).toFixed(3)}</td>
                    <td className="p-3 text-center text-slate-600">{(oData['recall'] || 0).toFixed(3)}</td>
                    <td className="p-3 text-center font-medium text-slate-800">{(aData['recall'] || 0).toFixed(3)}</td>
                    <td className="p-3 text-center text-slate-600">{(oData['f1-score'] || 0).toFixed(3)}</td>
                    <td className="p-3 text-center font-bold text-brand-600">{(aData['f1-score'] || 0).toFixed(3)}</td>
                    <td className={`p-3 text-center font-mono font-bold ${f1Diff >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                      {f1Diff >= 0 ? `+${f1Diff.toFixed(3)}` : f1Diff.toFixed(3)}
                    </td>
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
