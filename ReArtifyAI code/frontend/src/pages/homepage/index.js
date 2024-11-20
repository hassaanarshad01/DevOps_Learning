import React from 'react';
import bottomImage from '../../components/images/art4.jpg';
import Dropzone from '../../components/dropzone';
import topImage from '../../components/images/art1.jpg';
import { Button, Select } from 'antd';

const Homepage = ({ 
  handleFileChange, 
  handleClassify, 
  result, 
  model, 
  handleModelChange, 
  handlePredict, 
  predictionImage,
  setPredictionImage, 
  setIsModalVisible 
}) => {
  return (
    <div id="homepage">
      
      <img id="top-image" src={topImage} alt="Top" />

      <h1 className="heading">Time to ReArtify</h1>
      <div className="classify-dropzone-wrapper">
        
        <div className="classify-container">
          <Button id="classify-button" onClick={handleClassify}>Classify</Button>
          {result && <p id="classification-result">Result: {result}</p>}
        </div>

        
        <Dropzone handleFileChange={handleFileChange} />

        <Select 
          id="model-select"
          value={model}
          onChange={handleModelChange}
        >
          <Select.Option value="blur">Blur Removal</Select.Option>
          <Select.Option value="scratches">Scratch Removal</Select.Option>
          <Select.Option value="coloring">Coloring</Select.Option>
          <Select.Option value="smudges">Smudge Removal</Select.Option>
        </Select>

        
        <Button id="predict-button" onClick={handlePredict}>Predict</Button>
      </div>

      
      
      
      <img id="bottom-image" src={bottomImage} alt="Bottom" />
    </div>
  );
};

export default Homepage;
