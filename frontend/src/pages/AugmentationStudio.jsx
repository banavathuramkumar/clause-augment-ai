import React, { useState, useEffect } from 'react';
import { Sparkles, Play, CheckCircle2, AlertTriangle, XCircle, Filter, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

const TECHNIQUES = [
  { id: 'transformer_paraphrase', name: 'Transformer Paraphrasing', desc: 'Controlled Hugging Face T5/FLAN-T5 text-to-text paraphraser with legal preservation' },
  { id: 'nlpaug_synonym', name: 'NLPAug Word Augmentation', desc: 'Contextual synonym replacement powered by NLPAug with domain stopword guards' },
  { id: 'synonym_replacement', name: 'Synonym Replacement', desc: 'Contextual synonym replacement preserving legal terms' },
  { id: 'random_insertion', name: 'Random Insertion', desc: 'Inserts non-critical legal particles and qualifiers' },
  { id: 'random_swap', name: 'Random Swap', desc: 'Permutes coordinate adjectives or clauses' },
  { id: 'random_deletion', name: 'Random Deletion', desc: 'Safely removes non-critical redundant tokens' },
  { id: 'sentence_restructuring', name: 'Sentence Restructuring', desc: 'Controlled grammatical, conditional, and syntax transformations via spaCy' },
  { id: 'back_translation', name: 'Back Translation', desc: 'Offline translation model (disabled if models absent)' },
];

export default function AugmentationStudio({ dataset, onAugmentationsGenerated }) {
  const [selectedTechniques, setSelectedTechniques] = useState([
    'transformer_paraphrase',
    'nlpaug_synonym',
    'synonym_replacement',
    'sentence_restructuring'
  ]);
  const [multiplier, setMultiplier] = useState(1);
  const [randomSeed, setRandomSeed] = useState(42);
  const [similarityThreshold, setSimilarityThreshold] = useState(0.75);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [results, setResults] = useState([]);
  const [filterStatus, setFilterStatus] = useState('');
  const [filterTechnique, setFilterTechnique] = useState('');
  const [notification, setNotification] = useState(null);

  const categories = Object.keys(dataset?.stats?.category_distribution || {});

  useEffect(() => {
    if (dataset?.id) {
      loadResults(dataset.id);
    }
  }, [dataset?.id, filterStatus, filterTechnique]);

  const loadResults = async (datasetId) => {
    try {
      const data = await api.getAugmentationResults(datasetId, filterStatus, filterTechnique, 200, 0);
      setResults(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleTechnique = (techId) => {
    setSelectedTechniques((prev) =>
      prev.includes(techId) ? prev.filter((t) => t !== techId) : [...prev, techId]
    );
  };

  const handleToggleCategory = (cat) => {
    setSelectedCategories((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  };

  const handleGenerate = async () => {
    if (!dataset?.id) return;
    if (selectedTechniques.length === 0) {
      setNotification({ type: 'error', message: 'Please select at least one augmentation algorithm.' });
      return;
    }

    setGenerating(true);
    setNotification(null);
    try {
      const payload = {
        dataset_id: dataset.id,
        techniques: selectedTechniques,
        multiplier,
        selected_categories: selectedCategories.length > 0 ? selectedCategories : null,
        random_seed: randomSeed,
        similarity_threshold: similarityThreshold,
        auto_validate: true,
      };

      const created = await api.generateAugmentation(payload);
      setNotification({
        type: 'success',
        message: `Successfully generated and validated ${created.length} new contract clause variations!`,
      });
      loadResults(dataset.id);
      if (onAugmentationsGenerated) onAugmentationsGenerated();
    } catch (err) {
      setNotification({ type: 'error', message: err.message || 'Augmentation generation failed.' });
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Studio Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Contract Clause Augmentation Studio</h2>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl">
            Controlled perturbation engine. Every algorithm enforces strict immutability on legal obligations,
            modal verbs, parties, and negations to avoid meaning distortion.
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating || !dataset?.id}
          className="flex items-center space-x-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-brand-600/20 disabled:opacity-50 transition shrink-0"
        >
          <Sparkles className="w-4 h-4" />
          <span>{generating ? 'Synthesizing Clauses...' : 'Generate Variations'}</span>
        </button>
      </div>

      {notification && (
        <div
          className={`p-3 rounded-lg text-xs flex items-center space-x-2 ${
            notification.type === 'success'
              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
              : 'bg-rose-50 text-rose-700 border border-rose-200'
          }`}
        >
          {notification.type === 'success' ? <CheckCircle2 className="w-4 h-4 shrink-0" /> : <AlertTriangle className="w-4 h-4 shrink-0" />}
          <span>{notification.message}</span>
        </div>
      )}

      {/* Configuration Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Algorithms Checklist */}
        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm">Select Augmentation Techniques</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {TECHNIQUES.map((tech) => {
              const active = selectedTechniques.includes(tech.id);
              return (
                <div
                  key={tech.id}
                  onClick={() => handleToggleTechnique(tech.id)}
                  className={`p-3 rounded-lg border text-left cursor-pointer transition ${
                    active
                      ? 'border-brand-500 bg-brand-50/30'
                      : 'border-slate-200 bg-slate-50/40 hover:bg-slate-100/50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-bold text-slate-800">{tech.name}</span>
                    <input
                      type="checkbox"
                      checked={active}
                      onChange={() => {}}
                      className="rounded text-brand-600 focus:ring-brand-500 pointer-events-none"
                    />
                  </div>
                  <p className="text-[11px] text-slate-500 leading-tight">{tech.desc}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Hyperparameters & Category Scoping */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm">Hyperparameters & Scope</h3>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Augmentation Multiplier</label>
              <div className="grid grid-cols-4 gap-2">
                {[1, 2, 3, 5].map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => setMultiplier(m)}
                    className={`py-1.5 text-xs font-bold rounded-lg border transition ${
                      multiplier === m
                        ? 'bg-brand-600 text-white border-brand-600'
                        : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    {m}x
                  </button>
                ))}
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="text-xs font-semibold text-slate-700">Similarity Threshold</label>
                <span className="text-xs font-mono font-bold text-brand-600">{similarityThreshold}</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="0.95"
                step="0.05"
                value={similarityThreshold}
                onChange={(e) => setSimilarityThreshold(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Reproducibility Seed</label>
              <input
                type="number"
                value={randomSeed}
                onChange={(e) => setRandomSeed(parseInt(e.target.value) || 0)}
                className="w-full text-xs p-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 font-mono"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Results Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-50/50">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-800 text-sm">Generated Variations Catalog</span>
            <span className="text-xs text-slate-500">({results.length} records)</span>
          </div>

          <div className="flex items-center space-x-2">
            <select
              value={filterTechnique}
              onChange={(e) => setFilterTechnique(e.target.value)}
              className="text-xs border border-slate-300 rounded-lg p-1.5 focus:ring-brand-500 focus:border-brand-500"
            >
              <option value="">All Techniques</option>
              {TECHNIQUES.map((t) => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>

            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="text-xs border border-slate-300 rounded-lg p-1.5 focus:ring-brand-500 focus:border-brand-500"
            >
              <option value="">All Statuses</option>
              <option value="Accepted">Accepted</option>
              <option value="Needs Review">Needs Review</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto max-h-[500px]">
          <table className="w-full text-left border-collapse text-xs">
            <thead className="bg-slate-100 text-slate-700 sticky top-0 z-10 font-semibold border-b border-slate-200">
              <tr>
                <th className="p-3 w-28">Status</th>
                <th className="p-3 w-36">Technique</th>
                <th className="p-3 w-32">Category</th>
                <th className="p-3">Original Clause</th>
                <th className="p-3">Augmented Variation</th>
                <th className="p-3 w-24 text-center">Cosine Sim</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {results.map((aug) => {
                const statusStyles = {
                  Accepted: 'bg-emerald-50 text-emerald-700 border-emerald-200',
                  'Needs Review': 'bg-amber-50 text-amber-700 border-amber-200',
                  Rejected: 'bg-rose-50 text-rose-700 border-rose-200',
                };
                return (
                  <tr key={aug.id} className="hover:bg-slate-50/80 transition">
                    <td className="p-3">
                      <span className={`inline-block px-2 py-0.5 rounded-full text-[10px] font-bold border ${statusStyles[aug.status] || 'bg-slate-100'}`}>
                        {aug.status}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-[11px] text-slate-600">
                      {aug.technique.replace('_', ' ')}
                    </td>
                    <td className="p-3 font-medium text-slate-700">{aug.clause_type}</td>
                    <td className="p-3 text-slate-600 font-sans max-w-xs">{aug.original_text}</td>
                    <td className="p-3 text-slate-900 font-medium font-sans max-w-sm">{aug.augmented_text}</td>
                    <td className="p-3 text-center font-mono font-bold text-slate-800">
                      {(aug.similarity_score * 100).toFixed(1)}%
                    </td>
                  </tr>
                );
              })}
              {results.length === 0 && (
                <tr>
                  <td colSpan={6} className="p-6 text-center text-slate-400">
                    No variations generated yet. Click "Generate Variations" above.
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
