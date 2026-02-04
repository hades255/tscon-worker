# =============================================================================
# Auto-bot configuration – edit this file to change behavior
# =============================================================================

# --- Startup ---
START_DELAY_SEC = 20.0  # Seconds to wait before first action

# --- Delays between actions (random in this range) ---
DELAY_MIN_SEC = 0.5
DELAY_MAX_SEC = 2.0

# --- Process names (case-insensitive match on exe name) ---
VS_CODE_PROCESS_NAMES = ["Code.exe"]
CHROME_PROCESS_NAMES = ["chrome.exe"]

# --- VS Code: mouse move region (from_x, from_y, to_x, to_y) in pixels ---
VS_CODE_REGION = (400, 150, 800, 600)

# --- Chrome: mouse move region (min_x, min_y, max_x, max_y) in pixels ---
CHROME_REGION = (100, 100, 600, 600)

# --- After right-click: move this many pixels left, then left-click to close menu ---
CONTEXT_MENU_OFFSET_LEFT_PX = 10

VS_CODE_FILE_NAMES = ["config", "script", "header"]
# --- Text options for VS Code: list of lines; bot picks 1 to N random lines and types them ---
VS_CODE_TEXTS_LINES_MIN = 1
VS_CODE_TEXTS_LINES_MAX = 20
VS_CODE_TEXTS = (
    """
function renderBookmarksBar(bookmarkRoot) {
const bar = document.getElementById("bookmark-bar");
if (!bar) return;

bar.innerHTML = "";

const rootFolder = bookmarkRoot;
const topItems = (rootFolder.children || [])
.slice()
.sort((a, b) => (a.index ?? 0) - (b.index ?? 0));

const itemsHost = document.createElement("div");
itemsHost.style.display = "flex";
itemsHost.style.alignItems = "center";
itemsHost.style.gap = "2px";
itemsHost.style.minWidth = "0";
itemsHost.style.overflow = "hidden";
itemsHost.style.flex = "1 1 auto";
bar.appendChild(itemsHost);

const overflowBtn = document.createElement("button");
overflowBtn.className = "bb-item bb-overflow";
overflowBtn.type = "button";
overflowBtn.title = "More";
overflowBtn.innerHTML = `<span class="bb-title">»</span>`;
overflowBtn.style.display = "none";
bar.appendChild(overflowBtn);

let overflowItems = [];
let currentMenu = null;

const closeMenu = () => {
document.querySelectorAll(".bb-menu").forEach((el) => el.remove());
currentMenu = null;
};

document.addEventListener("click", (e) => {
if (
currentMenu &&
!currentMenu.contains(e.target) &&
e.target !== overflowBtn
) {
closeMenu();
}
});

window.addEventListener("resize", () => {
closeMenu();
layout();
});

function faviconForUrl(url) {
try {
const u = new URL(url);
if (u.protocol === "http:" || u.protocol === "https:") {
return `https://www.google.com/s2/favicons?domain=${encodeURIComponent(
u.hostname
)}&sz=16`;
}
} catch {}
return (
"data:image/svg+xml;utf8," +
encodeURIComponent(`
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">
<rect width="16" height="16" rx="3" ry="3" fill="#cbd5e1"/>
<text x="8" y="11" text-anchor="middle" font-size="9" fill="#334155">★</text>
</svg>
`)
);
}

function makeBookmarkEl(node) {
const a = document.createElement("a");
a.className = "bb-item";
a.href = node.url;
a.title = node.title || node.url;

// const img = document.createElement("img");
// img.className = "bb-favicon";
// img.alt = "";
// img.referrerPolicy = "no-referrer";
// img.src = faviconForUrl(node.url);
// img.onerror = () => {
//   img.src = faviconForUrl("");
// };

const title = document.createElement("span");
title.className = "bb-title";
title.textContent = node.title || node.url;

// a.appendChild(img);
a.appendChild(title);

a.addEventListener("click", (e) => {
closeMenu();
});

return a;
}

function makeFolderEl(folderNode) {
const btn = document.createElement("button");
btn.className = "bb-item";
btn.type = "button";
btn.title = folderNode.title || "Folder";

const icon = document.createElement("span");
icon.className = "bb-folder-icon";
icon.textContent = "📁";

const title = document.createElement("span");
title.className = "bb-title";
title.textContent = folderNode.title || "Folder";

const caret = document.createElement("span");
caret.className = "bb-folder-caret";
caret.textContent = "▾";

btn.appendChild(icon);
btn.appendChild(title);
btn.appendChild(caret);

btn.addEventListener("click", (e) => {
e.stopPropagation();
toggleMenuForFolder(btn, folderNode);
});

return btn;
}

function toggleMenuForFolder(anchorEl, folderNode) {
if (currentMenu) {
if (currentMenu.__anchor === anchorEl) {
closeMenu();
return;
}
closeMenu();
}
currentMenu = buildMenu(folderNode.children || [], anchorEl);
currentMenu.__anchor = anchorEl;
document.body.appendChild(currentMenu);

positionMenu(currentMenu, anchorEl);
}

function positionMenu(menuEl, anchorEl) {
const rect = anchorEl.getBoundingClientRect();
const margin = 6;

let left = rect.left;
let top = rect.bottom + margin;

const vw = window.innerWidth;
const vh = window.innerHeight;

menuEl.style.left = `${Math.round(left)}px`;
menuEl.style.top = "0px";
menuEl.style.visibility = "hidden";
menuEl.style.display = "block";
const mrect = menuEl.getBoundingClientRect();
menuEl.style.visibility = "";

if (left + mrect.width > vw - margin)
left = Math.max(margin, vw - margin - mrect.width);
if (top + mrect.height > vh - margin) {
const above = rect.top - margin - mrect.height;
top =
above >= margin ? above : Math.max(margin, vh - margin - mrect.height);
}

menuEl.style.left = `${Math.round(left)}px`;
menuEl.style.top = `${Math.round(top)}px`;
}

function buildMenu(children, anchorEl) {
const menu = document.createElement("div");
menu.className = "bb-menu";

const sorted = children
.slice()
.sort((a, b) => (a.index ?? 0) - (b.index ?? 0));

for (const node of sorted) {
if (node.url) {
menu.appendChild(makeBookmarkEl(node));
} else if (node.children) {
const row = document.createElement("button");
row.type = "button";
row.className = "bb-item";
row.title = node.title || "Folder";

const icon = document.createElement("span");
icon.className = "bb-folder-icon";
icon.textContent = "📁";

const title = document.createElement("span");
title.className = "bb-title";
title.textContent = node.title || "Folder";

const caret = document.createElement("span");
caret.className = "bb-folder-caret";
caret.textContent = "▸";

row.appendChild(icon);
row.appendChild(title);
row.appendChild(caret);

row.addEventListener("click", (e) => {
e.stopPropagation();

closeNested(menu);
const nested = buildMenu(node.children || [], row);
nested.__nested = true;
nested.__parentMenu = menu;
document.body.appendChild(nested);
positionNestedMenu(nested, row);
menu.__nestedMenu = nested;
});

menu.appendChild(row);
}
}

const escHandler = (ev) => {
if (ev.key === "Escape") {
ev.stopPropagation();
closeMenu();
document.removeEventListener("keydown", escHandler, true);
}
};
document.addEventListener("keydown", escHandler, true);

menu.addEventListener("click", (e) => e.stopPropagation());

return menu;
}

function closeNested(parentMenu) {
const nested = parentMenu?.__nestedMenu;
if (nested) {
nested.remove();
parentMenu.__nestedMenu = null;
}
}

function positionNestedMenu(nestedMenu, rowEl) {
const rect = rowEl.getBoundingClientRect();
const margin = 6;
let left = rect.right + margin;
let top = rect.top;

nestedMenu.style.left = `${Math.round(left)}px`;
nestedMenu.style.top = `${Math.round(top)}px`;
}

const rendered = topItems
.map((node) => {
if (node.url) return makeBookmarkEl(node);
if (node.children) return makeFolderEl(node);
return null;
})
.filter(Boolean);

for (const el of rendered) itemsHost.appendChild(el);

overflowBtn.addEventListener("click", (e) => {
e.stopPropagation();
if (currentMenu && currentMenu.__anchor === overflowBtn) {
closeMenu();
return;
}
closeMenu();
currentMenu = buildMenu(overflowItems, overflowBtn);
currentMenu.__anchor = overflowBtn;
document.body.appendChild(currentMenu);
positionMenu(currentMenu, overflowBtn);
});

function layout() {
overflowItems = [];
overflowBtn.style.display = "none";
for (const el of rendered) el.style.display = "";

const barRect = bar.getBoundingClientRect();
const maxRight = barRect.right - 6;

if (itemsHost.getBoundingClientRect().right <= maxRight) return;

overflowBtn.style.display = "";

const overflowBtnRect = overflowBtn.getBoundingClientRect();
const reserved = overflowBtnRect.width || 40;
const maxRightWithOverflow = maxRight - reserved;

for (let i = rendered.length - 1; i >= 0; i--) {
const el = rendered[i];
const r = el.getBoundingClientRect();

if (r.right > maxRightWithOverflow) {
el.style.display = "none";
overflowItems.unshift(topItems[i]);
}

if (itemsHost.getBoundingClientRect().right <= maxRightWithOverflow)
break;
}

if (overflowItems.length === 0) overflowBtn.style.display = "none";
}

requestAnimationFrame(layout);
}

function initBookmarkBar() {
chrome.bookmarks.getTree((tree) => {
// On most Chrome profiles: tree[0].children includes:
// "Bookmarks bar", "Other bookmarks", "Mobile bookmarks"
const root = tree[0];
const bookmarksBar = root.children?.find(
(n) => n.title === "Bookmarks bar"
);
renderBookmarksBar(bookmarksBar);
});
}

    """
).split("\n")

