import axios from 'axios';

const API_BASE_URL = 'http://localhost';

export const authService = {
  // 邮箱密码登录
  emailLogin: async (email, password) => {
    const response = await axios.post(`${API_BASE_URL}/login/`, {
      email,
      password
    });
    return response.data;
  },

  // 用户注册
  register: async (email, password, token) => {
    const response = await axios.post(`${API_BASE_URL}/register/`, {
      email,
      password,
      token
    });
    return response.data;
  },

  // 发送验证码
  sendVerificationEmail: async (email, tokenType) => {
    const response = await axios.post(`${API_BASE_URL}/send_verification_email/`, {
      email,
      token_type: tokenType
    });
    return response.data;
  },

  // 验证码登录
  loginWithToken: async (email, token) => {
    const response = await axios.post(`${API_BASE_URL}/login_with_token/`, {
      email,
      token
    });
    return response.data;
  }
};
