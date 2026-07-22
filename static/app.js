const API = "";  // ten sam host co frontend
const TOKEN_KEY = "recipe_token";

const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

// ============== AUTH ==============
function getToken() { return localStorage.getItem(TOKEN_KEY); }
function setToken(t) { localStorage.setItem(TOKEN_KEY, t); }
function clearToken() { localStorage.removeItem(TOKEN_KEY); }

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API}${path}`, { ...options, headers });
  if (res.status === 401) {
    clearToken();
    showAuth();
    throw new Error("Sesja wygasla");
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Blad" }));
    throw new Error(err.detail || "Blad");
  }
  return res.json();
}

function showAuth() {
  $("#app-view").classList.add("hidden");
  $("#auth-view").classList.remove("hidden");
  $("#auth-error").textContent = "";
}

function showApp() {
  $("#auth-view").classList.add("hidden");
  $("#app-view").classList.remove("hidden");
  showCategoryView();
}

function showCategoryView() {
  $("#category-view").classList.remove("hidden");
  $("#history-view").classList.add("hidden");
  $("#chat-view").classList.add("hidden");
}

function showHistoryView() {
  $("#category-view").classList.add("hidden");
  $("#history-view").classList.remove("hidden");
  $("#chat-view").classList.add("hidden");
}

function showChatView() {
  $("#category-view").classList.add("hidden");
  $("#history-view").classList.add("hidden");
  $("#chat-view").classList.remove("hidden");
}

// Taby logowanie / rejestracja
$$(".tab").forEach((t) => {
  t.addEventListener("click", () => {
    $$(".tab").forEach((x) => x.classList.remove("active"));
    t.classList.add("active");
    const target = t.dataset.tab;
    $("#login-form").classList.toggle("hidden", target !== "login");
    $("#register-form").classList.toggle("hidden", target !== "register");
    $("#auth-error").textContent = "";
  });
});

$("#login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  try {
    const body = new URLSearchParams({
      username: fd.get("username"),
      password: fd.get("password"),
    });
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Blad logowania");
    }
    const data = await res.json();
    setToken(data.access_token);
    await afterLogin();
  } catch (err) {
    $("#auth-error").textContent = err.message;
  }
});

$("#register-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const payload = {
    email: fd.get("email"),
    username: fd.get("username"),
    password: fd.get("password"),
  };
  try {
    const regRes = await fetch(`${API}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!regRes.ok) {
      const err = await regRes.json().catch(() => ({}));
      throw new Error(err.detail || "Blad rejestracji");
    }
    // Automatyczne logowanie po rejestracji
    const body = new URLSearchParams({ username: payload.username, password: payload.password });
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Blad logowania po rejestracji");
    }
    const data = await res.json();
    setToken(data.access_token);
    await afterLogin();
  } catch (err) {
    $("#auth-error").textContent = err.message;
  }
});

$("#logout-btn").addEventListener("click", () => {
  clearToken();
  showAuth();
});

async function afterLogin() {
  const me = await api("/auth/me");
  $("#user-greeting").textContent = `Hej, ${me.username}!`;
  showApp();
}

// ============== KATEGORIE -> CHAT ==============
$$(".cat-btn").forEach((btn) => {
  btn.addEventListener("click", () => openChat(btn.dataset.category));
});

$("#back-btn").addEventListener("click", () => {
  showCategoryView();
});

$("#new-chat-btn").addEventListener("click", () => {
  state.currentConversationId = null;
  $("#messages").innerHTML = "";
  $("#chat-input").focus();
});

let state = { category: null, currentConversationId: null };

async function openChat(category) {
  state.category = category;
  state.currentConversationId = null;
  showChatView();
  $("#chat-title").textContent = categoryEmoji(category) + " " + capitalize(category);

  // Wczytaj ostatnia konwersacje dla tej kategorii
  try {
    const convs = await api("/conversations/");
    const last = convs.find((c) => c.category === category);
    if (last) {
      state.currentConversationId = last.id;
      const msgs = await api(`/chat/${last.id}/messages`);
      $("#messages").innerHTML = "";
      msgs.forEach((m) => appendMessage(m.role, m.content, false));
    } else {
      $("#messages").innerHTML = "";
    }
  } catch (err) {
    console.error(err);
  }
  $("#chat-input").focus();
}

// Otwiera konkretna, wybrana z historii konwersacje (niezaleznie ktora jest "ostatnia")
async function openConversationById(conversationId, category) {
  state.category = category;
  state.currentConversationId = conversationId;
  showChatView();
  $("#chat-title").textContent = categoryEmoji(category) + " " + capitalize(category);
  $("#messages").innerHTML = "";
  try {
    const msgs = await api(`/chat/${conversationId}/messages`);
    msgs.forEach((m) => appendMessage(m.role, m.content, false));
  } catch (err) {
    console.error(err);
  }
  $("#chat-input").focus();
}

function categoryEmoji(c) {
  return { sniadanie: "🥐", obiad: "🍲", kolacja: "🥗" }[c] || "🍽️";
}
function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

function appendMessage(role, content, animate = true) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = content;
  $("#messages").appendChild(div);
  $("#messages").scrollTop = $("#messages").scrollHeight;
  return div;
}

$("#chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = $("#chat-input");
  const text = input.value.trim();
  if (!text) return;

  appendMessage("user", text);
  input.value = "";
  input.disabled = true;
  $('button[type="submit"]').disabled = true;

  const thinking = appendMessage("assistant", "Myślę...", true);
  thinking.classList.add("thinking");

  try {
    const res = await api("/chat/send", {
      method: "POST",
      body: JSON.stringify({
        category: state.category,
        message: text,
        conversation_id: state.currentConversationId,
      }),
    });
    thinking.classList.remove("thinking");
    thinking.textContent = res.ai_message;
    state.currentConversationId = res.conversation_id;
  } catch (err) {
    thinking.classList.remove("thinking");
    thinking.textContent = "❌ " + err.message;
  } finally {
    input.disabled = false;
    $('button[type="submit"]').disabled = false;
    input.focus();
  }
});

// ============== HISTORIA ==============
$("#history-btn").addEventListener("click", openHistory);
$("#history-back-btn").addEventListener("click", () => {
  showCategoryView();
});

async function openHistory() {
  showHistoryView();
  const list = $("#history-list");
  list.innerHTML = '<p class="history-empty">Wczytywanie...</p>';

  try {
    const convs = await api("/conversations/");
    if (!convs.length) {
      list.innerHTML = '<p class="history-empty">Nie masz jeszcze zadnych rozmow. Wybierz kategorie i zacznij czat!</p>';
      return;
    }
    list.innerHTML = "";
    convs.forEach((c) => {
      const item = document.createElement("div");
      item.className = "history-item";
      item.innerHTML = `
        <span class="history-item-category">${categoryEmoji(c.category)} ${capitalize(c.category)}</span>
        <span class="history-item-date">${formatDate(c.updated_at)}</span>
      `;
      item.addEventListener("click", () => openConversationById(c.id, c.category));
      list.appendChild(item);
    });
  } catch (err) {
    list.innerHTML = `<p class="history-empty">❌ ${err.message}</p>`;
  }
}

function formatDate(isoString) {
  const d = new Date(isoString);
  return d.toLocaleString("pl-PL", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// ============== INIT ==============
if (getToken()) {
  api("/auth/me").then(afterLogin).catch(showAuth);
} else {
  showAuth();
}