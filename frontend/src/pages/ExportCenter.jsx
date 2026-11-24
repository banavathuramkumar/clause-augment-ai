import React from 'react';
import {
  Download,
  FileSpreadsheet,
  FileText,
  FileCode,
  Image,
  Package,
  Layers,
  CheckCircle2
} from 'lucide-react';
import { api } from '../services/api';

export default function ExportCenter({ dataset, selectedExperiment, experiments }) {
  const exp = selectedExperiment || (experiments && experiments.length > 0 ? experiments[0] : null);

  const datasetExports = [
    {
      title: 'Original Dataset (CSV)',
      desc: 'Base legal benchmark corpus with clause_id, clause_text, and clause_type.',
      icon: FileSpreadsheet,
      url: api.getExportUrl('original_csv', dataset?.id),
      filename: `${dataset?.id}_original_clauses.csv`,
      color: 'blue'
    },
    {
      title: 'Full Augmented Dataset (CSV)',
      desc: 'All generated variations with technique metadata, status, and similarity scores.',
      icon: Layers,
      url: api.getExportUrl('augmented_csv', dataset?.id),
      filename: `${dataset?.id}_augmented_clauses.csv`,
      color: 'indigo'
    },
    {
      title: 'Accepted Variations Only (CSV)',
      desc: 'Only validated and approved variations ready for downstream model training.',
      icon: CheckCircle2,
      url: api.getExportUrl('accepted_csv', dataset?.id),
      filename: `${dataset?.id}_accepted_clauses.csv`,
      color: 'emerald'
    },
    {
      title: 'Rejected Variations (CSV)',
      desc: 'Flagged or rejected variations with explicit guardrail failure explanations.',
      icon: FileText,
      url: api.getExportUrl('rejected_csv', dataset?.id),
      filename: `${dataset?.id}_rejected_clauses.csv`,
      color: 'rose'
    },
    {
      title: 'Unified Research Corpus (JSON)',
      desc: 'Full hierarchical JSON document containing dataset metadata, original, and augmented clauses.',
      icon: FileCode,
      url: api.getExportUrl('dataset_json', dataset?.id),
      filename: `${dataset?.id}_dataset.json`,
      color: 'purple'
    }
  ];

  const modelExports = exp ? [
    {
      title: 'Academic Evaluation Report (PDF)',
      desc: 'Formal PDF evaluation summary with comparative tables and zero-leakage methodology.',
      icon: FileText,
      url: api.getExportUrl('evaluation_pdf', '', exp.id),
      filename: `${exp.id}_evaluation_report.pdf`,
      color: 'blue'
    },
    {
      title: 'Classification Report (CSV)',
      desc: 'Class-by-class precision, recall, f1-score, and support metrics for both models.',
      icon: FileSpreadsheet,
      url: api.getExportUrl('classification_report_csv', '', exp.id),
      filename: `${exp.id}_classification_report.csv`,
      color: 'indigo'
    },
    {
      title: 'Confusion Matrix Heatmap (PNG)',
      desc: 'High-resolution publication-ready confusion matrix visualization.',
      icon: Image,
      url: api.getExportUrl('confusion_matrix_png', '', exp.id),
      filename: `${exp.id}_confusion_matrices.png`,
      color: 'emerald'
    },
    {
      title: 'Trained Model Artifact (.joblib)',
      desc: 'Serialized scikit-learn TF-IDF pipeline for direct deployment and reproducible inference.',
      icon: Package,
      url: api.getExportUrl('trained_model', '', exp.id),
      filename: `${exp.id}_model.joblib`,
      color: 'amber'
    }
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm">
        <h2 className="text-xl font-bold text-slate-900">Export & Reproducibility Center</h2>
        <p className="text-xs text-slate-500 mt-1 max-w-2xl">
          Download standardized CSV/JSON datasets, publication-quality PDF reports, confusion matrix images,
          and trained scikit-learn pipeline artifacts.
        </p>
      </div>

      {/* Dataset Artifacts */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-slate-900">1. Dataset & Augmentation Artifacts</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {datasetExports.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div key={idx} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between hover:border-brand-300 transition">
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="p-2 rounded-lg bg-slate-100 text-slate-700">
                      <Icon className="w-4 h-4 text-brand-600" />
                    </div>
                    <h4 className="text-xs font-bold text-slate-900">{item.title}</h4>
                  </div>
                  <p className="text-[11px] text-slate-500 mb-4 leading-normal">{item.desc}</p>
                </div>
                <a
                  href={item.url}
                  download={item.filename}
                  className="flex items-center justify-center space-x-1.5 w-full py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 font-semibold text-xs rounded-lg border border-slate-200 transition"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download Artifact</span>
                </a>
              </div>
            );
          })}
        </div>
      </div>

      {/* Model & Evaluation Artifacts */}
      <div className="space-y-3 pt-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900">2. Evaluation & Model Artifacts</h3>
          {exp && (
            <span className="text-xs text-slate-500 font-mono">
              Bound to: {exp.name} ({exp.model_name})
            </span>
          )}
        </div>

        {exp ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {modelExports.map((item, idx) => {
              const Icon = item.icon;
              return (
                <div key={idx} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between hover:border-brand-300 transition">
                  <div>
                    <div className="flex items-center space-x-2 mb-2">
                      <div className="p-2 rounded-lg bg-slate-100 text-slate-700">
                        <Icon className="w-4 h-4 text-brand-600" />
                      </div>
                      <h4 className="text-xs font-bold text-slate-900">{item.title}</h4>
                    </div>
                    <p className="text-[11px] text-slate-500 mb-4 leading-normal">{item.desc}</p>
                  </div>
                  <a
                    href={item.url}
                    download={item.filename}
                    className="flex items-center justify-center space-x-1.5 w-full py-2 bg-brand-50 hover:bg-brand-100 text-brand-700 font-semibold text-xs rounded-lg border border-brand-200 transition"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download Artifact</span>
                  </a>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="p-6 bg-slate-50 border border-slate-200 rounded-xl text-center text-xs text-slate-500">
            Train a model first to generate evaluation reports and downloadable weights.
          </div>
        )}
      </div>
    </div>
  );
}
