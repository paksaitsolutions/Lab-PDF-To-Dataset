import React, { useEffect, useMemo, useState } from "react";
import { getDownloadUrl, uploadFiles } from "./api";

const DOWNLOAD_SKIP_VALUES = new Set(["N/A", "No rows extracted"]);

function isDownloadable(filename) {
  return filename && !DOWNLOAD_SKIP_VALUES.has(filename);
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

const DOWNLOAD_SKIP_VALUES = new Set(["N/A", "No rows extracted"]);

function isDownloadable(filename) {
  return filename && !DOWNLOAD_SKIP_VALUES.has(filename);
}

function DownloadButton({ filename, label, color, icon = '⬇' }) {
  return (
    <a
      href={`${API_BASE_URL}/download/${filename}`}
      target="_blank"
      rel="noopener noreferrer"
      className="download-btn"
      style={{ background: color }}
    >
      <span>{icon}</span>
      {label}
    </a>
  );
}

export default function UploadBox() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [testTypes, setTestTypes] = useState({ cbc: true, lft: true, rft: true, tft: true });

  const handleUpload = async () => {
    if (!files.length) {
      alert("Please select file(s) to upload");
      return;
    }

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
      <h2 style={{
        marginTop: 0,
        marginBottom: 'var(--spacing-lg)',
        color: 'var(--gray-800)',
        fontSize: '1.75rem'
      }}>
        📤 Upload Lab Reports
      </h2>

      {/* File Input */}
      <input
        type="file"
        multiple
        accept=".pdf,.zip,.doc,.docx"
        onChange={e => setFiles([...e.target.files])}
        style={{ marginBottom: 'var(--spacing-lg)' }}
      />

      {files.length > 0 && (
        <div className="alert alert-info" style={{ marginBottom: 'var(--spacing-lg)' }}>
          <span>📁</span>
          <span><strong>{files.length}</strong> file(s) selected</span>
        </div>
      )}

      {/* Test Type Selection */}
      <div style={{
        marginBottom: 'var(--spacing-lg)',
        padding: 'var(--spacing-md)',
        background: 'var(--gray-50)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--gray-200)'
      }}>
        <strong style={{
          display: 'block',
          marginBottom: 'var(--spacing-sm)',
          color: 'var(--gray-700)',
          fontSize: '0.95rem'
        }}>
          Select Report Types to Extract:
        </strong>
        <div style={{
          display: 'flex',
          gap: 'var(--spacing-lg)',
          flexWrap: 'wrap'
        }}>
          <label>
            <input
              type="checkbox"
              checked={testTypes.cbc}
              onChange={e => setTestTypes({ ...testTypes, cbc: e.target.checked })}
            />
            CBC
          </label>
          <label>
            <input
              type="checkbox"
              checked={testTypes.lft}
              onChange={e => setTestTypes({ ...testTypes, lft: e.target.checked })}
            />
            LFT
          </label>
          <label>
            <input
              type="checkbox"
              checked={testTypes.rft}
              onChange={e => setTestTypes({ ...testTypes, rft: e.target.checked })}
            />
            RFT
          </label>
          <label>
            <input
              type="checkbox"
              checked={testTypes.tft}
              onChange={e => setTestTypes({ ...testTypes, tft: e.target.checked })}
            />
            TFT
          </label>
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-lg)' }}>
        <button className="btn-primary" onClick={handleUpload} disabled={loading}>
          {loading ? '⏳ Processing...' : '🚀 Upload & Extract'}
        </button>
        <button className="btn-secondary" onClick={handleClear} disabled={loading}>
          🔄 Clear
        </button>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="fade-in" style={{
          marginTop: 'var(--spacing-xl)',
          textAlign: 'center',
          padding: 'var(--spacing-xl)',
          background: 'var(--primary-50)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--primary-100)'
        }}>
          <div className="spinner" style={{ marginBottom: 'var(--spacing-md)' }}></div>
          <p style={{
            fontWeight: '600',
            color: 'var(--primary-700)',
            margin: 0
          }}>
            Processing files... This may take a moment for OCR.
          </p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="alert alert-error fade-in">
          <span>❌</span>
          <span><strong>Error:</strong> {error}</span>
        </div>
      )}

      {/* Success Results */}
      {result && result.success && (
        <div className="fade-in" style={{
          marginTop: 'var(--spacing-xl)',
          padding: 'var(--spacing-xl)',
          background: 'linear-gradient(to bottom, var(--gray-50), white)',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--gray-200)'
        }}>
          <div className="alert alert-success" style={{ marginBottom: 'var(--spacing-lg)' }}>
            <span>✅</span>
            <span><strong>Success!</strong> Processing complete</span>
          </div>

          {/* Summary Stats */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: 'var(--spacing-md)',
            marginBottom: 'var(--spacing-xl)'
          }}>
            <div style={{
              padding: 'var(--spacing-md)',
              background: 'white',
              borderRadius: 'var(--radius-md)',
              textAlign: 'center',
              border: '1px solid var(--gray-200)'
            }}>
              <div style={{ fontSize: '2em', marginBottom: 'var(--spacing-xs)' }}>📊</div>
              <strong style={{ display: 'block', fontSize: '1.5rem', color: 'var(--primary-600)' }}>
                {result.total_files}
              </strong>
              <span style={{ fontSize: '0.9rem', color: 'var(--gray-600)' }}>Total Files</span>
            </div>

            <div style={{
              padding: 'var(--spacing-md)',
              background: 'white',
              borderRadius: 'var(--radius-md)',
              textAlign: 'center',
              border: '1px solid var(--gray-200)'
            }}>
              <div style={{ fontSize: '2em', marginBottom: 'var(--spacing-xs)' }}>✓</div>
              <strong style={{ display: 'block', fontSize: '1.5rem', color: 'var(--success-500)' }}>
                {result.processed_files}
              </strong>
              <span style={{ fontSize: '0.9rem', color: 'var(--gray-600)' }}>Processed</span>
            </div>

            {result.skipped_count > 0 && (
              <div style={{
                padding: 'var(--spacing-md)',
                background: 'white',
                borderRadius: 'var(--radius-md)',
                textAlign: 'center',
                border: '1px solid var(--gray-200)'
              }}>
                <div style={{ fontSize: '2em', marginBottom: 'var(--spacing-xs)' }}>⚠️</div>
                <strong style={{ display: 'block', fontSize: '1.5rem', color: 'var(--warning-500)' }}>
                  {result.skipped_count}
                </strong>
                <span style={{ fontSize: '0.9rem', color: 'var(--gray-600)' }}>Skipped</span>
              </div>
            )}
          </div>

          {/* Download Section */}
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <h3 style={{
              margin: '0 0 var(--spacing-md) 0',
              fontSize: '1.25rem',
              color: 'var(--gray-800)',
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--spacing-xs)'
            }}>
              <span>📥</span>
              Download Datasets
            </h3>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: 'var(--spacing-md)'
            }}>
              {/* CBC Downloads */}
              {(isDownloadable(result.cbc_file) || isDownloadable(result.cbc_file_excel)) && (
                <div style={{
                  background: 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
                  padding: 'var(--spacing-md)',
                  borderRadius: 'var(--radius-md)',
                  border: '2px solid #93c5fd'
                }}>
                  <strong style={{
                    color: '#1e40af',
                    display: 'block',
                    marginBottom: 'var(--spacing-sm)',
                    fontSize: '1.05rem'
                  }}>
                    📄 CBC Data ({result.cbc_count} rows)
                  </strong>
                  <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                    {isDownloadable(result.cbc_file) && (
                      <DownloadButton filename={result.cbc_file} label="CSV" color="#3b82f6" />
                    )}
                    {isDownloadable(result.cbc_file_excel) && (
                      <DownloadButton filename={result.cbc_file_excel} label="Excel" color="#1d4ed8" icon="📊" />
                    )}
                  </div>
                </div>
              )}

              {/* LFT Downloads */}
              {(isDownloadable(result.lft_file) || isDownloadable(result.lft_file_excel)) && (
                <div style={{
                  background: 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)',
                  padding: 'var(--spacing-md)',
                  borderRadius: 'var(--radius-md)',
                  border: '2px solid #6ee7b7'
                }}>
                  <strong style={{
                    color: '#065f46',
                    display: 'block',
                    marginBottom: 'var(--spacing-sm)',
                    fontSize: '1.05rem'
                  }}>
                    🧬 LFT Data ({result.lft_count} rows)
                  </strong>
                  <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                    {isDownloadable(result.lft_file) && (
                      <DownloadButton filename={result.lft_file} label="CSV" color="#10b981" />
                    )}
                    {isDownloadable(result.lft_file_excel) && (
                      <DownloadButton filename={result.lft_file_excel} label="Excel" color="#047857" icon="📊" />
                    )}
                  </div>
                </div>
              )}

              {/* RFT Downloads */}
              {(isDownloadable(result.rft_file) || isDownloadable(result.rft_file_excel)) && (
                <div style={{
                  background: 'linear-gradient(135deg, #fed7aa 0%, #fdba74 100%)',
                  padding: 'var(--spacing-md)',
                  borderRadius: 'var(--radius-md)',
                  border: '2px solid #fb923c'
                }}>
                  <strong style={{
                    color: '#92400e',
                    display: 'block',
                    marginBottom: 'var(--spacing-sm)',
                    fontSize: '1.05rem'
                  }}>
                    💉 RFT Data ({result.rft_count} rows)
                  </strong>
                  <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                    {isDownloadable(result.rft_file) && (
                      <DownloadButton filename={result.rft_file} label="CSV" color="#f59e0b" />
                    )}
                    {isDownloadable(result.rft_file_excel) && (
                      <DownloadButton filename={result.rft_file_excel} label="Excel" color="#b45309" icon="📊" />
                    )}
                  </div>
                </div>
              )}

              {/* TFT Downloads */}
              {(isDownloadable(result.tft_file) || isDownloadable(result.tft_file_excel)) && (
                <div style={{
                  background: 'linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%)',
                  padding: 'var(--spacing-md)',
                  borderRadius: 'var(--radius-md)',
                  border: '2px solid #c084fc'
                }}>
                  <strong style={{
                    color: '#5b21b6',
                    display: 'block',
                    marginBottom: 'var(--spacing-sm)',
                    fontSize: '1.05rem'
                  }}>
                    🦋 TFT Data ({result.tft_count} rows)
                  </strong>
                  <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                    {isDownloadable(result.tft_file) && (
                      <DownloadButton filename={result.tft_file} label="CSV" color="#8b5cf6" />
                    )}
                    {isDownloadable(result.tft_file_excel) && (
                      <DownloadButton filename={result.tft_file_excel} label="Excel" color="#6d28d9" icon="📊" />
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Report & Error Files */}
          {(isDownloadable(result.error_file) || isDownloadable(result.report_file)) && (
            <div style={{
              paddingTop: 'var(--spacing-md)',
              borderTop: '1px solid var(--gray-200)'
            }}>
              <div style={{ display: 'flex', gap: 'var(--spacing-sm)', flexWrap: 'wrap' }}>
                {isDownloadable(result.error_file) && (
                  <DownloadButton filename={result.error_file} label="Error Log" color="#ef4444" icon="⚠️" />
                )}
                {isDownloadable(result.report_file) && (
                  <DownloadButton filename={result.report_file} label="Full Report" color="#64748b" icon="📊" />
                )}
              </div>
            </div>
          )}

          {/* Skipped Files Details */}
          {!!result.skipped_files?.length && (
            <details style={{
              marginTop: 'var(--spacing-md)',
              padding: 'var(--spacing-md)',
              background: 'white',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--gray-200)'
            }}>
              <summary style={{
                cursor: 'pointer',
                fontWeight: '600',
                color: 'var(--gray-700)',
                padding: 'var(--spacing-xs)'
              }}>
                ⚠️ Show details for {result.skipped_files.length} skipped file(s)
              </summary>
              <ul style={{
                marginTop: 'var(--spacing-sm)',
                maxHeight: '200px',
                overflowY: 'auto',
                paddingLeft: 'var(--spacing-lg)'
              }}>
                {result.skipped_files.map((item, index) => (
                  <li key={`${item.file}-${index}`} style={{
                    fontSize: '0.9em',
                    marginBottom: 'var(--spacing-xs)',
                    color: 'var(--gray-700)'
                  }}>
                    <strong>{item.file}</strong>: <span style={{ color: 'var(--error-500)' }}>{item.reason}</span>
                  </li>
                ))}
              </ul>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
