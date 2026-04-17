import { useRef, useState, useEffect } from "react";
import { motion, AnimatePresence, useInView } from "framer-motion";
import { ArrowUp, ArrowRight, Loader2, Zap, Brain, Database, Search, Cpu, Paperclip, Globe, FolderCode } from "lucide-react";
import { cn } from "@/lib/utils";

// ── Types ────────────────────────────────────────────────────────────────────

interface RouteResponse {
  branch: string;
  rationale: string;
  model: string | null;
  cost_usd: number;
  naive_cost_usd: number;
  answer: string;
  latency_ms?: number;
}

// ── Branch config ─────────────────────────────────────────────────────────────

const BRANCH_META: Record<string, {
  label: string;
  color: string;
  bg: string;
  border: string;
  Icon: React.ElementType;
}> = {
  memory_answer:     { label: "Memory",  color: "text-emerald-400", bg: "bg-emerald-500/15", border: "border-emerald-500/40", Icon: Database },
  cheap_model:       { label: "Fast",    color: "text-blue-400",    bg: "bg-blue-500/15",    border: "border-blue-500/40",    Icon: Zap },
  mid_model:         { label: "Mid",     color: "text-amber-400",   bg: "bg-amber-500/15",   border: "border-amber-500/40",   Icon: Cpu },
  strong_model:      { label: "Strong",  color: "text-orange-400",  bg: "bg-orange-500/15",  border: "border-orange-500/40",  Icon: Brain },
  verification_tool: { label: "Verify",  color: "text-violet-400",  bg: "bg-violet-500/15",  border: "border-violet-500/40",  Icon: Search },
};

// ── Sub-components ────────────────────────────────────────────────────────────

function BranchBadge({ branch }: { branch: string }) {
  const meta = BRANCH_META[branch] ?? {
    label: branch, color: "text-gray-400", bg: "bg-gray-500/15", border: "border-gray-500/40", Icon: Cpu,
  };
  const { label, color, bg, border, Icon } = meta;
  return (
    <span className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold border", color, bg, border)}>
      <Icon className="h-3 w-3" />
      {label}
    </span>
  );
}

function CostTicker({ routerTotal, naiveTotal }: { routerTotal: number; naiveTotal: number }) {
  const saved = naiveTotal - routerTotal;
  const pct = naiveTotal > 0 ? Math.round((saved / naiveTotal) * 100) : 0;
  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-wrap items-center justify-center gap-6 rounded-2xl border border-white/10 bg-black/20 backdrop-blur-sm px-6 py-3 text-sm font-mono"
    >
      <div className="flex flex-col items-center gap-0.5">
        <span className="text-[10px] uppercase tracking-widest text-white/40">Router spent</span>
        <span className="text-white">${routerTotal.toFixed(6)}</span>
      </div>
      <div className="h-8 w-px bg-white/10" />
      <div className="flex flex-col items-center gap-0.5">
        <span className="text-[10px] uppercase tracking-widest text-white/40">GPT-4o would</span>
        <span className="text-white/50">${naiveTotal.toFixed(6)}</span>
      </div>
      <div className="h-8 w-px bg-white/10" />
      <div className="flex flex-col items-center gap-0.5">
        <span className="text-[10px] uppercase tracking-widest text-white/40">You saved</span>
        <span className="text-emerald-300 font-bold">
          ${saved.toFixed(6)}{" "}
          <span className="text-emerald-400/70">({pct}%)</span>
        </span>
      </div>
    </motion.div>
  );
}

function RouteTrace({ result }: { result: RouteResponse }) {
  const modelLabel = result.model
    ? result.model.split("/").pop() ?? result.model
    : "local";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
      className="w-full rounded-2xl border border-white/10 bg-black/20 backdrop-blur-sm p-5 space-y-4"
    >
      <div className="flex flex-wrap items-center gap-2">
        <BranchBadge branch={result.branch} />
        <span className="rounded-full border border-white/10 bg-white/5 px-2.5 py-0.5 text-xs text-white/50 font-mono">
          {modelLabel}
        </span>
        <span className="ml-auto text-xs text-white/30 font-mono">
          ${result.cost_usd.toFixed(6)}
          {result.latency_ms !== undefined && (
            <span className="ml-2 text-white/20">{result.latency_ms}ms</span>
          )}
        </span>
      </div>
      <p className="text-xs text-white/40 italic border-l-2 border-white/10 pl-3">
        {result.rationale}
      </p>
      <div className="h-px bg-white/10" />
      <p className="text-sm text-white/80 leading-relaxed whitespace-pre-wrap">
        {result.answer}
      </p>
    </motion.div>
  );
}

// ── Divider between action buttons ───────────────────────────────────────────

function Divider() {
  return <div className="h-5 w-px bg-white/15 mx-1" />;
}

// ── Main component ────────────────────────────────────────────────────────────

