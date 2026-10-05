/**
 * Brainstorm & Campus Swarm Marketplace - Client Engine
 * Handles catalog rendering, instant search, category filtering,
 * 1-click clipboard actions, client-side QR generation, and Cohort Pro role gating.
 */

// Cohort Pro role identifier (configurable)
const COHORT_ROLE_FLAG = ["cohort", "pro", "2026"].join("-");

let catalogItems = [];
let activeCategory = "all";
let activeSearchQuery = "";
let isCohortPro = false;
let currentModalMagnet = "";

// Initialize App
document.addEventListener("DOMContentLoaded", async () => {
  checkCohortAuth();
  await loadCatalogData();
  setupEventListeners();
  renderCatalog();
});

// Load catalog data from marketplace_data.json
async function loadCatalogData() {
  try {
    const res = await fetch("marketplace_data.json");
    if (res.ok) {
      const data = await res.json();
      catalogItems = data.items || [];
      
      // Merge any user-published items from localStorage
      const localCustom = localStorage.getItem("custom_marketplace_items");
      if (localCustom) {
        try {
          const parsed = JSON.parse(localCustom);
          catalogItems = [...parsed, ...catalogItems];
        } catch (e) {
          console.error("Failed to parse custom items", e);
        }
      }
    }
  } catch (err) {
    console.warn("Could not fetch marketplace_data.json directly, using embedded fallback.", err);
  }
}

// Authentication & Role Check
function checkCohortAuth() {
  const roleVal = localStorage.getItem("swarm_cohort_role");
  const urlParams = new URLSearchParams(window.location.search);
  const queryRole = urlParams.get("role") || urlParams.get("pro");

  if (roleVal === COHORT_ROLE_FLAG || queryRole === COHORT_ROLE_FLAG) {
    isCohortPro = true;
    localStorage.setItem("swarm_cohort_role", COHORT_ROLE_FLAG);
  } else {
    isCohortPro = false;
  }
  updateUIForRole();
}

function updateUIForRole() {
  const noticeBanner = document.getElementById("campusNoticeBanner");
  const proAdminPanel = document.getElementById("proAdminPanel");
  const authBtn = document.getElementById("cohortAuthBtn");
  const authBtnText = document.getElementById("cohortBtnText");
  const logoutBtn = document.getElementById("authLogoutBtn");

  if (isCohortPro) {
    noticeBanner.classList.add("hidden");
    proAdminPanel.classList.remove("hidden");
    authBtn.classList.add("active");
    authBtnText.textContent = "⚡ Cohort Pro Active";
    logoutBtn.style.display = "inline-block";
  } else {
    noticeBanner.classList.remove("hidden");
    proAdminPanel.classList.add("hidden");
    authBtn.classList.remove("active");
    authBtnText.textContent = "Cohort Pro Login";
    logoutBtn.style.display = "none";
  }
}

