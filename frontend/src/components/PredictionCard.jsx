export default function PredictionCard({ prediction, loading }) {
  const trendUp = prediction?.trend === "UP";

  return (
    <div className="card border-accent shadow-glow transition-all duration-300">
      <h2 className="mb-4 text-lg font-semibold text-accent">Prediction Panel</h2>
      {loading ? (
        <p className="animate-pulse text-slate-300">Generating prediction...</p>
      ) : prediction ? (
        <div className="space-y-3">
          <p className="text-sm text-slate-400">Predicted next close</p>
          <p className="font-mono text-3xl font-bold">${prediction.predicted_price}</p>
          <span
            className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
              trendUp ? "bg-emerald-600/20 text-emerald-300" : "bg-rose-600/20 text-rose-300"
            }`}
          >
            {prediction.trend}
          </span>
          <p className="text-sm text-slate-300">
            Confidence: <span className="font-mono">{(prediction.confidence * 100).toFixed(2)}%</span>
          </p>
          <p className="text-xs text-slate-500">Model: {prediction.model_used}</p>
        </div>
      ) : (
        <p className="text-slate-400">Train and predict to view results.</p>
      )}
    </div>
  );
}
