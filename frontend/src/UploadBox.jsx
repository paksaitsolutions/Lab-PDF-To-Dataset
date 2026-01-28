import React, { useState } from "react";
import { uploadFiles } from "./api";

export default function UploadBox() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [testTypes, setTestTypes] = useState({ cbc: true, lft: true, rft: true });

  const handleUpload = async () => {
    if (!files.length) return alert("Select file(s)");

    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const res = await uploadFiles(files, testTypes);
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

  const handleClear = () => {
    setFiles([]);
    setResult(null);
    setError(null);
    setTestTypes({ cbc: true, lft: true, rft: true });
    document.querySelector('input[type="file"]').value = '';
  };

  return (
    <div className="card">
      <input
        type="file"
        multiple
        accept=".pdf,.zip,.doc,.docx"
        onChange={e => setFiles([...e.target.files])}
      />

      <div style={{margin: '15px 0'}}>
        <label style={{marginRight: '15px'}}>
          <input type="checkbox" checked={testTypes.cbc} onChange={e => setTestTypes({...testTypes, cbc: e.target.checked})} />
          {' '}CBC
        </label>
        <label style={{marginRight: '15px'}}>
          <input type="checkbox" checked={testTypes.lft} onChange={e => setTestTypes({...testTypes, lft: e.target.checked})} />
          {' '}LFT
        </label>
        <label>
          <input type="checkbox" checked={testTypes.rft} onChange={e => setTestTypes({...testTypes, rft: e.target.checked})} />
          {' '}RFT
        </label>
      </div>

      <div style={{display: 'flex', gap: '10px'}}>
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload"}
        </button>
        <button onClick={handleClear} disabled={loading} style={{background: '#6b7280'}}>
          Clear
        </button>
      </div>

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
