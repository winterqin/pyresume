import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Mail, Clock } from 'lucide-react';
import authService from '../services/authService';

function RegisterForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [codeSent, setCodeSent] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const navigate = useNavigate();

  // 发送验证码
  const handleSendCode = async () => {
    if (!email) {
      setError('请输入邮箱地址');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await authService.sendVerificationCode(email);
      setCodeSent(true);
      setSuccess('验证码已发送到您的邮箱');
      
      // 开始60秒倒计时
      setCountdown(60);
      const timer = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      
    } catch (err) {
      setError(err.response?.data?.message || '发送验证码失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 注册
  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!email || !password || !verificationCode) {
      setError('请填写所有必填字段');
      return;
    }
    
    setLoading(true);
    
    try {
      await authService.register(email, password, verificationCode);
      setSuccess('注册成功！正在跳转...');
      setTimeout(() => {
        navigate('/'); // 注册成功后跳转到首页
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.message || '注册失败，请检查验证码是否正确');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <Card className="mx-auto max-w-sm">
        <CardHeader>
          <CardTitle className="text-2xl">注册账户</CardTitle>
          <CardDescription>
            输入您的邮箱和密码来创建账户
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRegister}>
            <div className="grid gap-4">
              <div className="grid gap-2">
                <Label htmlFor="email">邮箱地址</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your@email.com"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                />
              </div>
              
              <div className="grid gap-2">
                <Label htmlFor="password">密码</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="请输入密码"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                />
              </div>
              
              <div className="grid gap-2">
                <Label htmlFor="verificationCode">邮箱验证码</Label>
                <div className="flex gap-2">
                  <Input
                    id="verificationCode"
                    type="text"
                    placeholder="请输入验证码"
                    required
                    value={verificationCode}
                    onChange={(e) => setVerificationCode(e.target.value)}
                    disabled={loading}
                    className="flex-1"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleSendCode}
                    disabled={loading || countdown > 0}
                    className="whitespace-nowrap"
                  >
                    {loading ? (
                      <Clock className="h-4 w-4 animate-spin" />
                    ) : countdown > 0 ? (
                      `${countdown}s`
                    ) : (
                      <>
                        <Mail className="h-4 w-4 mr-1" />
                        {codeSent ? '重新发送' : '发送验证码'}
                      </>
                    )}
                  </Button>
                </div>
              </div>
              
              {error && <p className="text-red-500 text-sm">{error}</p>}
              {success && <p className="text-green-500 text-sm">{success}</p>}
              
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? '注册中...' : '创建账户'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

export default RegisterForm;
