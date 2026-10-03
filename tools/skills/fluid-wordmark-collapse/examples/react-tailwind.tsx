import React, { useState, useEffect } from 'react';

interface WordmarkProps {
  words?: Array<{ initial: string; rest: string }>;
  dot?: string;
  href?: string;
  ariaLabel?: string;
}

export const FluidWordmark: React.FC<WordmarkProps> = ({
  words = [
    { initial: 'A', rest: 'aradhya' },
    { initial: 'D', rest: 'ev' },
    { initial: 'T', rest: 'amrakar' },
  ],
  dot = '.',
  href = '/',
  ariaLabel = 'Aaradhya Dev Tamrakar',
}) => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    let ticking = false;
    const handleScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          setScrolled(window.scrollY > 50);
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 grid grid-cols-[250px_1fr_max-content] items-center gap-x-6 px-12 transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] ${
        scrolled
          ? 'py-3.5 bg-neutral-950/90 backdrop-blur-xl border-b border-neutral-800/60 shadow-lg'
          : 'py-7 bg-transparent border-b border-transparent'
      }`}
    >
      {/* Zone 1: Dedicated 250px Logo Slot */}
      <a
        href={href}
        aria-label={ariaLabel}
        className="group w-[250px] min-w-[250px] inline-flex items-center no-underline select-none"
      >
        <span
          aria-hidden="true"
          className={`inline-flex items-baseline font-serif transition-[gap] duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] ${
            scrolled ? 'gap-[0.04em] group-hover:gap-[0.28em]' : 'gap-[0.28em]'
          }`}
        >
          {words.map((w, i) => (
            <span key={i} className="inline-flex items-baseline">
              <span className="text-neutral-100 text-lg font-medium tracking-wide">
                {w.initial}
              </span>
              <span
                className={`inline-block overflow-hidden whitespace-nowrap align-baseline text-neutral-400 text-lg font-normal origin-left transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] will-change-[max-width,opacity,transform] ${
                  scrolled
                    ? 'max-w-0 opacity-0 -translate-x-1 scale-x-75 pointer-events-none group-hover:max-w-[140px] group-hover:opacity-95 group-hover:translate-x-0 group-hover:scale-x-100 group-hover:pointer-events-auto'
                    : 'max-w-[140px] opacity-90 translate-x-0 scale-x-100'
                }`}
              >
                {w.rest}
              </span>
            </span>
          ))}
          {dot && (
            <span className="text-amber-500 text-lg font-semibold ml-px">
              {dot}
            </span>
          )}
        </span>
      </a>

      {/* Zone 2: Navigation Links (Stationary) */}
      <nav className="flex items-center gap-x-2 justify-start ml-2">
        {['Work', 'Background', 'About', 'Build Log'].map((item) => (
          <a
            key={item}
            href={`#${item.toLowerCase().replace(' ', '-')}`}
            className="font-mono text-xs uppercase tracking-widest text-neutral-300 hover:text-white px-3.5 py-2 rounded transition-colors hover:bg-white/5"
          >
            {item}
          </a>
        ))}
      </nav>

      {/* Zone 3: Right Utility Controls (Stationary) */}
      <div className="flex items-center gap-x-3 justify-self-end">
        <a
          href="#connect"
          className="font-mono text-xs uppercase tracking-widest text-amber-400 border border-amber-500/80 px-4 h-9.5 inline-flex items-center rounded-sm hover:bg-amber-500 hover:text-black transition-all shadow-[0_0_12px_rgba(212,168,90,0.3)]"
        >
          Connect
        </a>
      </div>
    </header>
  );
};

export default FluidWordmark;
