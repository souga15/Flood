/**
 * AlertNotification - 4-tier alert banner for Model V4
 * Thresholds match backend classify_risk(): 20 / 40 / 65
 */
import { useState, useEffect } from 'react';

export default function AlertNotification({ confidence, riskLevel, prediction }) {
    const [dismissed, setDismissed] = useState(false);

    // Reset dismissed when prediction refreshes
    useEffect(() => {
        setDismissed(false);
    }, [confidence, prediction]);

    const getAlertConfig = (prob, level) => {
        // Use backend risk_level if provided, else derive from probability
        const tier = level || (() => {
            if (prob >= 65) return 'very_high';
            if (prob >= 40) return 'high';
            if (prob >= 20) return 'moderate';
            return null;
        })();

        const configs = {
            very_high: {
                level: 'very_high',
                label: 'CRITICAL ALERT',
                message: 'Immediate precautionary action required. Seek higher ground and follow emergency instructions from local authorities.',
            },
            high: {
                level: 'high',
                label: 'HIGH WARNING',
                message: 'Prepare for possible evacuation. Move valuables to higher floors and monitor official alerts closely.',
            },
            moderate: {
                level: 'moderate',
                label: 'ADVISORY',
                message: 'Monitor weather conditions. Stay informed about flood warnings in your area and prepare an emergency kit.',
            },
        };

        return configs[tier] || null;
    };

    const alertConfig = getAlertConfig(confidence, riskLevel);

    if (dismissed || !alertConfig || !confidence) {
        return null;
    }

    return (
        <div className={`alert-notification alert-${alertConfig.level}`}>
            <div className="alert-content">
                <div className="alert-header">
                    <span className="alert-badge">{alertConfig.label}</span>
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
                    <p>{alertConfig.message}</p>
                </div>
            </div>
        </div>
    );
}
