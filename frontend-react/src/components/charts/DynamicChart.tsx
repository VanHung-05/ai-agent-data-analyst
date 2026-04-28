/**
 * components/charts/DynamicChart.tsx
 * ===================================
 * Component tự động map dữ liệu và vẽ chart động dựa trên loại chart type
 */

import React from 'react';
import {
  BarChart,
  LineChart,
  PieChart,
  AreaChart,
  ScatterChart,
  Bar,
  Line,
  Pie,
  Area,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import type { VisualizationRecommendation } from '../../types';

interface DynamicChartProps {
  data: Record<string, any>[];
  recommendation?: VisualizationRecommendation;
}

// Color palette for charts
const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316'];

const DynamicChart: React.FC<DynamicChartProps> = ({ data, recommendation }) => {
  if (!data || data.length === 0) {
    return null;
  }

  const chartType = recommendation?.chart_type || 'bar';
  const xAxis = recommendation?.x || Object.keys(data[0])[0];
  const yAxis = recommendation?.y || Object.keys(data[0])[1];
  const title = recommendation?.title || 'Chart';

  if (!xAxis || !yAxis) {
    return (
      <div className="bg-gray-100 rounded-lg p-6 text-center text-gray-600">
        <p>Không đủ dữ liệu để vẽ biểu đồ</p>
      </div>
    );
  }

  try {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 mt-3">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>

        <ResponsiveContainer width="100%" height={400}>
          {chartType === 'line' ? (
            <LineChart
              data={data}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey={yAxis}
                stroke={COLORS[0]}
                strokeWidth={2}
                dot={{ fill: COLORS[0], r: 4 }}
              />
            </LineChart>
          ) : chartType === 'pie' ? (
            <PieChart>
              <Pie
                data={data}
                dataKey={yAxis}
                nameKey={xAxis}
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          ) : chartType === 'area' ? (
            <AreaChart
              data={data}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey={yAxis}
                fill={COLORS[0]}
                stroke={COLORS[0]}
                opacity={0.6}
              />
            </AreaChart>
          ) : chartType === 'scatter' ? (
            <ScatterChart
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxis} />
              <YAxis dataKey={yAxis} />
              <Tooltip />
              <Legend />
              <Scatter
                name={yAxis}
                data={data}
                fill={COLORS[0]}
              />
            </ScatterChart>
          ) : (
            // Default to Bar chart
            <BarChart
              data={data}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar
                dataKey={yAxis}
                fill={COLORS[0]}
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          )}
        </ResponsiveContainer>

        {recommendation?.reason && (
          <p className="text-xs text-gray-500 mt-4 italic">
            💡 {recommendation.reason}
          </p>
        )}
      </div>
    );
  } catch (error) {
    console.error('Error rendering chart:', error);
    return (
      <div className="bg-red-50 rounded-lg p-6 text-center text-red-600 border border-red-200 mt-3">
        <p>Lỗi khi vẽ biểu đồ</p>
        <p className="text-xs mt-2">{error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    );
  }
};

export default DynamicChart;
