import { useRef, useState, useEffect } from "react";
import { motion, AnimatePresence, useInView } from "framer-motion";
import { ArrowUp, ArrowRight, Loader2, Zap, Brain, Database, Search, Cpu, Wrench } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { cn } from "@/lib/utils";

// ── Types ────────────────────────────────────────────────────────────────────

interface RouteMeta {
  branch: string;
  rationale: string;
  model_used: string | null;
  cost_usd: number;
  naive_cost_usd: number;
  latency_ms?: number;
}

interface ToolUseEvent {
  tool: string;
  result: string;
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

function ToolUseBadge({ toolUse }: { toolUse: ToolUseEvent }) {
  const label = toolUse.tool === "fetch_url" ? "fetch_url" : toolUse.tool === "execute_python" ? "execute_python" : toolUse.tool;
  const preview = toolUse.result.length > 120 ? toolUse.result.slice(0, 120) + "…" : toolUse.result;
  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      transition={{ duration: 0.25 }}
      className="rounded-xl border border-cyan-500/30 bg-cyan-500/10 px-3 py-2 space-y-1"
    >
      <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-400">
        <Wrench className="h-3 w-3" />
        Tool: {label}
      </div>
      <p className="text-xs text-white/50 font-mono break-all">{preview}</p>
    </motion.div>
  );
}

