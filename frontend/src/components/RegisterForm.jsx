import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { authService } from '../services/authService';

const RegisterForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [token, setToken] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const { toast } = useToast();

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
      await authService.sendVerificationEmail(email, 'register');
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

  const handleRegister = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      toast({
        title: "密码不匹配",
        description: "请确保两次输入的密码相同",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      await authService.register(email, password, token);
      toast({
        title: "注册成功",
        description: "欢迎加入我们！",
      });
    } catch (error) {
      toast({
        title: "注册失败",
        description: error.response?.data?.message || "请检查您的信息",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>注册</CardTitle>
        <CardDescription>创建您的新账号</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleRegister} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="register-email">邮箱</Label>
            <div className="flex gap-2">
              <Input
                id="register-email"
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
            <Label htmlFor="register-token">验证码</Label>
            <Input
              id="register-token"
              type="text"
              placeholder="请输入验证码"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="register-password">密码</Label>
            <Input
              id="register-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirm-password">确认密码</Label>
            <Input
              id="confirm-password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "注册中..." : "注册"}
          </Button>
        </form>
      </CardContent>
      <CardFooter className="flex justify-center">
        <p className="text-sm text-gray-500">
          已有账号？ <a href="/login" className="text-blue-500 hover:underline">立即登录</a>
        </p>
      </CardFooter>
    </Card>
  );
};

export default RegisterForm;
