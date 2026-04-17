import { useEffect, useRef, useState } from "react";
import { motion, useInView } from "framer-motion";
import { Zap, Brain, Database, Search, Cpu, CheckCircle, XCircle, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";

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

// ── Branch config — light mode ────────────────────────────────────────────────

const BRANCH_META: Record<string, {
  label: string; color: string; bg: string; border: string; bar: string; dot: string;
  Icon: React.ElementType;
}> = {
  memory_answer:     { label: "Memory", color: "text-emerald-700", bg: "bg-emerald-50",  border: "border-emerald-200", bar: "bg-emerald-500", dot: "bg-emerald-500", Icon: Database },
  cheap_model:       { label: "Fast",   color: "text-blue-700",    bg: "bg-blue-50",     border: "border-blue-200",   bar: "bg-blue-500",    dot: "bg-blue-500",    Icon: Zap },
  mid_model:         { label: "Mid",    color: "text-amber-700",   bg: "bg-amber-50",    border: "border-amber-200",  bar: "bg-amber-500",   dot: "bg-amber-500",   Icon: Cpu },
  strong_model:      { label: "Strong", color: "text-orange-700",  bg: "bg-orange-50",   border: "border-orange-200", bar: "bg-orange-500",  dot: "bg-orange-500",  Icon: Brain },
  verification_tool: { label: "Verify", color: "text-violet-700",  bg: "bg-violet-50",   border: "border-violet-200", bar: "bg-violet-500",  dot: "bg-violet-500",  Icon: Search },
};

// ── Fade-in wrapper ───────────────────────────────────────────────────────────

function Reveal({ children, delay = 0, className }: {
  children: React.ReactNode; delay?: number; className?: string;
}) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.55, delay, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}

// ── Stat strip ────────────────────────────────────────────────────────────────

