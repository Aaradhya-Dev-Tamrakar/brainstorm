// background.js — MV3 service worker. Stateless request relay: receives a
// question from a content script, calls Gemini Flash with the stored API
// key, and returns the answer. Holds no persistent state itself — all
// "continuous" behavior lives in the content script's MutationObserver.

const GEMINI_ENDPOINT =
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent";

async function getApiKey() {
  const { geminiApiKey } = await chrome.storage.local.get("geminiApiKey");
  return geminiApiKey || null;
}

async function askGemini(question, apiKey) {
  const res = await fetch(`${GEMINI_ENDPOINT}?key=${apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: question }] }],
    }),
  });

  if (!res.ok) {
    const errBody = await res.text().catch(() => "");
    throw new Error(`Gemini API ${res.status}: ${errBody.slice(0, 200)}`);
  }

  const data = await res.json();
  const answer = data?.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!answer) throw new Error("No answer in Gemini response");
  return answer;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type !== "ANSWER_QUESTION") return false;

  (async () => {
    try {
      const apiKey = await getApiKey();
      if (!apiKey) {
        sendResponse({ error: "No API key set. Open the extension options page." });
        return;
      }
      const answer = await askGemini(message.question, apiKey);
      sendResponse({ answer });
    } catch (err) {
      sendResponse({ error: err.message || String(err) });
    }
  })();

  return true; // keep the message channel open for the async sendResponse
});
