/**
 * components/charts/DynamicChart.tsx
 * ===================================
 * Viết lại hoàn chỉnh, port từ charts.py + visualize_agent.py
 * Hỗ trợ: bar, line, area, pie, scatter, histogram, metric
 * - Tự suy trục x/y (ưu tiên hint từ backend)
 * - Nhận diện cột time-like & metric
 * - Xử lý dữ liệu kiểu string-number từ Databricks
 * - Pie tự cắt top-N & gộp "Khác" (như charts.py)
 * - Scatter đúng format {x,y} của Recharts
 * - Histogram tự bin dữ liệu số
 */

import React, { useMemo } from 'react';
import {
  BarChart, Bar,
  LineChart, Line,
  AreaChart, Area,
  PieChart, Pie, Cell,
  ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import type { VisualizationRecommendation } from '../../types';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────
interface DynamicChartProps {
  data: Record<string, any>[];
  recommendation?: VisualizationRecommendation;
}

// ─────────────────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────────────────
const PRIMARY_COLOR = '#3b82f6';
const PIE_COLORS = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444',
  '#8b5cf6', '#ec4899', '#06b6d4', '#f97316',
];

const TIME_KEYWORDS = [
  'date', 'time', 'month', 'year', 'yr', 'quarter', 'qtr', 'day',
  'hour', 'period', 'gio', 'thang', 'nam', 'quy', 'ngay', 'tuan',
];

const METRIC_KEYWORDS = [
  'total', 'count', 'revenue', 'amount', 'value', 'sales', 'orders',
  'sum', 'avg', 'mean', 'so_don', 'so_luong', 'doanh_thu', 'don_hang',
  'rate', 'ratio', 'percent', 'pct', 'score',
];

const CHART_MARGIN = { top: 12, right: 24, left: 10, bottom: 52 };
const GRID = { strokeDasharray: '3 3', stroke: 'rgba(255,255,255,0.07)' };
const AXIS = {
  tick: { fill: '#9ca3af', fontSize: 11 },
  axisLine: { stroke: 'rgba(255,255,255,0.12)' },
  tickLine: false as false,
};

// ─────────────────────────────────────────────────────────────────────────────
// Data helpers
// ─────────────────────────────────────────────────────────────────────────────

/** Ép giá trị về float, trả NaN nếu không thể */
function toFloat(v: any): number {
  if (v === null || v === undefined || v === '') return NaN;
  return typeof v === 'number' ? v : parseFloat(String(v).replace(/,/g, ''));
}

/** Kiểm tra cột có ≥80% giá trị là số không */
function isNumericCol(data: Record<string, any>[], col: string): boolean {
  const vals = data.map((r) => r[col]).filter((v) => v !== null && v !== undefined && v !== '');
  if (!vals.length) return false;
  return vals.filter((v) => !isNaN(toFloat(v))).length / vals.length >= 0.8;
}

function isTimeLike(col: string): boolean {
  const l = col.toLowerCase();
  return TIME_KEYWORDS.some((k) => l.includes(k));
}

function scoreMetric(col: string): number {
  const l = col.toLowerCase();
  return METRIC_KEYWORDS.filter((k) => l.includes(k)).length;
}

/** Trả về [xCol, yCol] tốt nhất từ dữ liệu */
function resolveAxes(
  data: Record<string, any>[],
  rec: VisualizationRecommendation | undefined,
  chartType: string,
): { x: string; y: string } {
  const cols = Object.keys(data[0] || {});
  const numeric = cols.filter((c) => isNumericCol(data, c));
  const nonNumeric = cols.filter((c) => !numeric.includes(c));
  const timeCols = cols.filter(isTimeLike);

  const xHint = rec?.x;
  const yHint = rec?.y;

  // ── X ──
  let x: string;
  if (xHint && cols.includes(xHint)) {
    x = xHint;
  } else if (['line', 'area'].includes(chartType) && timeCols.length) {
    x = timeCols[0];
  } else if (nonNumeric.length) {
    x = nonNumeric[0];
  } else {
    x = cols[0];
  }

  // ── Y ──
  const yPool = numeric.filter((c) => c !== x && !isTimeLike(c));
  let y: string;
  if (yHint && numeric.includes(yHint) && yHint !== x && !isTimeLike(yHint)) {
    y = yHint;
  } else if (yPool.length) {
    y = [...yPool].sort((a, b) => scoreMetric(b) - scoreMetric(a))[0];
  } else {
    const fallback = numeric.filter((c) => c !== x);
    y = fallback[0] ?? (cols.length > 1 ? cols[1] : cols[0]);
  }

  return { x, y };
}

