import React from 'react';
import UploadBox from "./UploadBox";

export default function App() {
  return (
    <div className="container">
      {/* Hero Header */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '3rem 2rem',
        borderRadius: 'var(--radius-xl)',
        marginBottom: 'var(--spacing-2xl)',
        color: 'white',
        textAlign: 'center',
        boxShadow: 'var(--shadow-xl)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'relative', zIndex: 1 }}>
          <h1 className="fade-in" style={{
            margin: '0 0 1rem 0',
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: '800',
            letterSpacing: '-0.02em'
          }}>
            🧪 Lab Data Extractor
          </h1>
          <p className="fade-in" style={{
            margin: '0',
            fontSize: 'clamp(1rem, 2.5vw, 1.25rem)',
            opacity: '0.95',
            maxWidth: '600px',
            marginLeft: 'auto',
            marginRight: 'auto',
            fontWeight: '400'
          }}>
            Transform medical lab reports into structured datasets instantly
          </p>
          <div className="fade-in" style={{
            marginTop: '1.5rem',
            display: 'flex',
            gap: 'var(--spacing-md)',
            justifyContent: 'center',
            flexWrap: 'wrap',
            fontSize: '0.9rem',
            opacity: '0.9'
          }}>
            <span>✓ PDF & Word Support</span>
            <span>✓ OCR for Scanned Docs</span>
            <span>✓ CSV & Excel Export</span>
          </div>
        </div>
        {/* Background decoration */}
        <div style={{
          position: 'absolute',
          top: '-50%',
          right: '-10%',
          width: '300px',
          height: '300px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '50%',
          filter: 'blur(60px)'
        }}></div>
      </div>

      {/* Feature Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: 'var(--spacing-lg)',
        marginBottom: 'var(--spacing-2xl)'
      }}>
        <div className="feature-card feature-card-cbc slide-up">
          <div style={{ fontSize: '3em', marginBottom: 'var(--spacing-sm)' }}>📄</div>
          <strong style={{ fontSize: '1.1rem', display: 'block', marginBottom: 'var(--spacing-xs)', color: 'var(--gray-800)' }}>
            CBC Reports
          </strong>
          <p style={{ fontSize: '0.9em', color: 'var(--gray-600)', margin: '0' }}>
            Complete Blood Count
          </p>
        </div>

        <div className="feature-card feature-card-lft slide-up" style={{ animationDelay: '0.1s' }}>
          <div style={{ fontSize: '3em', marginBottom: 'var(--spacing-sm)' }}>🧬</div>
          <strong style={{ fontSize: '1.1rem', display: 'block', marginBottom: 'var(--spacing-xs)', color: 'var(--gray-800)' }}>
            LFT Reports
          </strong>
          <p style={{ fontSize: '0.9em', color: 'var(--gray-600)', margin: '0' }}>
            Liver Function Test
          </p>
        </div>

        <div className="feature-card feature-card-rft slide-up" style={{ animationDelay: '0.2s' }}>
          <div style={{ fontSize: '3em', marginBottom: 'var(--spacing-sm)' }}>💉</div>
          <strong style={{ fontSize: '1.1rem', display: 'block', marginBottom: 'var(--spacing-xs)', color: 'var(--gray-800)' }}>
            RFT Reports
          </strong>
          <p style={{ fontSize: '0.9em', color: 'var(--gray-600)', margin: '0' }}>
            Renal Function Test
          </p>
        </div>

        <div className="feature-card feature-card-tft slide-up" style={{ animationDelay: '0.3s' }}>
          <div style={{ fontSize: '3em', marginBottom: 'var(--spacing-sm)' }}>🦋</div>
          <strong style={{ fontSize: '1.1rem', display: 'block', marginBottom: 'var(--spacing-xs)', color: 'var(--gray-800)' }}>
            TFT Reports
          </strong>
          <p style={{ fontSize: '0.9em', color: 'var(--gray-600)', margin: '0' }}>
            Thyroid Function Test
          </p>
        </div>

        <div style={{ padding: '20px', background: '#e0f2fe', borderRadius: '10px', textAlign: 'center' }}>
          <div style={{ fontSize: '2em' }}>🦋</div>
          <strong>TFT Reports</strong>
          <p style={{ fontSize: '0.9em', color: '#666', margin: '5px 0 0 0' }}>Thyroid Function Test</p>
        </div>
      </div>

      {/* Upload Section */}
      <div className="slide-up" style={{ animationDelay: '0.4s' }}>
        <UploadBox />
      </div>

      {/* Footer */}
      <footer style={{
        marginTop: 'var(--spacing-2xl)',
        paddingTop: 'var(--spacing-xl)',
        textAlign: 'center',
        color: 'var(--gray-600)',
        fontSize: '0.9rem',
        borderTop: '1px solid var(--gray-200)'
      }}>
        <p style={{ margin: '0', fontWeight: '500' }}>
          A project by <strong style={{ color: 'var(--primary-600)' }}>Paksa IT Solutions</strong>
        </p>
        <p style={{ margin: 'var(--spacing-xs) 0 0 0', fontSize: '0.85rem', opacity: '0.8' }}>
          © 2026 All rights reserved
        </p>
      </footer>
    </div>
  );
}
