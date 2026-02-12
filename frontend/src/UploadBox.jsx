import React, { useEffect, useMemo, useState } from "react";
import { getDownloadUrl, uploadFiles } from "./api";

const DOWNLOAD_SKIP_VALUES = new Set(["N/A", "No rows extracted"]);

function isDownloadable(filename) {
  return filename && !DOWNLOAD_SKIP_VALUES.has(filename);
}

export default function UploadBox() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [testTypes, setTestTypes] = useState({ cbc: true, lft: true, rft: true, tft: true });

  const downloadLinks = useMemo(() => {
    if (!result?.success) return [];

    const entries = [
      { label: "CBC Dataset", filename: result.cbc_file },
      { label: "LFT Dataset", filename: result.lft_file },
      { label: "RFT Dataset", filename: result.rft_file },
      { label: "TFT Dataset", filename: result.tft_file },
      { label: "Processing Report", filename: result.report_file },
    ];

    return entries
      .filter(entry => isDownloadable(entry.filename))
      .map(entry => ({
        ...entry,
        url: getDownloadUrl(entry.filename),
      }));
  }, [result]);

  useEffect(() => {
    if (!downloadLinks.length) return;

    downloadLinks.forEach(({ url, filename }) => {
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
    });
  }, [downloadLinks]);

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
      const message = e?.message || 'Upload failed';
      if (message.includes('Failed to fetch')) {
        setError('Cannot connect to backend API. Start Flask server or set VITE_API_BASE_URL to your deployed backend URL.');
      } else {
        setError(message);
      }
    }
    setLoading(false);
  };

  const handleClear = () => {
    setFiles([]);
    setResult(null);
    setError(null);
    setTestTypes({ cbc: true, lft: true, rft: true, tft: true });
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

      <div style={{ margin: '15px 0' }}>
        <label style={{ marginRight: '15px' }}>
          <input type="checkbox" checked={testTypes.cbc} onChange={e => setTestTypes({ ...testTypes, cbc: e.target.checked })} />
          {' '}CBC
        </label>
        <label style={{ marginRight: '15px' }}>
          <input type="checkbox" checked={testTypes.lft} onChange={e => setTestTypes({ ...testTypes, lft: e.target.checked })} />
          {' '}LFT
        </label>
        <label style={{ marginRight: '15px' }}>
          <input type="checkbox" checked={testTypes.rft} onChange={e => setTestTypes({ ...testTypes, rft: e.target.checked })} />
          {' '}RFT
        </label>
        <label>
          <input type="checkbox" checked={testTypes.tft} onChange={e => setTestTypes({ ...testTypes, tft: e.target.checked })} />
          {' '}TFT
        </label>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload"}
        </button>
        <button onClick={handleClear} disabled={loading} style={{ background: '#6b7280' }}>
          Clear
        </button>
      </div>

      {loading && <p>⏳ Processing files...</p>}

      {error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          ❌ Error: {error}
        </div>
      )}

      {result && result.success && (
        <div className="results">
          <p>✅ Processing complete!</p>
          <p>Total files: {result.total_files}</p>
          <p>Processed: {result.processed_files}</p>
          <p>Skipped: {result.skipped_count}</p>
          <p>CBC: {result.cbc_count} | LFT: {result.lft_count} | RFT: {result.rft_count} | TFT: {result.tft_count}</p>
          <p>Files saved: {result.cbc_file}, {result.lft_file}, {result.rft_file}, {result.tft_file}</p>
          <p>Processing report: {result.report_file}</p>

          {!!downloadLinks.length && (
            <div style={{ marginTop: '12px' }}>
              <strong>Downloads</strong>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
                {downloadLinks.map(link => (
                  <a
                    key={link.label}
                    href={link.url}
                    download={link.filename}
                    style={{
                      padding: '6px 12px',
                      borderRadius: '999px',
                      border: '1px solid #cbd5f5',
                      background: '#eef2ff',
                      color: '#3730a3',
                      fontSize: '0.85em',
                      textDecoration: 'none',
                    }}
                  >
                    ⬇️ {link.label}
                  </a>
                ))}
              </div>
            </div>
          )}

          {!!result.skipped_files?.length && (
            <details style={{ marginTop: '10px' }}>
              <summary>Show skipped files ({result.skipped_files.length})</summary>
              <ul style={{ marginTop: '8px' }}>
                {result.skipped_files.map((item, index) => (
                  <li key={`${item.file}-${index}`}>{item.file}: {item.reason}</li>
                ))}
              </ul>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