/** Chuẩn hóa data: ép cột numeric về số thực */
function normalizeData(data: Record<string, any>[], numericCols: string[]): Record<string, any>[] {
  return data.map((row) => {
    const r = { ...row };
    for (const c of numericCols) {
      const f = toFloat(r[c]);
      if (!isNaN(f)) r[c] = f;
    }
    return r;
  });
}

/** Tạo bins cho histogram */
function buildHistogramBins(
  data: Record<string, any>[],
  col: string,
  binCount = 20,
): { bin: string; count: number }[] {
  const vals = data.map((r) => toFloat(r[col])).filter((v) => !isNaN(v));
  if (!vals.length) return [];
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  if (min === max) return [{ bin: String(min), count: vals.length }];
  const step = (max - min) / binCount;
  const bins: { bin: string; count: number }[] = Array.from({ length: binCount }, (_, i) => ({
    bin: (min + i * step).toFixed(2),
    count: 0,
  }));
  for (const v of vals) {
    const idx = Math.min(Math.floor((v - min) / step), binCount - 1);
    bins[idx].count += 1;
  }
  return bins.filter((b) => b.count > 0);
}

/** Pie: top-N + gộp "Khác" như charts.py (max 8 lát) */
function buildPieData(
  data: Record<string, any>[],
  xCol: string,
  yCol: string,
  maxSlices = 8,
): { name: string; value: number }[] {
  const rows = data
    .map((r) => ({ name: String(r[xCol] ?? ''), value: toFloat(r[yCol]) }))
    .filter((r) => !isNaN(r.value) && r.value >= 0)
    .sort((a, b) => b.value - a.value);

  if (rows.length <= maxSlices) return rows;

  const top = rows.slice(0, maxSlices - 1);
  const othersVal = rows.slice(maxSlices - 1).reduce((s, r) => s + r.value, 0);
  return [...top, { name: 'Khác', value: othersVal }];
}

// ─────────────────────────────────────────────────────────────────────────────
// Tooltip
// ─────────────────────────────────────────────────────────────────────────────
const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.15)',
      borderRadius: 8, padding: '8px 12px', fontSize: 12, minWidth: 120,
    }}>
      {label !== undefined && (
        <p style={{ color: '#9ca3af', marginBottom: 4, fontWeight: 500 }}>{label}</p>
      )}
      {payload.map((p: any, i: number) => (
        <p key={i} style={{ color: p.color ?? PRIMARY_COLOR, margin: '2px 0' }}>
          {p.name}: <strong>
            {typeof p.value === 'number'
              ? p.value % 1 === 0 ? p.value.toLocaleString() : p.value.toLocaleString(undefined, { maximumFractionDigits: 2 })
              : p.value}
          </strong>
        </p>
      ))}
    </div>
  );
};

// Axis label helpers
const xLabel = (v: string) => ({ value: v, position: 'insideBottom' as const, offset: -10, fill: '#6b7280', fontSize: 11 });
const yLabel = (v: string) => ({ value: v, angle: -90, position: 'insideLeft' as const, offset: 14, fill: '#6b7280', fontSize: 11 });

