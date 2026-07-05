import { Switch, Route, Router as WouterRouter } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";
import { Layout } from "@/components/Layout";
import { CheetahIntro } from "@/components/CheetahIntro";
import { useState } from "react";

// Pages
import { Home } from "@/pages/home";
import { Login } from "@/pages/login";
import { Profile } from "@/pages/profile";
import { Orders } from "@/pages/orders";
import { Buy } from "@/pages/buy";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});

function Router() {
  return (
    <Layout>
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/login" component={Login} />
        <Route path="/profile" component={Profile} />
        <Route path="/orders" component={Orders} />
        <Route path="/buy/:planKey" component={Buy} />
        <Route component={NotFound} />
      </Switch>
    </Layout>
  );
}

const INTRO_KEY = "chita_intro_shown";

function App() {
  const [introDone, setIntroDone] = useState(() => {
    return sessionStorage.getItem(INTRO_KEY) === "1";
  });

  const handleIntroDone = () => {
    sessionStorage.setItem(INTRO_KEY, "1");
    setIntroDone(true);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        {!introDone && <CheetahIntro onDone={handleIntroDone} />}
        <WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, "")}>
          <Router />
        </WouterRouter>
        <Toaster />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
