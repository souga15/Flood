/**
 * FloodRiskIndicator - Enhanced with granular risk bands for Model V2
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

    // Calculate detailed risk band from probability
    const getRiskBand = (probability) => {
        if (probability < 20) return 'low';
        if (probability < 50) return 'moderate';
        if (probability < 75) return 'high';
        return 'severe';
    };

    const getRiskDescription = (band) => {
        const descriptions = {
            low: 'Status: Minimal flood risk. Conditions are currently stable.',
            moderate: 'Caution: Moderate flood risk. Monitor weather conditions.',
            high: 'Warning: High probability of flooding. Prepare for possible evacuation.',
            severe: 'Alert: Severe flood risk! Immediate action recommended.'
        };
        return descriptions[band] || descriptions.low;
    };

    const getRiskLabel = (band) => {
        const labels = {
            low: 'Low Risk',
            moderate: 'Moderate Risk',
            high: 'High Risk',
            severe: 'Severe Risk'
        };
        return labels[band] || labels.low;
    };

    const detailedRiskBand = getRiskBand(confidence);

    return (
        <div className={`flood-risk-indicator ${detailedRiskBand}`}>
            <div className="risk-header">
                <h2>Risk Assessment</h2>
            </div>

            <div className="risk-content">
                <div className="risk-text">
                    <h3 className="prediction-text">{prediction}</h3>
                    <div className="risk-badge">
                        <span className={`badge ${detailedRiskBand}`}>
                            {getRiskLabel(detailedRiskBand)}
                        </span>
                    </div>
                    <p className="risk-description">
                        {getRiskDescription(detailedRiskBand)}
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
                        <span className="low">0%</span>
                        <span className="moderate">20%</span>
                        <span className="high">50%</span>
                        <span className="severe">75%</span>
                        <span className="max">100%</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
