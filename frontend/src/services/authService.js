import { api } from '../config/api';
import { API_CONFIG } from '../config/constants';
import tokenService from './tokenService';

const authService = {
  login: async (email, password) => {
    console.log('开始登录请求...');
    const response = await api.post(API_CONFIG.AUTH.LOGIN, { email, password });
    console.log('登录响应:', response.data);
    
    // 修复：正确处理后端返回的tokens结构
    if (response.data.tokens && response.data.tokens.access && response.data.tokens.refresh) {
      console.log('保存tokens到localStorage...');
      tokenService.setTokens({
        access: response.data.tokens.access,
        refresh: response.data.tokens.refresh,
        user_email: response.data.user.email
      });
      console.log('Tokens已保存，accessToken:', tokenService.getAccessToken());
    }
    return response.data;
  },

  sendVerificationCode: async (email) => {
    const response = await api.post(API_CONFIG.AUTH.SEND_VERIFICATION_CODE, { 
      email, 
      code_type: 'register' 
    });
    return response.data;
  },

  // 新增：发送验证邮件（用于验证码登录）
  sendVerificationEmail: async (email, type = 'login') => {
    const response = await api.post(API_CONFIG.AUTH.SEND_VERIFICATION_CODE, { 
      email, 
      code_type: type 
    });
    return response.data;
  },

  // 新增：验证码登录
  loginWithToken: async (email, token) => {
    console.log('开始验证码登录请求...');
    const response = await api.post(API_CONFIG.AUTH.LOGIN_WITH_TOKEN, { 
      email, 
      token 
    });
    console.log('验证码登录响应:', response.data);
    
    // 处理后端返回的tokens结构
    if (response.data.tokens && response.data.tokens.access && response.data.tokens.refresh) {
      console.log('保存tokens到localStorage...');
      tokenService.setTokens({
        access: response.data.tokens.access,
        refresh: response.data.tokens.refresh
      });
      console.log('Tokens已保存，accessToken:', tokenService.getAccessToken());
    }
    return response.data;
  },

  register: async (email, password, verificationCode) => {
    console.log('开始注册请求...');
    const response = await api.post(API_CONFIG.AUTH.REGISTER, { 
      email, 
      password, 
      token: verificationCode 
    });
    console.log('注册响应:', response.data);
    
    // 注册成功后自动登录 - 修复tokens结构处理
    if (response.data.tokens && response.data.tokens.access && response.data.tokens.refresh) {
      console.log('保存tokens到localStorage...');
      tokenService.setTokens({
        access: response.data.tokens.access,
        refresh: response.data.tokens.refresh
      });
      console.log('Tokens已保存，accessToken:', tokenService.getAccessToken());
    }
    return response.data;
  },

  logout: () => {
    console.log('用户登出，清除tokens...');
    tokenService.clearTokens();
    // Redirect to login page after logout
    window.location.href = '/login';
  },
};

export default authService;
// 如需兼容命名导入： export { authService };
