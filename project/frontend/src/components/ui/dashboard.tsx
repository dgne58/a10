import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  X, ArrowRight,
  Zap, Brain, Database, Search, Cpu,
  CheckCircle, XCircle, TrendingDown,
} from "lucide-react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface EvalSummary {
  total: number;
  router_accuracy: number;
  naive_accuracy: number;
  router_cost_usd: number;
  naive_cost_usd: number;
  cost_reduction_pct: number;
  model_distribution: Record<string, number>;
}

interface EvalQuestion {
  id: string;
  question: string;
  router_branch: string;
  router_correct: boolean;
  router_cost: number;
  naive_correct: boolean;
  label: { complexity: string; domain: string };
}

// ── Design tokens ─────────────────────────────────────────────────────────────

const TEXT_DARK    = "#1A0E05";
const TEXT_MED     = "#6B4C30";
const TEXT_MUTED   = "#A89880";
const FONT_DISPLAY = '"DM Serif Display", Georgia, serif';

const INNER_CARD: React.CSSProperties = {
  background: "rgba(255,255,255,0.65)",
  border: "1px solid rgba(0,0,0,0.07)",
  borderRadius: 14,
};

const LABEL_STYLE: React.CSSProperties = {
  fontSize: 10,
  textTransform: "uppercase",
  letterSpacing: "0.12em",
  fontWeight: 500,
  color: TEXT_MUTED,
};

// ── Branch meta (gradient palette) ───────────────────────────────────────────

const BRANCH_META: Record<string, {
  label: string; barColor: string; textColor: string; Icon: React.ElementType;
}> = {
  memory_answer:     { label: "Memory", barColor: "#EEAECA", textColor: "#8B3A62", Icon: Database },
  cheap_model:       { label: "Fast",   barColor: "#94C9E9", textColor: "#1A6A99", Icon: Zap },
  mid_model:         { label: "Mid",    barColor: "#CAB3D6", textColor: "#6B3FA0", Icon: Cpu },
  strong_model:      { label: "Strong", barColor: "#F55702", textColor: "#B33D00", Icon: Brain },
  verification_tool: { label: "Verify", barColor: "#F5AA64", textColor: "#9A5A00", Icon: Search },
};

function hexAlpha(hex: string, alpha: number): string {
  return `${hex}${Math.round(alpha * 255).toString(16).padStart(2, "0")}`;
}

// ── Branch chip ───────────────────────────────────────────────────────────────

function BranchChip({ branch }: { branch: string }) {
  const meta = BRANCH_META[branch] ?? { label: branch, barColor: "#A89880", textColor: TEXT_MED, Icon: Cpu };
  const { label, barColor, textColor, Icon } = meta;
  return (
    <span
      className="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-medium whitespace-nowrap border"
      style={{
        background: hexAlpha(barColor, 0.14),
        borderColor: hexAlpha(barColor, 0.38),
        color: textColor,
      }}
    >
      <Icon className="h-3 w-3 shrink-0" />
      {label}
    </span>
  );
}

// ── Stat grid (2×2 for panel width) ──────────────────────────────────────────

