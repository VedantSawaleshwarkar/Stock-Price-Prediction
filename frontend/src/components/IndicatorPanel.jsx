export default function IndicatorPanel({ latest }) {
  const position =
    latest?.Close > latest?.BB_upper
      ? "Above Upper Band"
      : latest?.Close < latest?.BB_lower
        ? "Below Lower Band"
        : "Inside Bands";

  return (
    <div className="card">
      <h3 className="mb-3 text-base font-semibold text-accent">Indicator Panel</h3>
      {latest ? (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div>
            <p className="text-xs text-slate-400">RSI (14)</p>
            <p className="font-mono text-xl">{Number(latest.RSI_14 || 0).toFixed(2)}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400">MACD</p>
            <p className="font-mono text-xl">{Number(latest.MACD || 0).toFixed(4)}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400">Bollinger Position</p>
            <p className="font-mono text-lg">{position}</p>
          </div>
        </div>
      ) : (
        <p className="text-slate-400">Load history to view indicators.</p>
      )}
    </div>
  );
}
