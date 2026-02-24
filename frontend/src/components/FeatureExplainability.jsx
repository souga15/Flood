/**
 * FeatureExplainability - Shows top 5 features influencing the prediction
 */
export default function FeatureExplainability({ explanations }) {
    if (!explanations || explanations.length === 0) {
        return null;
    }

    return (
        <div className="explainability-panel">
            <div className="panel-header">
                <h3>What's Influencing This Prediction?</h3>
                <p className="panel-subtitle">Top factors considered by the AI model</p>
            </div>

            <div className="feature-list">
                {explanations.map((item, index) => (
                    <div key={index} className="feature-item">
                        <div className="feature-header">
                            <span className="feature-rank">#{index + 1}</span>
                            <span className="feature-name">{item.feature}</span>
                            <span className="feature-importance">{item.importance}%</span>
                        </div>
                        <div className="importance-bar-container">
                            <div
                                className="importance-bar"
                                style={{ width: `${item.importance}%` }}
                            />
                        </div>
                        <div className="feature-value">Value: {item.value}</div>
                    </div>
                ))}
            </div>

            <div className="explainability-footer">
                <small>Percentages show relative importance in the model's decision</small>
            </div>
        </div>
    );
}
