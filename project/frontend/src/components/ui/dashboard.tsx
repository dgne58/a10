import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  X,
  Zap, Brain, Database, Cpu,
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
      className="inline-flex items-center gap-1 rounded-full text-[11px] font-medium whitespace-nowrap border"
      style={{
        padding: "2px 8px",
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
            className="flex flex-col gap-1"
            style={{
              padding: 16,
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
          className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-x-2"
          style={{ borderBottom: "1px solid rgba(0,0,0,0.07)", padding: "8px 12px" }}
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
              className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-x-2 items-center transition-colors duration-150 cursor-default"
              style={{ borderTop: i > 0 ? "1px solid rgba(0,0,0,0.045)" : undefined, padding: "10px 12px" }}
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

// ── HumanEval types ───────────────────────────────────────────────────────────

interface HumanEvalSummary {
  total: number;
  router_pass_at_1: number;
  naive_pass_at_1: number;
  router_cost_usd: number;
  naive_cost_usd: number;
  cost_reduction_pct: number;
}

interface ParetoPoint { label: string; cost: number; quality: number; highlight: boolean; }
interface PGRData { pgr: number; router_cost_fraction: number; curve: { cost_fraction: number; quality: number }[]; }

// ── HumanEval stats card ──────────────────────────────────────────────────────

function HumanEvalStats({ data }: { data: HumanEvalSummary }) {
  return (
    <div className="space-y-2">
      <span style={LABEL_STYLE}>HumanEval — pass@1</span>
      <div style={{ ...INNER_CARD, overflow: "hidden" }}>
        <div className="grid grid-cols-2">
          {[
            { label: "Router pass@1", value: `${Math.round(data.router_pass_at_1 * 100)}%`, green: false },
            { label: "GPT-4o-mini",   value: `${Math.round(data.naive_pass_at_1 * 100)}%`,  green: false },
            { label: "Cost saved",    value: `${data.cost_reduction_pct}%`, green: true },
            { label: "Tasks solved",  value: `${Math.round(data.router_pass_at_1 * data.total)}/${data.total}`, green: false },
          ].map((s, i) => (
            <div
              key={s.label}
              className="flex flex-col gap-1"
              style={{
                padding: 14,
                borderRight: i % 2 === 0 ? "1px solid rgba(0,0,0,0.07)" : undefined,
                borderBottom: i < 2 ? "1px solid rgba(0,0,0,0.07)" : undefined,
              }}
            >
              <span style={LABEL_STYLE}>{s.label}</span>
              <span className="text-xl font-bold font-mono" style={{ color: s.green ? "#059669" : TEXT_DARK }}>
                {s.value}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Pareto frontier chart ─────────────────────────────────────────────────────

function ParetoChart({ points }: { points: ParetoPoint[] }) {
  const maxCost    = Math.max(...points.map(p => p.cost)) * 1.2 || 1;
  const maxQuality = 1.0;
  const W = 260, H = 120, PAD = 28;

  return (
    <div className="space-y-2">
      <span style={LABEL_STYLE}>Pareto frontier — cost vs quality</span>
      <div style={{ ...INNER_CARD, padding: 16 }}>
        <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{ display: "block" }}>
          {/* axes */}
          <line x1={PAD} y1={H - PAD} x2={W - 8} y2={H - PAD} stroke="rgba(0,0,0,0.1)" strokeWidth={1} />
          <line x1={PAD} y1={8}        x2={PAD}   y2={H - PAD} stroke="rgba(0,0,0,0.1)" strokeWidth={1} />
          <text x={W / 2} y={H - 4} textAnchor="middle" fontSize={8} fill={TEXT_MUTED}>Cost (USD)</text>
          <text x={8} y={H / 2} textAnchor="middle" fontSize={8} fill={TEXT_MUTED} transform={`rotate(-90,8,${H/2})`}>Quality</text>
          {points.map((p) => {
            const cx = PAD + ((p.cost / maxCost) * (W - PAD - 16));
            const cy = (H - PAD) - (p.quality / maxQuality) * (H - PAD - 12);
            return (
              <g key={p.label}>
                {p.highlight
                  ? <polygon points={`${cx},${cy - 7} ${cx + 6},${cy + 4} ${cx - 6},${cy + 4}`} fill="#059669" />
                  : <circle cx={cx} cy={cy} r={5} fill="rgba(107,76,48,0.25)" stroke="rgba(107,76,48,0.5)" strokeWidth={1} />
                }
                <text x={cx + 8} y={cy + 3} fontSize={7} fill={p.highlight ? "#059669" : TEXT_MUTED}>{p.label}</text>
              </g>
            );
          })}
        </svg>
        <p className="text-[10px] mt-1" style={{ color: TEXT_MUTED }}>
          ▲ = Router (green). Closer to top-left = better trade-off.
        </p>
      </div>
    </div>
  );
}

// ── PGR curve ─────────────────────────────────────────────────────────────────

function PGRCurve({ data }: { data: PGRData }) {
  const W = 260, H = 110, PAD = 28;
  const pts = data.curve;
  const toX = (f: number) => PAD + f * (W - PAD - 12);
  const toY = (q: number) => (H - PAD) - q * (H - PAD - 12);
  const pathD = pts.map((p, i) => `${i === 0 ? "M" : "L"}${toX(p.cost_fraction).toFixed(1)},${toY(p.quality).toFixed(1)}`).join(" ");
  const rx = toX(data.router_cost_fraction);

  return (
    <div className="space-y-2">
      <span style={LABEL_STYLE}>PGR curve — Performance Gap Recovered</span>
      <div style={{ ...INNER_CARD, padding: 16 }}>
        <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{ display: "block" }}>
          <line x1={PAD} y1={H - PAD} x2={W - 8}  y2={H - PAD} stroke="rgba(0,0,0,0.1)" strokeWidth={1} />
          <line x1={PAD} y1={8}        x2={PAD}    y2={H - PAD} stroke="rgba(0,0,0,0.1)" strokeWidth={1} />
          <path d={pathD} fill="none" stroke="#94C9E9" strokeWidth={2} strokeLinejoin="round" />
          <line x1={rx} y1={12} x2={rx} y2={H - PAD} stroke="#059669" strokeWidth={1.5} strokeDasharray="3,2" />
          <text x={rx + 3} y={22} fontSize={7} fill="#059669">router</text>
          <text x={W / 2} y={H - 4} textAnchor="middle" fontSize={8} fill={TEXT_MUTED}>Cost fraction</text>
          <text x={8} y={H / 2} textAnchor="middle" fontSize={8} fill={TEXT_MUTED} transform={`rotate(-90,8,${H/2})`}>Quality</text>
        </svg>
        <p className="text-[10px] mt-1 font-mono" style={{ color: TEXT_MUTED }}>
          PGR = {(data.pgr * 100).toFixed(0)}% of strong-model quality recovered
        </p>
      </div>
    </div>
  );
}

// ── Confusion matrix ──────────────────────────────────────────────────────────

function ConfusionMatrix({ matrix }: { matrix: Record<string, Record<string, number>> }) {
  const branches = Object.keys(matrix).filter(b => Object.values(matrix[b]).some(v => v > 0));
  if (branches.length === 0) return null;

  return (
    <div className="space-y-2">
      <span style={LABEL_STYLE}>Classifier confusion matrix</span>
      <div style={{ ...INNER_CARD, padding: 12, overflowX: "auto" }}>
        <table style={{ fontSize: 10, borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th style={{ padding: "3px 6px", color: TEXT_MUTED, textAlign: "left", fontWeight: 500 }}>actual\pred</th>
              {branches.map(b => (
                <th key={b} style={{ padding: "3px 4px", color: TEXT_MUTED, fontWeight: 500, textAlign: "center" }}>
                  {BRANCH_META[b]?.label ?? b}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {branches.map(row => (
              <tr key={row}>
                <td style={{ padding: "3px 6px", color: TEXT_MED, fontWeight: 500 }}>{BRANCH_META[row]?.label ?? row}</td>
                {branches.map(col => {
                  const v = matrix[row]?.[col] ?? 0;
                  const isCorrect = row === col && v > 0;
                  return (
                    <td
                      key={col}
                      style={{
                        padding: "3px 4px",
                        textAlign: "center",
                        fontFamily: "monospace",
                        background: isCorrect ? "rgba(5,150,105,0.1)" : v > 0 ? "rgba(239,68,68,0.07)" : undefined,
                        color: isCorrect ? "#059669" : v > 0 ? "#EF4444" : TEXT_MUTED,
                      }}
                    >
                      {v}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────────

interface DashboardProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Dashboard({ isOpen, onClose }: DashboardProps) {
  const setIsOpen = (val: boolean) => { if (!val) onClose(); };
  const [summary, setSummary] = useState<EvalSummary | null>(null);
  const [allQuestions, setAllQuestions] = useState<EvalQuestion[]>([]);
  const [humanEval, setHumanEval] = useState<HumanEvalSummary | null>(null);
  const [pareto, setPareto] = useState<ParetoPoint[] | null>(null);
  const [pgr, setPgr] = useState<PGRData | null>(null);
  const [confusion, setConfusion] = useState<Record<string, Record<string, number>> | null>(null);
  const [error, setError] = useState(false);
  const hasFetched = useRef(false);

  // Fetch on first open
  useEffect(() => {
    if (!isOpen || hasFetched.current) return;
    hasFetched.current = true;
    Promise.allSettled([
      fetch("http://localhost:5000/api/eval/summary").then((r) => r.json()),
      fetch("http://localhost:5000/api/eval/questions").then((r) => r.json()),
      fetch("http://localhost:5000/api/eval/humaneval").then((r) => r.json()),
      fetch("http://localhost:5000/api/eval/pareto").then((r) => r.json()),
      fetch("http://localhost:5000/api/eval/pgr").then((r) => r.json()),
      fetch("http://localhost:5000/api/eval/confusion").then((r) => r.json()),
    ]).then(([sum, qs, he, par, pg, conf]) => {
      if (sum.status === "fulfilled" && !sum.value.error) setSummary(sum.value);
      else setError(true);
      if (qs.status === "fulfilled" && Array.isArray(qs.value)) setAllQuestions(qs.value);
      if (he.status === "fulfilled" && !he.value.error) setHumanEval(he.value);
      if (par.status === "fulfilled" && Array.isArray(par.value)) setPareto(par.value);
      if (pg.status === "fulfilled" && !pg.value.error) setPgr(pg.value);
      if (conf.status === "fulfilled" && !conf.value.error) setConfusion(conf.value);
    });
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
                  <span style={LABEL_STYLE}>HumanEval · 100 Python problems · pass@1</span>
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
                  Router vs naive GPT-4o-mini on coding tasks. Grounded in{" "}
                  <span style={{ fontWeight: 600, color: TEXT_DARK }}>RouteLLM (Berkeley, 2024)</span>
                  {" "}— Pareto-optimal cost/quality trade-off.
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

                  {/* HumanEval stats */}
                  {humanEval && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.28 }}
                    >
                      <HumanEvalStats data={humanEval} />
                    </motion.div>
                  )}

                  {/* Pareto frontier */}
                  {pareto && pareto.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.32 }}
                    >
                      <ParetoChart points={pareto} />
                    </motion.div>
                  )}

                  {/* PGR curve */}
                  {pgr && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.36 }}
                    >
                      <PGRCurve data={pgr} />
                    </motion.div>
                  )}

                  {/* Confusion matrix */}
                  {confusion && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.40 }}
                    >
                      <ConfusionMatrix matrix={confusion} />
                    </motion.div>
                  )}

                  {/* Table */}
                  {questions.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.44 }}
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
