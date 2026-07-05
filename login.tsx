import { useEffect, useRef, useState } from "react";
import { useLocation } from "wouter";
import { useGetMe, getGetMeQueryKey } from "@workspace/api-client-react";
import { useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { motion, AnimatePresence } from "framer-motion";
import { ExternalLink, Loader2, CheckCircle2, Smartphone } from "lucide-react";

export function Login() {
  const [, setLocation] = useLocation();
  const { data: me, isLoading } = useGetMe({ query: { queryKey: getGetMeQueryKey() } });
  const [step, setStep] = useState<"idle" | "waiting" | "success">("idle");
  const [botLink, setBotLink] = useState("");
  const [token, setToken] = useState("");
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const queryClient = useQueryClient();
  const { toast } = useToast();

  useEffect(() => {
    if (me && !isLoading) {
      setLocation("/profile");
    }
  }, [me, isLoading, setLocation]);

  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  const handleOpenBot = async () => {
    try {
      const res = await fetch("/api/auth/create-login-link", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error("خطا در ایجاد لینک");
      const data = (await res.json()) as { token: string; link: string };
      setToken(data.token);
      setBotLink(data.link);
      setStep("waiting");

      window.open(data.link, "_blank");

      pollRef.current = setInterval(async () => {
        try {
          const r = await fetch(`/api/auth/poll/${data.token}`, { credentials: "include" });
          if (r.status === 404 || r.status === 410) {
            clearInterval(pollRef.current!);
            setStep("idle");
            toast({ variant: "destructive", title: "لینک منقضی شد", description: "دوباره امتحان کنید." });
            return;
          }
          if (r.ok) {
            const result = (await r.json()) as { pending: boolean };
            if (!result.pending) {
              clearInterval(pollRef.current!);
              setStep("success");
              await queryClient.invalidateQueries({ queryKey: getGetMeQueryKey() });
              setTimeout(() => setLocation("/profile"), 1500);
            }
          }
        } catch {
          // ignore network errors during polling
        }
      }, 2000);
    } catch {
      toast({ variant: "destructive", title: "خطا", description: "مشکلی پیش آمد. دوباره امتحان کنید." });
    }
  };

  const handleCancel = () => {
    if (pollRef.current) clearInterval(pollRef.current);
    setStep("idle");
    setToken("");
    setBotLink("");
  };

  return (
    <div className="flex items-center justify-center min-h-[80vh]">
      <div className="w-full max-w-md">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="text-center mb-10">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-primary/10 border border-primary/30 mb-6 mx-auto shadow-lg shadow-primary/20">
              <span className="text-4xl">🐆</span>
            </div>
            <h1 className="text-3xl font-black mb-2">ورود به چیتا نت</h1>
            <p className="text-muted-foreground">با یک کلیک از طریق تلگرام وارد شوید</p>
          </div>

          <div className="relative rounded-2xl border border-white/10 bg-card/80 backdrop-blur-sm overflow-hidden shadow-2xl shadow-black/40">
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none" />

            <div className="p-8 space-y-6 relative">
              <AnimatePresence mode="wait">
                {step === "idle" && (
                  <motion.div
                    key="idle"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="space-y-6"
                  >
                    <div className="bg-white/5 rounded-xl p-5 space-y-4 border border-white/5">
                      <div className="flex items-start gap-4">
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-sm">۱</div>
                        <div>
                          <p className="font-semibold">روی دکمه زیر کلیک کنید</p>
                          <p className="text-sm text-muted-foreground mt-1">ربات تلگرام چیتا نت باز می‌شود</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-4">
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-sm">۲</div>
                        <div>
                          <p className="font-semibold">دکمه Start را بزنید</p>
                          <p className="text-sm text-muted-foreground mt-1">ربات اطلاعات شما را دریافت می‌کند</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-4">
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-sm">۳</div>
                        <div>
                          <p className="font-semibold">به سایت برگردید</p>
                          <p className="text-sm text-muted-foreground mt-1">پروفایل شما به صورت خودکار ساخته می‌شود</p>
                        </div>
                      </div>
                    </div>

                    <Button
                      size="lg"
                      className="w-full h-14 text-lg font-bold rounded-xl bg-[#0088cc] hover:bg-[#0077b3] text-white shadow-lg gap-3 border-0"
                      onClick={handleOpenBot}
                    >
                      <Smartphone className="w-5 h-5" />
                      ورود با تلگرام
                      <ExternalLink className="w-4 h-4 opacity-70" />
                    </Button>
                  </motion.div>
                )}

                {step === "waiting" && (
                  <motion.div
                    key="waiting"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0 }}
                    className="text-center space-y-6 py-4"
                  >
                    <div className="relative w-20 h-20 mx-auto">
                      <div className="absolute inset-0 rounded-full border-4 border-primary/20" />
                      <div className="absolute inset-0 rounded-full border-4 border-primary border-t-transparent animate-spin" />
                      <Loader2 className="absolute inset-0 m-auto w-8 h-8 text-primary animate-pulse" />
                    </div>
                    <div>
                      <p className="text-xl font-bold mb-2">منتظر تأیید تلگرام...</p>
                      <p className="text-muted-foreground text-sm">
                        در تلگرام روی <span className="text-primary font-bold">Start</span> کلیک کنید
                      </p>
                    </div>
                    <div className="flex gap-3">
                      <Button
                        variant="outline"
                        className="flex-1"
                        onClick={() => window.open(botLink, "_blank")}
                      >
                        <ExternalLink className="w-4 h-4 ml-2" />
                        باز کردن ربات
                      </Button>
                      <Button
                        variant="ghost"
                        className="flex-1 text-muted-foreground"
                        onClick={handleCancel}
                      >
                        انصراف
                      </Button>
                    </div>
                  </motion.div>
                )}

                {step === "success" && (
                  <motion.div
                    key="success"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center space-y-4 py-4"
                  >
                    <div className="w-20 h-20 mx-auto rounded-full bg-green-500/20 border border-green-500/30 flex items-center justify-center">
                      <CheckCircle2 className="w-10 h-10 text-green-400" />
                    </div>
                    <div>
                      <p className="text-xl font-bold text-green-400">ورود موفق!</p>
                      <p className="text-muted-foreground text-sm mt-1">در حال انتقال به پروفایل...</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          <p className="text-center text-xs text-muted-foreground mt-6">
            با ورود، شرایط استفاده از خدمات چیتا نت را می‌پذیرید
          </p>
        </motion.div>
      </div>
    </div>
  );
}
