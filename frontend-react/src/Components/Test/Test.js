import React, { useState, useEffect } from 'react';
import './Test.css'; // Import your Test CSS file
import ChooseModels from '../main/ChooseModels';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import ReactModal from 'react-modal';

export default function Test() {
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedMetric, setSelectedMetric] = useState('BLEU');
  const [selectedArchitecture, setSelectedArchitecture] = useState('');
  const [modelsPerformance, setModelsPerformance] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [testResult, setTestResult] = useState('');
  const [responseFromBackend, setResponseFromBackend] = useState(null);
  const [showChart, setShowChart] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [lossData, setLossData] = useState([]); // State to store loss data
  const [bleuData, setBleuData] = useState([]); // State to store BLEU score data

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const handleShowChart = () => {
    if (bleuData.length > 0) {
      const bleuChartData = bleuData.map((bleuScores, index) => ({
        Epoch: index + 1, // Assuming the order of epochs starts from 1
        [`BLEU-${index + 1}`]: bleuScores,
      }));
  
      if (bleuChartData.length > 0) {
        setBleuData(bleuChartData);
        setShowChart(true);
      } else {
        setShowChart(false);
      }
    } else {
      setShowChart(false);
    }
  };
  
  
  const handleModelChange = (selectedModel) => {
    setSelectedModel(selectedModel);
  };

  const handlePerformanceOperation = (modelsPerformance) => {
    setModelsPerformance(modelsPerformance)
  };

  const handleArchitectureChange = (selectedArchitecture) => {
    console.log('ssssssssssssss',selectedArchitecture)
    setSelectedArchitecture(selectedArchitecture);
  };

  const handleMetricChange = (event) => {
    setSelectedMetric(event.target.value);
  };

  

  const handleTestModel = () => {
    const data = {
      model: selectedArchitecture,
      testMetric: selectedMetric,
    };

    if (!selectedModel || !selectedMetric) {
      setError('Please select a model and test metric.');
      return;
    }

    const apiUrl = 'http://127.0.0.1:8000/test_models/test';
    setLoading(true);
    setError('');

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((result) => {
        setTestResult(result);
        setResponseFromBackend(result);
        setLoading(false);
      })
      .catch((error) => {
        setError('Error testing model. Please try again later.');
        setLoading(false);
      });
  };

  useEffect(() => {
    // Check if the responseFromBackend state has data and render it
    if (responseFromBackend) {
      
      if (Object.keys(responseFromBackend).length > 0) {
        const bleu1 = responseFromBackend['BLEU-1'];
        const bleu2 = responseFromBackend['BLEU-2'];
        const bleu3 = responseFromBackend['BLEU-3'];
        const bleu4 = responseFromBackend['BLEU-4'];
        setBleuData([bleu1, bleu2, bleu3, bleu4]);
      }
    }
  }, [responseFromBackend]);
  

  return (
    <div className='container'>
      <div className="outerdiv">
        <div id="firstbox">
          <div>
            <ChooseModels
              onModelChange={handleModelChange}
              onArchitectureChange={handleArchitectureChange}
              onPerformanceClick={handlePerformanceOperation}
            />
          </div>
        </div>
        <div id="secondbox">
          <h3>Choose Test Metric</h3>
          <div>
            <select value={selectedMetric} onChange={handleMetricChange}>
              <option value="BLEU">BLEU Score</option>
              {/* Add other metric options if needed */}
            </select>
          </div>
        </div>
        <div id="thirdbox">
          <h3>Test Model</h3>
          <button onClick={handleTestModel}>Test Model</button>
          <div>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
          </div>
        </div>
        {responseFromBackend && (
          <div id="fourthbox">
            <h3>Backend Response</h3>
            <table>
        <thead>
          <tr>
            <th>Key</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {Object.keys(responseFromBackend).map((key) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{responseFromBackend[key]}</td>
            </tr>
          ))}
        </tbody>
      </table>
            <button onClick={handleShowChart}>Show Chart</button>
          </div>
        )}
      </div>
      <ReactModal
  isOpen={isModalOpen}
  onRequestClose={closeModal}
  style={{
    overlay: {
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
    content: {
      width: '70%',
      height: '70%',
      margin: 'auto',
      border: 'none',
      borderRadius: '10px',
      background: 'white',
      boxShadow: '0 0 10px rgba(0.5, 0.3, 0.7, 0.3)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
    },
  }}
>
  {showChart && (
    <>
      <h3>BLEU Score</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={bleuData}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Epoch" />
          <YAxis label={{ value: 'Value', angle: -90, position: 'insideLeft', offset: -2 }} />
          <Tooltip formatter={(value) => `${value.toFixed(2)}`} />
          <Legend />

          {Object.keys(bleuData[0]).map((key, index) => (
            <Line
              key={index}
              name={key}
              type="monotone"
              dataKey={key}
              stroke={`#${(index + 1) * 111}`} // Generate different colors for each line
              strokeWidth={2}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      <button onClick={closeModal}>Close</button>
    </>
  )}
</ReactModal>
    </div>
  );
}
