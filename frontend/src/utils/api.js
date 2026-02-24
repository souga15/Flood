/**
 * API client for backend communication
 */
import axios from 'axios';

// Use environment variable for production, fallback to localhost for dev
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30 seconds (Render free tier can be slow to wake)
});

/**
 * Fetch flood risk prediction for a city
 * @param {string} cityName - Name of the city
 * @returns {Promise} Response with weather and prediction data
 */
export const predictFloodRisk = async (cityName) => {
    try {
        const response = await api.post('/predict', {
            city: cityName
        });
        return response.data;
    } catch (error) {
        if (error.response) {
            throw new Error(error.response.data.error || 'Server error occurred');
        } else if (error.request) {
            throw new Error('Unable to connect to server. Please check if backend is running.');
        } else {
            throw new Error('Request failed: ' + error.message);
        }
    }
};

/**
 * Fetch list of available cities
 * @returns {Promise} Response with city list
 */
export const getCities = async () => {
    try {
        const response = await api.get('/cities');
        return response.data.cities;
    } catch (error) {
        console.error('Failed to fetch cities:', error);
        return ['Patna', 'Guwahati', 'Gorakhpur', 'Malda'];
    }
};

/**
 * Health check
 * @returns {Promise} Server health status
 */
export const checkHealth = async () => {
    try {
        const response = await api.get('/health');
        return response.data;
    } catch (error) {
        return { status: 'offline', model_loaded: false };
    }
};

export default api;
