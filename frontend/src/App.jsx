import { useEffect, useMemo, useState } from "react";
import { getHistory, getTickers, predictStock, trainModels } from "./api/client";
import IndicatorPanel from "./components/IndicatorPanel";
import ModelComparisonTable from "./components/ModelComparisonTable";
import PredictionCard from "./components/PredictionCard";
import PriceChart from "./components/PriceChart";
import DateRangePicker from "./components/DateRangePicker";
import StockSelector from "./components/StockSelector";
import TrainButton from "./components/TrainButton";
import VolumeChart from "./components/VolumeChart";

export default function App() {
  const [popularTickers, setPopularTickers] = useState(["AAPL"]);
  const [ticker, setTicker] = useState("AAPL");
  const [customTicker, setCustomTicker] = useState("");
  const [startDate, setStartDate] = useState("2019-01-01");

  const [history, setHistory] = useState([]);
  const [trainResult, setTrainResult] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loadingTrain, setLoadingTrain] = useState(false);
  const [loadingPredict, setLoadingPredict] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [error, setError] = useState("");

  const effectiveTicker = useMemo(
    () => (customTicker.trim() ? customTicker.trim().toUpperCase() : ticker.toUpperCase()),
    [customTicker, ticker]
  );

  const loadHistory = async (symbol) => {
    setLoadingHistory(true);
    setError("");
    try {
      const res = await getHistory(symbol);
      setHistory(res.history || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load history");
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    const bootstrap = async () => {
      try {
        const data = await getTickers();
        setPopularTickers(data);
        if (data?.length) setTicker(data[0]);
      } catch {
        setPopularTickers(["AAPL", "TSLA", "GOOGL", "MSFT"]);
      }
    };
    bootstrap();
  }, []);

  useEffect(() => {
    loadHistory(effectiveTicker);
  }, [effectiveTicker]);

  const onTrain = async () => {
    const selected = new Date(startDate + "T12:00:00");
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    selected.setHours(0, 0, 0, 0);
    if (selected >= today) {
      window.alert("Training start date must be before today. Choose an earlier date.");
      return;
    }

    setLoadingTrain(true);
    setError("");
    try {
      const data = await trainModels({ ticker: effectiveTicker, start_date: startDate });
      setTrainResult(data);
      await loadHistory(effectiveTicker);
    } catch (err) {
      setError(err?.response?.data?.detail || "Training failed");
    } finally {
      setLoadingTrain(false);
    }
  };

  const onPredict = async () => {
    setLoadingPredict(true);
    setError("");
    try {
      const data = await predictStock({ ticker: effectiveTicker });
      setPrediction(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Prediction failed");
    } finally {
      setLoadingPredict(false);
    }
  };

  const latest = history.length ? history[history.length - 1] : null;

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-5 p-4 md:p-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-accent md:text-3xl">Stock Price Prediction Dashboard</h1>
        <p className="text-sm text-slate-400">Ticker: {effectiveTicker}</p>
      </header>

      {error ? (
        <div className="rounded-lg border border-rose-600/40 bg-rose-600/10 px-4 py-2 text-rose-300">{error}</div>
      ) : null}

      <section className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <StockSelector
          ticker={ticker}
          setTicker={setTicker}
          popularTickers={popularTickers}
          customTicker={customTicker}
          setCustomTicker={setCustomTicker}
        />

        <div className="card flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-accent">Training Controls</h2>
          <DateRangePicker startDate={startDate} setStartDate={setStartDate} />
          <TrainButton onTrain={onTrain} loading={loadingTrain} />
          <button
            onClick={onPredict}
            disabled={loadingPredict}
            className="rounded-lg border border-accent px-4 py-2 font-semibold text-accent transition hover:bg-accent/10 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loadingPredict ? "Predicting..." : "Predict Next Day"}
          </button>
        </div>

        <PredictionCard prediction={prediction} loading={loadingPredict} />
      </section>

      <IndicatorPanel latest={latest} />

      <section className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <div className="relative">
          {loadingHistory ? <p className="absolute left-4 top-3 animate-pulse text-xs text-slate-400">Loading history...</p> : null}
          <PriceChart data={history} prediction={prediction} />
        </div>
        <VolumeChart data={history} />
      </section>

      <ModelComparisonTable trainResult={trainResult} />
    </main>
  );
}