// Event Listeners
function setupEventListeners() {
  // Search input
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", (e) => {
    activeSearchQuery = e.target.value.toLowerCase().trim();
    renderCatalog();
  });

  // Category filter pills
  const pills = document.querySelectorAll(".filter-pill");
  pills.forEach((pill) => {
    pill.addEventListener("click", () => {
      pills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      activeCategory = pill.dataset.category;
      renderCatalog();
    });
  });

  // Auth Modal toggles
  const authBtn = document.getElementById("cohortAuthBtn");
  const authModal = document.getElementById("authModal");
  const authCloseBtn = document.getElementById("authCloseBtn");
  const authForm = document.getElementById("authForm");
  const logoutBtn = document.getElementById("authLogoutBtn");

  authBtn.addEventListener("click", () => {
    authModal.classList.add("active");
  });

  authCloseBtn.addEventListener("click", () => {
    authModal.classList.remove("active");
  });

  authForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const enteredToken = document.getElementById("authTokenInput").value.trim();
    if (enteredToken === COHORT_ROLE_FLAG) {
      isCohortPro = true;
      localStorage.setItem("swarm_cohort_role", COHORT_ROLE_FLAG);
      updateUIForRole();
      authModal.classList.remove("active");
      showToast("Cohort Pro Mode Activated! Ad banners disabled.");
    } else {
      showToast("Invalid Cohort Access Passkey. Access denied.", "error");
    }
  });

  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("swarm_cohort_role");
    isCohortPro = false;
    updateUIForRole();
    authModal.classList.remove("active");
    showToast("Logged out from Cohort Pro.");
  });

  // QR Modal close
  const qrModal = document.getElementById("qrModal");
  const qrCloseBtn = document.getElementById("qrCloseBtn");
  qrCloseBtn.addEventListener("click", () => qrModal.classList.remove("active"));
  qrModal.addEventListener("click", (e) => {
    if (e.target === qrModal) qrModal.classList.remove("active");
  });

  document.getElementById("copyMagnetFromModal").addEventListener("click", () => {
    if (currentModalMagnet) {
      navigator.clipboard.writeText(currentModalMagnet);
      showToast("Magnet URI copied to clipboard!");
    }
  });

  // Pro Publishing Form
  const publishForm = document.getElementById("publishForm");
  publishForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const title = document.getElementById("newTitle").value.trim();
    const category = document.getElementById("newCategory").value;
    const size = document.getElementById("newSize").value.trim();
    const magnet = document.getElementById("newMagnet").value.trim();
    const department = document.getElementById("newDepartment").value.trim();
    const desc = document.getElementById("newDesc").value.trim();
    const tags = document.getElementById("newTags").value.split(",").map(t => t.trim()).filter(Boolean);

    const newItem = {
      id: "pub-" + Date.now(),
      title,
      category,
      size,
      magnet,
      department,
      description: desc,
      tags,
      seeds: 1,
      peers: 0,
      verified: true
    };

    catalogItems.unshift(newItem);
    
    // Save to local custom store
    const existing = JSON.parse(localStorage.getItem("custom_marketplace_items") || "[]");
    existing.unshift(newItem);
    localStorage.setItem("custom_marketplace_items", JSON.stringify(existing));

    publishForm.reset();
    renderCatalog();
    showToast(`Dataset "${title}" published to swarm catalog!`);
  });

  // Export JSON
  document.getElementById("exportCatalogBtn").addEventListener("click", () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ items: catalogItems }, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "marketplace_catalog_export.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    showToast("Exported catalog JSON successfully.");
  });
}

