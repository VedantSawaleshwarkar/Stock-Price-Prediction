# Stock Price Prediction System using ML

Full-stack stock prediction app with:
- **Backend**: FastAPI + scikit-learn + XGBoost + yfinance + ta
- **Frontend**: React (Vite) + Tailwind CSS + Recharts

The system trains 8 real ML models on historical market data and provides:
- Next-day closing price prediction (regression)
- Next-day trend prediction (classification)
- Model comparison metrics
- Interactive charts and indicator panels

## Project Structure

```text
backend/
  main.py
  data/
    fetcher.py
    features.py
  models/
    regression.py
    classification.py
  saved_models/
frontend/
  src/
    App.jsx
    api/client.js
    components/
```

## Backend Setup

1. Create and activate a Python virtual environment.
2. Install dependencies from the **repository root** (where `requirements.txt` is):

```bash
pip install -r requirements.txt
```

On Windows, if `pip` is not on your PATH, use:

```bash
python -m pip install -r requirements.txt
```

3. Run backend:

```bash
cd backend
uvicorn main:app --reload
```

If port 8000 is already in use:

```bash
uvicorn main:app --reload --port 8001
```

Backend defaults to `http://127.0.0.1:8000`. If you use another port, set the frontend URL (see below).

## Frontend Setup

1. Install frontend dependencies:

```bash
cd frontend
npm install
```

2. Run frontend:

```bash
npm run dev
```

Frontend will run at `http://localhost:5173`.

### Pointing the frontend at a different API URL

Copy `frontend/.env.example` to `frontend/.env` and set `VITE_API_BASE_URL` (include the `/api` suffix), for example:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8001/api
```

Restart `npm run dev` after changing `.env`.

## API Endpoints

- `POST /api/train`
  - Body: `{ "ticker": "AAPL", "start_date": "2019-01-01" }`
  - Trains all regression and classification models, saves best models, returns metrics.

- `POST /api/predict`
  - Body: `{ "ticker": "AAPL" }`
  - Returns predicted price, trend, confidence, and model names.

- `GET /api/history/{ticker}`
  - Returns last 90 days OHLCV + computed indicators.

- `GET /api/tickers`
  - Returns popular tickers list.

## Sample Tickers

Use any valid Yahoo Finance ticker, for example:
- `AAPL`
- `TSLA`
- `GOOGL`
- `MSFT`
- `AMZN`
- `NFLX`
- `META`
- `NVDA`

## Notes

- Data is fetched from **yfinance** and cached in `backend/cache`.
- If prediction is called before training, API returns a clear error.
- Invalid tickers or missing market data are handled with readable API errors.
