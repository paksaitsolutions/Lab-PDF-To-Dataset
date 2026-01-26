import React, { useState } from "react";
import { uploadFiles } from "./api";

export default function UploadBox() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!files.length) return alert("Select file(s)");

    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const res = await uploadFiles(files);
      if (res.success) {
        setResult(res);
      } else {
        setError(res.error || 'Processing failed');
      }
    } catch (e) {
      setError(e.message || 'Upload failed');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <input
        type="file"
        multiple
        accept=".pdf,.zip,.doc,.docx"
        onChange={e => setFiles([...e.target.files])}
      />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload"}
      </button>

      {loading && <p>⏳ Processing files...</p>}
      
      {error && (
        <div style={{color: 'red', marginTop: '10px'}}>
          ❌ Error: {error}
        </div>
      )}

      {result && result.success && (
        <div className="results">
          <p>✅ Processing complete!</p>
          <p>Total files: {result.total_files}</p>
          <p>Processed: {result.processed_files}</p>
          <p>CBC: {result.cbc_count} | LFT: {result.lft_count} | RFT: {result.rft_count}</p>
          <p>Files saved: {result.cbc_file}, {result.lft_file}, {result.rft_file}</p>
        </div>
      )}
    </div>
  );
}
