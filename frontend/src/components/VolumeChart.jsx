import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function VolumeChart({ data }) {
  const chartData = (data || []).map((row) => ({
    date: row.Date,
    volume: row.Volume,
  }));

  return (
    <div className="card h-[300px]">
      <h3 className="mb-3 text-base font-semibold text-accent">Volume (Last 90 Days)</h3>
      <ResponsiveContainer width="100%" height="88%">
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#253043" />
          <XAxis dataKey="date" tick={{ fill: "#94a3b8", fontSize: 10 }} />
          <YAxis tick={{ fill: "#94a3b8", fontSize: 10 }} />
          <Tooltip />
          <Bar dataKey="volume" fill="#00d4ff" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
