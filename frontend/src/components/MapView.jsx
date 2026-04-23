/**
 * MapView - Embeds an OpenStreetMap iframe centred on the selected city
 */
export default function MapView({ latitude, longitude, city }) {
    if (!latitude || !longitude) {
        return (
            <div className="map-view empty">
                <p>Select a city to view the map</p>
            </div>
        );
    }

    const delta = 0.4;
    const bbox = [
        longitude - delta,
        latitude  - delta,
        longitude + delta,
        latitude  + delta,
    ].join(',');

    const mapUrl =
        `https://www.openstreetmap.org/export/embed.html` +
        `?bbox=${bbox}&layer=mapnik&marker=${latitude},${longitude}`;

    return (
        <div className="map-view">
            <div className="map-header">
                <h3>📍 {city}</h3>
            </div>
            <div className="map-frame-container">
                <iframe
                    width="100%"
                    height="100%"
                    style={{ minHeight: '350px', border: 'none', display: 'block' }}
                    src={mapUrl}
                    title={`Map of ${city}`}
                    loading="lazy"
                    referrerPolicy="no-referrer"
                />
            </div>
        </div>
    );
}
