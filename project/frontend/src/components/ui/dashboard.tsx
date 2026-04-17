import { useEffect, useRef, useState } from "react";
import { motion, useInView } from "framer-motion";
import { TrendingDown, Target, Zap, Brain, Database, Search, Cpu, CheckCircle, XCircle } from "lucide-react";
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

// ── Branch config (mirrors query-panel) ──────────────────────────────────────

const BRANCH_META: Record<string, { label: string; color: string; bg: string; border: string; Icon: React.ElementType }> = {
  memory_answer:     { label: "Memory", color: "text-emerald-400", bg: "bg-emerald-500/15", border: "border-emerald-500/40", Icon: Database },
  cheap_model:       { label: "Fast",   color: "text-blue-400",    bg: "bg-blue-500/15",    border: "border-blue-500/40",    Icon: Zap },
  mid_model:         { label: "Mid",    color: "text-amber-400",   bg: "bg-amber-500/15",   border: "border-amber-500/40",   Icon: Cpu },
  strong_model:      { label: "Strong", color: "text-orange-400",  bg: "bg-orange-500/15",  border: "border-orange-500/40",  Icon: Brain },
  verification_tool: { label: "Verify", color: "text-violet-400",  bg: "bg-violet-500/15",  border: "border-violet-500/40",  Icon: Search },
};

const BRANCH_BAR_COLOR: Record<string, string> = {
  memory_answer:     "bg-emerald-500",
  cheap_model:       "bg-blue-500",
  mid_model:         "bg-amber-500",
  strong_model:      "bg-orange-500",
  verification_tool: "bg-violet-500",
};

// ── Stat card ─────────────────────────────────────────────────────────────────

interface StatCardProps {
  label: string;
  value: string;
  sub?: string;
  highlight?: boolean;
  delay?: number;
}

function StatCard({ label, value, sub, highlight, delay = 0 }: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: [0.16, 1, 0.3, 1] }}
      className={cn(
        "flex flex-col gap-2 rounded-2xl border p-6",
        highlight
          ? "border-emerald-500/30 bg-emerald-500/10"
          : "border-white/10 bg-white/5"
      )}
    >
      <span className="text-xs uppercase tracking-widest text-white/40">{label}</span>
      <span className={cn("text-4xl font-bold tracking-tight", highlight ? "text-emerald-300" : "text-white")}>
        {value}
      </span>
      {sub && <span className="text-xs text-white/40">{sub}</span>}
    </motion.div>
  );
}

// ── Branch bar chart ──────────────────────────────────────────────────────────

function BranchChart({ questions }: { questions: EvalQuestion[] }) {
  const dist: Record<string, number> = {};
  for (const q of questions) {
    dist[q.router_branch] = (dist[q.router_branch] ?? 0) + 1;
  }
  const total = questions.length;
  const sorted = Object.entries(dist).sort((a, b) => b[1] - a[1]);

  return (
    <div className="space-y-3">
      {sorted.map(([branch, count], i) => {
        const meta = BRANCH_META[branch];
        const pct = Math.round((count / total) * 100);
        const Icon = meta?.Icon ?? Cpu;
        return (
          <motion.div
            key={branch}
            initial={{ opacity: 0, x: -16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4, delay: i * 0.08 }}
            className="flex items-center gap-3"
          >
            <div className="flex w-20 items-center gap-1.5 shrink-0">
              <Icon className={cn("h-3.5 w-3.5 shrink-0", meta?.color ?? "text-gray-400")} />
              <span className="text-xs text-white/60 truncate">{meta?.label ?? branch}</span>
            </div>
            <div className="flex-1 h-2 rounded-full bg-white/5 overflow-hidden">
              <motion.div
                className={cn("h-full rounded-full", BRANCH_BAR_COLOR[branch] ?? "bg-gray-500")}
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 0.6, delay: 0.2 + i * 0.08, ease: [0.16, 1, 0.3, 1] }}
              />
            </div>
            <span className="w-16 text-right text-xs text-white/40 shrink-0 font-mono">
              {count} <span className="text-white/20">({pct}%)</span>
            </span>
          </motion.div>
        );
      })}
    </div>
  );
}

// ── Questions table ───────────────────────────────────────────────────────────

