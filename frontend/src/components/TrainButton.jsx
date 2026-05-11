export default function TrainButton({ onTrain, loading }) {
  return (
    <button
      onClick={onTrain}
      disabled={loading}
      className="rounded-lg bg-accent px-4 py-2 font-semibold text-black transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
    >
      {loading ? "Training..." : "Train Models"}
    </button>
  );
}
