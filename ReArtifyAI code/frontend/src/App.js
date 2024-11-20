import React, { useState } from 'react';
import axios from 'axios';
axios.defaults.baseURL = 'http://flask-api-service.my-project.svc.cluster.local:5000';
import HeaderComponent from "../src/components/header";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import GeneratePage from '../src/pages/generatePage';
import Homepage from './pages/homepage'; 
import { Modal, Button } from 'antd'; 
import MDBFooter from '../src/components/footer';


import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [model, setModel] = useState('blur');
  const [predictionImage, setPredictionImage] = useState(null);
  const [inpaintImage, setInpaintImage] = useState(null); 
  const [prompt, setPrompt] = useState(''); 
  
  // State for modal visibility
  const [isPredictionModalVisible, setIsPredictionModalVisible] = useState(false); 
  const [isClassificationModalVisible, setIsClassificationModalVisible] = useState(false); 
  const [isInpaintModalVisible, setIsInpaintModalVisible] = useState(false); 
  
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleModelChange = (value) => {
    console.log(value); 
    setModel(value); 
  };

  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };

  const handleClassify = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/classify', formData);
      setResult(response.data.classification);  
      setIsClassificationModalVisible(true);  
    } catch (error) {
      console.error("Error classifying the file:", error);
    }
  };

  const handlePredict = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('model_name', model);

    const response = await axios.post('/predict', formData, {
      responseType: 'blob', 
    });


    const imageUrl = URL.createObjectURL(response.data);
    setPredictionImage(imageUrl);
    setIsPredictionModalVisible(true); 
  };

  const handleGenerate = async () => {
    if (!file || !prompt) {
      alert("Please select a file and enter a prompt first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', prompt);

    try {
      const response = await axios.post('/inpaint', formData, {
        responseType: 'blob',
      });

      const imageUrl = URL.createObjectURL(response.data);
      setInpaintImage(imageUrl);
      setIsInpaintModalVisible(true);
    } catch (error) {
      console.error("Error generating the inpainted image:", error);
    }
  };

  const handleClosePredictionModal = () => {
    setIsPredictionModalVisible(false);
    setPredictionImage(null);
  };

  const handleCloseClassificationModal = () => {
    setIsClassificationModalVisible(false);
    setResult(null); 
  };

  const handleCloseInpaintModal = () => {
    setIsInpaintModalVisible(false);
    setInpaintImage(null);
  };

  return (
    <Router>
      <div className="App">
        <HeaderComponent />

        <Routes>
          <Route
            path="/"
            element={
              <Homepage
                handleFileChange={handleFileChange}
                handleClassify={handleClassify}
                result={result}
                model={model}
                handleModelChange={handleModelChange}
                handlePredict={handlePredict}
                predictionImage={predictionImage}
                setPredictionImage={setPredictionImage} 
                setIsModalVisible={setIsPredictionModalVisible} 
              />
            }
          />
          <Route 
            path="/generate" 
            element={
              <GeneratePage
                handleFileChange={handleFileChange}
                handlePromptChange={handlePromptChange}
                handleGenerate={handleGenerate}
              />
            } 
          />
        </Routes>

        {/* Modal for displaying the prediction image ////////////////////////////////*/}
        <Modal
          title="Prediction Result"
          visible={isPredictionModalVisible}
          onCancel={handleClosePredictionModal}
          footer={null} 
          width="80%" 
        >
          <div style={{ textAlign: 'center' }}>
            <img 
              src={predictionImage} 
              alt="Prediction" 
              style={{ 
                marginRight: '20px',
                marginLeft: '7%',
                maxWidth: '100%', 
                maxHeight: '400px', 
                marginBottom: '20px',
                marginTop: '2%',
                border: '2px solid #0f1235',
                borderRadius: '8px', 
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.5)', 
                padding: '5px', 
                backgroundColor: '#fff' 
              }} 
            />
            <Button 
              style={{ marginTop: '10px', marginLeft: '10px', }}
              onClick={() => {
                const link = document.createElement('a');
                link.href = predictionImage;
                link.download = 'prediction.png'; 
                link.click();
              }}
            >
              Download
            </Button>
          </div>
        </Modal>

        {/* Modal for displaying the classification result //////////////////////////*/}
        <Modal
          visible={isClassificationModalVisible}
          onCancel={handleCloseClassificationModal}
          footer={null} 
          width="80%"
        >
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <p id="classification-result">{result ? `Result: ${result}` : "Loading..."}</p>
          </div>
        </Modal>

        {/* Modal for displaying the inpainted image //////////////////////////////////*/}
        <Modal
          title="Inpaint Result"
          visible={isInpaintModalVisible}
          onCancel={handleCloseInpaintModal}
          footer={null}
          width="80%"
        >
          <div style={{ textAlign: 'center' }}>
            <img
              src={inpaintImage}
              alt="Inpaint"
              style={{ 
                maxWidth: '100%', 
                maxHeight: '400px', 
                marginBottom: '20px',
                border: '2px solid #0f1235',
                borderRadius: '8px',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.5)', 
              }}
            />
            <Button 
              style={{ marginTop: '10px', marginLeft: '10px' }}
              onClick={() => {
                const link = document.createElement('a');
                link.href = inpaintImage;
                link.download = 'inpainted_image.jpg'; 
                link.click();
              }}
            >
              Download
            </Button>
          </div>
        </Modal>

        <MDBFooter />
      </div>
    </Router>
  );
}

export default App;