# --- Mouse: smooth move ---
SMOOTH_MOVE_DURATION_MIN = 0.5
SMOOTH_MOVE_DURATION_MAX = 1.5
SMOOTH_MOVE_STEPS = 80

# --- Scroll: wheel delta (positive = up, negative = down); amount randomized ---
SCROLL_DELTA_BASE = 120
SCROLL_MULTIPLIER_MIN = 1
SCROLL_MULTIPLIER_MAX = 4

# --- Typing (VS Code) ---
TYPING_DELAY_PER_CHAR = 0.1

# --- Alt+Tab: hold Alt and press Tab N times (random in this range) ---
ALT_TAB_COUNT_MIN = 1
ALT_TAB_COUNT_MAX = 3

# --- Ctrl+Tab: hold Ctrl and press Tab N times (random in this range) ---
CTRL_TAB_COUNT_MIN = 1
CTRL_TAB_COUNT_MAX = 3

# --- Run control: on/off and mode (key defined here toggles on/off) ---
# Mode: "mins" = run for RUN_MINS minutes from when turned on; "fixed_time" = run only between RUN_TIME_FROM and RUN_TIME_TO
RUN_MODE = "mins"  # "mins" or "fixed_time"
RUN_MINS = 1  # minutes to run from when turned on (used when RUN_MODE == "mins")
RUN_TIME_FROM = (
    "09:30"  # HH:MM 24h, start of window (used when RUN_MODE == "fixed_time")
)
RUN_TIME_TO = "17:30"  # HH:MM 24h, end of window (used when RUN_MODE == "fixed_time")
# When fixed_time: from/to are randomized by ± this many minutes around the values above
RUN_TIME_RANDOM_MINUTES = 30
TOGGLE_KEY = "f12"  # key to toggle bot on/off (e.g. "f12", "ctrl+shift+a")

# --- At startup: move RDP session to console (so Hubstaff keeps tracking after disconnect) ---
RUN_TSCON_AT_STARTUP = False  # set True on VPS so bot runs tscon once at start; RDP will close

# --- When not running: activate this process and click top-right corner ---
IDLE_TARGET_PROCESS = "HubstaffClient.exe"  # find and activate this window when idle
IDLE_TOP_RIGHT_OFFSET_X = 170  # pixels from right edge for idle click
IDLE_TOP_RIGHT_OFFSET_Y = 180  # pixels from top edge for idle click
IDLE_TOP_LEFT_OFFSET_X = 170  # pixels from left edge for idle click
IDLE_TOP_LEFT_OFFSET_Y = 180  # pixels from top edge for idle click
