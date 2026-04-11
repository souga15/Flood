/**
 * FloodRiskIndicator - 4-tier risk display for Model V4
 * Tiers: low (<20%) | moderate (20-40%) | high (40-65%) | very_high (≥65%)
 */
export default function FloodRiskIndicator({ prediction, riskLevel, confidence }) {
    if (!prediction) {
        return (
            <div className="flood-risk-indicator empty">
                <div className="risk-placeholder">
                    <p>Prediction Pending...</p>
                </div>
            </div>
        );
    }

    // Derive tier from confidence, matching the V4 backend thresholds
    const getTier = (prob) => {
        if (prob < 20) return 'low';
        if (prob < 40) return 'moderate';
        if (prob < 65) return 'high';
        return 'very_high';
    };

    const tierConfig = {
        low: {
            label: 'Low Risk',
            description: 'Status: Minimal flood risk. Conditions are currently stable.',
        },
        moderate: {
            label: 'Moderate Risk',
            description: 'Caution: Moderate flood risk detected. Monitor weather conditions closely.',
        },
        high: {
            label: 'High Risk',
            description: 'Warning: High probability of flooding. Prepare for possible evacuation.',
        },
        very_high: {
            label: 'Very High Risk',
            description: 'Alert: Very high flood risk! Take immediate precautionary action.',
        },
    };

    // Use backend's risk_level if available, otherwise derive from confidence
    const tier = riskLevel || getTier(confidence);
    const config = tierConfig[tier] || tierConfig.low;

    // Scale bar tick positions matching new thresholds (0, 20, 40, 65, 100)
    const tickLabels = ['0%', '20%', '40%', '65%', '100%'];

    return (
        <div className={`flood-risk-indicator ${tier}`}>
            <div className="risk-header">
                <h2>Risk Assessment</h2>
            </div>

            <div className="risk-content">
                <div className="risk-text">
                    <h3 className="prediction-text">
                        {prediction}
                    </h3>
                    <div className="risk-badge">
                        <span className={`badge ${tier}`}>
                            {config.label}
                        </span>
                    </div>
                    <p className="risk-description">
                        {config.description}
                    </p>
                </div>
            </div>

            <div className="risk-footer">
                <div className="confidence-meter">
                    <span className="confidence-label">Flood Probability:</span>
                    <span className="confidence-value">{confidence}%</span>
                </div>
                <div className="risk-scale">
                    <div className="scale-bar">
                        <div
                            className="scale-fill"
                            style={{ width: `${Math.min(confidence, 100)}%` }}
                        />
                    </div>
                    <div className="scale-labels">
                        {tickLabels.map((t) => (
                            <span key={t}>{t}</span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
