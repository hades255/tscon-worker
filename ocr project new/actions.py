# =============================================================================
# Auto-bot configuration – edit this file to change behavior
# =============================================================================

SPEED = 6

# --- Startup ---
START_DELAY_SEC = 20.0  # Seconds to wait before first action
TSCON_DELAY_SEC = 20.0  # Seconds to wait before tscon action

# --- Delays between actions (random in this range) ---
DELAY_MIN_SEC = 0.5 * SPEED
DELAY_MAX_SEC = 2.0 * SPEED

# --- Process names (case-insensitive match on exe name) ---
VS_CODE_PROCESS_NAMES = ["Code.exe"]
CHROME_PROCESS_NAMES = ["chrome.exe"]

# --- VS Code: mouse move region (from_x, from_y, to_x, to_y) in pixels ---
VS_CODE_REGION = (400, 150, 1000, 600)

# --- Chrome: mouse move region (min_x, min_y, max_x, max_y) in pixels ---
CHROME_REGION = (300, 100, 1000, 600)
CHROME_SEARCH_KEYWORDS = [
    "How to implement Twilio Verify API for SMS phone verification in my tech stack?",
    "How to buy a domain and connect it to a hosting provider like Vercel or AWS?",
    "How to implement social media sharing for TikTok and Instagram Stories in a web app?",
    "How to programmatically add a logo watermark and CTA overlay to a video file?",
    "What are the integration steps for Persona KYC and how to handle verification webhooks?",
    "How to configure a production SMTP service like SendGrid or Amazon SES to avoid sandbox limits?",
    "How to build a sequential file upload button that triggers the next upload without a page refresh?",
    "How to design a transaction history UI with data fetching from a financial database?",
    "How to improve image loading performance using WebP, lazy loading, and CDN integration?",
    "How to create a zoomed-in admin interface to set specific coordinates for a scratchable canvas area?",
]

# --- After right-click: move this many pixels left, then left-click to close menu ---
CONTEXT_MENU_OFFSET_LEFT_PX = 10

VS_CODE_FILE_NAMES = [
    "ImageUploadPage.jsx ",
    "Sidebar.jsx ",
    "UserDetailPage.jsx ",
    "UsersPage.jsx ",
    ".env",
    "index.html",
    "GameForm.jsx ",
    "PageHeader.jsx ",
    "FilterBar.jsx ",
    "LogsPage.jsx ",
    "logs.js ",
    "LogDetailPage.jsx ",
    "H+",
    "LOGS_API.md ",
    "App.jsx ",
    "index.js ",
]
# --- Text options for VS Code: list of lines; bot picks 1 to N random lines and types them ---
VS_CODE_TEXTS_LINES_MIN = 1
VS_CODE_TEXTS_LINES_MAX = 20
VS_CODE_TEXTS = (
    """

.finally(() => {
if (!cancelled) setPendingLoading(false);
});
return () => {
cancelled = true;
};
}, []);

const handleFileSelect = async (role, file) => {
if (!file) return;
setLoading((prev) => ({ ...prev, [role]: true }));
setErrors((prev) => ({ ...prev, [role]: null }));
setResponses((prev) => ({ ...prev, [role]: null }));

try {
const data = await uploadImage(file);
setResponses((prev) => ({ ...prev, [role]: data }));
} catch (err) {
setErrors((prev) => ({
...prev,
[role]: err.message || "Upload failed",
}));
} finally {
setLoading((prev) => ({ ...prev, [role]: false }));
}
};

const handleInputChange = (role, e) => {
const file = e.target.files?.[0];
if (file) handleFileSelect(role, file);
e.target.value = "";
};

const handleUploadAll = async () => {
const { fa, fb, b } = responses;
if (!fa?.image_base64 || !fb?.image_base64 || !b?.image_base64) {
setUploadAllError(
"Upload and process FA, FB, and B images first (select a file for each)."
);
return;
}
const name =
(selectedFolderName || "").trim().replace(/[^\w.-]/g, "_") || "";
if (!name) {
setUploadAllError("Pick a pending ticket from the dropdown.");
return;
}

setUploadAllLoading(true);
setUploadAllError(null);
setUploadAllResult(null);

try {
const fileFa = base64ToFile(
fa.image_base64,
fa.content_type || "image/png",
"fa"
);
const fileFb = base64ToFile(
fb.image_base64,
fb.content_type || "image/png",
"fb"
);
const fileB = base64ToFile(
b.image_base64,
b.content_type || "image/png",
"b"
);

const result = await uploadImagesThree(name, fileFa, fileFb, fileB);
setUploadAllResult(result);
if (selectedTicket?.id) {
setUploadedTicketIds((prev) => new Set([...prev, selectedTicket.id]));
}
setResponses({ fa: null, fb: null, b: null });
setSelectedTicket(null);
} catch (err) {
setUploadAllError(err.message || "Upload failed");
} finally {
setUploadAllLoading(false);
}
};

const canUploadAll =
responses.fa?.image_base64 &&
responses.fb?.image_base64 &&
responses.b?.image_base64;

useEffect(() => {
function handleClickOutside(e) {
if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
setDropdownOpen(false);
}
}
if (dropdownOpen) {
document.addEventListener("mousedown", handleClickOutside);
return () =>
document.removeEventListener("mousedown", handleClickOutside);
}
}, [dropdownOpen]);

return (
<div className="space-y-6">
<PageHeader
title="Image upload"
description="Select FA, FB, and B ticket images. Each is uploaded and processed (Background removal + Skew correction); then upload all three to the server."
/>

<div className="rounded-xl border border-slate-100 bg-white p-4 shadow-sm">
<label className="mb-2 block text-sm font-medium text-slate-700">
S3 folder (for final upload)
</label>
{pendingLoading ? (
<LoadingSpinner label="Loading pending tickets…" />
) : pendingError ? (
<div className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
{pendingError}
</div>
) : null}
{!pendingLoading && (
<div ref={dropdownRef} className="relative max-w-2xl">
<button
type="button"
onClick={() => setDropdownOpen((open) => !open)}
className="flex w-full items-center justify-between rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-left text-sm shadow-sm hover:bg-slate-50"
>
<span className="truncate">
{selectedTicket
? `${
selectedTicket.game_name ?? selectedTicket.ticket_ref
} — (${selectedTicket.s3_folder_name})`
: "Select pending ticket…"}
</span>
<span className="ml-2 text-slate-400">
{dropdownOpen ? "▴" : "▾"}
</span>
</button>
{dropdownOpen && (
<div className="absolute z-10 mt-1 max-h-80 w-full overflow-hidden rounded-lg border border-slate-200 bg-white shadow-lg">
<div className="sticky top-0 border-b border-slate-100 bg-white p-2">
<input
type="text"
value={dropdownSearch}
onChange={(e) => setDropdownSearch(e.target.value)}
placeholder="Search s3_folder_name…"
className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-300"
onClick={(e) => e.stopPropagation()}
/>
</div>
<div className="max-h-64 overflow-auto py-1">
{pendingTickets.length === 0 ? (
<div className="px-3 py-4 text-center text-sm text-slate-500">
No pending tickets
</div>
) : filteredPendingTickets.length === 0 ? (
<div className="px-3 py-4 text-center text-sm text-slate-500">
No tickets matching &quot;{dropdownSearch}&quot;
</div>
) : (
filteredPendingTickets.map((t) => {
const isUploaded = uploadedTicketIds.has(t.id);
return (
<button
key={t.id}
type="button"
disabled={isUploaded}
onClick={() => {
if (isUploaded) return;
setSelectedTicket(t);
setDropdownOpen(false);
}}
className={`w-full px-3 py-2.5 text-left text-sm ${
isUploaded
? "cursor-not-allowed bg-slate-50 text-slate-400"
: selectedTicket?.id === t.id
? "bg-slate-100 hover:bg-slate-50"
: "hover:bg-slate-50"
}`}
    """
).split("\n")

