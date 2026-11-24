import React, { useState, useEffect } from 'react';
import { Upload, Download, Search, Filter, AlertCircle, CheckCircle, FileSpreadsheet } from 'lucide-react';
import { api } from '../services/api';

export default function DatasetManagement({ dataset, onDatasetUpdated }) {
  const [clauses, setClauses] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');

  // Upload form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);

  useEffect(() => {
    if (dataset?.id) {
      loadClauses(dataset.id, selectedCategory);
    }
  }, [dataset?.id, selectedCategory]);

  const loadClauses = async (id, cat) => {
    try {
      const data = await api.getClauses(id, cat, 200, 0);
      setClauses(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || !name) {
      setUploadError('Please specify dataset name and select a valid CSV/JSON file.');
      return;
    }

    setUploading(true);
    setUploadError('');
    setUploadSuccess('');

    try {
      const formData = new FormData();
      formData.append('name', name);
      formData.append('description', description);
      formData.append('file', file);

      const newDs = await api.uploadDataset(formData);
      setUploadSuccess(`Successfully uploaded and validated "${newDs.name}" with ${newDs.total_clauses} clauses!`);
      setName('');
      setDescription('');
      setFile(null);
      if (onDatasetUpdated) onDatasetUpdated(newDs);
    } catch (err) {
      setUploadError(err.message || 'Failed to upload dataset.');
    } finally {
      setUploading(false);
    }
  };

  const filteredClauses = clauses.filter((c) =>
    c.clause_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.clause_id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const categories = Object.keys(dataset?.stats?.category_distribution || {});

  return (
    <div className="space-y-6">
      {/* Header and Download */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Legal Dataset Management</h2>
          <p className="text-xs text-slate-500 mt-1">
            Validate mandatory schema (<code>clause_id</code>, <code>clause_text</code>, <code>clause_type</code>), detect duplicates, and monitor class balance.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <a
            href={api.getExportUrl('original_csv', dataset?.id)}
            download
            className="flex items-center space-x-2 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-200 transition"
          >
            <Download className="w-4 h-4" />
            <span>Download CSV</span>
          </a>
          <a
            href={api.getExportUrl('dataset_json', dataset?.id)}
            download
            className="flex items-center space-x-2 px-3.5 py-2 bg-brand-50 hover:bg-brand-100 text-brand-700 rounded-lg text-xs font-semibold border border-brand-200 transition"
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>Download JSON</span>
          </a>
        </div>
      </div>

      {/* Dataset Statistics Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Total Clauses</p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{dataset?.total_clauses || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Active Categories</p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{dataset?.num_categories || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Avg Word Count</p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{dataset?.stats?.avg_word_count || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 text-center">
          <p className="text-xs text-slate-500 font-medium">Class Imbalance Ratio</p>
          <p className={`text-2xl font-bold mt-1 ${
            (dataset?.stats?.imbalance_ratio || 1) > 2 ? 'text-amber-600' : 'text-emerald-600'
          }`}>
            {dataset?.stats?.imbalance_ratio || 1.0}:1
          </p>
        </div>
      </div>

      {/* Upload Custom Dataset Section */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <h3 className="font-bold text-slate-900 text-base mb-1">Ingest Custom Legal Dataset</h3>
        <p className="text-xs text-slate-500 mb-4">
          Upload CSV or JSON files. Automatic deduplication and schema validation will be performed.
        </p>

        {uploadError && (
          <div className="mb-4 p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{uploadError}</span>
          </div>
        )}
        {uploadSuccess && (
          <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs rounded-lg flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 shrink-0" />
            <span>{uploadSuccess}</span>
          </div>
        )}

        <form onSubmit={handleUpload} className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Dataset Name *</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Master Services Agreement Corpus"
              className="w-full text-xs p-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Description</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional notes or source context"
              className="w-full text-xs p-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">File (.csv or .json) *</label>
            <div className="flex space-x-2">
              <input
                type="file"
                accept=".csv,.json"
                required
                onChange={(e) => setFile(e.target.files[0])}
                className="w-full text-xs text-slate-500 file:mr-2 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 cursor-pointer"
              />
              <button
                type="submit"
                disabled={uploading}
                className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold shadow disabled:opacity-50 shrink-0 flex items-center space-x-1"
              >
                <Upload className="w-3.5 h-3.5" />
                <span>{uploading ? 'Validating...' : 'Upload'}</span>
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Clause Explorer Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-50/50">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-800 text-sm">Clause Explorer</span>
            <span className="text-xs text-slate-500">({filteredClauses.length} records)</span>
          </div>

          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search clause text..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 pr-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 w-48 md:w-64"
              />
            </div>

            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="text-xs border border-slate-300 rounded-lg p-1.5 focus:ring-brand-500 focus:border-brand-500"
            >
              <option value="">All Categories ({dataset?.total_clauses})</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat} ({dataset?.stats?.category_distribution[cat]})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="overflow-x-auto max-h-[500px]">
          <table className="w-full text-left border-collapse text-xs">
            <thead className="bg-slate-100 text-slate-700 sticky top-0 z-10 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3 w-28">Clause ID</th>
                <th className="p-3 w-40">Category</th>
                <th className="p-3">Clause Text</th>
                <th className="p-3 w-20 text-center">Words</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredClauses.map((clause) => (
                <tr key={clause.id} className="hover:bg-slate-50/80 transition">
                  <td className="p-3 font-mono font-medium text-slate-600">{clause.clause_id}</td>
                  <td className="p-3">
                    <span className="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-brand-50 text-brand-700 border border-brand-200">
                      {clause.clause_type}
                    </span>
                  </td>
                  <td className="p-3 text-slate-800 leading-relaxed font-sans">{clause.clause_text}</td>
                  <td className="p-3 text-center text-slate-500">{clause.clause_text.split(' ').length}</td>
                </tr>
              ))}
              {filteredClauses.length === 0 && (
                <tr>
                  <td colSpan={4} className="p-6 text-center text-slate-400">
                    No matching clauses found.
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
