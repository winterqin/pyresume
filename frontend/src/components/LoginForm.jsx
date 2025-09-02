import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authService from '../services/authService';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const LoginForm = () => {
  const [tab, setTab] = useState('password');

  // 密码登录
  const [emailPwd, setEmailPwd] = useState('');
  const [password, setPassword] = useState('');
  const [pwdErr, setPwdErr] = useState('');
  const [pwdLoading, setPwdLoading] = useState(false);

  // 验证码登录
  const [emailTok, setEmailTok] = useState('');
  const [token, setToken] = useState('');
  const [tokErr, setTokErr] = useState('');
  const [tokLoading, setTokLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const timerRef = useRef(null);

  const navigate = useNavigate();

  useEffect(() => {
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, []);

  // 密码登录
  const handlePasswordLogin = async (e) => {
    e.preventDefault();
    setPwdErr('');
    setPwdLoading(true);
    try {
      await authService.login(emailPwd, password);
      navigate('/');
    } catch (err) {
      setPwdErr(err?.response?.data?.message || '登录失败，请检查邮箱和密码。');
    } finally {
      setPwdLoading(false);
    }
  };

  // 发送验证码（用于免密登录）
  const handleSendLoginCode = async () => {
    if (!emailTok) {
      setTokErr('请输入邮箱再发送验证码');
      return;
    }
    setTokErr('');
    setTokLoading(true);
    try {
      // 后端根据 type 做场景区分（你已有 login_with_token）
      await authService.sendVerificationEmail(emailTok, 'login_with_token');
      // 开启 60s 倒计时
      setCountdown(60);
      timerRef.current = setInterval(() => {
        setCountdown((n) => {
          if (n <= 1) { clearInterval(timerRef.current); return 0; }
          return n - 1;
        });
      }, 1000);
    } catch (err) {
      setTokErr(err?.response?.data?.message || '验证码发送失败，请稍后再试。');
    } finally {
      setTokLoading(false);
    }
  };

  // 验证码登录
  const handleTokenLogin = async (e) => {
    e.preventDefault();
    setTokErr('');
    setTokLoading(true);
    try {
      await authService.loginWithToken(emailTok, token);
      navigate('/');
    } catch (err) {
      setTokErr(err?.response?.data?.message || '验证码错误或已过期。');
    } finally {
      setTokLoading(false);
    }
  };

  return (
    <Card className="mx-auto w-[380px]">
      <CardHeader>
        <CardTitle className="text-2xl">登录</CardTitle>
        <CardDescription>选择一种你喜欢的方式登录</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={tab} onValueChange={setTab} className="w-full">
          <TabsList className="grid grid-cols-2 w-full">
            <TabsTrigger value="password">密码登录</TabsTrigger>
            <TabsTrigger value="token">验证码登录</TabsTrigger>
          </TabsList>

          <TabsContent value="password">
            <form onSubmit={handlePasswordLogin} className="grid gap-4">
              <div className="grid gap-2">
                <Label htmlFor="login-email">邮箱</Label>
                <Input
                  id="login-email"
                  type="email"
                  placeholder="m@example.com"
                  required
                  value={emailPwd}
                  onChange={(e) => setEmailPwd(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="login-password">密码</Label>
                <Input
                  id="login-password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              {pwdErr && <p className="text-red-500 text-sm">{pwdErr}</p>}
              <Button type="submit" className="w-full" disabled={pwdLoading}>
                {pwdLoading ? '登录中…' : '登录'}
              </Button>
            </form>
          </TabsContent>

          <TabsContent value="token">
            <form onSubmit={handleTokenLogin} className="grid gap-4">
              <div className="grid gap-2">
                <Label htmlFor="token-email">邮箱</Label>
                <div className="flex gap-2">
                  <Input
                    id="token-email"
                    type="email"
                    placeholder="m@example.com"
                    required
                    value={emailTok}
                    onChange={(e) => setEmailTok(e.target.value)}
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleSendLoginCode}
                    disabled={tokLoading || countdown > 0}
                  >
                    {countdown > 0 ? `${countdown}s` : '发送验证码'}
                  </Button>
                </div>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="token-code">验证码</Label>
                <Input
                  id="token-code"
                  placeholder="请输入验证码"
                  required
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                />
              </div>
              {tokErr && <p className="text-red-500 text-sm">{tokErr}</p>}
              <Button type="submit" className="w-full" disabled={tokLoading}>
                {tokLoading ? '登录中…' : '登录'}
              </Button>
            </form>
          </TabsContent>
        </Tabs>
      </CardContent>
      <CardFooter className="justify-center">
        <p className="text-sm text-muted-foreground">
          还没有账号？ <Link to="/register" className="text-blue-500 hover:underline">去注册</Link>
        </p>
      </CardFooter>
    </Card>
  );
};

export default LoginForm;
