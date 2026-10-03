/**
 * ============================================================================
 * Fluid Wordmark Navbar — Client Script & Kinematics Engine
 * ============================================================================
 * Handles passive scroll event detection via requestAnimationFrame,
 * manages the collapsed/expanded states, and provides optional dynamic
 * syllable decomposition for plain text brand names.
 */

(function () {
  'use strict';

  // Configurable thresholds
  const SCROLL_THRESHOLD = 50; // px of scroll before collapsing
  const NAV_SELECTOR = '#nav';
  const WORDMARK_SELECTOR = '.nav-logo';

  /**
   * Initializes passive scroll listening with requestAnimationFrame throttling.
   */
  function initScrollWatcher() {
    const nav = document.querySelector(NAV_SELECTOR);
    if (!nav) return;

    let ticking = false;
    let isScrolled = false;

    function updateNavState() {
      const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
      const shouldBeScrolled = currentScroll > SCROLL_THRESHOLD;

      if (shouldBeScrolled !== isScrolled) {
        isScrolled = shouldBeScrolled;
        if (isScrolled) {
          nav.classList.add('scrolled');
        } else {
          nav.classList.remove('scrolled');
        }
      }

      ticking = false;
    }

    window.addEventListener(
      'scroll',
      function () {
        if (!ticking) {
          window.requestAnimationFrame(updateNavState);
          ticking = true;
        }
      },
      { passive: true }
    );

    // Initial check on load
    updateNavState();
  }

  /**
   * Helper utility to dynamically decompose a plain-text brand string into
   * root initials and collapsible syllables.
   *
   * @param {HTMLElement} containerElement Target DOM container
   * @param {string} fullName e.g. "Aaradhya Dev Tamrakar"
   * @param {string} dotChar Punctuation char, e.g. "."
   */
  function renderDecomposedWordmark(containerElement, fullName, dotChar = '.') {
    if (!containerElement || !fullName) return;

    const words = fullName.trim().split(/\s+/);
    containerElement.setAttribute('aria-label', fullName);

    const brandSpan = document.createElement('span');
    brandSpan.className = 'nav-brand-text';

    words.forEach((word) => {
      const wordSpan = document.createElement('span');
      wordSpan.className = 'nav-word';
      wordSpan.dataset.word = word;

      const initialSpan = document.createElement('span');
      initialSpan.className = 'nav-initial';
      initialSpan.textContent = word.charAt(0);

      const restSpan = document.createElement('span');
      restSpan.className = 'nav-rest';
      restSpan.textContent = word.slice(1);

      wordSpan.appendChild(initialSpan);
      wordSpan.appendChild(restSpan);
      brandSpan.appendChild(wordSpan);
    });

    if (dotChar) {
      const dotSpan = document.createElement('span');
      dotSpan.className = 'nav-dot';
      dotSpan.setAttribute('aria-hidden', 'true');
      dotSpan.textContent = dotChar;
      brandSpan.appendChild(dotSpan);
    }

    containerElement.innerHTML = '';
    containerElement.appendChild(brandSpan);
  }

  // Auto-init on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollWatcher);
  } else {
    initScrollWatcher();
  }

  // Export helper for module environments or manual setup
  if (typeof window !== 'undefined') {
    window.FluidWordmarkNavbar = {
      initScrollWatcher,
      renderDecomposedWordmark,
    };
  }
})();
