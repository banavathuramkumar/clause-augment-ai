const BASE_URL = '/api';

export const api = {
  // Datasets
  async getDatasets() {
    const res = await fetch(`${BASE_URL}/datasets`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getDataset(id) {
    const res = await fetch(`${BASE_URL}/datasets/${id}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getPreview(id, limit = 15) {
    const res = await fetch(`${BASE_URL}/datasets/${id}/preview?limit=${limit}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getStats(id) {
    const res = await fetch(`${BASE_URL}/datasets/${id}/stats`);
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

  async updateConfig(id, config) {
    const res = await fetch(`${BASE_URL}/datasets/${id}/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Augmentation
  async getAlgorithms() {
    const res = await fetch(`${BASE_URL}/augmentation/algorithms`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getGeminiStatus() {
    const res = await fetch(`${BASE_URL}/augmentation/gemini-status`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getRecommendations(datasetId) {
    const res = await fetch(`${BASE_URL}/augmentation/recommendations/${datasetId}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async generateAugmentation(payload) {
    const res = await fetch(`${BASE_URL}/augmentation/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Validation
  async getValidationRules() {
    const res = await fetch(`${BASE_URL}/validation/rules`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getValidationRecords(datasetId, status = 'all') {
    const res = await fetch(`${BASE_URL}/validation/dataset/${datasetId}?status=${status}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Training
  async getModels() {
    const res = await fetch(`${BASE_URL}/training/models`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async runTraining(payload) {
    const res = await fetch(`${BASE_URL}/training/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Export
  getExportUrl(datasetId, format = 'csv') {
    return `${BASE_URL}/export/dataset/${datasetId}?format=${format}`;
  },

  async getAcademicReport(datasetId) {
    const res = await fetch(`${BASE_URL}/export/report/${datasetId}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }
};
