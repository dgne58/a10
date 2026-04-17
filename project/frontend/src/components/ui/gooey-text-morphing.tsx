import { useEffect, useRef } from "react";
import { cn } from "@/lib/utils";

interface GooeyTextProps {
  texts: string[];
  morphTime?: number;
  cooldownTime?: number;
  className?: string;
  textClassName?: string;
}

export function GooeyText({
  texts,
  morphTime = 1.5,
  cooldownTime = 2.0,
  className,
  textClassName,
}: GooeyTextProps) {
  const text1Ref = useRef<HTMLSpanElement>(null);
  const text2Ref = useRef<HTMLSpanElement>(null);

  const indexRef = useRef(0);
  const morphRef = useRef(0);
  const cooldownRef = useRef(cooldownTime);
  const timeRef = useRef(Date.now());
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (texts.length < 2) return;

    const t1 = text1Ref.current!;
    const t2 = text2Ref.current!;

    function show(el: HTMLSpanElement) {
      el.style.opacity = "1";
      el.style.filter = "blur(0px)";
    }
    function hide(el: HTMLSpanElement) {
      el.style.opacity = "0";
      el.style.filter = "blur(8px)";
    }

    t1.textContent = texts[0];
    t2.textContent = texts[1];
    show(t1);
    hide(t2);

    function tick() {
      rafRef.current = requestAnimationFrame(tick);

      const now = Date.now();
      const dt = (now - timeRef.current) / 1000;
      timeRef.current = now;

      cooldownRef.current -= dt;
      if (cooldownRef.current > 0) return;

      morphRef.current += dt;
      const f = Math.min(morphRef.current / morphTime, 1);

      // text1 blurs out, text2 blurs in
      t1.style.opacity = `${1 - f}`;
      t1.style.filter = `blur(${f * 8}px)`;
      t2.style.opacity = `${f}`;
      t2.style.filter = `blur(${(1 - f) * 8}px)`;

      if (f >= 1) {
        const next = (indexRef.current + 1) % texts.length;
        indexRef.current = next;
        t1.textContent = texts[next];
        t2.textContent = texts[(next + 1) % texts.length];
        show(t1);
        hide(t2);
        morphRef.current = 0;
        cooldownRef.current = cooldownTime;
      }
    }

    timeRef.current = Date.now();
    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)}>
      <span className="relative inline-block">
        <span ref={text1Ref} className={cn("select-none", textClassName)} />
        <span
          ref={text2Ref}
          className={cn("absolute inset-0 select-none", textClassName)}
          aria-hidden="true"
        />
      </span>
    </div>
  );
}
