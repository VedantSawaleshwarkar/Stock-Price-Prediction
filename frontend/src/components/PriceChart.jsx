import {
  CartesianGrid,
  Dot,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function PriceChart({ data, prediction }) {
  const chartData = (data || []).map((row) => ({
    date: row.Date,
    close: row.Close,
    sma20: row.SMA_20,
    sma50: row.SMA_50,
  }));

  if (prediction && chartData.length) {
    chartData.push({
      date: "Next",
      close: null,
      sma20: null,
      sma50: null,
      predicted: prediction.predicted_price,
    });
  }

  return (
    <div className="card h-[340px]">
      <h3 className="mb-3 text-base font-semibold text-accent">Price + SMA Overlay</h3>
      <ResponsiveContainer width="100%" height="92%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#253043" />
          <XAxis dataKey="date" tick={{ fill: "#94a3b8", fontSize: 10 }} />
          <YAxis tick={{ fill: "#94a3b8", fontSize: 10 }} />
          <Tooltip />
          <Line type="monotone" dataKey="close" stroke="#00d4ff" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="sma20" stroke="#22c55e" dot={false} />
          <Line type="monotone" dataKey="sma50" stroke="#eab308" dot={false} />
          <Line
            type="linear"
            dataKey="predicted"
            stroke="#f43f5e"
            dot={(props) =>
              props.payload?.predicted ? (
                <Dot {...props} r={6} fill="#f43f5e" stroke="#fff" strokeWidth={1} />
              ) : null
            }
            connectNulls={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
