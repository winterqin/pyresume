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
  COMPANIES: {
    LIST: '/api/companies/',
    CREATE: '/api/companies/create/',
    UPDATE: '/api/companies/{id}/update/',
    DELETE: '/api/companies/{id}/delete/',
    OPTIONS: '/api/companies/options/',
  },
  APPLICATIONS: {
    LIST: '/api/applications/',
    CREATE: '/api/applications/create/',
    UPDATE: '/api/applications/{id}/update/',
    DELETE: '/api/applications/{id}/delete/',
  },
};