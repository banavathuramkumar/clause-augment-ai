import React, { useState } from 'react';
import { Play, Sparkles, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

const DEFAULT_SAMPLE_CLAUSE =
  "The Receiving Party shall maintain in strict confidence and shall not disclose to any third party any Confidential Information of the Disclosing Party without prior written consent.";

export default function TextPreprocessing() {
  const [text, setText] = useState(DEFAULT_SAMPLE_CLAUSE);
  const [removeStopwords, setRemoveStopwords] = useState(false);
  const [lemmatize, setLemmatize] = useState(false);
  const [preserveLegalTerms, setPreserveLegalTerms] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleProcess = async () => {
    if (!text.trim()) {
      setError('Please provide text to preprocess.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await api.runPreprocessing({
        text,
        remove_stopwords: removeStopwords,
        lemmatize,
        preserve_legal_terms: preserveLegalTerms,
      });
      setResult(res);
    } catch (err) {
      setError(err.message || 'Preprocessing failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <h2 className="text-xl font-bold text-slate-900">Legal Text Preprocessing Pipeline</h2>
        <p className="text-xs text-slate-500 mt-1 max-w-3xl">
          Unlike generic NLP preprocessing, legal text preprocessing must strictly preserve legal terminology,
          negations ("not", "never", "without"), modal verbs ("shall", "may", "must"), dates, and numeric obligations.
        </p>
      </div>

      {/* Editor & Configuration */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Input Text Box */}
        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold uppercase tracking-wider text-slate-700">Contract Clause Input</label>
            <button
              onClick={() => setText(DEFAULT_SAMPLE_CLAUSE)}
              className="text-xs text-brand-600 hover:underline"
            >
              Reset to Sample Clause
            </button>
          </div>

          <textarea
            rows={5}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type or paste contract clause text..."
            className="w-full text-xs font-sans p-3 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 leading-relaxed"
          />

          <div className="flex justify-end">
            <button
              onClick={handleProcess}
              disabled={loading}
              className="flex items-center space-x-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold shadow disabled:opacity-50 transition"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{loading ? 'Executing Pipeline...' : 'Run Preprocessing Pipeline'}</span>
            </button>
          </div>
        </div>

        {/* Pipeline Controls */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm">Pipeline Parameters</h3>

          <div className="space-y-3 pt-2">
            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={preserveLegalTerms}
                onChange={(e) => setPreserveLegalTerms(e.target.checked)}
                className="mt-0.5 rounded text-brand-600 focus:ring-brand-500"
              />
              <div>
                <span className="text-xs font-semibold text-slate-800">Preserve Legal Modal & Negation Rules</span>
                <p className="text-[11px] text-slate-500 mt-0.5">Protects "shall", "must", "not", "without", "except" from deletion.</p>
              </div>
            </label>

            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={removeStopwords}
                onChange={(e) => setRemoveStopwords(e.target.checked)}
                className="mt-0.5 rounded text-brand-600 focus:ring-brand-500"
              />
              <div>
                <span className="text-xs font-semibold text-slate-800">Filter Non-Critical Stopwords</span>
                <p className="text-[11px] text-slate-500 mt-0.5">Removes peripheral filler words while honoring legal protection.</p>
              </div>
            </label>

            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={lemmatize}
                onChange={(e) => setLemmatize(e.target.checked)}
                className="mt-0.5 rounded text-brand-600 focus:ring-brand-500"
              />
              <div>
                <span className="text-xs font-semibold text-slate-800">Morphological Lemmatization</span>
                <p className="text-[11px] text-slate-500 mt-0.5">Converts eligible inflected words into standard WordNet base lemmas.</p>
              </div>
            </label>
          </div>

          <div className="mt-4 p-3 bg-slate-50 rounded-lg border border-slate-200 text-[11px] text-slate-600 space-y-1">
            <span className="font-semibold text-slate-700 block">Default Operations:</span>
            <p>1. Unicode Normalization (Quotes, dashes)</p>
            <p>2. Whitespace & line-break compaction</p>
            <p>3. Punctuation boundary tokenization</p>
            <p>4. Legal sentence segmentation</p>
          </div>
        </div>
      </div>

      {/* Preprocessing Inspection Output */}
      {result && (
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-5">
          <div className="flex items-center justify-between border-b border-slate-200 pb-3">
            <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Pipeline Inspection Results</span>
            </h3>
            <div className="flex items-center space-x-4 text-xs font-mono text-slate-600">
              <span>Words: {result.original_word_count} &rarr; {result.processed_word_count}</span>
              <span>Tokens: {result.token_count}</span>
            </div>
          </div>

          {/* Processed Text Comparison Box */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">Original Text</p>
              <p className="text-xs text-slate-800 leading-relaxed">{result.original_text}</p>
            </div>
            <div className="p-3 bg-brand-50/50 rounded-lg border border-brand-200">
              <p className="text-[11px] font-bold uppercase tracking-wider text-brand-700 mb-1">Processed Output</p>
              <p className="text-xs text-slate-900 font-medium leading-relaxed">{result.processed_text}</p>
            </div>
          </div>

          {/* Operations breakdown */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Operations Applied</h4>
            <div className="flex flex-wrap gap-2">
              {result.operations_applied.map((op, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 bg-slate-100 text-slate-700 border border-slate-200 rounded-md text-xs font-medium"
                >
                  &bull; {op}
                </span>
              ))}
            </div>
          </div>

          {/* Token Chips */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Token Sequence View</h4>
            <div className="flex flex-wrap gap-1.5 p-3 bg-slate-50 rounded-lg border border-slate-200 max-h-48 overflow-y-auto">
              {result.tokens.map((tok, idx) => {
                const lower = tok.toLowerCase();
                const isModal = ['shall', 'may', 'must', 'will'].includes(lower);
                const isNeg = ['not', 'never', 'neither', 'nor', 'without', 'except', 'unless'].includes(lower);
                return (
                  <span
                    key={idx}
                    className={`px-2 py-0.5 rounded text-[11px] font-mono font-medium ${
                      isModal
                        ? 'bg-purple-100 text-purple-800 border border-purple-300'
                        : isNeg
                        ? 'bg-rose-100 text-rose-800 border border-rose-300'
                        : 'bg-white text-slate-700 border border-slate-200'
                    }`}
                  >
                    {tok}
                  </span>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