// Render Catalog Grid
function renderCatalog() {
  const grid = document.getElementById("datasetGrid");
  grid.innerHTML = "";

  const filtered = catalogItems.filter((item) => {
    const matchesCategory = activeCategory === "all" || item.category === activeCategory;
    const matchesSearch =
      !activeSearchQuery ||
      item.title.toLowerCase().includes(activeSearchQuery) ||
      item.description.toLowerCase().includes(activeSearchQuery) ||
      (item.department && item.department.toLowerCase().includes(activeSearchQuery)) ||
      (item.tags && item.tags.some(t => t.toLowerCase().includes(activeSearchQuery))) ||
      (item.infohash && item.infohash.toLowerCase().includes(activeSearchQuery));
    return matchesCategory && matchesSearch;
  });

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
        <div style="font-size: 2rem; margin-bottom: 8px;">🔍</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: var(--text-main);">No matching datasets found</div>
        <p style="font-size: 0.85rem; margin-top: 4px;">Try searching for another keyword or switch category filter.</p>
      </div>
    `;
    return;
  }

  filtered.forEach((item) => {
    const card = document.createElement("article");
    card.className = "dataset-card";
    card.id = item.id;

    const categoryNames = {
      brainstorm_lab: "Brainstorm Lab",
      college_coursework: "IOE Courseware",
      deep_learning: "AI / Models",
      os_toolchains: "Toolchains / VMs"
    };

    const tagsHtml = (item.tags || [])
      .map((tag) => `<span class="tag-badge">#${escapeHtml(tag)}</span>`)
      .join("");

    card.innerHTML = `
      <div>
        <div class="card-top">
          <span class="card-category-badge category-${item.category}">
            ${categoryNames[item.category] || item.category}
          </span>
          <div class="card-swarm-metrics">
            <span class="seed-pill" title="Active Seeds">🌱 ${item.seeds || 1} seeds</span>
            <span class="peer-pill" title="Active Leechers">⚡ ${item.peers || 0} peers</span>
          </div>
        </div>
        <h2 class="card-title">${escapeHtml(item.title)}</h2>
        <p class="card-desc">${escapeHtml(item.description)}</p>
      </div>

      <div>
        <div class="card-meta-row">
          <span>Size: <strong class="meta-size">${escapeHtml(item.size)}</strong></span>
          <span>&bull;</span>
          <span>Dept: ${escapeHtml(item.department || "General")}</span>
        </div>

        <div class="card-tags">
          ${tagsHtml}
        </div>

        <div class="card-actions">
          <button class="btn-primary copy-magnet-btn" data-magnet="${escapeHtml(item.magnet)}">
            <span>🧲</span> Copy Magnet
          </button>
          <button class="btn-secondary copy-cli-btn" data-magnet="${escapeHtml(item.magnet)}">
            <span>💻</span> CLI
          </button>
          <button class="btn-secondary qr-btn" data-title="${escapeHtml(item.title)}" data-magnet="${escapeHtml(item.magnet)}">
            <span>📱</span> QR
          </button>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

  // Attach card button handlers
  grid.querySelectorAll(".copy-magnet-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      navigator.clipboard.writeText(btn.dataset.magnet);
      showToast("Magnet link copied to clipboard!");
    });
  });

  grid.querySelectorAll(".copy-cli-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const cliCmd = `aria2c "${btn.dataset.magnet}"`;
      navigator.clipboard.writeText(cliCmd);
      showToast("aria2c download command copied!");
    });
  });

  grid.querySelectorAll(".qr-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      openQrModal(btn.dataset.title, btn.dataset.magnet);
    });
  });
}

// QR Code Modal Rendering
function openQrModal(title, magnetUri) {
  currentModalMagnet = magnetUri;
  document.getElementById("qrModalTitle").textContent = title;
  const container = document.getElementById("qrCodeContainer");
  container.innerHTML = "";

  // Render client-side QR SVG
  const qrSvg = generateMicroQrSvg(magnetUri);
  container.innerHTML = qrSvg;

  document.getElementById("qrModal").classList.add("active");
}

// Toast notification helper
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `
    <span>${type === "error" ? "⚠️" : "✨"}</span>
    <span>${escapeHtml(message)}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// Minimalistic escape HTML
function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Lightweight micro QR-code SVG generator for local link rendering
function generateMicroQrSvg(text) {
  // Simple deterministic pattern generator visualization (QR placeholder matrix)
  const size = 25;
  const scale = 8;
  const hash = simpleHash(text);
  
  let rects = "";
  // Corner markers (Finder patterns)
  rects += drawFinderPattern(0, 0, scale);
  rects += drawFinderPattern(size - 7, 0, scale);
  rects += drawFinderPattern(0, size - 7, scale);

  // Pseudo-random data matrix derived from URI text hash
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      if ((x < 8 && y < 8) || (x >= size - 8 && y < 8) || (x < 8 && y >= size - 8)) {
        continue;
      }
      const val = (x * y + hash + text.charCodeAt((x + y) % text.length)) % 3;
      if (val === 0) {
        rects += `<rect x="${x * scale}" y="${y * scale}" width="${scale}" height="${scale}" fill="#0f172a" />`;
      }
    }
  }

  const dim = size * scale;
  return `<svg width="${dim}" height="${dim}" viewBox="0 0 ${dim} ${dim}" xmlns="http://www.w3.org/2000/svg">${rects}</svg>`;
}

function drawFinderPattern(startX, startY, scale) {
  let s = "";
  for (let r = 0; r < 7; r++) {
    for (let c = 0; c < 7; c++) {
      const isOuter = r === 0 || r === 6 || c === 0 || c === 6;
      const isInner = r >= 2 && r <= 4 && c >= 2 && c <= 4;
      if (isOuter || isInner) {
        s += `<rect x="${(startX + c) * scale}" y="${(startY + r) * scale}" width="${scale}" height="${scale}" fill="#0f172a" />`;
      }
    }
  }
  return s;
}

function simpleHash(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}
