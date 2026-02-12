import React from 'react';
import UploadBox from "./UploadBox";

export default function App() {
  return (
    <div className="container">
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '40px 20px',
        borderRadius: '15px',
        marginBottom: '30px',
        color: 'white',
        textAlign: 'center',
        boxShadow: '0 10px 30px rgba(0,0,0,0.2)'
      }}>
        <h1 style={{ margin: '0 0 10px 0', fontSize: '2.5em', fontWeight: 'bold' }}>
          🧪 Paksa Lab Data Extractor
        </h1>
        <p style={{ margin: '0', fontSize: '1.1em', opacity: '0.95' }}>
          Transform medical lab reports into structured datasets instantly
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '15px',
        marginBottom: '30px'
      }}>
        <div style={{ padding: '20px', background: '#f0f9ff', borderRadius: '10px', textAlign: 'center' }}>
          <div style={{ fontSize: '2em' }}>📄</div>
          <strong>CBC Reports</strong>
          <p style={{ fontSize: '0.9em', color: '#666', margin: '5px 0 0 0' }}>Complete Blood Count</p>
        </div>
        <div style={{ padding: '20px', background: '#fef3c7', borderRadius: '10px', textAlign: 'center' }}>
          <div style={{ fontSize: '2em' }}>🧬</div>
          <strong>LFT Reports</strong>
          <p style={{ fontSize: '0.9em', color: '#666', margin: '5px 0 0 0' }}>Liver Function Test</p>
        </div>
        <div style={{ padding: '20px', background: '#fce7f3', borderRadius: '10px', textAlign: 'center' }}>
          <div style={{ fontSize: '2em' }}>💉</div>
          <strong>RFT Reports</strong>
          <p style={{ fontSize: '0.9em', color: '#666', margin: '5px 0 0 0' }}>Renal Function Test</p>
        </div>

        <div style={{ padding: '20px', background: '#e0f2fe', borderRadius: '10px', textAlign: 'center' }}>
          <div style={{ fontSize: '2em' }}>🦋</div>
          <strong>TFT Reports</strong>
          <p style={{ fontSize: '0.9em', color: '#666', margin: '5px 0 0 0' }}>Thyroid Function Test</p>
        </div>
      </div>

      <UploadBox />
      
      <footer style={{ marginTop: '50px', textAlign: 'center', color: '#666', fontSize: '14px', paddingTop: '20px', borderTop: '1px solid #e5e7eb' }}>
        <p style={{ margin: '0' }}>A project by <strong style={{ color: '#667eea' }}>Paksa IT Solutions</strong></p>
        <p style={{ margin: '5px 0 0 0', fontSize: '12px' }}>© 2026 All rights reserved</p>
      </footer>
    </div>
  );
}
