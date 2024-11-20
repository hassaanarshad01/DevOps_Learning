import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud } from 'react-icons/fi';

const Dropzone = ({ handleFileChange }) => {
  const [previewImage, setPreviewImage] = useState(null);
  const [fileName, setFileName] = useState(null); 

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        handleFileChange({ target: { files: acceptedFiles } });

       
        const imageUrl = URL.createObjectURL(file);
        setPreviewImage(imageUrl); 
        setFileName(file.name); 
      }
    },
  });

  return (
    <div className="dropzone" {...getRootProps()}>
      <input {...getInputProps()} />
      
      {fileName && <p className="file-name">Uploaded: {fileName}</p>}
      
      {previewImage ? (
        <img src={previewImage} alt="Uploaded" style={{ width: '30%', height: '30%', borderRadius: '5px', objectFit: 'cover' }} />
      ) : (
        <>
          <FiUploadCloud size={50} />
          <p>Drag or Select file</p>
        </>
      )}
    </div>
  );
};

export default Dropzone;
