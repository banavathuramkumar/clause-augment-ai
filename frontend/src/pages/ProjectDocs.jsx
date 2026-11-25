import React from 'react';
import { BookOpen, ShieldCheck, Sparkles, Scale, Database, Cpu } from 'lucide-react';

export default function ProjectDocs() {
  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Title */}
      <div className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm">
        <h2 className="text-2xl font-bold text-slate-900">ClauseAugment AI: Architecture & Academic Documentation</h2>
        <p className="text-xs text-slate-500 mt-1">
          A controlled legal NLP data augmentation framework and leakage-free benchmark pipeline for commercial contract clause classification.
        </p>
      </div>

      {/* 1. Problem Statement */}
      <section className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
        <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <Scale className="w-5 h-5 text-brand-600" />
          <span>1. Problem Statement & Motivation</span>
        </h3>
        <p className="text-xs text-slate-700 leading-relaxed">
          Supervised classification of contractual clauses suffers heavily from data scarcity and severe stylistic overfitting.
          Commercial contracts are drafted across diverse drafting traditions, jurisdictional nuances, and organizational templates.
          However, naive generic data augmentation techniques (such as unrestricted back-translation or random word masking) frequently alter
          imperative legal obligations—inverting negations, substituting precise terms of art (e.g., swapping "indemnify" for "compensate"), or
          dropping conditional triggers ("unless", "provided that").
        </p>
        <p className="text-xs text-slate-700 leading-relaxed">
          <b>ClauseAugment AI</b> implements an explainable, algorithmic legal augmentation pipeline coupled with a strict semantic validation
          engine and a zero-leakage training harness to evaluate whether controlled augmentation genuinely improves classifier generalization and robustness.
        </p>
      </section>

      {/* 2. Augmentation Algorithms & Guardrails */}
      <section className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
        <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-brand-600" />
          <span>2. Controlled Augmentation Algorithms</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
            <span className="font-bold text-slate-800">A. Hugging Face Transformer Paraphrasing</span>
            <p className="text-slate-600">
              Controlled sequence-to-sequence paraphrasing using Hugging Face Transformers (T5/FLAN-T5 architecture).
              Enforces strict legal parameter controls (temperature, top-p, max/min length, repetition penalty) while
              preserving obligations, negations, party names, and dates.
            </p>
          </div>
          <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
            <span className="font-bold text-slate-800">B. NLPAug Word-Level Augmentation</span>
            <p className="text-slate-600">
              Integrates NLPAug for context-preserving lexical and synonym transformations with strict legal domain stopword filters.
            </p>
          </div>
          <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
            <span className="font-bold text-slate-800">C. spaCy Syntactic Restructuring</span>
            <p className="text-slate-600">
              Uses spaCy linguistic dependency parsing to safely reorder independent contractual conditions,
              apply introductory phrase shifts (<i>"In the event that" &harr; "If"</i>), and perform active/passive conversions.
            </p>
          </div>
          <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
            <span className="font-bold text-slate-800">D. Synonym Replacement & Random Operators</span>
            <p className="text-slate-600">
              WordNet-backed synonym replacement, safe modifier insertion, and coordinate term swaps with entity guardrails.
            </p>
          </div>
          <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
            <span className="font-bold text-slate-800">E. Sentence Restructuring</span>
            <p className="text-slate-600">
              Executes controlled syntactic transpositions: introductory adverbial clauses (<i>"In the event that" &harr; "If"</i>),
              subordinate phrase transpositions, and active/passive obligation conversions.
            </p>
          </div>
          <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
            <span className="font-bold text-slate-800">F. Back Translation</span>
            <p className="text-slate-600">
              Provides an optional modular translation interface. When offline or without local weights, it reports disabled status rather than fabricating synthetic data.
            </p>
          </div>
        </div>
      </section>

      {/* 3. Zero Leakage Methodology */}
      <section className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
        <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-emerald-600" />
          <span>3. Data Leakage Prevention Protocol</span>
        </h3>
        <p className="text-xs text-slate-700 leading-relaxed">
          A common methodological flaw in text augmentation research is augmenting the entire dataset prior to splitting, or fitting feature
          extractors on augmented corpora that contain variations of test instances. ClauseAugment AI strictly enforces four golden rules:
        </p>
        <ol className="list-decimal list-inside text-xs text-slate-700 space-y-1.5 pl-2">
          <li><b>Partition First:</b> The original clause corpus is stratified into training and held-out test splits prior to any augmentation.</li>
          <li><b>Training-Only Augmentation:</b> Augmentation algorithms are invoked exclusively on clauses belonging to the training partition. All variations of a clause remain bound to the training partition.</li>
          <li><b>Unseen Test Partition:</b> The test set consists strictly of original, un-augmented clauses to measure genuine generalization.</li>
          <li><b>Isolated Feature Fitting:</b> TF-IDF vectorizers are fitted solely on training partition instances without any exposure to test clauses.</li>
        </ol>
      </section>

      {/* 4. Supported Legal Categories */}
      <section className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
        <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <Database className="w-5 h-5 text-brand-600" />
          <span>4. 10 Commercial Legal Categories</span>
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-[11px]">
          {[
            'Confidentiality', 'Indemnification', 'Termination', 'Liability',
            'Governing Law', 'Payment', 'Force Majeure', 'Dispute Resolution',
            'Intellectual Property', 'Data Protection'
          ].map((cat) => (
            <div key={cat} className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 font-semibold text-center">
              {cat}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
