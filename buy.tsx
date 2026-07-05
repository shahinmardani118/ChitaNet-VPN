import { useRef, useState } from "react";
import { useRoute, useLocation } from "wouter";
import {
  useGetMe, getGetMeQueryKey,
  useListPlans, getListPlansQueryKey,
  useCreateOrder,
  useGetPaymentInfo, getGetPaymentInfoQueryKey
} from "@workspace/api-client-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { Copy, CreditCard, CheckCircle2, AlertTriangle, ShieldCheck, Upload, ImageIcon, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function Buy() {
  const [match, params] = useRoute("/buy/:planKey");
  const [, setLocation] = useLocation();
  const { toast } = useToast();

  const { data: me, isLoading: meLoading } = useGetMe({ query: { queryKey: getGetMeQueryKey() } });
  const { data: plans } = useListPlans({ query: { queryKey: getListPlansQueryKey() } });
  const { data: paymentInfo } = useGetPaymentInfo({ query: { queryKey: getGetPaymentInfoQueryKey() } });

  const createOrder = useCreateOrder();
  const [orderId, setOrderId] = useState<number | null>(null);
  const [orderCode, setOrderCode] = useState<string | null>(null);
  const [orderAmount, setOrderAmount] = useState<number | null>(null);

  const [receiptFile, setReceiptFile] = useState<File | null>(null);
  const [receiptPreview, setReceiptPreview] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [receiptSent, setReceiptSent] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!meLoading && !me) {
    setLocation(`/login`);
    return null;
  }

  const plan = plans?.find(p => p.key === params?.planKey);

  if (!match || !plan) {
    return (
      <div className="py-12 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto" />
        <h2 className="text-2xl font-bold">پلن مورد نظر یافت نشد</h2>
        <Button onClick={() => setLocation("/")}>بازگشت به صفحه اصلی</Button>
      </div>
    );
  }

  const handleCreateOrder = () => {
    createOrder.mutate({ data: { planKey: plan.key } }, {
      onSuccess: (data) => {
        setOrderId(data.id);
        setOrderCode(data.orderCode);
        setOrderAmount(data.amount);
      },
      onError: () => {
        toast({ variant: "destructive", title: "خطا در ثبت سفارش", description: "لطفاً دوباره تلاش کنید." });
      }
    });
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast({ title: "کپی شد", description: label });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      toast({ variant: "destructive", title: "فقط تصویر مجاز است", description: "لطفاً یک فایل تصویری انتخاب کنید." });
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      toast({ variant: "destructive", title: "حجم فایل زیاد است", description: "حداکثر حجم ۵ مگابایت است." });
      return;
    }
    setReceiptFile(file);
    const reader = new FileReader();
    reader.onload = (ev) => setReceiptPreview(ev.target?.result as string);
    reader.readAsDataURL(file);
  };

  const handleSubmitReceipt = async () => {
    if (!receiptPreview || !orderId) return;
    setIsUploading(true);
    try {
      const res = await fetch(`/api/orders/${orderId}/receipt`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ receiptData: receiptPreview }),
      });
      if (!res.ok) {
        const err = (await res.json()) as { error?: string };
        throw new Error(err.error || "خطا");
      }
      setReceiptSent(true);
      toast({ title: "رسید ثبت شد", description: "پس از بررسی، سرویس شما فعال می‌شود." });
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "خطای ناشناخته";
      toast({ variant: "destructive", title: "خطا در ارسال رسید", description: msg });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto py-8 space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-black mb-1">تکمیل خرید</h1>
        <p className="text-muted-foreground">{plan.name}</p>
      </div>

      <AnimatePresence mode="wait">

        {/* Step 1 — Confirm order */}
        {!orderCode && (
          <motion.div key="step1" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
            <div className="rounded-2xl border border-white/10 bg-card overflow-hidden">
              <div className="p-6 border-b border-white/6 space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">سرور</span>
                  <span className="font-medium">{plan.server}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">سرعت</span>
                  <span className="font-medium">{plan.speed}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">اعتبار</span>
                  <span className="font-medium">{plan.days} روز</span>
                </div>
                <div className="flex items-center justify-between pt-3 border-t border-white/6">
                  <span className="font-semibold">مبلغ قابل پرداخت</span>
                  <span className="text-2xl font-black text-primary">
                    {plan.price.toLocaleString("fa-IR")} <span className="text-sm font-normal text-muted-foreground">تومان</span>
                  </span>
                </div>
              </div>
              <div className="p-6 flex items-start gap-3 text-sm text-muted-foreground bg-primary/5 border-b border-white/6">
                <ShieldCheck className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                <p>با تأیید سفارش، یک کد یکتا برای پیگیری صادر می‌شود. سپس مبلغ را به کارت واریز کنید و رسید را در سایت آپلود کنید.</p>
              </div>
              <div className="p-6">
                <Button
                  className="w-full h-12 text-base font-bold rounded-xl"
                  onClick={handleCreateOrder}
                  disabled={createOrder.isPending}
                >
                  {createOrder.isPending ? (
                    <><Loader2 className="w-4 h-4 ml-2 animate-spin" />در حال ثبت...</>
                  ) : (
                    <>تأیید و دریافت کد سفارش</>
                  )}
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Step 2 — Payment + receipt upload */}
        {orderCode && !receiptSent && (
          <motion.div key="step2" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-4">

            {/* Order code */}
            <div className="rounded-2xl border border-primary/30 bg-primary/5 p-5 flex items-center justify-between">
              <div>
                <p className="text-xs text-muted-foreground mb-1">کد سفارش شما</p>
                <p className="font-mono font-bold text-lg tracking-wider" dir="ltr">{orderCode}</p>
              </div>
              <Button variant="ghost" size="icon" onClick={() => copyToClipboard(orderCode, "کد سفارش کپی شد")}>
                <Copy className="w-4 h-4" />
              </Button>
            </div>

            {/* Bank card */}
            <div className="rounded-2xl border border-white/10 bg-card p-6 space-y-5">
              <div className="flex items-center gap-2 text-sm font-semibold">
                <CreditCard className="w-5 h-5 text-primary" />
                اطلاعات واریز
              </div>

              <div className="space-y-4">
                <div>
                  <p className="text-xs text-muted-foreground mb-2">مبلغ قابل پرداخت</p>
                  <p className="text-3xl font-black">
                    {(orderAmount ?? 0).toLocaleString("fa-IR")}
                    <span className="text-base font-normal text-muted-foreground mr-1">تومان</span>
                  </p>
                </div>
                <div className="h-px bg-white/6" />
                <div>
                  <p className="text-xs text-muted-foreground mb-2">شماره کارت</p>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-xl font-bold tracking-widest text-primary" dir="ltr">
                      {paymentInfo?.bankCard.match(/.{1,4}/g)?.join("  ")}
                    </span>
                    <Button variant="ghost" size="icon" className="hover:bg-primary/20 hover:text-primary" onClick={() => copyToClipboard(paymentInfo?.bankCard || "", "شماره کارت کپی شد")}>
                      <Copy className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">به نام</p>
                  <p className="font-bold text-base">{paymentInfo?.bankOwner}</p>
                </div>
              </div>
            </div>

            {/* Receipt upload */}
            <div className="rounded-2xl border border-white/10 bg-card p-6 space-y-4">
              <div className="flex items-center gap-2 text-sm font-semibold">
                <Upload className="w-5 h-5 text-primary" />
                آپلود رسید پرداخت
              </div>
              <p className="text-sm text-muted-foreground">پس از واریز، تصویر رسید را اینجا آپلود کنید تا سرویس شما فعال شود.</p>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleFileChange}
              />

              {!receiptPreview ? (
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="w-full h-36 rounded-xl border-2 border-dashed border-white/20 hover:border-primary/50 hover:bg-primary/5 transition-colors flex flex-col items-center justify-center gap-3 text-muted-foreground hover:text-primary cursor-pointer"
                >
                  <ImageIcon className="w-10 h-10" />
                  <span className="text-sm font-medium">کلیک کنید یا تصویر را اینجا بکشید</span>
                  <span className="text-xs opacity-60">JPG، PNG — حداکثر ۵ مگابایت</span>
                </button>
              ) : (
                <div className="space-y-3">
                  <div className="relative rounded-xl overflow-hidden border border-white/10 max-h-64">
                    <img src={receiptPreview} alt="رسید پرداخت" className="w-full object-contain max-h-64" />
                    <button
                      type="button"
                      onClick={() => { setReceiptFile(null); setReceiptPreview(null); }}
                      className="absolute top-2 left-2 w-8 h-8 rounded-full bg-black/60 text-white flex items-center justify-center text-xs hover:bg-black/80"
                    >
                      ✕
                    </button>
                  </div>
                  <p className="text-xs text-muted-foreground text-center">{receiptFile?.name}</p>
                </div>
              )}

              <div className="flex gap-3">
                {receiptPreview && (
                  <Button variant="outline" className="flex-1" onClick={() => fileInputRef.current?.click()}>
                    تغییر تصویر
                  </Button>
                )}
                <Button
                  className="flex-1 font-bold"
                  disabled={!receiptPreview || isUploading}
                  onClick={handleSubmitReceipt}
                >
                  {isUploading ? (
                    <><Loader2 className="w-4 h-4 ml-2 animate-spin" />در حال ارسال...</>
                  ) : (
                    <>ارسال رسید</>
                  )}
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Step 3 — Success */}
        {receiptSent && (
          <motion.div key="step3" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="text-center space-y-6 py-8">
            <div className="w-24 h-24 mx-auto rounded-3xl bg-green-500/15 border border-green-500/30 flex items-center justify-center">
              <CheckCircle2 className="w-12 h-12 text-green-400" />
            </div>
            <div>
              <h2 className="text-2xl font-black text-green-400 mb-2">رسید ثبت شد!</h2>
              <p className="text-muted-foreground max-w-xs mx-auto">
                رسید شما با موفقیت دریافت شد. پس از بررسی توسط پشتیبانی، سرویس شما فعال می‌شود.
              </p>
            </div>
            <div className="flex gap-3 justify-center">
              <Button variant="outline" onClick={() => setLocation("/orders")}>مشاهده سفارش‌ها</Button>
              <Button onClick={() => setLocation("/")}>صفحه اصلی</Button>
            </div>
          </motion.div>
        )}

      </AnimatePresence>
    </div>
  );
}
