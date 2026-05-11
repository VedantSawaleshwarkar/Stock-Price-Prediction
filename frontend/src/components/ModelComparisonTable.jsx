export default function ModelComparisonTable({ trainResult }) {
  const regRows = trainResult?.regression?.metrics || [];
  const clsRows = trainResult?.classification?.metrics || [];

  const rows = [
    ...regRows.map((r) => ({
      type: "Regression",
      model: r.model,
      metricA: `MAE: ${r.mae.toFixed(4)}`,
      metricB: `RMSE: ${r.rmse.toFixed(4)}`,
      metricC: `R2: ${r.r2.toFixed(4)}`,
    })),
    ...clsRows.map((r) => ({
      type: "Classification",
      model: r.model,
      metricA: `Acc: ${r.accuracy.toFixed(4)}`,
      metricB: `Prec: ${r.precision.toFixed(4)}`,
      metricC: `F1: ${r.f1.toFixed(4)}`,
    })),
  ];

  return (
    <div className="card overflow-x-auto">
      <h3 className="mb-3 text-base font-semibold text-accent">Model Comparison Table</h3>
      <table className="w-full min-w-[720px] text-left text-sm">
        <thead>
          <tr className="border-b border-slate-700 text-slate-300">
            <th className="py-2">Type</th>
            <th className="py-2">Model</th>
            <th className="py-2">Metric 1</th>
            <th className="py-2">Metric 2</th>
            <th className="py-2">Metric 3</th>
          </tr>
        </thead>
        <tbody>
          {rows.length ? (
            rows.map((row) => (
              <tr key={`${row.type}-${row.model}`} className="border-b border-slate-800 text-slate-200">
                <td className="py-2">{row.type}</td>
                <td className="py-2">{row.model}</td>
                <td className="py-2 font-mono">{row.metricA}</td>
                <td className="py-2 font-mono">{row.metricB}</td>
                <td className="py-2 font-mono">{row.metricC}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={5} className="py-4 text-slate-400">
                No training metrics yet.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
