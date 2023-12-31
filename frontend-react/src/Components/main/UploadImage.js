import React, { useState } from 'react';
import './UploadImage.css'; // Import the CSS file for styling

export default function UploadImage({ onImageUpload }) {
  const [image, setImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      const img = new Image();
      img.src = reader.result;

      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        const MAX_WIDTH = 300;
        const MAX_HEIGHT = 300;

        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          }
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          }
        }

        canvas.width = width;
        canvas.height = height;

        ctx.drawImage(img, 0, 0, width, height);

        const imageData = canvas.toDataURL('image/jpeg');

        setImage(imageData);
        onImageUpload(imageData);
      };
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleImageRemove = () => {
    setImage(null);
  };

  return (
    <div className="upload-image-container">
      {/* Hidden input element */}
      <input type="file" accept="image/*" id="imageInput" onChange={handleImageUpload} style={{ display: 'none' }} />
      {/* Render the Upload Image button only if no image is selected */}
      {!image && (
        <label htmlFor="imageInput" className="upload-image-button">
          Upload Image
        </label>
      )}
      {image && (
        <div>
          <img src={image} alt="Uploaded" />
          <button className="remove-image-button" onClick={handleImageRemove}>
            Remove Image
          </button>
        </div>
      )}
    </div>
  );
}