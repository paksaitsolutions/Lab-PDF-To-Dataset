import React from 'react';
import UploadBox from "./UploadBox";

export default function App() {
  return (
    <div className="container">
      <h1>Lab PDF → Excel Dataset</h1>
      <p>Upload PDF(s), Word files, or ZIP</p>
      <UploadBox />
    </div>
  );
}
