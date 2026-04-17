import { useState } from "react";
import IntroAnimation from "@/components/ui/scroll-morph-hero";
import QueryPanel from "@/components/ui/query-panel";
import Dashboard from "@/components/ui/dashboard";

export default function App() {
  const [benchmarkOpen, setBenchmarkOpen] = useState(false);

  return (
    <>
      <div className="w-full" style={{ background: "#FAF8F5" }}>
        {/* Hero — tall container gives scroll distance for animation */}
        <div style={{ height: "calc(100vh + 3000px)" }} className="relative">
          <div className="sticky top-0 h-screen overflow-hidden">
            <IntroAnimation />
          </div>
        </div>

        <QueryPanel onOpenBenchmark={() => setBenchmarkOpen(true)} />
      </div>

      {/* Benchmark panel — fixed overlay, outside page flow */}
      <Dashboard isOpen={benchmarkOpen} onClose={() => setBenchmarkOpen(false)} />
    </>
  );
}
