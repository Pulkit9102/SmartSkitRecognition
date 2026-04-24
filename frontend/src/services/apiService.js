import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const apiService = {
  /**
   * Health check to verify backend is running
   */
  async healthCheck() {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  /**
   * Predict skin disease from image
   * @param {File} imageFile - The image file to analyze
   * @param {boolean} useSerpApi - Whether to use SerpAPI for recommendations
   */
  async predictDisease(imageFile, useSerpApi = true) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      formData.append('use_serpapi', useSerpApi.toString());

      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  /**
   * Get list of available disease classes
   */
  async getClasses() {
    try {
      const response = await axios.get(`${API_BASE_URL}/classes`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  /**
   * Search for recommendations for a specific disease
   * @param {string} diseaseName - Name of the disease
   */
  async searchRecommendations(diseaseName) {
    try {
      const response = await axios.post(`${API_BASE_URL}/search-recommendations`, {
        disease: diseaseName,
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  /**
   * Send a chat message to the skincare chatbot.
   * @param {string} message
   * @param {Array<{role: 'user'|'assistant', content: string}>} history
   * @returns {Promise<{reply: string}>}
   */
  async chat(message, history = []) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/chat`,
        { message, history },
        { headers: { 'Content-Type': 'application/json' }, timeout: 35000 }
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  },

  /**
   * Handle API errors
   * @param {Error} error - The error object
   */
 handleError(error) {
  if (error.response && error.response.data) {
    // 🔥 Return FULL backend response
    return {
      error: error.response.data.error || "Error",
      message: error.response.data.message || "Something went wrong"
    };
  } else if (error.request) {
    return {
      error: "Network Error",
      message: "Cannot connect to server. Please ensure the backend is running."
    };
  } else {
    return {
      error: "Error",
      message: error.message || "An unexpected error occurred"
    };
  }
}
};

export default apiService;
