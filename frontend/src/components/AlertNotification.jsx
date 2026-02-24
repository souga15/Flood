/**
 * AlertNotification - Color-coded alert banner for flood risk warnings
 */
import { useState, useEffect } from 'react';

export default function AlertNotification({ confidence, riskLevel, prediction }) {
    const [dismissed, setDismissed] = useState(false);

    // Reset dismissed state when prediction changes
    useEffect(() => {
        setDismissed(false);
    }, [confidence, prediction]);

    // Determine alert level based on probability
    const getAlertLevel = (prob) => {
        if (prob >= 75) return { level: 'severe', label: 'SEVERE ALERT', color: '#991b1b' };
        if (prob >= 50) return { level: 'high', label: 'HIGH WARNING', color: '#dc2626' };
        if (prob >= 20) return { level: 'moderate', label: 'ADVISORY', color: '#d97706' };
        return null; // No alert for < 20%
    };

    const getPrecautionMessage = (level) => {
        const messages = {
            severe: '🚨 Immediate evacuation recommended. Seek higher ground immediately. Follow official emergency instructions.',
            high: '⚠️ Prepare for possible evacuation. Move valuables to higher floors. Monitor official alerts closely.',
            moderate: '⚡ Monitor weather conditions. Stay informed about flood warnings. Prepare emergency supplies.'
        };
        return messages[level] || '';
    };

    const alertInfo = getAlertLevel(confidence);

    // Don't show if dismissed or no alert needed
    if (dismissed || !alertInfo || !confidence) {
        return null;
    }

    return (
        <div className={`alert-notification alert-${alertInfo.level}`}>
            <div className="alert-content">
                <div className="alert-header">
                    <span className="alert-badge">{alertInfo.label}</span>
                    <span className="alert-probability">Flood Probability: {confidence}%</span>
                    <button
                        className="alert-dismiss"
                        onClick={() => setDismissed(true)}
                        aria-label="Dismiss alert"
                    >
                        ✕
                    </button>
                </div>
                <div className="alert-message">
                    <strong>{prediction}</strong>
                    <p>{getPrecautionMessage(alertInfo.level)}</p>
                </div>
            </div>
        </div>
    );
}
