// content.js — runs in page context. Watches DOM for new text nodes,
// flags naive "question-like" text (ends in '?'), sends it to the
// background worker for answering, and renders the result inline.

const QUESTION_RE = /[^.!?]{8,300}\?/g; // naive: 8-300 chars ending in '?'
const seen = new Set(); // dedupe: don't re-query identical text repeatedly
const debounceTimers = new Map();

function extractQuestions(root) {
  const text = root.innerText || root.textContent || "";
  const matches = text.match(QUESTION_RE);
  if (!matches) return [];
  return matches
    .map((m) => m.trim())
    .filter((m) => m.length > 0 && !seen.has(m));
}

function findTextNodeForMatch(root, matchText) {
  // Locate an element whose innerText contains the match, so the overlay
  // can be anchored near it. Walk shallow-to-deep, prefer smallest match.
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, {
    acceptNode(node) {
      const t = node.innerText || "";
      return t.includes(matchText) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
    },
  });
  let best = null;
  let node;
  while ((node = walker.nextNode())) {
    best = node; // keep descending to the most specific match
  }
  return best;
}

function showOverlay(anchorEl, question, answerText, isLoading) {
  let overlay = anchorEl.__screenQaOverlay;
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.className = "screen-qa-overlay";
    document.body.appendChild(overlay);
    anchorEl.__screenQaOverlay = overlay;
  }

  const rect = anchorEl.getBoundingClientRect();
  overlay.style.top = `${window.scrollY + rect.bottom + 4}px`;
  overlay.style.left = `${window.scrollX + rect.left}px`;

  if (isLoading) {
    overlay.textContent = "Thinking…";
    overlay.classList.add("screen-qa-loading");
  } else {
    overlay.classList.remove("screen-qa-loading");
    overlay.textContent = answerText;
  }
}

function handleQuestion(question, anchorEl) {
  seen.add(question);
  showOverlay(anchorEl, question, "", true);

  chrome.runtime.sendMessage(
    { type: "ANSWER_QUESTION", question },
    (response) => {
      if (chrome.runtime.lastError) {
        showOverlay(anchorEl, question, `Error: ${chrome.runtime.lastError.message}`, false);
        return;
      }
      if (response?.error) {
        showOverlay(anchorEl, question, `Error: ${response.error}`, false);
        return;
      }
      showOverlay(anchorEl, question, response?.answer || "(no answer)", false);
    }
  );
}

function scan() {
  const questions = extractQuestions(document.body);
  for (const q of questions) {
    const anchor = findTextNodeForMatch(document.body, q) || document.body;
    handleQuestion(q, anchor);
  }
}

function debouncedScan() {
  clearTimeout(debouncedScan._t);
  debouncedScan._t = setTimeout(scan, 500);
}

// Initial pass
debouncedScan();

// Continuous watching via content-script MutationObserver — not subject to
// MV3 service-worker idle kill, since this runs in the page context.
const observer = new MutationObserver(() => {
  debouncedScan();
});
observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: true,
});
