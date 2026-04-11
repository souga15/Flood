/**
 * Dashboard - Main container with Model V4 metrics panel
 */
import { useState, useEffect } from 'react';
import CitySelector from './CitySelector';
import WeatherDisplay from './WeatherDisplay';
import FloodRiskIndicator from './FloodRiskIndicator';
import MapView from './MapView';
import AlertNotification from './AlertNotification';
import FeatureExplainability from './FeatureExplainability';
import { predictFloodRisk, getCities, checkHealth } from '../utils/api';

/* ── Model Metrics Card ─────────────────────────────────────────────── */
function ModelMetricsPanel({ metrics, version }) {
    const [open, setOpen] = useState(false);
    if (!metrics) return null;

    const rows = [
        { label: 'Test AUC',       value: metrics.auc?.toFixed(4),       good: true  },
        { label: 'Test AP',        value: metrics.ap?.toFixed(4),        good: true  },
        { label: 'Test F1',        value: metrics.f1?.toFixed(4),        good: true  },
        { label: 'Test MCC',       value: metrics.mcc?.toFixed(4),       good: true  },
        { label: 'Recall',         value: `${(metrics.recall * 100).toFixed(1)}%`,   good: true },
        { label: 'Precision',      value: `${(metrics.precision * 100).toFixed(1)}%`, good: true },
        { label: 'Train AUC',      value: metrics.train_auc?.toFixed(4), good: null },
        { label: 'Val AUC',        value: metrics.val_auc?.toFixed(4),   good: null },
    ];

    return (
        <div className="metrics-panel">
            <button
                className="metrics-toggle"
                onClick={() => setOpen((o) => !o)}
                aria-expanded={open}
            >
                <span>Model {version?.toUpperCase()} Performance</span>
                <span className="metrics-chevron">{open ? '▲' : '▼'}</span>
            </button>

            {open && (
                <div className="metrics-body">
                    <p className="metrics-subtitle">
                        XGBoost classifier trained on 2017–2022 all-India flood data. Evaluated on
                        held-out 2023–2024 data from 34 stations.
                    </p>
                    <div className="metrics-grid">
                        {rows.map(({ label, value }) => (
                            <div key={label} className="metric-chip">
                                <span className="chip-label">{label}</span>
                                <span className="chip-value">{value ?? '—'}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

/* ── Dashboard ──────────────────────────────────────────────────────── */
export default function Dashboard() {
    const [cities, setCities] = useState(['Patna', 'Guwahati', 'Gorakhpur', 'Malda']);
    const [selectedCity, setSelectedCity] = useState('');
    const [weatherData, setWeatherData] = useState(null);
    const [predictionData, setPredictionData] = useState(null);
    const [featureExplanations, setFeatureExplanations] = useState(null);
    const [mapLocation, setMapLocation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [serverStatus, setServerStatus] = useState({ status: 'checking', model_loaded: false });
    const [modelInfo, setModelInfo] = useState({ version: null, featureCount: null });
    const [modelMetrics, setModelMetrics] = useState(null);

    useEffect(() => {
        checkServerHealth();
        fetchCities();
    }, []);

    const checkServerHealth = async () => {
        const health = await checkHealth();
        setServerStatus(health);
    };

    const fetchCities = async () => {
        const cityList = await getCities();
        setCities(cityList);
    };

    const handleCityChange = async (city) => {
        setSelectedCity(city);
        setError(null);
        if (!city) {
            setWeatherData(null);
            setPredictionData(null);
            setMapLocation(null);
            return;
        }
        await fetchPrediction(city);
    };

    const fetchPrediction = async (city) => {
        setLoading(true);
        setError(null);

        try {
            const result = await predictFloodRisk(city);

            setWeatherData({
                temperature: result.temperature,
                rainfall: result.rainfall,
                windspeed: result.windspeed,
                humidity: result.humidity,
            });

            setPredictionData({
                prediction: result.prediction,
                riskLevel: result.risk_level,
                riskTier: result.risk_tier,
                confidence: result.confidence,
            });

            setModelInfo({
                version: result.model_version || 'unknown',
                featureCount: result.feature_count || null,
            });

            if (result.feature_explanations) {
                setFeatureExplanations(result.feature_explanations);
            }

            // Store model metrics (V4 only)
            if (result.model_metrics) {
                setModelMetrics(result.model_metrics);
            }

            if (result.latitude && result.longitude) {
                setMapLocation({ latitude: result.latitude, longitude: result.longitude });
            }
        } catch (err) {
            setError(err.message);
            setWeatherData(null);
            setPredictionData(null);
        } finally {
            setLoading(false);
        }
    };

    const handleRefresh = () => {
        if (selectedCity) fetchPrediction(selectedCity);
    };

    return (
        <div className="dashboard">
            <header className="dashboard-header clean">
                <h1>Flood Risk Dashboard</h1>
                <div className="server-status">
                    <span className={`status-dot ${serverStatus.status}`}></span>
                    <span className="status-text">
                        System: {serverStatus.status === 'healthy' ? 'Online' : 'Offline'}
                    </span>
                    {modelInfo.version && (
                        <span className="model-version-badge">
                            Model {modelInfo.version.toUpperCase()}
                            {modelInfo.featureCount ? ` · ${modelInfo.featureCount} features` : ''}
                        </span>
                    )}
                </div>
            </header>

            <div className="dashboard-content">
                <div className="controls-section">
                    <CitySelector
                        selectedCity={selectedCity}
                        onCityChange={handleCityChange}
                        cities={cities}
                        disabled={loading}
                    />
                    <button
                        onClick={handleRefresh}
                        disabled={!selectedCity || loading}
                        className="refresh-button clean"
                    >
                        {loading ? 'Updating...' : 'Refresh Data'}
                    </button>
                </div>

                {/* Model Performance Panel */}
                <ModelMetricsPanel metrics={modelMetrics} version={modelInfo.version} />

                {/* Alert Banner */}
                <AlertNotification
                    confidence={predictionData?.confidence}
                    riskLevel={predictionData?.riskLevel}
                    prediction={predictionData?.prediction}
                />

                {error && (
                    <div className="error-message">
                        <span>Error: {error}</span>
                    </div>
                )}

                <div className="dashboard-grid">
                    {/* Left Column: Weather + Risk + Explainability */}
                    <div className="data-panel">
                        <WeatherDisplay weatherData={weatherData} />
                        <div className="spacer" />
                        <FloodRiskIndicator
                            prediction={predictionData?.prediction}
                            riskLevel={predictionData?.riskLevel}
                            confidence={predictionData?.confidence}
                        />
                        <div className="spacer" />
                        <FeatureExplainability explanations={featureExplanations} />
                    </div>

                    {/* Right Column: Map */}
                    <div className="map-panel">
                        <MapView
                            latitude={mapLocation?.latitude}
                            longitude={mapLocation?.longitude}
                            city={selectedCity}
                        />
                    </div>
                </div>

                {selectedCity && weatherData && (
                    <div className="info-footer">
                        <p>
                            Data: Open-Meteo API &nbsp;|&nbsp; Model:{' '}
                            {modelInfo.version?.toUpperCase() || 'N/A'} (XGBoost, 52 features)
                        </p>
                        <p>Last Update: {new Date().toLocaleTimeString()}</p>
                    </div>
                )}
            </div>
        </div>
    );
}
