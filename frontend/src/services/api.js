const BASE_URL = '/api';

export const api = {
  // Datasets
  async getDatasets() {
    const res = await fetch(`${BASE_URL}/datasets`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async uploadDataset(formData) {
    const res = await fetch(`${BASE_URL}/datasets/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getDataset(id) {
    const res = await fetch(`${BASE_URL}/datasets/${id}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getClauses(datasetId, category = '', limit = 100, offset = 0) {
    const params = new URLSearchParams({ limit, offset });
    if (category) params.append('category', category);
    const res = await fetch(`${BASE_URL}/datasets/${datasetId}/clauses?${params.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getExpansion(datasetId) {
    const res = await fetch(`${BASE_URL}/datasets/${datasetId}/expansion`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Preprocessing
  async runPreprocessing(payload) {
    const res = await fetch(`${BASE_URL}/preprocessing/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Augmentation
  async generateAugmentation(payload) {
    const res = await fetch(`${BASE_URL}/augmentation/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getAugmentationResults(datasetId, status = '', technique = '', limit = 100, offset = 0) {
    const params = new URLSearchParams({ dataset_id: datasetId, limit, offset });
    if (status) params.append('status', status);
    if (technique) params.append('technique', technique);
    const res = await fetch(`${BASE_URL}/augmentation/results?${params.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async approveAugmentations(clauseIds, reason = '') {
    const res = await fetch(`${BASE_URL}/augmentation/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ augmented_clause_ids: clauseIds, action: 'approve', reason }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async rejectAugmentations(clauseIds, reason = '') {
    const res = await fetch(`${BASE_URL}/augmentation/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ augmented_clause_ids: clauseIds, action: 'reject', reason }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Validation
  async runValidation(payload) {
    const res = await fetch(`${BASE_URL}/validation/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Training & Evaluation
  async runTraining(payload) {
    const res = await fetch(`${BASE_URL}/training/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getExperiments(datasetId = '') {
    const url = datasetId ? `${BASE_URL}/training/experiments?dataset_id=${datasetId}` : `${BASE_URL}/training/experiments`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getEvaluation(experimentId) {
    const res = await fetch(`${BASE_URL}/evaluation/${experimentId}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Robustness
  async runRobustness(payload) {
    const res = await fetch(`${BASE_URL}/robustness/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Export URLs
  getExportUrl(type, datasetId = '', experimentId = '') {
    const params = new URLSearchParams();
    if (datasetId) params.append('dataset_id', datasetId);
    if (experimentId) params.append('experiment_id', experimentId);
    return `${BASE_URL}/export/${type}?${params.toString()}`;
  }
};