function RouteTrace({
  meta,
  answer,
  isStreaming,
  toolUse,
}: {
  meta: RouteMeta;
  answer: string;
  isStreaming: boolean;
  toolUse: ToolUseEvent | null;
}) {
  const modelLabel = meta.model_used
    ? meta.model_used.split("/").pop() ?? meta.model_used
    : "local";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
      className="w-full rounded-2xl border border-white/10 bg-black/20 backdrop-blur-sm p-5 space-y-4"
    >
      <div className="flex flex-wrap items-center gap-2">
        <BranchBadge branch={meta.branch} />
        <span className="rounded-full border border-white/10 bg-white/5 px-2.5 py-0.5 text-xs text-white/50 font-mono">
          {modelLabel}
        </span>
        {toolUse && (
          <span className="inline-flex items-center gap-1 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-2.5 py-0.5 text-xs font-semibold text-cyan-400">
            <Wrench className="h-3 w-3" />
            {toolUse.tool === "fetch_url" ? "fetch_url" : toolUse.tool === "execute_python" ? "execute_python" : toolUse.tool}
          </span>
        )}
        <span className="ml-auto text-xs text-white/30 font-mono">
          {isStreaming ? (
            <span className="text-white/20 animate-pulse">streaming…</span>
          ) : (
            <>
              ${meta.cost_usd.toFixed(6)}
              {meta.latency_ms !== undefined && (
                <span className="ml-2 text-white/20">{meta.latency_ms}ms</span>
              )}
            </>
          )}
        </span>
      </div>
      <p className="text-xs text-white/40 italic border-l-2 border-white/10 pl-3">
        {meta.rationale}
      </p>
      {toolUse && <ToolUseBadge toolUse={toolUse} />}
      <div className="h-px bg-white/10" />
      <div className="overflow-y-auto max-h-72 pr-1 [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-white/20 [&::-webkit-scrollbar-track]:bg-transparent
        prose prose-sm prose-invert max-w-none text-white/80
        [&>h1]:text-base [&>h1]:font-semibold [&>h1]:mt-3 [&>h1]:mb-1
        [&>h2]:text-base [&>h2]:font-semibold [&>h2]:mt-3 [&>h2]:mb-1
        [&>h3]:text-sm  [&>h3]:font-semibold [&>h3]:mt-2 [&>h3]:mb-0.5
        [&>p]:leading-relaxed [&>p]:mb-2
        [&>ul]:pl-4 [&>ul]:mb-2 [&>ul>li]:list-disc [&>ul>li]:mb-0.5
        [&>ol]:pl-4 [&>ol]:mb-2 [&>ol>li]:list-decimal [&>ol>li]:mb-0.5
        [&>pre]:bg-white/5 [&>pre]:rounded-lg [&>pre]:p-3 [&>pre]:overflow-x-auto [&>pre]:mb-2
        [&_code]:bg-white/10 [&_code]:rounded [&_code]:px-1 [&_code]:py-0.5 [&_code]:text-xs [&_code]:font-mono
        [&>pre_code]:bg-transparent [&>pre_code]:p-0
        [&>blockquote]:border-l-2 [&>blockquote]:border-white/20 [&>blockquote]:pl-3 [&>blockquote]:text-white/50
        [&>hr]:border-white/10">
        <ReactMarkdown>{answer}</ReactMarkdown>
        {isStreaming && (
          <span className="inline-block w-0.5 h-4 bg-white/60 ml-0.5 animate-[blink_0.9s_step-end_infinite] align-middle" />
        )}
      </div>
    </motion.div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

interface QueryPanelProps {
  onOpenBenchmark: () => void;
}

export default function QueryPanel({ onOpenBenchmark }: QueryPanelProps) {
  const sectionRef = useRef<HTMLElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isInView = useInView(sectionRef, { once: false, margin: "-80px" });

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [meta, setMeta] = useState<RouteMeta | null>(null);
  const [answer, setAnswer] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [toolUse, setToolUse] = useState<ToolUseEvent | null>(null);
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
    setIsStreaming(false);
    setError(null);
    setMeta(null);
    setAnswer("");
    setToolUse(null);
    setQuery("");

    try {
      const res = await fetch("http://localhost:5000/api/route/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      if (!res.body) throw new Error("No response body");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      setLoading(false);
      setIsStreaming(true);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const event = JSON.parse(line.slice(6));
            if (event.type === "meta") {
              setMeta({
                branch: event.branch,
                rationale: event.rationale,
                model_used: event.model_used,
                cost_usd: 0,
                naive_cost_usd: 0,
              });
            } else if (event.type === "token") {
              setAnswer((a) => a + event.text);
            } else if (event.type === "tool_use") {
              setToolUse({ tool: event.tool, result: event.result });
            } else if (event.type === "done") {
              setMeta((m) => m ? {
                ...m,
                cost_usd: event.cost_usd,
                naive_cost_usd: event.naive_cost_usd,
                latency_ms: event.latency_ms,
              } : m);
              setRouterTotal((t) => t + (event.cost_usd ?? 0));
              setNaiveTotal((t) => t + (event.naive_cost_usd ?? 0));
              setIsStreaming(false);
            }
          } catch {
            // malformed SSE line — skip
          }
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
      setIsStreaming(false);
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
            className="w-full resize-none bg-transparent text-sm text-gray-100 placeholder:text-gray-500 focus:outline-none disabled:opacity-50"
            style={{ minHeight: 44, maxHeight: 200, padding: "10px 14px" }}
          />

          {/* Actions row */}
          <div className="flex items-center justify-end gap-2 px-1 pt-1">
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
            const active = meta?.branch === b;
            return (
              <span
                key={b}
                className={cn(
                  "inline-flex items-center gap-2 rounded-full text-sm font-medium border transition-all duration-300",
                  active
                    ? cn(color, bg, border)
                    : "text-white/70 bg-white/15 border-white/25"
                )}
                style={{ padding: "8px 16px" }}
              >
                <Icon className="h-4 w-4" />
                {label}
              </span>
            );
          })}
        </div>

        {/* Benchmark CTA */}
        <button
          onClick={onOpenBenchmark}
          className="group flex items-center gap-2 rounded-full text-sm font-semibold transition-all duration-200 hover:bg-white/25 cursor-pointer"
          style={{
            padding: "10px 22px",
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
          {meta && (
            <RouteTrace meta={meta} answer={answer} isStreaming={isStreaming} toolUse={toolUse} />
          )}
        </AnimatePresence>
      </motion.div>
    </section>
  );
}
