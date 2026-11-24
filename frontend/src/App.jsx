import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Overview from './pages/Overview';
import DatasetManagement from './pages/DatasetManagement';
import TextPreprocessing from './pages/TextPreprocessing';
import AugmentationStudio from './pages/AugmentationStudio';
import SemanticValidation from './pages/SemanticValidation';
import DatasetComparison from './pages/DatasetComparison';
import ModelTraining from './pages/ModelTraining';
import EvaluationResults from './pages/EvaluationResults';
import RobustnessTesting from './pages/RobustnessTesting';
import ExportCenter from './pages/ExportCenter';
import ProjectDocs from './pages/ProjectDocs';
import { api } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [expansion, setExpansion] = useState(null);
  const [experiments, setExperiments] = useState([]);
  const [selectedExperiment, setSelectedExperiment] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (selectedDataset?.id) {
      loadDatasetDetails(selectedDataset.id);
    }
  }, [selectedDataset?.id]);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const dsList = await api.getDatasets();
      setDatasets(dsList);
      if (dsList.length > 0) {
        setSelectedDataset(dsList[0]);
      }
    } catch (err) {
      console.error('Failed to load datasets:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadDatasetDetails = async (id) => {
    try {
      const expData = await api.getExpansion(id);
      setExpansion(expData);

      const exps = await api.getExperiments(id);
      setExperiments(exps);
      if (exps.length > 0) {
        setSelectedExperiment(exps[0]);
      } else {
        setSelectedExperiment(null);
      }
    } catch (err) {
      console.error('Failed to load dataset details:', err);
    }
  };

  const handleRefresh = async () => {
    if (selectedDataset?.id) {
      await loadInitialData();
      await loadDatasetDetails(selectedDataset.id);
    }
  };

  const handleDatasetUpdated = (newDs) => {
    setDatasets((prev) => [newDs, ...prev]);
    setSelectedDataset(newDs);
    setActiveTab('dataset');
  };

  const handleAugmentationsGenerated = async () => {
    if (selectedDataset?.id) {
      await loadDatasetDetails(selectedDataset.id);
    }
  };

  const handleExperimentTrained = (newExp) => {
    setExperiments((prev) => [newExp, ...prev]);
    setSelectedExperiment(newExp);
    setActiveTab('evaluation');
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 text-slate-800">
      {/* Navigation Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Header */}
        <Header
          datasets={datasets}
          selectedDataset={selectedDataset}
          onSelectDataset={setSelectedDataset}
          onRefresh={handleRefresh}
          loading={loading}
        />

        {/* Scrollable View Container */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          {activeTab === 'overview' && (
            <Overview
              dataset={selectedDataset}
              expansion={expansion}
              experiments={experiments}
              onNavigate={setActiveTab}
            />
          )}

          {activeTab === 'dataset' && (
            <DatasetManagement
              dataset={selectedDataset}
              onDatasetUpdated={handleDatasetUpdated}
            />
          )}

          {activeTab === 'preprocessing' && <TextPreprocessing />}

          {activeTab === 'augmentation' && (
            <AugmentationStudio
              dataset={selectedDataset}
              onAugmentationsGenerated={handleAugmentationsGenerated}
            />
          )}

          {activeTab === 'validation' && (
            <SemanticValidation
              dataset={selectedDataset}
              onStatusChanged={handleAugmentationsGenerated}
            />
          )}

          {activeTab === 'comparison' && (
            <DatasetComparison
              dataset={selectedDataset}
              expansion={expansion}
            />
          )}

          {activeTab === 'training' && (
            <ModelTraining
              dataset={selectedDataset}
              onExperimentTrained={handleExperimentTrained}
              onSelectExperiment={setSelectedExperiment}
            />
          )}

          {activeTab === 'evaluation' && (
            <EvaluationResults
              experiments={experiments}
              selectedExperiment={selectedExperiment}
              onSelectExperiment={setSelectedExperiment}
            />
          )}

          {activeTab === 'robustness' && (
            <RobustnessTesting
              experiments={experiments}
              selectedExperiment={selectedExperiment}
            />
          )}

          {activeTab === 'export' && (
            <ExportCenter
              dataset={selectedDataset}
              selectedExperiment={selectedExperiment}
              experiments={experiments}
            />
          )}

          {activeTab === 'docs' && <ProjectDocs />}
        </main>
      </div>
    </div>
  );
}