function StatGrid({ summary }: { summary: EvalSummary }) {
  const stats = [
    {
      label: "Router accuracy",
      value: `${Math.round(summary.router_accuracy * 100)}%`,
      sub: `${Math.round(summary.router_accuracy * summary.total)} / ${summary.total}`,
      green: false,
    },
    {
      label: "Naive GPT-4o",
      value: `${Math.round(summary.naive_accuracy * 100)}%`,
      sub: `${Math.round(summary.naive_accuracy * summary.total)} / ${summary.total}`,
      green: false,
    },
    {
      label: "Cost saved",
      value: `${summary.cost_reduction_pct}%`,
      sub: `$${summary.router_cost_usd.toFixed(4)} vs $${summary.naive_cost_usd.toFixed(4)}`,
      green: true,
    },
    {
      label: "Savings factor",
      value: `${(summary.naive_cost_usd / summary.router_cost_usd).toFixed(1)}×`,
      sub: "cheaper than GPT-4o",
      green: false,
    },
  ];

  return (
    <div style={{ ...INNER_CARD, overflow: "hidden" }}>
      <div className="grid grid-cols-2">
        {stats.map((s, i) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: 0.05 + i * 0.07 }}
            className="flex flex-col gap-1 p-4"
            style={{
              borderRight: i % 2 === 0 ? "1px solid rgba(0,0,0,0.07)" : undefined,
              borderBottom: i < 2 ? "1px solid rgba(0,0,0,0.07)" : undefined,
            }}
          >
            <span style={LABEL_STYLE}>{s.label}</span>
            <span
              className="text-2xl font-bold font-mono tracking-tight"
              style={{ color: s.green ? "#059669" : TEXT_DARK }}
            >
              {s.value}
            </span>
            <span className="text-[11px] font-mono" style={{ color: TEXT_MUTED }}>{s.sub}</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

// ── Branch routing chart ──────────────────────────────────────────────────────

function BranchChart({ questions }: { questions: EvalQuestion[] }) {
  const dist: Record<string, number> = {};
  for (const q of questions) dist[q.router_branch] = (dist[q.router_branch] ?? 0) + 1;
  const total = questions.length;
  const sorted = Object.entries(dist).sort((a, b) => b[1] - a[1]);

  return (
    <div className="space-y-2">
      <span style={LABEL_STYLE}>Branch routing</span>
      <div style={{ ...INNER_CARD, padding: 16 }} className="space-y-3">
        {sorted.map(([branch, count], i) => {
          const meta = BRANCH_META[branch] ?? { label: branch, barColor: "#A89880", textColor: TEXT_MED, Icon: Cpu };
          const pct = Math.round((count / total) * 100);
          return (
            <motion.div
              key={branch}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: i * 0.06 }}
              className="space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <BranchChip branch={branch} />
                <span className="text-xs font-mono" style={{ color: TEXT_MUTED }}>
                  {count}{" "}
                  <span style={{ color: "#D4C4B4" }}>({pct}%)</span>
                </span>
              </div>
              <div
                className="h-1.5 rounded-full overflow-hidden"
                style={{ background: "rgba(0,0,0,0.07)" }}
              >
                <motion.div
                  className="h-full rounded-full"
                  style={{ background: meta.barColor }}
                  initial={{ width: 0 }}
                  animate={{ width: `${pct}%` }}
                  transition={{ duration: 0.65, delay: 0.15 + i * 0.07, ease: [0.16, 1, 0.3, 1] }}
                />
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

// ── Accuracy chart ────────────────────────────────────────────────────────────

function AccuracyChart({ summary }: { summary: EvalSummary }) {
  const routerPct = Math.round(summary.router_accuracy * 100);
  const naivePct  = Math.round(summary.naive_accuracy * 100);
  const delta     = naivePct - routerPct;

  return (
    <div className="space-y-2">
      <span style={LABEL_STYLE}>Accuracy trade-off</span>
      <div style={{ ...INNER_CARD, padding: 16 }} className="space-y-4">
        {[
          { label: "Router", pct: routerPct, color: "#94C9E9" },
          { label: "GPT-4o", pct: naivePct,  color: "#6B4C30" },
        ].map((row, i) => (
          <div key={row.label} className="space-y-1.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium" style={{ color: TEXT_MED }}>{row.label}</span>
              <span className="font-mono font-semibold" style={{ color: TEXT_DARK }}>{row.pct}%</span>
            </div>
            <div
              className="h-1.5 rounded-full overflow-hidden"
              style={{ background: "rgba(0,0,0,0.07)" }}
            >
              <motion.div
                className="h-full rounded-full"
                style={{ background: row.color }}
                initial={{ width: 0 }}
                animate={{ width: `${row.pct}%` }}
                transition={{ duration: 0.65, delay: 0.2 + i * 0.1, ease: [0.16, 1, 0.3, 1] }}
              />
            </div>
          </div>
        ))}
        <div
          className="rounded-xl px-3 py-2.5 flex items-start gap-2"
          style={{ background: "rgba(0,0,0,0.04)", border: "1px solid rgba(0,0,0,0.05)" }}
        >
          <TrendingDown className="h-3.5 w-3.5 mt-0.5 shrink-0" style={{ color: TEXT_MUTED }} />
          <p className="text-xs leading-relaxed" style={{ color: TEXT_MED }}>
            <span className="font-semibold" style={{ color: TEXT_DARK }}>{delta}-point accuracy gap</span>
            {" "}— the Pareto trade-off. {summary.cost_reduction_pct}% cost reduction at ~{delta}%
            accuracy cost.
          </p>
        </div>
      </div>
    </div>
  );
}

// ── Question table (compact for 456px content width) ─────────────────────────

function QuestionTable({ questions }: { questions: EvalQuestion[] }) {
  return (
    <div className="space-y-2">
      <span style={LABEL_STYLE}>Sample questions</span>
      <div style={{ ...INNER_CARD, overflow: "hidden" }}>
        <div
          className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-x-2 px-3 py-2"
          style={{ borderBottom: "1px solid rgba(0,0,0,0.07)" }}
        >
          {(["Question", "Branch", "R", "N", "Cost"] as const).map((h, i) => (
            <span
              key={h}
              style={{
                ...LABEL_STYLE,
                textAlign: (i === 2 || i === 3) ? "center" : i === 4 ? "right" : "left",
              }}
            >
              {h}
            </span>
          ))}
        </div>
        <div>
          {questions.map((q, i) => (
            <motion.div
              key={q.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.02 + i * 0.025 }}
              className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-x-2 items-center px-3 py-2.5 transition-colors duration-150 cursor-default"
              style={{ borderTop: i > 0 ? "1px solid rgba(0,0,0,0.045)" : undefined }}
              onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(0,0,0,0.02)")}
              onMouseLeave={(e) => (e.currentTarget.style.background = "")}
            >
              <span className="text-xs truncate pr-1" style={{ color: TEXT_MED }}>
                {q.question.length > 30 ? q.question.slice(0, 30) + "…" : q.question}
              </span>
              <BranchChip branch={q.router_branch} />
              <span className="flex justify-center">
                {q.router_correct
                  ? <CheckCircle className="h-3.5 w-3.5 text-emerald-500" />
                  : <XCircle className="h-3.5 w-3.5 text-red-400" />}
              </span>
              <span className="flex justify-center">
                {q.naive_correct
                  ? <CheckCircle className="h-3.5 w-3.5 text-emerald-500" />
                  : <XCircle className="h-3.5 w-3.5 text-red-400" />}
              </span>
              <span className="text-right font-mono text-[10px]" style={{ color: TEXT_MUTED }}>
                ${q.router_cost.toFixed(5)}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const [isOpen, setIsOpen] = useState<boolean>(() => {
    try { return sessionStorage.getItem("benchmarkPanel") === "open"; }
    catch { return false; }
  });
  const [summary, setSummary] = useState<EvalSummary | null>(null);
  const [allQuestions, setAllQuestions] = useState<EvalQuestion[]>([]);
  const [error, setError] = useState(false);
  const hasFetched = useRef(false);

  // Persist panel state
  useEffect(() => {
    try { sessionStorage.setItem("benchmarkPanel", isOpen ? "open" : "closed"); }
    catch { /* noop */ }
  }, [isOpen]);

  // Fetch on first open
  useEffect(() => {
    if (!isOpen || hasFetched.current) return;
    hasFetched.current = true;
    Promise.all([
      fetch("http://localhost:5000/api/eval/summary").then((r) => r.json()),
      fetch("http://localhost:5000/api/eval/questions").then((r) => r.json()),
    ])
      .then(([sum, qs]) => {
        setSummary(sum);
        setAllQuestions(Array.isArray(qs) ? qs : []);
      })
      .catch(() => setError(true));
  }, [isOpen]);

  // Esc to close
  useEffect(() => {
    if (!isOpen) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") setIsOpen(false);
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [isOpen]);

  const questions = allQuestions.slice(0, 10);

  return (
    <>
      {/* ── Floating CTA pill ─────────────────────────────────────────────────
          Wrapper owns fixed+translateY so Framer Motion x-transforms don't
          fight the CSS transform needed for vertical centering. */}
      <div
        style={{
          position: "fixed",
          right: 16,
          top: "50%",
          transform: "translateY(-50%)",
          zIndex: 40,
          pointerEvents: isOpen ? "none" : "auto",
        }}
      >
        <AnimatePresence>
          {!isOpen && (
            <motion.button
              className="group"
              initial={{ opacity: 0, x: 24 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 24 }}
              whileHover={{ x: -2 }}
              transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
              onClick={() => setIsOpen(true)}
              aria-label="Open benchmark panel"
              style={{
                backdropFilter: "blur(12px)",
                WebkitBackdropFilter: "blur(12px)",
                background: "rgba(255,245,235,0.85)",
                border: "1px solid rgba(255,255,255,0.68)",
                boxShadow: "0 4px 24px rgba(100,50,10,0.18), inset 0 1px 0 rgba(255,255,255,0.55)",
                borderRadius: 999,
                padding: "10px 18px",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                gap: 8,
                fontSize: 13,
                fontWeight: 600,
                color: TEXT_DARK,
                letterSpacing: "0.01em",
                whiteSpace: "nowrap",
              }}
            >
              See the benchmarks
              <span className="inline-flex transition-transform duration-150 group-hover:translate-x-0.5">
                <ArrowRight style={{ width: 14, height: 14 }} />
              </span>
            </motion.button>
          )}
        </AnimatePresence>
      </div>

      {/* ── Backdrop + slide-out panel ─────────────────────────────────────── */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop dim — click to close */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.22 }}
              onClick={() => setIsOpen(false)}
              style={{
                position: "fixed",
                inset: 0,
                background: "rgba(0,0,0,0.10)",
                zIndex: 45,
              }}
            />

            {/* Panel */}
            <motion.div
              role="dialog"
              aria-modal="true"
              aria-label="Benchmark results"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              style={{
                position: "fixed",
                right: 0,
                top: 0,
                bottom: 0,
                width: "min(520px, 100vw)",
                zIndex: 50,
                background: "#FDF8F4",
                borderRadius: "20px 0 0 20px",
                boxShadow: "-8px 0 48px rgba(100,50,10,0.14), -1px 0 0 rgba(0,0,0,0.07)",
                overflow: "hidden",
                display: "flex",
                flexDirection: "column",
              }}
            >
              {/* Sticky header */}
              <div
                style={{
                  position: "sticky",
                  top: 0,
                  background: "#FDF8F4",
                  padding: "28px 32px 20px",
                  borderBottom: "1px solid rgba(0,0,0,0.07)",
                  flexShrink: 0,
                  zIndex: 2,
                }}
              >
                {/* Close button */}
                <button
                  onClick={() => setIsOpen(false)}
                  aria-label="Close benchmark panel"
                  style={{
                    position: "absolute",
                    top: 20,
                    right: 20,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: 32,
                    height: 32,
                    borderRadius: "50%",
                    border: "1px solid rgba(0,0,0,0.10)",
                    background: "rgba(0,0,0,0.04)",
                    cursor: "pointer",
                    color: TEXT_MUTED,
                    transition: "background 0.15s",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(0,0,0,0.09)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "rgba(0,0,0,0.04)")}
                >
                  <X style={{ width: 14, height: 14 }} />
                </button>

                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
                  <div style={{ height: 1, width: 16, background: "rgba(168,152,128,0.4)" }} />
                  <span style={LABEL_STYLE}>MMLU Benchmark · 100 questions · 5 subjects</span>
                </div>
                <h2 style={{
                  fontFamily: FONT_DISPLAY,
                  fontSize: 28,
                  lineHeight: 1.2,
                  color: TEXT_DARK,
                  marginBottom: 8,
                }}>
                  Benchmark results
                </h2>
                <p style={{ fontSize: 13, color: TEXT_MED, lineHeight: 1.6, maxWidth: 380 }}>
                  Router vs naive GPT-4o. Grounded in{" "}
                  <span style={{ fontWeight: 600, color: TEXT_DARK }}>RouteLLM (Berkeley, 2024)</span>
                  {" "}— up to 3.66× cost reduction at minimal accuracy cost.
                </p>
              </div>

              {/* Scrollable body */}
              <div style={{ flex: 1, overflowY: "auto", padding: "24px 32px 48px" }}>
                <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>

                  {/* Hero stat */}
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.06 }}
                    style={{
                      display: "flex",
                      alignItems: "flex-end",
                      justifyContent: "space-between",
                      gap: 16,
                      padding: "20px 0",
                      borderTop: "1px solid rgba(0,0,0,0.07)",
                      borderBottom: "1px solid rgba(0,0,0,0.07)",
                    }}
                  >
                    <div>
                      <span style={{
                        display: "block",
                        fontSize: 72,
                        fontWeight: 900,
                        lineHeight: 1,
                        letterSpacing: "-0.04em",
                        color: TEXT_DARK,
                      }}>
                        94%
                      </span>
                      <span style={{ fontSize: 16, fontWeight: 300, letterSpacing: "0.02em", color: TEXT_MED }}>
                        cheaper than GPT-4o
                      </span>
                    </div>
                    <div style={{ textAlign: "right", paddingBottom: 4 }}>
                      <p style={{ fontSize: 11, fontFamily: "monospace", color: TEXT_MED, marginBottom: 2 }}>
                        $0.0025 router cost
                      </p>
                      <p style={{ fontSize: 11, fontFamily: "monospace", color: TEXT_MUTED, marginBottom: 2 }}>
                        vs $0.0417 GPT-4o
                      </p>
                      <p style={{ fontSize: 11, fontWeight: 600, color: TEXT_MED }}>
                        16.6× savings factor
                      </p>
                    </div>
                  </motion.div>

                  {/* Error */}
                  {error && (
                    <div style={{
                      borderRadius: 12,
                      border: "1px solid rgba(254,202,202,0.8)",
                      background: "rgba(254,242,242,0.8)",
                      padding: "12px 16px",
                      fontSize: 13,
                      color: "#EF4444",
                    }}>
                      Backend offline — start Flask server to load live data.
                    </div>
                  )}

                  {/* Loading */}
                  {!summary && !error && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                      style={{
                        textAlign: "center",
                        padding: "48px 0",
                        color: TEXT_MUTED,
                        fontSize: 13,
                      }}
                    >
                      Loading benchmark data…
                    </motion.div>
                  )}

                  {/* Stat grid */}
                  {summary && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.12 }}
                    >
                      <StatGrid summary={summary} />
                    </motion.div>
                  )}

                  {/* Branch chart */}
                  {allQuestions.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.18 }}
                    >
                      <BranchChart questions={allQuestions} />
                    </motion.div>
                  )}

                  {/* Accuracy chart */}
                  {summary && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.24 }}
                    >
                      <AccuracyChart summary={summary} />
                    </motion.div>
                  )}

                  {/* Table */}
                  {questions.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.3 }}
                    >
                      <QuestionTable questions={questions} />
                    </motion.div>
                  )}

                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
