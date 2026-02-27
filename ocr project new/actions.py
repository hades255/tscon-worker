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
    "How to implement draw-based lottery system backend architecture?",
    "How to generate provably fair lottery draw numbers?",
    "How to design ticket purchase and draw settlement logic in FastAPI?",
    "How to prevent duplicate ticket purchase using idempotency keys?",
    "How to design draw lifecycle states (scheduled → closed → drawn → settled)?",
    "How to calculate lottery odds programmatically?",
    "How to implement prize pool distribution logic?",
    "How to design scalable lottery database schema (tickets, draws, users)?",
    "US lottery app compliance requirements by state",
    "How to prevent lottery fraud in web applications?",
    "How to implement geo-restriction in gaming apps?",
    "How to implement audit logging for gaming systems?",
    "Tebex API integration example Node.js Python",
    "How Tebex handles digital goods payments?",
    "Tebex webhook verification implementation",
    "Tebex chargeback handling best practices",
    "Tebex payout system documentation",
    "Tebex vs Stripe for gaming platforms",
    "How to integrate Tebex checkout into React app?",
    "Plaid ACH payment integration tutorial",
    "Plaid Link React example",
    "Plaid backend token exchange flow FastAPI example",
    "Plaid sandbox testing guide",
    "Plaid identity verification API example",
    "Plaid vs Stripe ACH comparison",
    "How to verify bank account ownership using Plaid?",
    "How to run cron job in FastAPI?",
    "Python APScheduler vs Celery beat comparison",
    "How to run daily background task in Docker container?",
    "Kubernetes cronjob example for scraping",
    "Python scrape dynamic website with Playwright",
    "How to bypass basic bot detection in scraping?",
    "How to store scraped data in PostgreSQL efficiently?",
    "How to detect changes between daily scraped data?",
    "How to log cron job execution results?",
    "How to retry failed cron jobs automatically?",
    "How to send alert if scraping fails?",
    "BTCPayServer self-hosted setup guide",
    "BTCPayServer Docker installation",
    "BTCPayServer API payment integration example",
    "How to verify BTCPay webhook signature?",
    "BTCPayServer vs Coinbase Commerce comparison",
    "How to accept Bitcoin payments in React app?",
    "How to handle payment confirmation after 3 blocks?",
    "Most used payment methods in US mobile gaming",
    "Stripe vs PayPal vs Apple Pay for game apps",
    "ACH vs credit card for gaming platforms",
    "How to reduce payment processing fees in gaming apps?",
    "US gambling payment regulations 2026",
    "Best payment gateway for regulated gaming app",
    "Best crypto payment gateway for US gaming apps",
    "Is USDT allowed for gaming payments in US?",
    "How to accept USDC payments legally in US?",
    "Crypto KYC requirements in US gaming apps",
    "Coinbase Commerce vs BTCPayServer comparison",
    "How to implement crypto wallet payments in web app?",
    "How to handle crypto price volatility in checkout?",
    "How to detect user state using IP geolocation?",
    "Best IP geolocation API for US states",
    "How to dynamically render UI based on user state in React?",
    "React conditional rendering based on feature flags",
    "How to implement state-based feature toggle system?",
    "Backend-driven UI configuration example",
    "How to store user state in JWT token?",
    "How to restrict KYC flow by US state?",
    "Persona API state restriction example",
    "How to block onboarding for restricted states?",
    "Backend validation before KYC start",
    "How to check user eligibility before identity verification?",
    "GeoIP validation before KYC",
    "Gaming compliance states requiring identity verification",
    "Event-driven architecture for gaming platform",
    "Microservices vs monolith for lottery app",
    "How to implement payment idempotency safely?",
    "How to design scalable transaction ledger system?",
    "PCI compliance requirements for gaming app",
    "How to design anti-money laundering system for gaming platform?",
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
