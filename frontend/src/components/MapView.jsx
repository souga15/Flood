/**
 * MapView - Displays a map of the selected city
 */
export default function MapView({ latitude, longitude, city }) {
    if (!latitude || !longitude) {
        return (
            <div className="map-view empty">
                <p>Select a city to view map</p>
            </div>
        );
    }

    // Calculate bounding box for map view (simple zoom level approximation)
    const delta = 0.05;
    const minLon = longitude - delta;
    const minLat = latitude - delta;
    const maxLon = longitude + delta;
    const maxLat = latitude + delta;

    // OpenStreetMap Embed URL
    const src = `https://www.openstreetmap.org/export/embed.html?bbox=${minLon},${minLat},${maxLon},${maxLat}&layer=mapnik&marker=${latitude},${longitude}`;

    return (
        <div className="map-view">
            <div className="map-header">
                <h3>📍 {city} Location</h3>
            </div>
            <div className="map-frame-container">
                <iframe
                    width="100%"
                    height="100%"
                    frameBorder="0"
                    scrolling="no"
                    marginHeight="0"
                    marginWidth="0"
                    src={src}
                    title={`${city} Map`}
                    style={{ border: 0 }}
                ></iframe>
            </div>
        </div>
    );
}
