import IntroAnimation from "@/components/ui/scroll-morph-hero";
import QueryPanel from "@/components/ui/query-panel";
import Dashboard from "@/components/ui/dashboard";

export default function App() {
  return (
    <>
      <div className="w-full" style={{ background: "#FAF8F5" }}>
        {/* Hero — tall container gives scroll distance for animation */}
        <div style={{ height: "calc(100vh + 3000px)" }} className="relative">
          <div className="sticky top-0 h-screen overflow-hidden">
            <IntroAnimation />
          </div>
        </div>

        <QueryPanel />
      </div>

      {/* Benchmark panel — fixed overlay, outside page flow */}
      <Dashboard />
    </>
  );
}
