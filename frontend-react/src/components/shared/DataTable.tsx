/**
 * components/shared/DataTable.tsx — Dark theme
 */

import React, { useState } from 'react';

interface DataTableProps {
  data: Record<string, any>[];
  rowCount?: number;
  maxRows?: number;
}

const DataTable: React.FC<DataTableProps> = ({ data, rowCount, maxRows = 10 }) => {
  const [currentPage, setCurrentPage] = useState(1);

  const handleExportCSV = () => {
    if (!data || data.length === 0) return;
    const columns = Object.keys(data[0] || {});
    const csvContent = [
      columns.join(','),
      ...data.map(row => columns.map(col => {
        const val = row[col];
        const strVal = val === null || val === undefined ? '' : String(val);
        return `"${strVal.replace(/"/g, '""')}"`;
      }).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'results.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (!data || data.length === 0) return null;

  const columns = Object.keys(data[0] || {});
  const totalPages = Math.ceil(data.length / maxRows);
  const startIdx = (currentPage - 1) * maxRows;
  const paginatedData = data.slice(startIdx, startIdx + maxRows);

  return (
    <div
      className="rounded-xl overflow-hidden text-sm"
      style={{ border: '1px solid var(--input-border)', background: 'var(--chat-surface)' }}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between px-4 py-2.5"
        style={{ background: '#252526', borderBottom: '1px solid var(--input-border)' }}
      >
        <div className="flex items-center gap-2">
          <svg className="w-3.5 h-3.5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M3 10h18M3 6h18M3 14h18M3 18h18" />
          </svg>
          <span className="text-xs font-medium" style={{ color: '#d4d4d4' }}>
            Results
          </span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>
            <span className="font-semibold text-green-400">{rowCount || data.length}</span> rows
            {columns.length > 0 && <span className="ml-1">· {columns.length} cols</span>}
          </span>
          <button
            onClick={handleExportCSV}
            className="text-xs px-2 py-1 rounded transition-colors"
            style={{ background: 'rgba(255,255,255,0.08)', color: 'var(--text-primary)', border: '1px solid var(--input-border)' }}
            title="Xuất ra CSV"
          >
            Export CSV
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr style={{ background: 'rgba(255,255,255,0.04)', borderBottom: '1px solid var(--input-border)' }}>
              <th className="px-3 py-2.5 text-left font-medium w-10" style={{ color: 'var(--text-muted)' }}>#</th>
              {columns.slice(0, 8).map((col) => (
                <th
                  key={col}
                  className="px-3 py-2.5 text-left font-medium max-w-xs truncate"
                  style={{ color: 'var(--text-secondary)' }}
                  title={col}
                >
                  {col}
                </th>
              ))}
              {columns.length > 8 && (
                <th className="px-3 py-2.5 text-left font-medium" style={{ color: 'var(--text-muted)' }}>
                  +{columns.length - 8}
                </th>
              )}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, rowIdx) => (
              <tr
                key={startIdx + rowIdx}
                className="transition-colors"
                style={{
                  borderBottom: '1px solid rgba(255,255,255,0.05)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255,255,255,0.04)')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                <td className="px-3 py-2.5" style={{ color: 'var(--text-muted)' }}>
                  {startIdx + rowIdx + 1}
                </td>
                {columns.slice(0, 8).map((col) => {
                  const value = row[col];
                  const display =
                    value === null || value === undefined
                      ? <span style={{ color: 'var(--text-muted)' }}>NULL</span>
                      : typeof value === 'object'
                        ? JSON.stringify(value)
                        : String(value);
                  return (
                    <td
                      key={`${rowIdx}-${col}`}
                      className="px-3 py-2.5 max-w-xs truncate"
                      style={{ color: 'var(--text-primary)' }}
                      title={typeof display === 'string' ? display : undefined}
                    >
                      {display}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div
          className="flex items-center justify-between px-4 py-2.5"
          style={{ borderTop: '1px solid var(--input-border)', background: '#252526' }}
        >
          <button
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className="text-xs px-3 py-1 rounded transition-colors disabled:opacity-40"
            style={{ background: 'rgba(255,255,255,0.08)', color: 'var(--text-secondary)' }}
          >
            ← Prev
          </button>
          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
            {currentPage} / {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className="text-xs px-3 py-1 rounded transition-colors disabled:opacity-40"
            style={{ background: 'rgba(255,255,255,0.08)', color: 'var(--text-secondary)' }}
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
};

export default DataTable;