# --- Mouse: smooth move ---
SMOOTH_MOVE_DURATION_MIN = 0.5 * SPEED
SMOOTH_MOVE_DURATION_MAX = 1.5 * SPEED
SMOOTH_MOVE_STEPS = 80

# --- Scroll: wheel delta (positive = up, negative = down); amount randomized ---
SCROLL_DELTA_BASE = 120
SCROLL_MULTIPLIER_MIN = 1
SCROLL_MULTIPLIER_MAX = 4

# --- Typing (VS Code) ---
TYPING_DELAY_PER_CHAR = 0.1 * SPEED

# --- Alt+Tab: hold Alt and press Tab N times (random in this range) ---
ALT_TAB_COUNT_MIN = 1
ALT_TAB_COUNT_MAX = 9
#   code, chrome, ssh, terminal, hubstaff, navicat, mobaxterm, chrome, code

# --- Ctrl+Tab: hold Ctrl and press Tab N times (random in this range) ---
CTRL_TAB_COUNT_MIN = 1
CTRL_TAB_COUNT_MAX = 5

# --- At startup: move RDP session to console (so Hubstaff keeps tracking after disconnect) ---
RUN_TSCON_AT_STARTUP = (
    True  # set True on VPS so bot runs tscon once at start; RDP will close
)

# --- When not running: activate this process and click top-right corner ---
IDLE_TARGET_PROCESS = "HubstaffClient.exe"  # find and activate this window when idle
IDLE_TOP_RIGHT_OFFSET_X = 170  # pixels from right edge for idle click
IDLE_TOP_RIGHT_OFFSET_Y = 180  # pixels from top edge for idle click
IDLE_TOP_LEFT_OFFSET_X = 170  # pixels from left edge for idle click
IDLE_TOP_LEFT_OFFSET_Y = 180  # pixels from top edge for idle click

# --- Run control: on/off and mode (key defined here toggles on/off) ---
# Mode: "mins" = run for RUN_MINS minutes from when turned on; "fixed_time" = run only between RUN_TIME_FROM and RUN_TIME_TO
RUN_MODE = "mins"  # "mins" or "fixed_time"
RUN_TIME_FROM = (
    "09:30"  # HH:MM 24h, start of window (used when RUN_MODE == "fixed_time")
)
RUN_TIME_TO = "17:30"  # HH:MM 24h, end of window (used when RUN_MODE == "fixed_time")
# When fixed_time: from/to are randomized by ± this many minutes around the values above
RUN_TIME_RANDOM_MINUTES = 30
TOGGLE_KEY = "f12"  # key to toggle bot on/off (e.g. "f12", "ctrl+shift+a")

RUN_MINS = 10  # minutes to run from when turned on (used when RUN_MODE == "mins")
