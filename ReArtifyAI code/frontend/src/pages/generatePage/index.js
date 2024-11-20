import React from 'react';
import bottomImage from '../../components/images/war-1.jpg';
import Dropzone from '../../components/dropzone';
import topImage from '../../components/images/war-2.jpg';
import { Button } from 'antd';

function GeneratePage({ handleFileChange, handlePromptChange, handleGenerate }) {
  return (
    <div id="generatepage">
      
      <img id="top-image" src={topImage} alt="Top" />
      <h1 className="heading">Perfect Your Art: Inpaint with Precision</h1>
      <div className="content-wrapper">
        <Dropzone handleFileChange={handleFileChange} className="generate-page-dropzone" />

        <input
          type="text"
          placeholder="Enter your prompt here for inpainting on your painting. Best results are given by input painting having black-marked damage."
          className="custom-textbox"
          onChange={handlePromptChange} 
        />

        <Button className="generate-button" onClick={handleGenerate}>Generate</Button>
      </div>

      <img id="bottom-image" src={bottomImage} alt="Bottom" />
    </div>
  );
}

export default GeneratePage;
