import { useListPlans, getListPlansQueryKey, useGetMe, getGetMeQueryKey } from "@workspace/api-client-react";
import { Link, useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Shield, Zap, Globe, Clock, CheckCircle2, Star, ArrowLeft, Server } from "lucide-react";
import { motion } from "framer-motion";

const categoryLabel: Record<string, string> = {
  economy: "اقتصادی",
  standard: "عادی",
  premium: "پرمیوم",
  popular: "پربازدید",
  pro: "حرفه‌ای",
};

const serverEmoji: Record<string, string> = {
  germany: "🇩🇪",
  netherlands: "🇳🇱",
  france: "🇫🇷",
  usa: "🇺🇸",
  uk: "🇬🇧",
  turkey: "🇹🇷",
};

function getServerEmoji(server: string) {
  const lower = server.toLowerCase();
  for (const [key, emoji] of Object.entries(serverEmoji)) {
    if (lower.includes(key)) return emoji;
  }
  return "🌐";
}

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

const item = {
  hidden: { opacity: 0, y: 32, scale: 0.97 },
  show: { opacity: 1, y: 0, scale: 1 },
};

const features = [
  {
    icon: <Shield className="w-7 h-7" />,
    title: "رمزنگاری نظامی",
    desc: "پروتکل‌های AES-256 و WireGuard برای امنیت کامل حریم خصوصی",
  },
  {
    icon: <Zap className="w-7 h-7" />,
    title: "پینگ فوق‌العاده پایین",
    desc: "مناسب ترید، گیمینگ و استریم بدون هیچ افت سرعتی",
  },
  {
    icon: <Server className="w-7 h-7" />,
    title: "سرورهای اختصاصی",
    desc: "دیتاسنترهای اروپایی با آپتایم ۹۹.۹٪ و پشتیبان‌گیری خودکار",
  },
  {
    icon: <Clock className="w-7 h-7" />,
    title: "تحویل آنی ۲۴/۷",
    desc: "دریافت کانفیگ در کمتر از ۳۰ ثانیه پس از تأیید پرداخت",
  },
];

