import React, { useState, useEffect } from 'react';
import ChartComponent from '../Charts/ChartComponent';
import ReactModal from 'react-modal';
import './ChooseModels.css'


const ChooseModels = ({ onModelChange, onArchitectureChange, onPerformanceClick }) => {
  const [trainedModels, setTrainedModels] = useState({});
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedArchitecture, setSelectedArchitecture] = useState('');
  const [modelsForSelectedModel, setModelsForSelectedModel] = useState([]);
  const [modelsPerformance, setModelsPerformance] = useState({});
  const [showChartModal, setShowChartModal] = useState(false);
  const [performanceData, setPerformanceData] = useState(null);

   // Function to pass modelsPerformance data to the parent component
   const passModelsPerformanceToParent = () => {
    onPerformanceClick(modelsPerformance);
  };

  useEffect(() => {
    // Function to fetch data from the API
    const fetchData = () => {
      fetch('http://127.0.0.1:8000/main_app/list_models')
        .then((response) => response.json())
        .then((data) => {
          setTrainedModels(data.models_data); // Set the entire data object from the API response
          setModelsPerformance(data.models_performance)
        })
        .catch((error) => console.error('Error fetching models:', error));
    };

    // Fetch data immediately on mount
    fetchData();

    // Set up an interval to fetch data every 3 seconds
    const intervalId = setInterval(fetchData, 20000);

    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  const handleModelChange = (e) => {
    const selectedModel = e.target.value;
    setSelectedModel(selectedModel);

    // Set the models for the selected model
    const models = trainedModels[selectedModel] || [];
    setModelsForSelectedModel(models);

    // Reset selectedArchitecture when a new model is selected
    setSelectedArchitecture('');

    // Notify the parent component of the selected model
    onModelChange(selectedModel);
  };
  const handleArchitectureChange = (e) => {
    const selectedArchitecture = e.target.options[e.target.selectedIndex].value;
    setSelectedArchitecture(selectedArchitecture);
  
    // Notify the parent component of the selected sub-model (architecture)
    onArchitectureChange(selectedArchitecture);
  };

  const handlePerformanceClick = () => {
    // Get the selected architecture key without the ".keras" extension
    const selectedKey = selectedArchitecture.replace('.keras', '');

     // Extract the architecture and model name without the number and "Epochs" part
    const [architecture, modelName, epochs, uniqueFileKey] = selectedKey.split('___');
    const selectedKeyWithoutNumber = `${architecture}___${modelName}___'Epochs'___${uniqueFileKey}`;


    // Check if the selected key exists in the models_performance object
    if (modelsPerformance[selectedKeyWithoutNumber]) {
      console.log(modelsPerformance[selectedKeyWithoutNumber]);

      const dataForChart = modelsPerformance[selectedKeyWithoutNumber];

      // // Display the chart with the extracted data
      //  ReactDOM.render(<ChartComponent data={dataForChart} />, document.getElementById('chartContainer'));

       setPerformanceData(dataForChart); // Set the data for the ChartComponent
       passModelsPerformanceToParent(dataForChart);

       // Notify the parent component of the selected sub-model (architecture)
       
      onPerformanceClick(dataForChart);

      setShowChartModal(true);
    }
  };

  const handleCloseModal = () => {
    setShowChartModal(false);
  };




  return (
  
 <div className="models-container">
      <div>
        <h3>Choose your Models</h3>
        <div className="model-select">
          <label htmlFor="modelSelect">Available Models:</label>
          <select id="modelSelect" onChange={handleModelChange}>
            <option value="">Select a Model</option>
            {Object.keys(trainedModels).map((model, index) => (
              <option key={index} value={model}>
                {model}
              </option>
            ))}
          </select>
        </div>

        {selectedModel && (
          <div>
            <label>Version of {selectedModel}:</label>
            <select onChange={handleArchitectureChange} value={selectedArchitecture}>
              <option value="">Select a Model</option>
              {modelsForSelectedModel.map((model, index) => (
                <option key={index} value={model}>
                  {model}
                </option>
              ))}
            </select>
            {selectedArchitecture && (
              <button class= 'model-performance-button' onClick={handlePerformanceClick}>See Model's Performance</button>
            )}
          </div>
        )}

      <ReactModal
        isOpen={showChartModal}
        onRequestClose={handleCloseModal}
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
        <h2>Model Performance</h2>
        {performanceData && <ChartComponent data={performanceData} />}
        <button class= 'model-performance-button' onClick={handleCloseModal}>Close</button>
      </ReactModal>

      </div>
    </div>
   
  );
};

export default ChooseModels;