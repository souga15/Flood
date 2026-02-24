/**
 * Dashboard - Main container component
 */
import { useState, useEffect } from 'react';
import CitySelector from './CitySelector';
import WeatherDisplay from './WeatherDisplay';
import FloodRiskIndicator from './FloodRiskIndicator';
import MapView from './MapView';
import AlertNotification from './AlertNotification';
import FeatureExplainability from './FeatureExplainability';
import { predictFloodRisk, getCities, checkHealth } from '../utils/api';

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

    // Check server health on mount
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

            // Extract weather data
            setWeatherData({
                temperature: result.temperature,
                rainfall: result.rainfall,
                windspeed: result.windspeed,
                humidity: result.humidity
            });

            // Extract prediction data
            setPredictionData({
                prediction: result.prediction,
                riskLevel: result.risk_level,
                confidence: result.confidence
            });

            // Model info
            setModelInfo({
                version: result.model_version || 'unknown',
                featureCount: result.feature_count || null
            });

            // Extract feature explanations (if available)
            if (result.feature_explanations) {
                setFeatureExplanations(result.feature_explanations);
            }

            // Extract map coordinates
            if (result.latitude && result.longitude) {
                setMapLocation({
                    latitude: result.latitude,
                    longitude: result.longitude
                });
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
        if (selectedCity) {
            fetchPrediction(selectedCity);
        }
    };

    return (
        <div className="dashboard">
            <header className="dashboard-header clean">
                <h1>Flood Risk Dashboard</h1>
                <div className="server-status">
                    <span className={`status-dot ${serverStatus.status}`}></span>
                    <span className="status-text">
                        System Status: {serverStatus.status === 'healthy' ? 'Online' : 'Offline'}
                    </span>
                    {modelInfo.version && (
                        <span className="model-version-badge">
                            Model {modelInfo.version.toUpperCase()}
                            {modelInfo.featureCount ? ` (${modelInfo.featureCount} features)` : ''}
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

                {/* Alert Notification Banner */}
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
                    {/* Top Row: Weather & Risk */}
                    <div className="data-panel">
                        <WeatherDisplay weatherData={weatherData} />
                        <div className="spacer"></div>
                        <FloodRiskIndicator
                            prediction={predictionData?.prediction}
                            riskLevel={predictionData?.riskLevel}
                            confidence={predictionData?.confidence}
                        />
                        <div className="spacer"></div>
                        {/* Feature Explainability Panel */}
                        <FeatureExplainability explanations={featureExplanations} />
                    </div>

                    {/* Map Panel */}
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
                        <p>Data Source: Open-Meteo realtime API | Model: {modelInfo.version?.toUpperCase() || 'N/A'}</p>
                        <p>Last Update: {new Date().toLocaleTimeString()}</p>
                    </div>
                )}
            </div>
        </div>
    );
}