function StatStrip({ summary }: { summary: EvalSummary }) {
  const stats = [
    {
      label: "Router accuracy",
      value: `${Math.round(summary.router_accuracy * 100)}%`,
      sub: `${Math.round(summary.router_accuracy * summary.total)} / ${summary.total} correct`,
      accent: false,
    },
    {
      label: "Naive GPT-4o",
      value: `${Math.round(summary.naive_accuracy * 100)}%`,
      sub: `${Math.round(summary.naive_accuracy * summary.total)} / ${summary.total} correct`,
      accent: false,
    },
    {
      label: "Cost saved",
      value: `${summary.cost_reduction_pct}%`,
      sub: `$${summary.router_cost_usd.toFixed(4)} vs $${summary.naive_cost_usd.toFixed(4)}`,
      accent: true,
    },
    {
      label: "Savings factor",
      value: `${(summary.naive_cost_usd / summary.router_cost_usd).toFixed(1)}×`,
      sub: "cheaper than GPT-4o",
      accent: true,
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-gray-100 rounded-2xl border border-gray-100 bg-white shadow-sm overflow-hidden">
      {stats.map((s, i) => (
        <motion.div
          key={s.label}
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.05 + i * 0.07, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col gap-1 px-6 py-5"
        >
          <span className="text-[10px] uppercase tracking-widest text-gray-400 font-medium">{s.label}</span>
          <span className={cn("text-3xl font-bold tracking-tight font-mono", s.accent ? "text-emerald-600" : "text-gray-900")}>
            {s.value}
          </span>
          <span className="text-xs text-gray-400 font-mono">{s.sub}</span>
        </motion.div>
      ))}
    </div>
  );
}

// ── Branch routing card ───────────────────────────────────────────────────────

function BranchCard({ questions }: { questions: EvalQuestion[] }) {
  const dist: Record<string, number> = {};
  for (const q of questions) dist[q.router_branch] = (dist[q.router_branch] ?? 0) + 1;
  const total = questions.length;
  const sorted = Object.entries(dist).sort((a, b) => b[1] - a[1]);

  return (
    <div className="rounded-2xl border border-gray-100 bg-white shadow-sm p-6 space-y-5">
      <div>
        <h3 className="text-sm font-semibold text-gray-900">Branch routing</h3>
        <p className="text-xs text-gray-400 mt-0.5">How the router split 100 MMLU questions</p>
      </div>
      <div className="space-y-3">
        {sorted.map(([branch, count], i) => {
          const meta = BRANCH_META[branch];
          const pct = Math.round((count / total) * 100);
          const Icon = meta?.Icon ?? Cpu;
          return (
            <motion.div
              key={branch}
              initial={{ opacity: 0, x: -10 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.35, delay: i * 0.06 }}
              className="flex items-center gap-3"
            >
              <span className={cn(
                "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-medium w-[4.5rem] shrink-0",
                meta?.color ?? "text-gray-600",
                meta?.bg ?? "bg-gray-50",
                meta?.border ?? "border-gray-200"
              )}>
                <Icon className="h-3 w-3 shrink-0" />
                {meta?.label ?? branch}
              </span>
              <div className="flex-1 h-2 rounded-full bg-gray-100 overflow-hidden">
                <motion.div
                  className={cn("h-full rounded-full", meta?.bar ?? "bg-gray-400")}
                  initial={{ width: 0 }}
                  whileInView={{ width: `${pct}%` }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.65, delay: 0.1 + i * 0.06, ease: [0.16, 1, 0.3, 1] }}
                />
              </div>
              <span className="w-16 shrink-0 text-right text-xs font-mono text-gray-400">
                {count} <span className="text-gray-300">({pct}%)</span>
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

// ── Accuracy comparison card ──────────────────────────────────────────────────

function AccuracyCard({ summary }: { summary: EvalSummary }) {
  const routerPct = Math.round(summary.router_accuracy * 100);
  const naivePct = Math.round(summary.naive_accuracy * 100);
  const delta = naivePct - routerPct;

  return (
    <div className="rounded-2xl border border-gray-100 bg-white shadow-sm p-6 space-y-5">
      <div>
        <h3 className="text-sm font-semibold text-gray-900">Accuracy trade-off</h3>
        <p className="text-xs text-gray-400 mt-0.5">Router vs GPT-4o baseline</p>
      </div>

      <div className="space-y-4">
        {[
          { label: "Router", pct: routerPct, color: "bg-blue-500", textColor: "text-blue-700" },
          { label: "GPT-4o", pct: naivePct, color: "bg-gray-800", textColor: "text-gray-700" },
        ].map((row, i) => (
          <div key={row.label} className="space-y-1.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium text-gray-600">{row.label}</span>
              <span className={cn("font-mono font-semibold", row.textColor)}>{row.pct}%</span>
            </div>
            <div className="h-2 rounded-full bg-gray-100 overflow-hidden">
              <motion.div
                className={cn("h-full rounded-full", row.color)}
                initial={{ width: 0 }}
                whileInView={{ width: `${row.pct}%` }}
                viewport={{ once: true }}
                transition={{ duration: 0.65, delay: 0.15 + i * 0.1, ease: [0.16, 1, 0.3, 1] }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Delta callout */}
      <div className="rounded-xl bg-gray-50 border border-gray-100 px-4 py-3 flex items-start gap-2.5">
        <TrendingDown className="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0" />
        <p className="text-xs text-gray-500 leading-relaxed">
          <span className="font-semibold text-gray-700">{delta}-point accuracy gap</span> — the Pareto
          trade-off. RouteLLM shows the same pattern: {summary.cost_reduction_pct}% cost reduction
          at ~{delta}% accuracy cost.
        </p>
      </div>
    </div>
  );
}

// ── Question table ────────────────────────────────────────────────────────────

function QuestionTable({ questions }: { questions: EvalQuestion[] }) {
  return (
    <div className="rounded-2xl border border-gray-100 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-x-4 bg-gray-50 border-b border-gray-100 px-5 py-3">
        {["Question", "Branch", "Router", "Naive", "Cost"].map((h, i) => (
          <span key={h} className={cn(
            "text-[10px] font-semibold uppercase tracking-widest text-gray-400",
            i === 2 || i === 3 ? "text-center" : "",
            i === 4 ? "text-right" : ""
          )}>{h}</span>
        ))}
      </div>

      {/* Rows */}
      <div className="divide-y divide-gray-50">
        {questions.map((q, i) => {
          const meta = BRANCH_META[q.router_branch];
          const Icon = meta?.Icon ?? Cpu;
          return (
            <motion.div
              key={q.id}
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.025 }}
              className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-x-4 items-center px-5 py-3 hover:bg-gray-50/70 transition-colors duration-150"
            >
              <span className="text-sm text-gray-600 truncate pr-2">
                {q.question.length > 65 ? q.question.slice(0, 65) + "…" : q.question}
              </span>

              <span className={cn(
                "inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-medium whitespace-nowrap",
                meta?.color ?? "text-gray-600",
                meta?.bg ?? "bg-gray-50",
                meta?.border ?? "border-gray-200"
              )}>
                <Icon className="h-3 w-3" />
                {meta?.label ?? q.router_branch}
              </span>

              <span className="flex justify-center">
                {q.router_correct
                  ? <CheckCircle className="h-4 w-4 text-emerald-500" />
                  : <XCircle className="h-4 w-4 text-red-400" />}
              </span>

              <span className="flex justify-center">
                {q.naive_correct
                  ? <CheckCircle className="h-4 w-4 text-emerald-500" />
                  : <XCircle className="h-4 w-4 text-red-400" />}
              </span>

              <span className="text-right font-mono text-[11px] text-gray-400">
                ${q.router_cost.toFixed(6)}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const sectionRef = useRef<HTMLElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: "-80px" });

  const [summary, setSummary] = useState<EvalSummary | null>(null);
  const [allQuestions, setAllQuestions] = useState<EvalQuestion[]>([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!isInView) return;
    Promise.all([
      fetch("http://localhost:5000/api/eval/summary").then((r) => r.json()),
      fetch("http://localhost:5000/api/eval/questions").then((r) => r.json()),
    ])
      .then(([sum, qs]) => {
        setSummary(sum);
        setAllQuestions(Array.isArray(qs) ? qs : []);
      })
      .catch(() => setError(true));
  }, [isInView]);

  const questions = allQuestions.slice(0, 10);

  return (
    <section
      ref={sectionRef}
      className="relative w-full"
      style={{
        background:
          "linear-gradient(to bottom, rgba(202,179,214,0.6) 0%, rgba(238,174,202,0.25) 20%, rgba(245,170,100,0.06) 36%, #FAFAFA 52%)",
      }}
    >
      <div className="relative mx-auto max-w-4xl px-5 pt-20 pb-28 space-y-10">

        {/* Section heading — sits on gradient, no card */}
        <Reveal>
          <div className="flex items-center gap-3 mb-3">
            <div className="h-px w-6 bg-white/60" />
            <span className="text-[10px] uppercase tracking-widest text-white/70 font-medium drop-shadow-sm">
              MMLU Benchmark · 100 questions · 5 subjects
            </span>
          </div>
          <h2 className="text-4xl font-semibold tracking-tight text-gray-900 drop-shadow-sm">
            Benchmark results
          </h2>
          <p className="mt-2 text-sm text-gray-600 max-w-lg leading-relaxed">
            Router vs naive GPT-4o. Grounded in{" "}
            <span className="text-gray-800 font-medium">RouteLLM (Berkeley, 2024)</span>{" "}
            — up to 3.66× cost reduction at minimal accuracy cost.
          </p>
        </Reveal>

        {/* Hero metric — floats on gradient */}
        <Reveal delay={0.08}>
          <div className="flex flex-col sm:flex-row sm:items-end gap-4 py-6 border-y border-white/40">
            <div>
              <span className="block text-[5.5rem] font-black leading-none tracking-tighter text-emerald-700 drop-shadow-sm">
                94%
              </span>
              <span className="text-xl font-light text-gray-600 tracking-wide">
                cheaper than GPT-4o
              </span>
            </div>
            <div className="sm:ml-auto sm:text-right space-y-1 pb-1">
              <p className="text-xs text-gray-500 font-mono">$0.0025 router cost</p>
              <p className="text-xs text-gray-400 font-mono">vs $0.0417 GPT-4o</p>
              <p className="text-xs text-gray-500">16.6× savings factor</p>
            </div>
          </div>
        </Reveal>

        {/* Backend offline */}
        {error && (
          <div className="rounded-xl border border-red-100 bg-red-50 px-5 py-4 text-sm text-red-500">
            Backend offline — start Flask server to load live data.
          </div>
        )}

        {/* Stat strip */}
        {summary && (
          <Reveal delay={0.12}>
            <StatStrip summary={summary} />
          </Reveal>
        )}

        {/* Two-column: routing + accuracy */}
        {summary && allQuestions.length > 0 && (
          <div className="grid md:grid-cols-5 gap-4">
            <Reveal delay={0.1} className="md:col-span-3">
              <BranchCard questions={allQuestions} />
            </Reveal>
            <Reveal delay={0.18} className="md:col-span-2">
              <AccuracyCard summary={summary} />
            </Reveal>
          </div>
        )}

        {/* Question table */}
        {questions.length > 0 && (
          <Reveal delay={0.15}>
            <div className="space-y-3">
              <div>
                <h3 className="text-sm font-semibold text-gray-900">Sample questions</h3>
                <p className="text-xs text-gray-400 mt-0.5">
                  First 10 of 100 — router branch, correctness vs GPT-4o
                </p>
              </div>
              <QuestionTable questions={questions} />
            </div>
          </Reveal>
        )}

      </div>
    </section>
  );
}
