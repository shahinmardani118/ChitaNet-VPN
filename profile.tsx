import { useGetMe, getGetMeQueryKey, useGetUserProfile, getGetUserProfileQueryKey } from "@workspace/api-client-react";
import { useLocation } from "wouter";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { UserCircle, Wallet, ShoppingCart, CheckCircle2, Clock } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export function Profile() {
  const [, setLocation] = useLocation();
  const { data: me, isLoading: meLoading } = useGetMe({ query: { queryKey: getGetMeQueryKey() } });
  const { data: profile, isLoading: profileLoading } = useGetUserProfile({ 
    query: { 
      queryKey: getGetUserProfileQueryKey(),
      enabled: !!me 
    } 
  });

  if (!meLoading && !me) {
    setLocation("/login");
    return null;
  }

  if (profileLoading || !profile) {
    return (
      <div className="space-y-6">
        <div className="h-32 bg-card animate-pulse rounded-xl border border-border"></div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1,2,3,4].map(i => <div key={i} className="h-24 bg-card animate-pulse rounded-xl border border-border"></div>)}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">داشبورد کاربری</h1>
        <p className="text-muted-foreground mt-2">خلاصه حساب و سفارش‌های شما</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-1 border-primary/20 bg-card/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <UserCircle className="w-5 h-5 text-primary" />
              اطلاعات حساب
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-muted-foreground">نام</span>
              <span className="font-medium">{profile.user.firstName} {profile.user.lastName}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-muted-foreground">شناسه تلگرام</span>
              <span className="font-medium font-mono text-sm" dir="ltr">{profile.user.telegramId}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-muted-foreground">نام کاربری</span>
              <span className="font-medium font-mono text-sm" dir="ltr">@{profile.user.username || '---'}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-muted-foreground">تاریخ عضویت</span>
              <span className="font-medium" dir="ltr">
                {new Date(profile.user.createdAt).toLocaleDateString('fa-IR')}
              </span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-muted-foreground">وضعیت حساب</span>
              <Badge variant={profile.user.accountStatus === 'active' ? 'default' : 'destructive'}>
                {profile.user.accountStatus === 'active' ? 'فعال' : 'غیرفعال'}
              </Badge>
            </div>
          </CardContent>
        </Card>

        <div className="lg:col-span-2 space-y-8">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <Card className="bg-card">
              <CardContent className="p-4 flex flex-col justify-center items-center text-center space-y-2">
                <ShoppingCart className="w-8 h-8 text-primary mb-1" />
                <span className="text-2xl font-bold">{profile.stats.total}</span>
                <span className="text-sm text-muted-foreground">کل سفارش‌ها</span>
              </CardContent>
            </Card>
            <Card className="bg-card">
              <CardContent className="p-4 flex flex-col justify-center items-center text-center space-y-2">
                <CheckCircle2 className="w-8 h-8 text-green-500 mb-1" />
                <span className="text-2xl font-bold">{profile.stats.completed}</span>
                <span className="text-sm text-muted-foreground">تکمیل شده</span>
              </CardContent>
            </Card>
            <Card className="bg-card">
              <CardContent className="p-4 flex flex-col justify-center items-center text-center space-y-2">
                <Clock className="w-8 h-8 text-amber-500 mb-1" />
                <span className="text-2xl font-bold">{profile.stats.pending}</span>
                <span className="text-sm text-muted-foreground">در انتظار پرداخت</span>
              </CardContent>
            </Card>
            <Card className="bg-card">
              <CardContent className="p-4 flex flex-col justify-center items-center text-center space-y-2">
                <Wallet className="w-8 h-8 text-primary mb-1" />
                <span className="text-lg font-bold">{profile.stats.totalSpent.toLocaleString('fa-IR')}</span>
                <span className="text-sm text-muted-foreground">مجموع خرید (تومان)</span>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>۵ سفارش اخیر</CardTitle>
            </CardHeader>
            <CardContent>
              {profile.orders.length > 0 ? (
                <div className="rounded-md border border-white/10 overflow-hidden">
                  <Table>
                    <TableHeader className="bg-secondary/50">
                      <TableRow>
                        <TableHead className="text-right">کد سفارش</TableHead>
                        <TableHead className="text-right">سرویس</TableHead>
                        <TableHead className="text-right">مبلغ (تومان)</TableHead>
                        <TableHead className="text-right">وضعیت</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {profile.orders.slice(0, 5).map((order) => (
                        <TableRow key={order.id}>
                          <TableCell className="font-mono text-sm">{order.orderCode}</TableCell>
                          <TableCell>{order.planName}</TableCell>
                          <TableCell>{order.amount.toLocaleString('fa-IR')}</TableCell>
                          <TableCell>
                            {order.status === 'pending' && <Badge variant="outline" className="text-amber-500 border-amber-500/20 bg-amber-500/10">در انتظار پرداخت</Badge>}
                            {order.status === 'completed' && <Badge variant="outline" className="text-green-500 border-green-500/20 bg-green-500/10">تکمیل شده</Badge>}
                            {order.status === 'failed' && <Badge variant="outline" className="text-red-500 border-red-500/20 bg-red-500/10">لغو شده</Badge>}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  هیچ سفارشی ثبت نکرده‌اید.
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
