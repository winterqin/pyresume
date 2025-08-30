import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";
import { authService } from '../services/authService';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const { toast } = useToast();

  const handlePasswordLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await authService.emailLogin(email, password);
      toast({
        title: "登录成功",
        description: "欢迎回来！",
      });
    } catch (error) {
      toast({
        title: "登录失败",
        description: error.response?.data?.message || "请检查您的邮箱和密码",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendVerificationCode = async () => {
    if (!email) {
      toast({
        title: "请输入邮箱",
        description: "需要邮箱才能发送验证码",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      await authService.sendVerificationEmail(email, 'login_with_token');
      toast({
        title: "验证码已发送",
        description: "请检查您的邮箱",
      });
      
      // 开始倒计时
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
    } catch (error) {
      toast({
        title: "发送失败",
        description: error.response?.data?.message || "请稍后重试",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleTokenLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await authService.loginWithToken(email, token);
      toast({
        title: "登录成功",
        description: "欢迎回来！",
      });
    } catch (error) {
      toast({
        title: "登录失败",
        description: error.response?.data?.message || "请检查您的验证码",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>登录</CardTitle>
        <CardDescription>选择您喜欢的登录方式</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="password" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="password">密码登录</TabsTrigger>
            <TabsTrigger value="token">验证码登录</TabsTrigger>
          </TabsList>
          
          <TabsContent value="password">
            <form onSubmit={handlePasswordLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">邮箱</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">密码</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "登录中..." : "登录"}
              </Button>
            </form>
          </TabsContent>
          
          <TabsContent value="token">
            <form onSubmit={handleTokenLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="token-email">邮箱</Label>
                <div className="flex gap-2">
                  <Input
                    id="token-email"
                    type="email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                  <Button 
                    type="button" 
                    variant="outline"
                    onClick={handleSendVerificationCode}
                    disabled={isLoading || countdown > 0}
                  >
                    {countdown > 0 ? `${countdown}s` : "发送验证码"}
                  </Button>
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="token">验证码</Label>
                <Input
                  id="token"
                  type="text"
                  placeholder="请输入验证码"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "登录中..." : "登录"}
              </Button>
            </form>
          </TabsContent>
        </Tabs>
      </CardContent>
      <CardFooter className="flex justify-center">
        <p className="text-sm text-gray-500">
          还没有账号？ <a href="/register" className="text-blue-500 hover:underline">立即注册</a>
        </p>
      </CardFooter>
    </Card>
  );
};

export default LoginForm;
