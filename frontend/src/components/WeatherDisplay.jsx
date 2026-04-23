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

    const metrics = [
        { icon: '🌡️', label: 'Temperature', value: `${weatherData.temperature}°C` },
        { icon: '🌧️', label: 'Rainfall',    value: `${weatherData.rainfall} mm` },
        { icon: '💨', label: 'Wind Speed',  value: `${weatherData.windspeed} km/h` },
        { icon: '💧', label: 'Humidity',    value: weatherData.humidity != null ? `${weatherData.humidity}%` : '—' },
    ];

    return (
        <div className="weather-display">
            <h3>Current Conditions</h3>
            <div className="weather-metrics">
                {metrics.map(({ icon, label, value }) => (
                    <div key={label} className="metric-card">
                        <span className="metric-icon" aria-hidden="true">{icon}</span>
                        <div className="metric-info">
                            <span className="metric-label">{label}</span>
                            <span className="metric-value">{value}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
