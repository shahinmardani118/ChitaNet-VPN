import { useGetMe, getGetMeQueryKey, useListOrders, getListOrdersQueryKey } from "@workspace/api-client-react";
import { useLocation } from "wouter";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Copy, ShoppingBag, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export function Orders() {
  const [, setLocation] = useLocation();
  const { data: me, isLoading: meLoading } = useGetMe({ query: { queryKey: getGetMeQueryKey() } });
  const { data: orders, isLoading: ordersLoading } = useListOrders({ 
    query: { 
      queryKey: getListOrdersQueryKey(),
      enabled: !!me 
    } 
  });
  const { toast } = useToast();

  if (!meLoading && !me) {
    setLocation("/login");
    return null;
  }

  const copyConfig = (config: string) => {
    navigator.clipboard.writeText(config);
    toast({
      title: "کپی شد",
      description: "کانفیگ در کلیپ‌بورد کپی شد.",
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <ShoppingBag className="w-8 h-8 text-primary" />
          تاریخچه سفارش‌ها
        </h1>
      </div>

      <Card>
        <CardContent className="p-0">
          {ordersLoading ? (
            <div className="p-8 space-y-4">
              {[1, 2, 3, 4].map(i => <div key={i} className="h-12 bg-secondary/50 animate-pulse rounded-md" />)}
            </div>
          ) : !orders || orders.length === 0 ? (
            <div className="text-center py-16 text-muted-foreground">
              <ShoppingBag className="w-16 h-16 mx-auto mb-4 opacity-20" />
              <p>هیچ سفارشی یافت نشد.</p>
            </div>
          ) : (
            <div className="rounded-md overflow-hidden">
              <Table>
                <TableHeader className="bg-secondary/50">
                  <TableRow>
                    <TableHead className="text-right py-4">کد سفارش</TableHead>
                    <TableHead className="text-right py-4">سرویس</TableHead>
                    <TableHead className="text-right py-4">مبلغ (تومان)</TableHead>
                    <TableHead className="text-right py-4">وضعیت</TableHead>
                    <TableHead className="text-right py-4">تاریخ ثبت</TableHead>
                    <TableHead className="text-right py-4">جزئیات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {orders.map((order) => (
                    <TableRow key={order.id} className="border-border">
                      <TableCell className="font-mono text-sm">{order.orderCode}</TableCell>
                      <TableCell className="font-medium">{order.planName}</TableCell>
                      <TableCell>{order.amount.toLocaleString('fa-IR')}</TableCell>
                      <TableCell>
                        {order.status === 'pending' && <Badge variant="outline" className="text-amber-500 border-amber-500/20 bg-amber-500/10">در انتظار</Badge>}
                        {order.status === 'completed' && <Badge variant="outline" className="text-green-500 border-green-500/20 bg-green-500/10">تکمیل شده</Badge>}
                        {order.status === 'failed' && <Badge variant="outline" className="text-red-500 border-red-500/20 bg-red-500/10">لغو شده</Badge>}
                      </TableCell>
                      <TableCell dir="ltr" className="text-right text-sm">
                        {new Date(order.createdAt).toLocaleDateString('fa-IR')}
                      </TableCell>
                      <TableCell>
                        {order.config && order.status === 'completed' ? (
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="secondary" size="sm" className="gap-2">
                                <Eye className="w-4 h-4" /> مشاهده کانفیگ
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-md" dir="rtl">
                              <DialogHeader>
                                <DialogTitle>اطلاعات کانفیگ شما</DialogTitle>
                                <DialogDescription>
                                  متن زیر را کپی کرده و در نرم‌افزار مربوطه وارد کنید.
                                </DialogDescription>
                              </DialogHeader>
                              <div className="mt-4 relative">
                                <pre className="p-4 bg-background border border-border rounded-lg text-sm font-mono overflow-x-auto text-left" dir="ltr">
                                  {order.config}
                                </pre>
                                <Button 
                                  size="icon" 
                                  className="absolute top-2 right-2"
                                  onClick={() => copyConfig(order.config!)}
                                >
                                  <Copy className="w-4 h-4" />
                                </Button>
                              </div>
                              {order.expiryDate && (
                                <div className="mt-4 text-sm text-center bg-secondary/30 p-2 rounded text-muted-foreground">
                                  تاریخ انقضا: {new Date(order.expiryDate).toLocaleDateString('fa-IR')}
                                </div>
                              )}
                            </DialogContent>
                          </Dialog>
                        ) : order.status === 'pending' ? (
                          <Button variant="outline" size="sm" onClick={() => setLocation(`/buy/${order.planKey}`)}>
                            ادامه پرداخت
                          </Button>
                        ) : (
                          <span className="text-muted-foreground text-sm">-</span>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
