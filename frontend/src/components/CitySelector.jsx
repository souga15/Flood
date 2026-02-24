/**
 * CitySelector - Dropdown to select city
 */
export default function CitySelector({ selectedCity, onCityChange, cities, disabled }) {
    return (
        <div className="city-selector">
            <label htmlFor="city-select">Select City</label>
            <select
                id="city-select"
                value={selectedCity}
                onChange={(e) => onCityChange(e.target.value)}
                disabled={disabled}
                className="city-dropdown"
            >
                <option value="">-- Choose a city --</option>
                {cities.map((city) => (
                    <option key={city} value={city}>
                        {city}
                    </option>
                ))}
            </select>
        </div>
    );
}
