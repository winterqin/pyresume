// 统一管理本地 token 的工具：不要依赖 api.js，避免循环依赖
import axios from 'axios';
import { API_CONFIG } from '../config/constants';

const ACCESS_KEY = 'accessToken';
const REFRESH_KEY = 'refreshToken';

// JWT解析工具函数
const parseJWT = (token) => {
  try {
    if (!token) return null;
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('JWT解析失败:', error);
    return null;
  }
};

const tokenService = {
  getAccessToken() {
    return localStorage.getItem(ACCESS_KEY);
  },
  getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
  },
  setTokens({ access, refresh,user_email }) {
    if (access) localStorage.setItem(ACCESS_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
    if (user_email) localStorage.setItem('user_email', user_email);
  },
  clearTokens() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem('user_email');
  },
  // 获取当前用户信息从JWT token
  getCurrentUser() {
    const token = this.getAccessToken();
    if (!token) return null;

    return {
      userId: parseJWT(token).user_id,
      email: localStorage.getItem('user_email'),
    };
  },
  // 检查token是否过期
  isTokenExpired() {
    const user = this.getCurrentUser();
    if (!user || !user.exp) return true;
    
    const currentTime = Date.now() / 1000;
    return user.exp < currentTime;
  },
  // 单独提供刷新接口（用裸 axios，避免引用 api 实例）
  async refreshToken() {
    const refresh = localStorage.getItem(REFRESH_KEY);
    if (!refresh) throw new Error('No refresh token');
    const { data } = await axios.post(
      `${API_CONFIG.BASE_URL}${API_CONFIG.AUTH.REFRESH_TOKEN}`,
      { refresh },
      { headers: { 'Content-Type': 'application/json' } }
    );
    const newAccess = data?.access;
    if (!newAccess) throw new Error('No access in refresh response');
    localStorage.setItem(ACCESS_KEY, newAccess);
    return newAccess;
  },
};

export default tokenService;
