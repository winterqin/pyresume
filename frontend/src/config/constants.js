export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  AUTH: {
    LOGIN: '/api/auth/login/',
    REGISTER: '/api/auth/register/',
    SEND_VERIFICATION_CODE: '/api/auth/send_verification_email/',
    LOGIN_WITH_TOKEN: '/api/auth/login_with_token/',
    REFRESH_TOKEN: '/api/auth/token/refresh/',
    VERIFY_TOKEN: '/api/auth/token/verify/',
    SELF_INFO: '/api/auth/selfinfo/',
  },
  DASHBOARD: {
    STATS: '/api/dashboard/stats/',
  },
  COMPANY: {
    LIST: '/api/companies/',
    CREATE: '/api/companies/create/',
    UPDATE: (id) => `/api/companies/${id}/update/`,
    DELETE: (id) => `/api/companies/${id}/delete/`,
    OPTIONS: '/api/companies/options/',
  },
  APPLICATION: {
    LIST: '/api/applications/',
    CREATE: '/api/applications/create/',
    UPDATE: (id) => `/api/applications/${id}/update/`,
    DELETE: (id) => `/api/applications/${id}/delete/`,
  },
};