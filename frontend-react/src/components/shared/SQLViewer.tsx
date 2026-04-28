/**
 * components/shared/SQLViewer.tsx — Dark theme
 */

import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface SQLViewerProps {
  sql: string;
}

const SQLViewer: React.FC<SQLViewerProps> = ({ sql }) => {
  const [copied, setCopied] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className="rounded-xl overflow-hidden text-sm"
      style={{ border: '1px solid var(--input-border)', background: '#1e1e1e' }}
    >
      {/* Header bar */}
      <div
        className="flex items-center justify-between px-4 py-2"
        style={{ background: '#252526', borderBottom: '1px solid var(--input-border)' }}
      >
        <div className="flex items-center gap-2">
          <svg className="w-3.5 h-3.5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 7h16M4 12h16M4 17h7" />
          </svg>
          <span className="text-xs font-medium" style={{ color: '#d4d4d4' }}>Generated SQL</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="text-xs px-2 py-0.5 rounded transition-colors hover:bg-white/10"
            style={{ color: '#8e8ea0' }}
          >
            {collapsed ? 'Show' : 'Hide'}
          </button>
          <button
            onClick={handleCopy}
            className="text-xs px-2 py-0.5 rounded transition-colors"
            style={{
              background: copied ? 'rgba(25,195,125,0.2)' : 'rgba(255,255,255,0.08)',
              color: copied ? '#19c37d' : '#8e8ea0',
            }}
          >
            {copied ? '✓ Copied' : 'Copy'}
          </button>
        </div>
      </div>

      {/* Code block */}
      {!collapsed && (
        <div className="overflow-x-auto">
          <SyntaxHighlighter
            language="sql"
            style={vscDarkPlus}
            customStyle={{ margin: 0, borderRadius: 0, fontSize: '12px', padding: '14px 16px', background: '#1e1e1e' }}
            wrapLongLines
          >
            {sql}
          </SyntaxHighlighter>
        </div>
      )}
    </div>
  );
};

export default SQLViewer;
