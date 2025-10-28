import axios from "axios";

const hostname = window.location.hostname;

let API_BASE_URL;

// Check if running locally
if (hostname === "localhost" || hostname === "127.0.0.1") {
  API_BASE_URL = "http://127.0.0.1:8000/api";
} else {
  // Use LAN IP for phones or other PCs on same Wi-Fi
  API_BASE_URL = "http://192.168.43.52:8000/api";
}

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");

      if (refreshToken) {
        try {
          const response = await axios.post(
            `${API_BASE_URL}/auth/token/refresh/`,
            {
              refresh: refreshToken,
            }
          );
          const { access } = response.data;
          localStorage.setItem("access_token", access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (username, password) =>
    api.post("/auth/token/", { username, password }),
  register: (data) => api.post("/auth/register/", data),
  getProfile: () => api.get("/auth/profile/"),
  verifyPhone: (data) => api.post("/auth/verify-phone/", data),
  requestPasswordReset: (data) =>
    api.post("/auth/password-reset/request/", data),
  resetPassword: (data) => api.post("/auth/password-reset/confirm/", data),
};

export const coreAPI = {
  // Past Papers
  getPapers: (params = {}) => api.get("/core/papers/", { params }),
  getPaper: (id) => api.get(`/core/papers/${id}/`),
  downloadPaper: (id) => api.post(`/core/papers/${id}/download/`),
  getPaperAccessToken: (paperId) =>
    api.get(`/core/papers/${paperId}/access-token/`),

  getPaperPDFData: (paperId) => api.get(`/core/papers/${paperId}/pdf-data/`),

  // Subjects & Categories
  getSubjects: () => api.get("/core/subjects/"),
  getCategories: () => api.get("/core/categories/"),

  // Subscriptions
  getSubscriptionPlans: () => api.get("/core/subscriptions/plans/"),
  getUserSubscription: () => api.get("/core/subscriptions/my/"),
  createSubscription: (planId) =>
    api.post("/core/subscriptions/create/", { plan_id: planId }),

  // Quizzes
  getQuizzes: (params = {}) => api.get("/core/quizzes/", { params }),
  getQuiz: (id) => api.get(`/core/quizzes/${id}/`),
  startQuiz: (quizId) => api.post(`/core/quizzes/${quizId}/start/`),
  submitQuiz: (attemptId, answers) =>
    api.post(`/core/attempts/${attemptId}/submit/`, { answers }),

  // User Activity
  getUserActivity: () => api.get("/core/activity/"),
};

export const adminAPI = {
  // Dashboard
  getAdminDashboardStats: () => api.get("/core/admin/dashboard/stats/"),

  // Users
  getAdminUsers: (params = {}) => api.get("/core/admin/users/", { params }),
  getAdminUser: (id) => api.get(`/core/admin/users/${id}/`),
  updateAdminUser: (id, data) => api.put(`/core/admin/users/${id}/`, data),
  deleteAdminUser: (id) => api.delete(`/core/admin/users/${id}/`),

  // Papers
  getAdminPapers: (params = {}) => api.get("/core/admin/papers/", { params }),
  getAdminPaper: (id) => api.get(`/core/admin/papers/${id}/`),
  createAdminPaper: (data) => api.post("/core/admin/papers/", data),
  updateAdminPaper: (id, data) => api.put(`/core/admin/papers/${id}/`, data),
  deleteAdminPaper: (id) => api.delete(`/core/admin/papers/${id}/`),
  bulkApprovePapers: (paperIds) =>
    api.post("/core/admin/papers/bulk-approve/", { paper_ids: paperIds }),

  // Quizzes
  getAdminQuizzes: () => api.get("/core/admin/quizzes/"),
  getAdminQuiz: (id) => api.get(`/core/admin/quizzes/${id}/`),
  createAdminQuiz: (data) => api.post("/core/admin/quizzes/", data),
  updateAdminQuiz: (id, data) => api.put(`/core/admin/quizzes/${id}/`, data),
  deleteAdminQuiz: (id) => api.delete(`/core/admin/quizzes/${id}/`),

  // Subscriptions
  getAdminSubscriptions: (params = {}) =>
    api.get("/core/admin/subscriptions/", { params }),

  // Settings
  getSystemSettings: () => api.get("/core/admin/settings/"),
  updateSystemSetting: (id, data) =>
    api.put(`/core/admin/settings/${id}/`, data),

  // Logs
  getAdminLogs: () => api.get("/core/admin/logs/"),
};

export const exposedAPI = {
  getExposedDashboard: () => api.get("/exposed/dashboard/"),
  getChildren: (params = {}) => api.get("/exposed/children/", { params }),
  getChild: (id) => api.get(`/exposed/children/${id}`),
  updateChild: (id) => api.put(`/exposed/children/${id}`),
  createChild: (data) => api.post(`/exposed/children/`, data),
};

export default api;
