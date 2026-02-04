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
VS_CODE_REGION = (400, 150, 1000, 600)

# --- Chrome: mouse move region (min_x, min_y, max_x, max_y) in pixels ---
CHROME_REGION = (300, 100, 1000, 600)
CHROME_SEARCH_KEYWORDS = [
    "react lottery ticket ui",
    "react scratch card game",
    "react ticket selection flow",
    "react number picker lottery",
    "react quick pick lottery",
    "react scratch card canvas",
    "scratch card effect react",
    "html5 canvas scratch card",
    "react touch swipe canvas",
    "mobile scratch card ui react",
    "react checkout flow example",
    "react wallet balance ui",
    "react order history ui",
    "react ticket status timeline",
    "react payment success failure ui",
    "react polling backend status",
    "react websocket real time updates",
    "react optimistic ui payments",
    "react react-query mutation flow",
    "react infinite list orders",
    "lottery app ui ux",
    "mobile gambling app ui patterns",
    "scratch card animation css",
    "react confetti prize animation",
    "react celebration animation",
    "lottery system architecture diagram",
    "gaming platform backend frontend architecture",
    "financial app backend frontend flow",
    "microservices lottery system",
    "high concurrency ticket system",
    "event driven backend fastapi",
]

# --- After right-click: move this many pixels left, then left-click to close menu ---
CONTEXT_MENU_OFFSET_LEFT_PX = 10

VS_CODE_FILE_NAMES = [
    "src/api/apijs",
    "src/api/mockapijs",
    "useCallOnce.js",
    "storeauthstorejs",
    "storegameflowstorejs",
    "storescratchcartjs",
    "appjs",
    "mainjs",
    "utilsdatetimejs",
    "utilsgameflowmoney",
    "utilsgameflowrandom",
]
# --- Text options for VS Code: list of lines; bot picks 1 to N random lines and types them ---
VS_CODE_TEXTS_LINES_MIN = 1
VS_CODE_TEXTS_LINES_MAX = 20
VS_CODE_TEXTS = (
    """
const code = searchParams.get("code");
const state = searchParams.get("state");
const error = searchParams.get("error");

if (error) {
setError("Authentication failed. Please try again.");
setTimeout(() => navigate("/signin"), 3000);
return;
}

if (!code) {
setError("Invalid callback. Please try again.");
setTimeout(() => navigate("/signin"), 3000);
return;
}

// Exchange code for token
const result = await api.auth.oauthCallback({ code, state });

if (result?.user) {
// Refresh session
await checkSession();
navigate("/", { replace: true });
} else {
setError("Authentication failed. Please try again.");
setTimeout(() => navigate("/signin"), 3000);
}

e.preventDefault();
setError("");
setLoading(true);

if (!otpSent) {
// Send OTP
const result = await sendOTP(phone);
if (result.success) {
setOtpSent(true);
} else {
setError(result.error || "Failed to send code");
}
} else {
// Verify OTP
const result = await verifyOTP(phone, otpCode);
if (result.success) {
navigate(from, { replace: true });
} else {
setError(result.error || "Invalid code");
}
}
setLoading(false);

// Block back navigation during payment flow

const handleNextClick = () => {
if (!method || submitting) return;
setSubmitting(true);
api.payments
.startAddFunds({ amount, method })
.then((res) => {
if (res?.paymentIntentId) {
sessionStorage.setItem("plotto:addfunds:intent", res.paymentIntentId);
}
navigate("/add-funds/processing");
})
.catch(() => setSubmitting(false));
};



const res = await api.orders.scratch.getStatus(orderId);

if (res.status === "RESERVED") {
setStatusMessage("Reserving ticket...");
// Wait a bit, then check again (simulating manager picking)
setTimeout(pollOrderStatus, 1500);
} else if (res.status === "PICKED") {
setStatusMessage("Scanning ticket...");
// Wait a bit, then check again (simulating OCR/scanning)
setTimeout(pollOrderStatus, 1500);
} else if (res.status === "DELIVERED_DIGITALLY") {
// Order is ready!
navigate("/scratch-order-success", { replace: true });
} else {
// Unexpected status, go to success anyway
navigate("/scratch-order-success", { replace: true });
}


const navigate = useNavigate();
const { state, dispatch } = useScratchCart();
const [statusMessage, setStatusMessage] = useState(
"Processing your order..."
);
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
ALT_TAB_COUNT_MAX = 9
#   code, chrome, ssh, terminal, hubstaff, chrome

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
