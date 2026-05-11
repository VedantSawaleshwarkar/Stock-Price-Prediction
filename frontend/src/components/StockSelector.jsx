export default function StockSelector({
  ticker,
  setTicker,
  popularTickers,
  customTicker,
  setCustomTicker,
}) {
  return (
    <div className="card flex flex-col gap-4">
      <h2 className="text-lg font-semibold text-accent">Stock Selector</h2>

      <label className="text-sm text-slate-300">Popular tickers</label>
      <select
        className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2"
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
      >
        {popularTickers.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>

      <label className="text-sm text-slate-300">Or enter custom ticker</label>
      <input
        className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 uppercase"
        placeholder="e.g. NVDA"
        value={customTicker}
        onChange={(e) => setCustomTicker(e.target.value.toUpperCase())}
      />
    </div>
  );
}
