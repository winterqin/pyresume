import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

const Index = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>欢迎使用我们的服务</CardTitle>
          <CardDescription>请选择以下操作</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button asChild className="w-full">
            <a href="/login">登录</a>
          </Button>
          <Button asChild variant="outline" className="w-full">
            <a href="/register">注册</a>
          </Button>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-gray-500">
            体验我们的服务
          </p>
        </CardFooter>
      </Card>
    </div>
  );
};

export default Index;