export function Home() {
  const { data: plans, isLoading } = useListPlans({ query: { queryKey: getListPlansQueryKey() } });
  const { data: me } = useGetMe({ query: { queryKey: getGetMeQueryKey() } });
  const [, setLocation] = useLocation();

  const handleBuy = (planKey: string) => {
    if (!planKey) {
      document.getElementById("plans-section")?.scrollIntoView({ behavior: "smooth" });
      return;
    }
    if (me) setLocation(`/buy/${planKey}`);
    else setLocation(`/login`);
  };

  const popularPlan = plans?.find(p => p.category === "پربازدید" || p.category === "ویژه");

  return (
    <div className="space-y-24 pb-16">

      {/* ─── Hero ─── */}
      <section className="relative pt-12 pb-4 text-center overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[350px] rounded-full bg-primary/10 blur-[100px]" />
        </div>

        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-primary/30 bg-primary/10 text-primary text-sm font-semibold mb-6">
            <Star className="w-4 h-4 fill-primary" />
            سریع‌ترین VPN ایران
            <Star className="w-4 h-4 fill-primary" />
          </span>

          <h1 className="text-5xl md:text-7xl font-black tracking-tight leading-tight mb-6">
            اینترنت آزاد<br />
            <span className="text-gradient">بدون محدودیت</span>
          </h1>

          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed mb-10">
            دسترسی امن، پرسرعت و پایدار به تمام اینترنت جهانی.<br />
            بدون قطعی، بدون لاگ، با پشتیبانی تلگرامی ۲۴ ساعته.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              size="lg"
              className="h-14 px-8 text-lg font-bold rounded-2xl shadow-lg shadow-primary/30 glow-primary gap-2"
              onClick={() => handleBuy(popularPlan?.key ?? "")}
            >
              مشاهده پلن‌ها و شروع
              <ArrowLeft className="w-5 h-5" />
            </Button>
            {!me && (
              <Button variant="outline" size="lg" className="h-14 px-8 text-lg font-medium rounded-2xl border-white/10" asChild>
                <Link href="/login">ورود به حساب</Link>
              </Button>
            )}
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="flex flex-wrap justify-center gap-8 mt-14"
        >
          {[
            { value: "+۵۰۰۰", label: "کاربر فعال" },
            { value: "۹۹.۹٪", label: "آپتایم سرور" },
            { value: "۱ گیگ", label: "سرعت پورت" },
            { value: "۲۴/۷", label: "پشتیبانی تلگرام" },
          ].map((s) => (
            <div key={s.label} className="text-center">
              <div className="text-2xl md:text-3xl font-black text-primary">{s.value}</div>
              <div className="text-sm text-muted-foreground mt-1">{s.label}</div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* ─── Plans ─── */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-black mb-3">
            تعرفه‌های <span className="text-gradient">اشتراک</span>
          </h2>
          <p className="text-muted-foreground">پلنی که مناسب نیاز شماست را انتخاب کنید</p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-[420px] rounded-2xl bg-card/50 animate-pulse border border-border" />
            ))}
          </div>
        ) : (
          <motion.div
            variants={container}
            initial="hidden"
            animate="show"
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {plans?.map((plan) => {
              const isPopular = plan.category === "popular" || plan.category === "premium";
              return (
                <motion.div variants={item} key={plan.key}>
                  <div className={`relative rounded-2xl border bg-card card-hover flex flex-col h-full overflow-hidden ${isPopular ? "border-primary/50 shadow-xl shadow-primary/10" : "border-white/8"}`}>
                    {isPopular && (
                      <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-primary to-transparent" />
                    )}
                    {isPopular && (
                      <div className="absolute top-4 left-4">
                        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-primary text-primary-foreground text-xs font-bold">
                          <Star className="w-3 h-3 fill-current" /> محبوب‌ترین
                        </span>
                      </div>
                    )}

                    <div className="p-6 pt-8 text-center border-b border-white/5">
                      <Badge variant="secondary" className="bg-primary/15 text-primary border-primary/20 mb-4">
                        {categoryLabel[plan.category] ?? plan.category}
                      </Badge>
                      <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                      <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground mb-4">
                        <span>{getServerEmoji(plan.server)}</span>
                        <span>{plan.server}</span>
                        <Globe className="w-3.5 h-3.5" />
                      </div>
                      <div className="mt-2">
                        <span className="text-4xl font-black">{plan.price.toLocaleString("fa-IR")}</span>
                        <span className="text-muted-foreground text-sm mr-1">تومان</span>
                      </div>
                    </div>

                    <div className="p-6 space-y-3 flex-1">
                      {[
                        `سرعت: ${plan.speed}`,
                        `اعتبار: ${plan.days} روز`,
                        "پشتیبانی تلگرامی اختصاصی",
                        "بدون محدودیت ترافیک",
                        "آپتایم ۹۹.۹٪ سرورها",
                      ].map((feat) => (
                        <div key={feat} className="flex items-center gap-3 text-sm">
                          <CheckCircle2 className="w-4 h-4 text-primary shrink-0" />
                          <span>{feat}</span>
                        </div>
                      ))}
                    </div>

                    <div className="p-6 pt-0">
                      <Button
                        className={`w-full h-12 font-bold rounded-xl text-base ${isPopular ? "shadow-lg shadow-primary/30" : ""}`}
                        variant={isPopular ? "default" : "outline"}
                        onClick={() => handleBuy(plan.key)}
                      >
                        خرید اشتراک
                      </Button>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        )}
      </section>

      {/* ─── Features ─── */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-black mb-3">
            چرا <span className="text-gradient">چیتا نت</span>؟
          </h2>
          <p className="text-muted-foreground">بهترین ویژگی‌ها برای بهترین تجربه</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass rounded-2xl p-6 text-center group hover:border-primary/30 transition-colors"
            >
              <div className="w-14 h-14 rounded-2xl bg-primary/15 border border-primary/20 flex items-center justify-center mx-auto mb-4 text-primary group-hover:bg-primary/25 transition-colors">
                {f.icon}
              </div>
              <h3 className="text-base font-bold mb-2">{f.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ─── CTA Banner ─── */}
      <section>
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="relative rounded-3xl border border-primary/30 bg-gradient-to-br from-primary/10 via-card to-card overflow-hidden p-10 text-center"
        >
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[400px] h-[200px] rounded-full bg-primary/20 blur-[80px]" />
          </div>
          <h2 className="text-3xl md:text-4xl font-black mb-4">
            همین الان شروع کنید
          </h2>
          <p className="text-muted-foreground mb-8 max-w-lg mx-auto">
            در کمتر از ۲ دقیقه متصل شوید. بدون نیاز به تجربه قبلی — پشتیبانی همیشه در کنار شماست.
          </p>
          {me ? (
            <Button size="lg" className="h-14 px-10 text-lg font-bold rounded-2xl glow-primary" asChild>
              <Link href="/profile">رفتن به داشبورد</Link>
            </Button>
          ) : (
            <Button size="lg" className="h-14 px-10 text-lg font-bold rounded-2xl glow-primary" asChild>
              <Link href="/login">ورود با تلگرام — رایگان</Link>
            </Button>
          )}
        </motion.div>
      </section>
    </div>
  );
}
