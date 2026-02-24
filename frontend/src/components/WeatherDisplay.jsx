/**
 * WeatherDisplay - Show current weather metrics including humidity
 */
export default function WeatherDisplay({ weatherData }) {
    if (!weatherData) {
        return (
            <div className="weather-display empty">
                <p className="empty-message">Select a city to view weather data</p>
            </div>
        );
    }

    return (
        <div className="weather-display">
            <h3>Current Conditions</h3>
            <div className="weather-metrics">
                <div className="metric-card">
                    <div className="metric-info">
                        <span className="metric-label">Temperature</span>
                        <span className="metric-value">{weatherData.temperature}°C</span>
                    </div>
                </div>

                <div className="metric-card">
                    <div className="metric-info">
                        <span className="metric-label">Rainfall</span>
                        <span className="metric-value">{weatherData.rainfall} mm</span>
                    </div>
                </div>

                <div className="metric-card">
                    <div className="metric-info">
                        <span className="metric-label">Wind Speed</span>
                        <span className="metric-value">{weatherData.windspeed} km/h</span>
                    </div>
                </div>

                <div className="metric-card">
                    <div className="metric-info">
                        <span className="metric-label">Humidity</span>
                        <span className="metric-value">{weatherData.humidity ?? '—'}%</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
