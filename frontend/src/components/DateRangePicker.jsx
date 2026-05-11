export default function DateRangePicker({ startDate, setStartDate }) {
  return (
    <>
      <label className="text-sm text-slate-300">Date range start</label>
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
        className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2"
      />
    </>
  );
}
