import React, { useState } from 'react';
import './MainContent.css';
import UploadImage from './UploadImage';
import ChooseModels from './ChooseModels';

export default function MainContent() {
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedArchitecture, setSelectedArchitecture] = useState('');
  const [modelsPerformance, setModelsPerformance] = useState({});
  const [generatedCaption, setGeneratedCaption] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [imageData, setImageData] = useState(null); // Added imageData state

  const handleModelChange = (selectedModel) => {
    setSelectedModel(selectedModel);
    // Additional logic or actions based on the selected model can be placed here
  };

  const handleArchitectureChange = (selectedArchitecture) => {
    setSelectedArchitecture(selectedArchitecture);
    // Additional logic or actions based on the selected architecture can be placed here
  };

  // const handlePerformanceClick = (selectedArchitecture) =>{
  //   setModelsPerformance(selectedArchitecture)
  // }

  const handleUploadImage = (imageData) => {
    setImageData(imageData); // Set the selected image data to imageData state
  };

  const handlePerformanceOperation = (modelsPerformance) =>{
    setModelsPerformance(modelsPerformance)
  }

  const handleGenerateCaption = () => {

     // Prepare the data to send to the backend
     const data = {
      model: selectedArchitecture,
      image: imageData,
    };

    if (!selectedArchitecture || !imageData) {
      setError('Please select a model and upload an image.');
      return;
    }

    // Replace 'your_backend_caption_api_url' with the actual URL of your Django backend caption generation API
    const apiUrl = 'http://127.0.0.1:8000/main_app/generate_caption';
    setLoading(true);
    setError('');

    // Send the API request using fetch or any other method of your choice
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((result) => {
      // Assuming result.descriptions contains the string "start in in in the end"
      const start = "start";
      const end = "end";
      const description = result.descriptions;

      const startIndex = description.indexOf(start) + start.length;
      const endIndex = description.lastIndexOf(end);
      const generatedCaption = description.substring(startIndex, endIndex).trim();
      setGeneratedCaption(generatedCaption);
      setLoading(false);
      })
      .catch((error) => {
        setError('Error generating caption. Please try again later.');
        setLoading(false);
      });
  };

  return (
      <div className="outerdiv">
      <div id="firstbox">
        <div>
          {/* Pass the handleModelChange and handleArchitectureChange functions as props */}
          <ChooseModels
            onModelChange={handleModelChange}
            onArchitectureChange={handleArchitectureChange}
            onPerformanceClick={handlePerformanceOperation}
            // onPerformanceClick={handlePerformanceClick}
          />
        </div>
      </div>
      <div id="secondbox">
        <h3>Upload Your Image Here</h3>
        <div>
          {/* Pass the handleUploadImage function as a prop */}
          <UploadImage onImageUpload={handleUploadImage} />
        </div>
        
      </div>
      <div id="thirdbox">
        <h3>Your Captions Will Appear Here</h3>
      <button onClick={handleGenerateCaption}>Generate Caption</button>
        <div>
          {/* Display the generated caption */}
          {generatedCaption && <p>{generatedCaption}</p>}
        </div>
      </div>

    </div>
    
  );
}