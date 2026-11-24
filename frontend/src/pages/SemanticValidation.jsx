import React, { useState, useEffect } from 'react';
import { ShieldCheck, Check, X, AlertTriangle, CheckCircle2, XCircle, Filter, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

export default function SemanticValidation({ dataset, onStatusChanged }) {
  const [results, setResults] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [filterStatus, setFilterStatus] = useState('Needs Review');
  const [loading, setLoading] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    if (dataset?.id) {
      loadResults(dataset.id, filterStatus);
    }
  }, [dataset?.id, filterStatus]);

  const loadResults = async (datasetId, status) => {
    setLoading(true);
    try {
      const data = await api.getAugmentationResults(datasetId, status, '', 200, 0);
      setResults(data);
      setSelectedIds([]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedIds(results.map((r) => r.id));
    } else {
      setSelectedIds([]);
    }
  };

  const handleToggleSelect = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const handleBatchApprove = async () => {
    if (selectedIds.length === 0) return;
    try {
      await api.approveAugmentations(selectedIds, 'Manually reviewed and approved by researcher');
      setNotification({ type: 'success', message: `Approved ${selectedIds.length} clause variations.` });
      loadResults(dataset.id, filterStatus);
      if (onStatusChanged) onStatusChanged();
    } catch (err) {
      setNotification({ type: 'error', message: err.message });
    }
  };

  const handleBatchReject = async () => {
    if (selectedIds.length === 0) return;
    try {
      await api.rejectAugmentations(selectedIds, rejectReason || 'Rejected during semantic review');
      setNotification({ type: 'success', message: `Rejected ${selectedIds.length} clause variations.` });
      setRejectReason('');
      loadResults(dataset.id, filterStatus);
      if (onStatusChanged) onStatusChanged();
    } catch (err) {
      setNotification({ type: 'error', message: err.message });
    }
  };

  const handleSingleAction = async (id, action) => {
    try {
      if (action === 'approve') {
        await api.approveAugmentations([id], 'Individually approved');
      } else {
        await api.rejectAugmentations([id], 'Individually rejected');
      }
      loadResults(dataset.id, filterStatus);
      if (onStatusChanged) onStatusChanged();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Semantic & Legal Guardrails Validation</h2>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl">
            Semantic similarity alone does not constitute legal equivalence. Review flagged variations where
            modals, entities, or threshold bounds require human validation.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleBatchApprove}
            disabled={selectedIds.length === 0}
            className="flex items-center space-x-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow disabled:opacity-40 transition"
          >
            <Check className="w-3.5 h-3.5" />
            <span>Approve Selected ({selectedIds.length})</span>
          </button>
          <button
            onClick={handleBatchReject}
            disabled={selectedIds.length === 0}
            className="flex items-center space-x-1.5 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-semibold shadow disabled:opacity-40 transition"
          >
            <X className="w-3.5 h-3.5" />
            <span>Reject Selected ({selectedIds.length})</span>
          </button>
        </div>
      </div>

      {notification && (
        <div
          className={`p-3 rounded-lg text-xs flex items-center space-x-2 ${
            notification.type === 'success'
              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
              : 'bg-rose-50 text-rose-700 border border-rose-200'
          }`}
        >
          {notification.type === 'success' ? <CheckCircle2 className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
          <span>{notification.message}</span>
        </div>
      )}

      {/* Review Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-50/50">
          <div className="flex items-center space-x-3">
            <span className="font-bold text-slate-800 text-sm">Review Queue</span>
            <div className="flex items-center space-x-1 bg-slate-200/60 p-0.5 rounded-lg text-xs font-medium">
              {['Needs Review', 'Accepted', 'Rejected', ''].map((st) => (
                <button
                  key={st}
                  onClick={() => setFilterStatus(st)}
                  className={`px-3 py-1 rounded-md transition ${
                    filterStatus === st
                      ? 'bg-white text-slate-900 shadow-sm font-semibold'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {st || 'All'}
                </button>
              ))}
            </div>
          </div>

          <span className="text-xs text-slate-500">{results.length} records currently displayed</span>
        </div>

        <div className="overflow-x-auto max-h-[600px]">
          <table className="w-full text-left border-collapse text-xs">
            <thead className="bg-slate-100 text-slate-700 sticky top-0 z-10 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3 w-10">
                  <input
                    type="checkbox"
                    checked={results.length > 0 && selectedIds.length === results.length}
                    onChange={handleSelectAll}
                    className="rounded text-brand-600 focus:ring-brand-500"
                  />
                </th>
                <th className="p-3 w-28">Status</th>
                <th className="p-3 w-28">Technique</th>
                <th className="p-3 w-28">Category</th>
                <th className="p-3">Original vs Augmented Text</th>
                <th className="p-3 w-64">Validation Reason / Guardrails</th>
                <th className="p-3 w-20 text-center">Cosine Sim</th>
                <th className="p-3 w-24 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {results.map((aug) => {
                const isSelected = selectedIds.includes(aug.id);
                return (
                  <tr key={aug.id} className={`hover:bg-slate-50/80 transition ${isSelected ? 'bg-brand-50/30' : ''}`}>
                    <td className="p-3">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => handleToggleSelect(aug.id)}
                        className="rounded text-brand-600 focus:ring-brand-500"
                      />
                    </td>
                    <td className="p-3">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                          aug.status === 'Accepted'
                            ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                            : aug.status === 'Needs Review'
                            ? 'bg-amber-50 text-amber-700 border-amber-200'
                            : 'bg-rose-50 text-rose-700 border-rose-200'
                        }`}
                      >
                        {aug.status}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-[11px] text-slate-600">{aug.technique}</td>
                    <td className="p-3 font-medium text-slate-700">{aug.clause_type}</td>
                    <td className="p-3 space-y-1.5 max-w-md">
                      <div className="text-slate-500 text-[11px] bg-slate-50 p-2 rounded border border-slate-100">
                        <span className="font-semibold text-slate-700 block text-[10px] uppercase">Original:</span>
                        {aug.original_text}
                      </div>
                      <div className="text-slate-900 font-medium text-[11px] bg-brand-50/30 p-2 rounded border border-brand-100">
                        <span className="font-semibold text-brand-700 block text-[10px] uppercase">Augmented:</span>
                        {aug.augmented_text}
                      </div>
                    </td>
                    <td className="p-3 text-[11px] text-slate-600 leading-snug">
                      {aug.validation_reason || 'Verified'}
                    </td>
                    <td className="p-3 text-center font-mono font-bold text-slate-800">
                      {(aug.similarity_score * 100).toFixed(1)}%
                    </td>
                    <td className="p-3 text-center">
                      <div className="flex items-center justify-center space-x-1">
                        <button
                          onClick={() => handleSingleAction(aug.id, 'approve')}
                          title="Approve"
                          className="p-1 rounded bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200"
                        >
                          <Check className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleSingleAction(aug.id, 'reject')}
                          title="Reject"
                          className="p-1 rounded bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200"
                        >
                          <X className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
              {results.length === 0 && (
                <tr>
                  <td colSpan={8} className="p-6 text-center text-slate-400">
                    No variations found in queue for filter "{filterStatus || 'All'}".
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
