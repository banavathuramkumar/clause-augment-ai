import React, { useState } from 'react';
import { Cpu, Play, CheckCircle2, ShieldCheck, AlertCircle, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

const MODELS = [
  { id: 'LogisticRegression', name: 'Logistic Regression', desc: 'L2-regularized multinomial classifier with class-weight balancing.' },
  { id: 'LinearSVM', name: 'Linear SVM', desc: 'Linear Support Vector Classifier optimizing max-margin hyperplane.' },
  { id: 'MultinomialNB', name: 'Multinomial Naive Bayes', desc: 'Probabilistic n-gram frequency classifier with Laplace smoothing.' },
  { id: 'RandomForest', name: 'Random Forest', desc: 'Ensemble of 100 decision trees with feature subsampling.' },
];

export default function ModelTraining({ dataset, onExperimentTrained, onSelectExperiment }) {
  const [modelName, setModelName] = useState('LogisticRegression');
  const [featureType, setFeatureType] = useState('tfidf_unigram');
  const [trainRatio, setTrainRatio] = useState(0.8);
  const [randomState, setRandomState] = useState(42);
  const [useApprovedOnly, setUseApprovedOnly] = useState(false);
  const [training, setTraining] = useState(false);
  const [notification, setNotification] = useState(null);

  const handleTrain = async () => {
    if (!dataset?.id) return;
    setTraining(true);
    setNotification(null);

    try {
      const payload = {
        dataset_id: dataset.id,
        model_name: modelName,
        feature_type: featureType,
        train_ratio: trainRatio,
        random_state: randomState,
        use_approved_only: useApprovedOnly,
      };

      const experiment = await api.runTraining(payload);
      setNotification({
        type: 'success',
        message: `Experiment "${experiment.name}" trained successfully! Test Accuracy: ${(experiment.metrics?.Augmented?.accuracy * 100).toFixed(1)}%`,
      });

      if (onExperimentTrained) onExperimentTrained(experiment);
    } catch (err) {
      setNotification({ type: 'error', message: err.message || 'Training failed.' });
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Machine Learning Training Engine</h2>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl">
            Trains dual models under identical conditions: <b>Experiment A</b> (Original Data) vs <b>Experiment B</b> (Augmented Data).
            Evaluated on an identical held-out test partition with strict zero data leakage.
          </p>
        </div>
        <button
          onClick={handleTrain}
          disabled={training || !dataset?.id}
          className="flex items-center space-x-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-brand-600/20 disabled:opacity-50 transition shrink-0"
        >
          <Play className="w-4 h-4 fill-current" />
          <span>{training ? 'Training Both Models...' : 'Run Comparative Experiment'}</span>
        </button>
      </div>

      {notification && (
        <div
          className={`p-4 rounded-xl text-xs flex items-center justify-between ${
            notification.type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
              : 'bg-rose-50 text-rose-800 border border-rose-200'
          }`}
        >
          <div className="flex items-center space-x-2">
            {notification.type === 'success' ? <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" /> : <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />}
            <span className="font-medium">{notification.message}</span>
          </div>
        </div>
      )}

      {/* Model Selection & Feature Extraction */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Model choice */}
        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm">Select Classification Architecture</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {MODELS.map((m) => {
              const active = modelName === m.id;
              return (
                <div
                  key={m.id}
                  onClick={() => setModelName(m.id)}
                  className={`p-3.5 rounded-lg border text-left cursor-pointer transition ${
                    active
                      ? 'border-brand-600 bg-brand-50/40 shadow-sm'
                      : 'border-slate-200 bg-slate-50/40 hover:bg-slate-100/50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-xs font-bold ${active ? 'text-brand-700' : 'text-slate-800'}`}>
                      {m.name}
                    </span>
                    <input
                      type="radio"
                      checked={active}
                      onChange={() => {}}
                      className="text-brand-600 focus:ring-brand-500 pointer-events-none"
                    />
                  </div>
                  <p className="text-[11px] text-slate-500 leading-normal">{m.desc}</p>
                </div>
              );
            })}
          </div>

          <div className="pt-2">
            <h3 className="font-bold text-slate-900 text-sm mb-2">Feature Representation</h3>
            <div className="grid grid-cols-2 gap-3">
              {[
                { id: 'tfidf_unigram', label: 'TF-IDF Unigrams (1-gram)', desc: 'Standard word frequency-inverse document frequency' },
                { id: 'tfidf_bigram', label: 'TF-IDF Unigrams + Bigrams (1,2-gram)', desc: 'Captures legal word pairs e.g. "hold harmless", "force majeure"' },
              ].map((f) => (
                <div
                  key={f.id}
                  onClick={() => setFeatureType(f.id)}
                  className={`p-3 rounded-lg border cursor-pointer transition ${
                    featureType === f.id
                      ? 'border-brand-600 bg-brand-50/40 shadow-sm'
                      : 'border-slate-200 bg-slate-50/40 hover:bg-slate-100/50'
                  }`}
                >
                  <span className={`text-xs font-bold block ${featureType === f.id ? 'text-brand-700' : 'text-slate-800'}`}>
                    {f.label}
                  </span>
                  <p className="text-[11px] text-slate-500 mt-1">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Hyperparameters & Leakage Shield */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm">Experimental Controls</h3>

          <div className="space-y-3">
            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="text-xs font-semibold text-slate-700">Train/Test Split Ratio</label>
                <span className="text-xs font-mono font-bold text-brand-600">{(trainRatio * 100).toFixed(0)}% Train / {((1 - trainRatio) * 100).toFixed(0)}% Test</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="0.9"
                step="0.05"
                value={trainRatio}
                onChange={(e) => setTrainRatio(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Reproducibility Seed</label>
              <input
                type="number"
                value={randomState}
                onChange={(e) => setRandomState(parseInt(e.target.value) || 0)}
                className="w-full text-xs p-2 border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 font-mono"
              />
            </div>

            <div className="pt-2">
              <label className="flex items-start space-x-2.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={useApprovedOnly}
                  onChange={(e) => setUseApprovedOnly(e.target.checked)}
                  className="mt-0.5 rounded text-brand-600 focus:ring-brand-500"
                />
                <div>
                  <span className="text-xs font-semibold text-slate-800">Only Use Explicitly Approved Clauses</span>
                  <p className="text-[11px] text-slate-500 mt-0.5">Excludes pending variations requiring human review.</p>
                </div>
              </label>
            </div>
          </div>

          {/* Leakage Protection Guarantee */}
          <div className="mt-4 p-3.5 bg-emerald-50 rounded-lg border border-emerald-200 space-y-1.5">
            <div className="flex items-center space-x-1.5 text-emerald-800 font-bold text-xs">
              <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>Leakage-Free Guarantee</span>
            </div>
            <p className="text-[11px] text-emerald-700 leading-normal">
              1. Split original data before any augmentation.<br/>
              2. Augment strictly training partition clauses.<br/>
              3. Fit TF-IDF exclusively on training instances.<br/>
              4. Evaluate both on identical held-out original test set.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
