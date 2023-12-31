import React, { useState } from 'react';
import {Link} from 'react-router-dom';
import './Train.css'
import './TrainModal.css'
import ReactModal from 'react-modal';



const Train = () => {
  const [dataset, setDataset] = useState('');
  const [responseData, setResponseData] = useState(null);

  const [modelSummary, setModelSummary] = useState('');
  const [modalIsOpen, setModalIsOpen] = useState(false);

    // Function to open the modal
    const openModal = () => {
      setModalIsOpen(true);
    };

    // Function to close the modal
  const closeModal = () => {
    setModalIsOpen(false);
  };
  
  const [error, setError] = useState(null);
  const [trainingParams, setTrainingParams] = useState('');
  const [testingParams, setTestingParams] = useState('');
  const [pretrainedCNNModel, setPretrainedCNNModel] = useState('');
  const [lstmArchitecture, setLstmArchitecture] = useState('');
  const [numLayersForLSTM, setNumLayersForLSTM] = useState(1);
  const [dropoutRate, setDropoutRate] = useState('');
  const [denseLayersCNN, setDenseLayersCNN] = useState('');
  const [denseLayersLSTM, setDenseLayersLSTM] = useState('');
  const [epochs, setEpochs] = useState('');
  const [optimizer, setOptimizer] = useState('Adam'); // New state for Optimizer dropdown
  const [learningRate, setLearningRate] = useState('0.1');
  const [l2Regularizer, setL2Regularizer] = useState('0.001'); // New state for L2 Regularizer dropdown

  const [errorMessage, setErrorMessage] = useState('');
  const [formData, setFormData] = useState({
    trainingParams: '',
    testingParams: '',
    denseLayersCNN: '',
    denseLayersLSTM: '',
    epochs: '',
    nameOfModel:'',
    // Add other input fields here and set their initial values as empty strings
  });

  const [formErrors, setFormErrors] = useState({
    nameOfModel: '',
  });

  const handleInputChangeForTrainAndTest = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });

    // Validate the input and set the error message if necessary
    if (value === '') {
      setFormErrors({
        ...formErrors,
        [name]: 'This field is required.',
      });
    } else if (!validateIntegerInput(value, 1000, 8000)) {
      setFormErrors({
        ...formErrors,
        [name]: 'Must be an integer value between 1000 and 8000',
      });
    } else {
      // Clear the error message for this input field if valid
      setFormErrors({
        ...formErrors,
        [name]: '',
      });
    }
  };



  const handleInputChangeForDenseLayers = (e) =>{
    const {name, value}= e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    // Validate the input and set the error message if necessary
    if (value === '') {
      setFormErrors({
        ...formErrors,
        [name]: 'This field is required.',
      });
    } else if (!validateIntegerInput(value, 100, 1000)) {
      setFormErrors({
        ...formErrors,
        [name]: 'Must be an integer value between 100 and 1000',
      });
    } else {
      // Clear the error message for this input field if valid
      setFormErrors({
        ...formErrors,
        [name]: '',
      });
    }
  }

  const handleLstmArchitectureChange = (e) => {
    setLstmArchitecture(e.target.value);
    // If the selected LSTM architecture is "Single", reset the numLayers state to 1
    if (e.target.value === 'Single') {
      setNumLayersForLSTM(1);
    }
  };

  const handleInputChangeForEpochs = (e) =>{
    const {name, value}= e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    // Validate the input and set the error message if necessary
    if (value === '') {
      setFormErrors({
        ...formErrors,
        [name]: 'This field is required.',
      });
    } else if (!validateIntegerInput(value, 1, 50)) {
      setFormErrors({
        ...formErrors,
        [name]: 'Must be an integer value between 1 and 50',
      });
    } else {
      // Clear the error message for this input field if valid
      setFormErrors({
        ...formErrors,
        [name]: '',
      });
    }
  }

  const handleInputChangeForNameOfModel = (e) =>{
    const {name, value}= e.target;
    console.log(name)
    console.log(value)
    setFormData({
      ...formData,
      [name]: value,
    });
    if (value === '') {
      setFormErrors({
        ...formErrors,
        [name]: 'This field is required.',
      });
    }else {
      // Clear the error message for this input field if valid
      setFormErrors({
        ...formErrors,
        [name]: '',
      });
    }
  }


  const handleDownloadSummary = () => {
    if (responseData && responseData.parameters.model_summary) {
      const modelSummary = responseData.parameters.model_summary;
      const modelName = formData.nameOfModel || 'model'; // Use 'model' as a default name if nameOfModel is not set
  
      const blob = new Blob([modelSummary], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${modelName}_summary.txt`; // Set the filename as nameOfModel_summary.txt
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const handleTrain = () => {
    // Gather all the form data
    const data = {
      dataset,
      trainingParams: formData.trainingParams,
      testingParams: formData.testingParams,
      pretrainedCNNModel,
      lstmArchitecture,
      numLayersForLSTM,
      dropoutRate,
      denseLayersCNN: formData.denseLayersCNN,
      denseLayersLSTM: formData.denseLayersLSTM,
      epochs: formData.epochs,
      optimizer, // Include the selected optimizer in the data
      learningRate,
      l2Regularizer, // Include the selected L2 Regularizer in the data
      nameOfModel: formData.nameOfModel,
    };
  
    // API call with the 'data' object
    console.log(data)
    fetch('http://127.0.0.1:8000/train_models/train/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((responseData) => {
        // Handle the API response here
        setResponseData(responseData);
        setError(null);
        openModal(); // Open the modal after receiving the response
      })
      .catch((error) => {
        // Handle any error that occurred during the API call
        setError('An error occurred while fetching data from the server.');
        console.error('Error:', error);
      });
  };

  const validateIntegerInput = (value, min, max) => {
    const intValue = parseInt(value);
    return Number.isInteger(intValue) && intValue >= min && intValue <= max;
  };

  return (
    <div className="train-container">
    <h1 className="train-heading">Train Model</h1>
      <Link to='/train'></Link>
      <div className="train-label">
        <label>
        Dataset:
        <select value={dataset} onChange={(e) => setDataset(e.target.value)}>
          <option value="">Select Dataset</option>
          <option value="Flickr8k">Flickr8k</option>
          <option value="Flickr30k">Flickr30k</option>
        </select>
      </label></div>
      
      <br />
      <div className="train-label">
      <label>
        No. of Training Parameters:
        <input
          type="number"
          name="trainingParams"
          value={formData.trainingParams}
          onChange={handleInputChangeForTrainAndTest}
        />
        {formErrors.trainingParams ? (
          <span className="error-message">{formErrors.trainingParams}</span>
        ) : null}
      </label>
      </div>
      
      <br />
      <div className="train-label">
      <label>
        No. of Testing Parameters:
        <input
          type="number"
          name="testingParams"
          value={formData.testingParams}
          onChange={handleInputChangeForTrainAndTest}
        />
        {formErrors.testingParams ? (
          <span className="error-message">{formErrors.testingParams}</span>
        ) : null}
      </label>
      </div>
      
      <br />
      <div className="train-label">
        
      <label>
        Pre-trained CNN models:
        <select
          value={pretrainedCNNModel}
          onChange={(e) => setPretrainedCNNModel(e.target.value)}
        >
          <option value="">Select Pre-trained Model</option>
          <option value="Xception">Xception</option>
          <option value="VGG16">VGG16</option>
          <option value="Inception">Inception</option>
        </select>
      </label>
      </div>

      <br />

      <div className="train-label">
      <label>
        LSTM Architectures:
        <select
          value={lstmArchitecture}
          onChange={handleLstmArchitectureChange}
        >
          <option value="">Select LSTM Architecture</option>
          <option value="Single">Single</option>
          <option value="Stacked">Stacked</option>
          <option value="Bidirectional">Bidirectional</option>
        </select>
      </label>

       {/* Conditionally render the additional input form for Stacked and Bidirectional */}
       {lstmArchitecture === 'Stacked' || lstmArchitecture === 'Bidirectional' ? (
        <label>
          Number of Layers:
          <input
            type="number"
            value={numLayersForLSTM}
            onChange={(e) => setNumLayersForLSTM(e.target.value)}
            min={1}
            max={5}
          />
        </label>
      ) : null}
      </div>
     
      <br />
      <div className="train-label">
      <label>
        Dropout Rate:
        <select value={dropoutRate} onChange={(e) => setDropoutRate(e.target.value)}>
          <option value="">Select Dropout Rate</option>
          <option value="0.1">0.1</option>
          <option value="0.3">0.3</option>
          <option value="0.5">0.5</option>
          <option value="0.8">0.8</option>
          <option value="1">1</option>
        </select>
      </label>
      </div>
     
      <br />
      <div className="train-label">
      <label>
        Dense Layers for CNN:
        <input
          type="number"
          name='denseLayersCNN'
          value={formData.denseLayersCNN}
          onChange={handleInputChangeForDenseLayers}
          />
            {formErrors.denseLayersCNN ? (
          <span className="error-message">{formErrors.denseLayersCNN}</span>
        ) : null}
      </label>
      </div>
      
      <br />
      <div className="train-label">
      <label>
        Dense Layers for LSTM:
        <input
          type="number"
          name='denseLayersLSTM'
          value={formData.denseLayersLSTM}
          onChange={handleInputChangeForDenseLayers}
        />
         {formErrors.denseLayersLSTM ? (
          <span className="error-message">{formErrors.denseLayersLSTM}</span>
        ) : null}
      </label>
      </div>
      
      <br />
      <div className="train-label">
      <label>
        Number of Epochs:
        <input
          type="number"
          name='epochs'
          value={formData.epochs}
          onChange={handleInputChangeForEpochs}
        />
         {formErrors.epochs ? (
          <span className="error-message">{formErrors.epochs}</span>
        ) : null}
      </label>
      </div>

      <br />
         {/* Dropdown for Optimizers */}
         <div className="train-label">
        <label>
          Optimizers:
          <select value={optimizer} onChange={(e) => setOptimizer(e.target.value)}>
            <option value="Adam">Adam</option>
            <option value="SGD">SGD</option>
            <option value="RMSProp">RMSProp</option>
            <option value="ADAGrad">ADAGrad</option>
          </select>
        </label>
      </div>

      <br />

       {/* Conditionally render the Learning Rate dropdown */}
       {optimizer && (
        <div className="train-label">
          <label>
            Learning Rate:
            <select value={learningRate} onChange={(e) => setLearningRate(e.target.value)}>
              <option value="0.001">0.001</option>
              <option value="0.01">0.01</option>
              <option value="0.1">0.1</option>
            </select>
          </label>
        </div>
      )}

      <br/>

      {/* Dropdown for L2 Regularizer */}
      <div className="train-label">
        <label>
          L2 Regularizer:
          <select value={l2Regularizer} onChange={(e) => setL2Regularizer(e.target.value)}>
            <option value="0.001">0.001</option>
            <option value="0.01">0.01</option>
            <option value="0.1">0.1</option>
          </select>
        </label>
      </div>

      <br/>
      <div className="train-label">
        <label>
          Name of Model:
          <input
            type="text"
            name='nameOfModel'
            value={formData.nameOfModel}
            onChange={handleInputChangeForNameOfModel}
          />
           {formErrors.nameOfModel ? (
          <span className="error-message">{formErrors.nameOfModel}</span>
        ) : null}
          {/* You can add validation error message for this input field if needed */}
        </label>
      </div>

      <br />
      <button className="train-button" onClick={handleTrain}>Train Model</button>

{/* Modal for displaying API response */}
    <ReactModal
      isOpen={modalIsOpen}
      onRequestClose={closeModal}
      contentLabel="API Response"
      className="modal"
      overlayClassName="modal-overlay"
      ariaHideApp={false}
    >
      {responseData && (
        <div className="modal-content">
          <button className="close-button" onClick={closeModal}>
            Close
          </button>
          <h2 className="modal-heading">API Response</h2>
           {/* Highlight "Your Model Name" */}
           {responseData.parameters['Model Name'] && (
              <h5><strong>{responseData.parameters['Model Name']}</strong></h5>
            )}
          <pre className="response-data">
            {JSON.stringify(
          // Filter out the model_architecture_image from the response data
          { ...responseData, parameters: { ...responseData.parameters, model_architecture_image: 'Please Download', model_summary: 'Please Download', } },
          null,
          2
        )}
          </pre>
        </div>
      )}

      {responseData && responseData.parameters.model_architecture_image && (
        <div className="modal-content">
          
          <h2 className="modal-heading">Model Architecture Image</h2>
          <a
            className="download-link"
            href={`data:image/png;base64,${responseData.parameters.model_architecture_image}`}
            download="model_architecture_image.png"
          >
            <button className='download-button'>Download Image</button>
          </a>
          <img
            className="architecture-image"
            src={`data:image/png;base64,${responseData.parameters.model_architecture_image}`}
            alt="Model Architecture"
          />
          
          
        </div>
      )}
      {/* Button to download the model summary */}
      {responseData && responseData.parameters.model_summary && (
          <div className="modal-content">
            <div className="modal-content-last">
            <h2 className="modal-heading">Your Model Summary</h2>
            <button className="download-button" onClick={handleDownloadSummary}>
              Download Summary
            </button>
            </div>
            
          </div>
        )}

    </ReactModal>

    </div>
  );
};

export default Train;