function QuestionsTable({ questions }: { questions: EvalQuestion[] }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-white/10">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-white/10 bg-white/5">
            <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-widest text-white/30">Question</th>
            <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-widest text-white/30">Branch</th>
            <th className="px-4 py-3 text-center text-xs font-medium uppercase tracking-widest text-white/30">Router</th>
            <th className="px-4 py-3 text-center text-xs font-medium uppercase tracking-widest text-white/30">Naive</th>
            <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-widest text-white/30">Cost</th>
          </tr>
        </thead>
        <tbody>
          {questions.map((q, i) => {
            const meta = BRANCH_META[q.router_branch];
            const Icon = meta?.Icon ?? Cpu;
            return (
              <motion.tr
                key={q.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.04 }}
                className="border-b border-white/5 last:border-0 hover:bg-white/5 transition-colors"
              >
                <td className="max-w-[280px] px-4 py-3 text-white/70 truncate">
                  {q.question.length > 70 ? q.question.slice(0, 70) + "…" : q.question}
                </td>
                <td className="px-4 py-3">
                  <span className={cn(
                    "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium border",
                    meta?.color ?? "text-gray-400",
                    meta?.bg ?? "bg-gray-500/15",
                    meta?.border ?? "border-gray-500/40"
                  )}>
                    <Icon className="h-3 w-3" />
                    {meta?.label ?? q.router_branch}
                  </span>
                </td>
                <td className="px-4 py-3 text-center">
                  {q.router_correct
                    ? <CheckCircle className="h-4 w-4 text-emerald-400 inline" />
                    : <XCircle className="h-4 w-4 text-red-400/70 inline" />
                  }
                </td>
                <td className="px-4 py-3 text-center">
                  {q.naive_correct
                    ? <CheckCircle className="h-4 w-4 text-emerald-400 inline" />
                    : <XCircle className="h-4 w-4 text-red-400/70 inline" />
                  }
                </td>
                <td className="px-4 py-3 text-right font-mono text-xs text-white/30">
                  ${q.router_cost.toFixed(6)}
                </td>
              </motion.tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ── Section wrapper ───────────────────────────────────────────────────────────

function Section({ children, delay = 0 }: { children: React.ReactNode; delay?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const sectionRef = useRef<HTMLElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: "-100px" });

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
      className="relative w-full bg-[#0C0C0E] px-4 py-24"
    >
      {/* Fade from QueryPanel gradient into dark */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-40"
        style={{
          background: "linear-gradient(to bottom, rgba(148,201,233,0.4) 0%, #0C0C0E 100%)",
        }}
      />

      <div className="relative mx-auto max-w-4xl space-y-12">
        {/* Heading */}
        <Section>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Target className="h-5 w-5 text-white/30" />
              <span className="text-xs uppercase tracking-widest text-white/30">MMLU Benchmark — 100 questions</span>
            </div>
            <h2 className="text-3xl font-semibold tracking-tight text-white">Benchmark results</h2>
            <p className="text-sm text-white/40 max-w-xl">
              Router vs naive GPT-4o on 100 MMLU questions across 5 subjects.
              Grounded in <span className="text-white/60">RouteLLM (Berkeley, 2024)</span> — up to 3.66× cost reduction.
            </p>
          </div>
        </Section>

        {/* Backend offline */}
        {error && (
          <div className="rounded-2xl border border-red-500/20 bg-red-500/10 px-5 py-4 text-sm text-red-400">
            Backend offline — start Flask server to load live data.
          </div>
        )}

        {/* Stat cards */}
        {summary && (
          <Section delay={0.1}>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <StatCard
                label="Router accuracy"
                value={`${Math.round(summary.router_accuracy * 100)}%`}
                sub={`${Math.round(summary.router_accuracy * summary.total)}/${summary.total} correct`}
                delay={0.1}
              />
              <StatCard
                label="Naive (GPT-4o)"
                value={`${Math.round(summary.naive_accuracy * 100)}%`}
                sub={`${Math.round(summary.naive_accuracy * summary.total)}/${summary.total} correct`}
                delay={0.15}
              />
              <StatCard
                label="Cost saved"
                value={`${summary.cost_reduction_pct}%`}
                sub={`$${summary.router_cost_usd.toFixed(4)} vs $${summary.naive_cost_usd.toFixed(4)}`}
                highlight
                delay={0.2}
              />
              <StatCard
                label="Savings factor"
                value={`${(summary.naive_cost_usd / summary.router_cost_usd).toFixed(1)}×`}
                sub="cheaper than GPT-4o"
                highlight
                delay={0.25}
              />
            </div>

            {/* Pareto note */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="mt-4 flex items-start gap-2 rounded-xl border border-white/5 bg-white/5 px-4 py-3 text-xs text-white/40"
            >
              <TrendingDown className="h-3.5 w-3.5 mt-0.5 shrink-0 text-white/30" />
              <span>
                The {Math.round((summary.naive_accuracy - summary.router_accuracy) * 100)}-point accuracy gap is the Pareto trade-off.
                RouteLLM shows the same pattern on MT-Bench — 3.66× cost reduction at minimal accuracy cost.
                Our rules-based classifier trades ~{Math.round((summary.naive_accuracy - summary.router_accuracy) * 100)}% accuracy for {summary.cost_reduction_pct}% cost savings.
              </span>
            </motion.p>
          </Section>
        )}

        {/* Branch distribution */}
        {allQuestions.length > 0 && (
          <Section delay={0.2}>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6 space-y-5">
              <div>
                <h3 className="text-sm font-semibold text-white">Branch distribution</h3>
                <p className="text-xs text-white/40 mt-0.5">Which branch handled each of the 100 MMLU questions</p>
              </div>
              <BranchChart questions={allQuestions} />
            </div>
          </Section>
        )}

        {/* Sample questions table */}
        {questions.length > 0 && (
          <Section delay={0.3}>
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-semibold text-white">Sample questions</h3>
                <p className="text-xs text-white/40 mt-0.5">First 10 of 100 — router branch + correctness vs GPT-4o baseline</p>
              </div>
              <QuestionsTable questions={questions} />
            </div>
          </Section>
        )}
      </div>
    </section>
  );
}
