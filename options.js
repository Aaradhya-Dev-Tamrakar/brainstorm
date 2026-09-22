const input = document.getElementById("apiKey");
const status = document.getElementById("status");

chrome.storage.local.get("geminiApiKey", ({ geminiApiKey }) => {
  if (geminiApiKey) input.value = geminiApiKey;
});

document.getElementById("save").addEventListener("click", () => {
  const value = input.value.trim();
  chrome.storage.local.set({ geminiApiKey: value }, () => {
    status.textContent = "Saved.";
    setTimeout(() => (status.textContent = ""), 1500);
  });
});