export default function QueryPanel() {
  const sectionRef = useRef<HTMLElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isInView = useInView(sectionRef, { once: false, margin: "-80px" });

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RouteResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [routerTotal, setRouterTotal] = useState(0);
  const [naiveTotal, setNaiveTotal] = useState(0);
  const hasRun = routerTotal > 0;

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [query]);

  async function handleSubmit() {
    const q = query.trim();
    if (!q || loading) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch("http://localhost:5000/api/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: RouteResponse = await res.json();
      setResult(data);
      setRouterTotal((t) => t + (data.cost_usd ?? 0));
      setNaiveTotal((t) => t + (data.naive_cost_usd ?? 0));
      setQuery("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  const hasContent = query.trim().length > 0;

  return (
    <section
      ref={sectionRef}
      className="relative w-full min-h-screen flex flex-col items-center justify-center"
      style={{
        background: "radial-gradient(125% 125% at 50% 101%, rgba(245,87,2,1) 10.5%, rgba(245,120,2,1) 16%, rgba(245,140,2,1) 17.5%, rgba(245,170,100,1) 25%, rgba(238,174,202,1) 40%, rgba(202,179,214,1) 65%, rgba(148,201,233,1) 100%)",
      }}
    >
      {/* Fade from hero's #FAFAFA into gradient at very top */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-32"
        style={{ background: "linear-gradient(to bottom, #FAFAFA 0%, transparent 100%)" }}
      />

      <motion.div
        initial={{ opacity: 0, y: 32 }}
        animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 32 }}
        transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 flex w-full max-w-[620px] flex-col items-center gap-6 px-4 py-20"
      >
        {/* Heading */}
        <div className="text-center space-y-2">
          <h2
            className="text-3xl tracking-tight text-white drop-shadow-sm"
            style={{ fontFamily: '"DM Serif Display", Georgia, serif' }}
          >
            Try the router
          </h2>
          <p className="text-sm text-white/60">
            Each query routes to the cheapest model that can answer it.
          </p>
        </div>

        {/* Cost ticker — appears after first query */}
        <AnimatePresence>
          {hasRun && <CostTicker routerTotal={routerTotal} naiveTotal={naiveTotal} />}
        </AnimatePresence>

        {/* Input box — styled to match reference dark pill */}
        <div
          className={cn(
            "w-full rounded-3xl border border-white/20 bg-[rgba(25,12,4,0.82)] backdrop-blur-md p-2 shadow-[0_8px_40px_rgba(100,40,0,0.25)] transition-all duration-300",
            loading && "border-white/25"
          )}
        >
          {/* Textarea */}
          <textarea
            ref={textareaRef}
            rows={1}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            placeholder="Type your message here..."
            className="w-full resize-none bg-transparent px-3 py-2 text-sm text-gray-100 placeholder:text-gray-500 focus:outline-none disabled:opacity-50"
            style={{ minHeight: 44, maxHeight: 200 }}
          />

          {/* Actions row */}
          <div className="flex items-center justify-between gap-2 px-1 pt-1">
            {/* Left: attachment + routing mode chips */}
            <div className="flex items-center gap-1">
              {/* Paperclip (decorative, disabled for our use) */}
              <button
                disabled
                className="flex h-8 w-8 items-center justify-center rounded-full text-gray-500 opacity-40 cursor-default"
              >
                <Paperclip className="h-4 w-4" />
              </button>

              <Divider />

              {/* Globe = web search mode chip */}
              <button
                disabled
                className="flex h-8 items-center justify-center gap-1 rounded-full px-2 text-gray-500 opacity-40 cursor-default"
              >
                <Globe className="h-4 w-4" />
              </button>

              <Divider />

              {/* Brain = router intelligence */}
              <button
                disabled
                className="flex h-8 items-center justify-center gap-1 rounded-full px-2 text-gray-500 opacity-40 cursor-default"
              >
                <Brain className="h-4 w-4" />
              </button>

              <Divider />

              {/* FolderCode = verify branch */}
              <button
                disabled
                className="flex h-8 items-center justify-center gap-1 rounded-full px-2 text-gray-500 opacity-40 cursor-default"
              >
                <FolderCode className="h-4 w-4" />
              </button>
            </div>

            {/* Right: send button */}
            <button
              onClick={handleSubmit}
              disabled={!hasContent || loading}
              className={cn(
                "flex h-8 w-8 items-center justify-center rounded-full transition-all duration-200",
                hasContent && !loading
                  ? "bg-white text-[#1F2023] hover:bg-white/90"
                  : "bg-white/10 text-gray-500 cursor-not-allowed"
              )}
            >
              {loading
                ? <Loader2 className="h-4 w-4 animate-spin" />
                : <ArrowUp className="h-4 w-4" />
              }
            </button>
          </div>
        </div>

        {/* Active branch chips — light up when response arrives */}
        <div className="flex flex-wrap justify-center gap-2">
          {(Object.keys(BRANCH_META) as Array<keyof typeof BRANCH_META>).map((b) => {
            const { label, color, bg, border, Icon } = BRANCH_META[b];
            const active = result?.branch === b;
            return (
              <span
                key={b}
                className={cn(
                  "inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[13px] font-medium border transition-all duration-300",
                  active
                    ? cn(color, bg, border)
                    : "text-white/70 bg-white/15 border-white/25"
                )}
              >
                <Icon className="h-3.5 w-3.5" />
                {label}
              </span>
            );
          })}
        </div>

        {/* Benchmark CTA */}
        <button
          onClick={() => window.dispatchEvent(new CustomEvent("open-benchmark"))}
          className="group flex items-center gap-2 rounded-full px-5 py-2 text-sm font-semibold transition-all duration-200 hover:bg-white/25 cursor-pointer"
          style={{
            backdropFilter: "blur(10px)",
            WebkitBackdropFilter: "blur(10px)",
            background: "rgba(255,255,255,0.15)",
            border: "1px solid rgba(255,255,255,0.30)",
            color: "rgba(255,255,255,0.80)",
          }}
        >
          See the benchmarks
          <ArrowRight className="h-4 w-4 transition-transform duration-150 group-hover:translate-x-0.5" />
        </button>

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full rounded-xl border border-red-400/20 bg-red-500/10 px-4 py-2 text-sm text-red-300 text-center"
            >
              {error} — is the backend running?
            </motion.p>
          )}
        </AnimatePresence>

        {/* Route trace */}
        <AnimatePresence>
          {result && <RouteTrace result={result} />}
        </AnimatePresence>
      </motion.div>
    </section>
  );
}
