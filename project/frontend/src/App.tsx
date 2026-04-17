import IntroAnimation from "@/components/ui/scroll-morph-hero";
import QueryPanel from "@/components/ui/query-panel";
import Dashboard from "@/components/ui/dashboard";

export default function App() {
  return (
    <div className="w-full bg-[#FAFAFA]">
      {/* Hero — tall container gives scroll distance for animation */}
      <div style={{ height: "calc(100vh + 3000px)" }} className="relative">
        <div className="sticky top-0 h-screen overflow-hidden">
          <IntroAnimation />
        </div>
      </div>

      <QueryPanel />
      <Dashboard />
    </div>
  );
}