// ─────────────────────────────────────────────────────────────────────────────
// Main Component
// ─────────────────────────────────────────────────────────────────────────────
const DynamicChart: React.FC<DynamicChartProps> = ({ data, recommendation }) => {
  const chartType = (recommendation?.chart_type ?? 'bar').toLowerCase();

  // Bỏ qua nếu không cần vẽ
  if (!data || data.length === 0) return null;
  if (['table', 'conversation'].includes(chartType)) return null;

  const cols = Object.keys(data[0] || {});
  const numericCols = cols.filter((c) => isNumericCol(data, c));
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const normData = useMemo(() => normalizeData(data, numericCols), [data]);

  const { x, y } = resolveAxes(normData, recommendation, chartType);
  const reason = recommendation?.reason;
  const title = recommendation?.title;

  // ── METRIC ───────────────────────────────────────────────────────────────
  if (chartType === 'metric') {
    const label = recommendation?.label ?? title ?? 'Kết quả';
    const raw = recommendation?.value ?? normData[0]?.[y] ?? normData[0]?.[cols[0]];
    const val = typeof raw === 'number'
      ? raw % 1 === 0 ? raw.toLocaleString() : raw.toLocaleString(undefined, { maximumFractionDigits: 2 })
      : raw;
    return (
      <div className="rounded-xl p-6 mt-3 flex flex-col items-center gap-1"
        style={{ border: '1px solid var(--input-border)', background: 'var(--chat-surface)' }}>
        <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{label}</p>
        <p className="text-4xl font-bold" style={{ color: PRIMARY_COLOR }}>{val}</p>
        {reason && <p className="text-xs mt-2 italic" style={{ color: 'var(--text-muted)' }}>💡 {reason}</p>}
      </div>
    );
  }

  // ── HISTOGRAM ─────────────────────────────────────────────────────────────
  if (chartType === 'histogram') {
    // Chọn cột số để bin: ưu tiên y-hint, sau đó cột số đầu tiên không phải x
    const histCol = (recommendation?.y && numericCols.includes(recommendation.y))
      ? recommendation.y
      : numericCols.find((c) => c !== x) ?? numericCols[0] ?? y;
    const bins = buildHistogramBins(normData, histCol, 20);

    return (
      <ChartWrapper chartType={chartType} title={title} reason={reason}>
        <BarChart data={bins} margin={CHART_MARGIN}>
          <CartesianGrid {...GRID} />
          <XAxis dataKey="bin" {...AXIS} label={xLabel(histCol)}
            interval={Math.floor(bins.length / 8)} angle={-35} textAnchor="end" />
          <YAxis {...AXIS} label={yLabel('Tần suất')} />
          <Tooltip content={<CustomTooltip />} />
          <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 16, color: '#9ca3af', fontSize: 12 }} />
          <Bar dataKey="count" name="Tần suất" fill={PRIMARY_COLOR} radius={[3, 3, 0, 0]} />
        </BarChart>
      </ChartWrapper>
    );
  }

  // ── PIE ──────────────────────────────────────────────────────────────────
  if (chartType === 'pie') {
    const pieData = buildPieData(normData, x, y, 8);
    const RADIAN = Math.PI / 180;
    const renderPieLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
      if (percent < 0.04) return null;
      const r = innerRadius + (outerRadius - innerRadius) * 0.55;
      return (
        <text
          x={cx + r * Math.cos(-midAngle * RADIAN)}
          y={cy + r * Math.sin(-midAngle * RADIAN)}
          fill="#fff" textAnchor="middle" dominantBaseline="central" fontSize={11} fontWeight={600}
        >
          {`${(percent * 100).toFixed(1)}%`}
        </text>
      );
    };

    return (
      <ChartWrapper chartType={chartType} title={title} reason={reason}>
        <PieChart>
          <Pie
            data={pieData} dataKey="value" nameKey="name"
            cx="50%" cy="50%" outerRadius={145}
            labelLine={false} label={renderPieLabel}
          >
            {pieData.map((_, i) => (
              <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(v: any) => typeof v === 'number' ? v.toLocaleString(undefined, { maximumFractionDigits: 2 }) : v}
          />
          <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 16, color: '#9ca3af', fontSize: 12 }} />
        </PieChart>
      </ChartWrapper>
    );
  }

  // ── SCATTER ──────────────────────────────────────────────────────────────
  if (chartType === 'scatter') {
    // Recharts Scatter cần array {x, y} dạng số
    const xNumeric = numericCols.includes(x);
    const scatterData = normData
      .map((r) => ({
        xVal: xNumeric ? toFloat(r[x]) : undefined,
        label: xNumeric ? undefined : String(r[x] ?? ''),
        yVal: toFloat(r[y]),
      }))
      .filter((r) => !isNaN(r.yVal));

    if (!xNumeric) {
      // Fallback: dùng BarChart khi x không phải số
      return (
        <ChartWrapper chartType="bar" title={title} reason={reason}>
          <BarChart data={normData} margin={CHART_MARGIN}>
            <CartesianGrid {...GRID} />
            <XAxis dataKey={x} {...AXIS} interval={0}
              angle={normData.length > 10 ? -35 : 0}
              textAnchor={normData.length > 10 ? 'end' : 'middle'}
              label={xLabel(x)} />
            <YAxis {...AXIS} tickFormatter={(v) => typeof v === 'number' ? v.toLocaleString() : v} label={yLabel(y)} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey={y} fill={PRIMARY_COLOR} radius={[5, 5, 0, 0]} />
          </BarChart>
        </ChartWrapper>
      );
    }

    const scatterFmt = scatterData.map((d) => ({ x: d.xVal, y: d.yVal }));
    return (
      <ChartWrapper chartType={chartType} title={title} reason={reason}>
        <ScatterChart margin={CHART_MARGIN}>
          <CartesianGrid {...GRID} />
          <XAxis type="number" dataKey="x" name={x} {...AXIS}
            tickFormatter={(v) => typeof v === 'number' ? v.toLocaleString() : v}
            label={xLabel(x)} />
          <YAxis type="number" dataKey="y" name={y} {...AXIS}
            tickFormatter={(v) => typeof v === 'number' ? v.toLocaleString() : v}
            label={yLabel(y)} />
          <Tooltip cursor={{ strokeDasharray: '3 3' }}
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const d = payload[0]?.payload;
              return (
                <div style={{ background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.15)', borderRadius: 8, padding: '8px 12px', fontSize: 12 }}>
                  <p style={{ color: '#9ca3af' }}>{x}: <strong style={{ color: '#fff' }}>{d?.x?.toLocaleString()}</strong></p>
                  <p style={{ color: '#9ca3af' }}>{y}: <strong style={{ color: PRIMARY_COLOR }}>{d?.y?.toLocaleString()}</strong></p>
                </div>
              );
            }} />
          <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 16, color: '#9ca3af', fontSize: 12 }} />
          <Scatter name={`${x} vs ${y}`} data={scatterFmt} fill={PRIMARY_COLOR} fillOpacity={0.75} />
        </ScatterChart>
      </ChartWrapper>
    );
  }

  // ── LINE ────────────────────────────────────────────────────────────────
  if (chartType === 'line') {
    return (
      <ChartWrapper chartType={chartType} title={title} reason={reason}>
        <LineChart data={normData} margin={CHART_MARGIN}>
          <CartesianGrid {...GRID} />
          <XAxis dataKey={x} {...AXIS}
            interval={normData.length > 12 ? Math.floor(normData.length / 12) : 0}
            angle={normData.length > 12 ? -35 : 0}
            textAnchor={normData.length > 12 ? 'end' : 'middle'}
            label={xLabel(x)} />
          <YAxis {...AXIS} tickFormatter={(v) => typeof v === 'number' ? v.toLocaleString() : v} label={yLabel(y)} />
          <Tooltip content={<CustomTooltip />} />
          <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 16, color: '#9ca3af', fontSize: 12 }} />
          <Line type="monotone" dataKey={y} stroke={PRIMARY_COLOR} strokeWidth={2.5}
            dot={{ fill: PRIMARY_COLOR, r: 3, strokeWidth: 0 }} activeDot={{ r: 6 }} />
        </LineChart>
      </ChartWrapper>
    );
  }

  // ── AREA ────────────────────────────────────────────────────────────────
  if (chartType === 'area') {
    return (
      <ChartWrapper chartType={chartType} title={title} reason={reason}>
        <AreaChart data={normData} margin={CHART_MARGIN}>
          <defs>
            <linearGradient id="areaG" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={PRIMARY_COLOR} stopOpacity={0.35} />
              <stop offset="95%" stopColor={PRIMARY_COLOR} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid {...GRID} />
          <XAxis dataKey={x} {...AXIS}
            interval={normData.length > 12 ? Math.floor(normData.length / 12) : 0}
            angle={normData.length > 12 ? -35 : 0}
            textAnchor={normData.length > 12 ? 'end' : 'middle'}
            label={xLabel(x)} />
          <YAxis {...AXIS} tickFormatter={(v) => typeof v === 'number' ? v.toLocaleString() : v} label={yLabel(y)} />
          <Tooltip content={<CustomTooltip />} />
          <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 16, color: '#9ca3af', fontSize: 12 }} />
          <Area type="monotone" dataKey={y} stroke={PRIMARY_COLOR} strokeWidth={2.5} fill="url(#areaG)" />
        </AreaChart>
      </ChartWrapper>
    );
  }

  // ── BAR (default) ────────────────────────────────────────────────────────
  const rotateX = normData.length > 8;
  return (
    <ChartWrapper chartType={chartType} title={title} reason={reason}>
      <BarChart data={normData} margin={CHART_MARGIN}>
        <CartesianGrid {...GRID} />
        <XAxis dataKey={x} {...AXIS}
          interval={0}
          angle={rotateX ? -38 : 0}
          textAnchor={rotateX ? 'end' : 'middle'}
          label={xLabel(x)} />
        <YAxis {...AXIS} tickFormatter={(v) => typeof v === 'number' ? v.toLocaleString() : v} label={yLabel(y)} />
        <Tooltip content={<CustomTooltip />} />
        <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 16, color: '#9ca3af', fontSize: 12 }} />
        <Bar dataKey={y} fill={PRIMARY_COLOR} radius={[5, 5, 0, 0]} maxBarSize={60} />
      </BarChart>
    </ChartWrapper>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Wrapper: header + card + responsive container
// ─────────────────────────────────────────────────────────────────────────────
const CHART_ICONS: Record<string, string> = {
  bar: '📊', histogram: '📊', line: '📈', area: '📉',
  pie: '🥧', scatter: '✦', metric: '🔢',
};

interface WrapperProps {
  chartType: string;
  title?: string | null;
  reason?: string | null;
  children: React.ReactElement;
}

const ChartWrapper: React.FC<WrapperProps> = ({ chartType, reason, children }) => (
  <div className="rounded-xl mt-3 overflow-hidden"
    style={{ border: '1px solid var(--input-border)', background: 'var(--chat-surface)' }}>
    {/* Header */}
    <div className="px-4 pt-3 pb-1 flex items-center gap-2">
      <span className="text-xs font-semibold" style={{ color: '#d4d4d4' }}>
        {CHART_ICONS[chartType] ?? '📌'} Biểu đồ
      </span>
      {reason && (
        <span className="text-xs italic" style={{ color: 'var(--text-muted)' }}>— {reason}</span>
      )}
    </div>
    {/* Chart */}
    <div className="px-2 pb-4">
      <ResponsiveContainer width="100%" height={360}>
        {children}
      </ResponsiveContainer>
    </div>
  </div>
);

export default DynamicChart;
