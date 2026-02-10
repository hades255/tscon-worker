# =============================================================================
# Auto-bot configuration – edit this file to change behavior
# =============================================================================

SPEED = 8

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
    "react tailwind modal component",
    "react tailwind modal best practices",
    "react tailwind modal controlled state",
    "react tailwind modal portal",
    "react createPortal modal tailwind",
    "accessible modal react tailwind",
    "react dialog tailwindcss",
    "react tailwind modal fade in fade out",
    "tailwind opacity transition modal",
    "react conditional render animation tailwind",
    "react tailwind animate opacity on mount",
    "tailwind transition-opacity modal",
    "react unmount animation tailwind",
    "react tailwind modal slide in slide out",
    "tailwind translate transition modal",
    "react tailwind bottom sheet modal",
    "react tailwind slide up modal",
    "tailwind transform transition modal",
    "react mobile modal slide animation",
    "react tailwind image modal",
    "react tailwind lightbox modal",
    "react image preview modal tailwind",
    "react fullscreen image modal",
    "react modal view image zoom",
    "react gallery modal tailwind",
    "headless ui dialog tailwind animation",
    "react headless ui modal transition",
    "react tailwind framer motion modal",
    "framer motion modal fade slide",
    "framer motion animate presence modal",
    "tailwind animate css modal",
    "tailwind keyframes modal animation",
    "react tailwind modal prevent body scroll",
    "react modal mobile viewport tailwind",
    "react modal overscroll fix",
    "tailwind modal z-index issue",
    "react modal focus trap",
    "react tailwind modal animate on unmount",
    "react modal exit animation tailwind",
    "react tailwind modal with createPortal and animation",
    "react modal image viewer with tailwind",
    "react modal slide up fade tailwind",
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

const brushPx = 40;

const [ticket, setTicket] = useState(null);
const [revealPercent, setRevealPercent] = useState(0);
const [isRevealed, setIsRevealed] = useState(false);
const [loading, setLoading] = useState(true);
const [submitting, setSubmitting] = useState(false);
const [showTicketModal, setShowTicketModal] = useState(false);
const [showResultModal, setShowResultModal] = useState(false);
const [processingResult, setProcessingResult] = useState(false);
const [showInstructionModal, setShowInstructionModal] = useState(false);
const [showActionsSheet, setShowActionsSheet] = useState(false);
const [playAgainLoading, setPlayAgainLoading] = useState(false);
const [imagesLoaded, setImagesLoaded] = useState({
unscratched: false,
scratched: false,
});
const [recordedStrokes, setRecordedStrokes] = useState([]);
const recordedStrokesRef = useRef([]);
const revealPercentRef = useRef(0);

useEffect(() => {
recordedStrokesRef.current = recordedStrokes;
}, [recordedStrokes]);

useEffect(() => {
revealPercentRef.current = revealPercent;
}, [revealPercent]);

useEffect(() => {
if (!ticketRef) {
navigate("/scratch-orders");
return;
}
api.orders.scratch
.getTicket(ticketRef, true)
.then((data) => {
if (data && data.ticket) setTicket(data.ticket);
if (
data.ticket?.status === "REVEALED" ||
data.ticket?.status === "WIN_CREDITED"
) {
setIsRevealed(true);
} else if (data.ticket?.status === "DELIVERED_DIGITALLY") {
setShowInstructionModal(true);
} else setTicket(null);
setRecordedStrokes([]);
// setShowInstructionModal(false);
setIsRevealed(false);
})
.catch(() => {
navigate("/scratch-orders");
});
}, [ticketRef, navigate]);

useEffect(() => {
if (!ticket) return;
const unscratchedImage =
ticket?.frontUnscratchedImage || ticket?.image || null;
const scratchedImage = ticket?.frontScratchedImage || ticket?.image || null;

// Reset image loading state
setImagesLoaded({ unscratched: false, scratched: false });

let unscratchedLoaded = false;
let scratchedLoaded = false;

const checkAllLoaded = () => {
if (unscratchedLoaded && scratchedLoaded) {
setImagesLoaded({ unscratched: true, scratched: true });
setLoading(false);
}
};

// Load unscratched image
const unscratchedImg = new Image();
unscratchedImg.crossOrigin = "anonymous";
unscratchedImg.onload = () => {
unscratchedLoaded = true;
checkAllLoaded();
};
unscratchedImg.onerror = () => {
// Even if image fails to load, mark as loaded to prevent infinite loading
unscratchedLoaded = true;
checkAllLoaded();
};
unscratchedImg.src = unscratchedImage;

// Load scratched image
const scratchedImg = new Image();
scratchedImg.crossOrigin = "anonymous";
scratchedImg.onload = () => {
scratchedLoaded = true;
checkAllLoaded();
};
scratchedImg.onerror = () => {
// Even if image fails to load, mark as loaded to prevent infinite loading
scratchedLoaded = true;
checkAllLoaded();
};
scratchedImg.src = scratchedImage;
}, [ticket]);

const handleStrokeRecord = (point) => {
// Record stroke point (only if not revealed)
if (!isRevealed) {
setRecordedStrokes((prev) => {
const updated = [...prev, point];
recordedStrokesRef.current = updated; // Update ref immediately
return updated;
});
}
};

const handleRevealWithValues = async (
percentValue = 0,
strokesValue = null
) => {
if (submitting || isRevealed || ticket?.status !== "DELIVERED_DIGITALLY")
return;
setSubmitting(true);
setProcessingResult(true);
try {
const { ticket: updated } = await api.orders.scratch.reveal(
ticketRef,
strokesValue,
brushPx
);
setTimeout(() => {
setIsRevealed(true);
setTicket((prev) =>
prev
? {
...prev,
prizeAmountCents: updated.prizeAmountCents,
status: updated.status,
winnings:
updated.prizeAmountCents != null
? updated.prizeAmountCents / 100
: 0,
}
: null
);
setProcessingResult(false);
setShowResultModal(true);
}, 2000);
} catch (error) {
console.error("Reveal error:", error);
setProcessingResult(false);
} finally {
setSubmitting(false);
}
};

const triggerRevealOnce = useCallOnce(() => {
handleRevealWithValues(
revealPercentRef.current,
recordedStrokesRef.current
);
});

const handleRevealPercent = (percent) => {
setRevealPercent(percent);
revealPercentRef.current = percent;
if (
percent >= 90 &&
!isRevealed &&
ticket?.status === "DELIVERED_DIGITALLY"
) {
setTimeout(() => triggerRevealOnce(), 100);
}
};

const handleRevealPrize = async () => {
handleRevealWithValues();
};

const handlePlayAgain = async () => {
if (!ticket?.gameId || playAgainLoading) return;
setShowActionsSheet(false);
setPlayAgainLoading(true);
try {
const game = await api.games.getScratchById(ticket.gameId);
if (!game) {
console.error("Game not found:", ticket.gameId);
return;
}
const priceRaw = game.pricePerPlay ?? game.price;
const price =
typeof priceRaw === "string"
? parseFloat(priceRaw) || 0
: Number(priceRaw) ?? 0;
const topPrizeRaw = game.topPrize ?? game.jackpot;
const topPrize =
typeof topPrizeRaw === "string"
? parseFloat(topPrizeRaw) || 0
: Number(topPrizeRaw) ?? 0;
const image =
game.image ??
game.frontUnscratchedImage ??
game.frontScratchedImage ??
ticket.image ??
ticket.frontUnscratchedImage ??
ticket.frontScratchedImage;
dispatch({
type: "ADD_ITEM",
gameId: game.id,
title: game.title,
price,
image,
topPrize,
});
navigate("/scratch-order-cart");
} catch (err) {
console.error("Play again failed:", err);
} finally {
setPlayAgainLoading(false);
}
};

const scratchRegion = useMemo(() => {
if (!ticket || !ticket.scratchable_areas) {
return {
width: 100,
height: 100,
boxes: [{ x: 0, y: 0, w: 100, h: 600 }],
};
}
const { width: W, height: H, boxes } = ticket.scratchable_areas;
const ratio = W / H;
const is4to3 = W > H && Math.abs(ratio - 4 / 3) < 0.15;

if (!is4to3) return ticket.scratchable_areas;

// clockwise 90°: swap W/H, transform boxes
const newRegion = {
width: H,
height: W,
boxes: boxes.map(({ x, y, w, h }) => ({
x: y,
y: W - x - w,
w: h,
h: w,
})),
};
return newRegion;
}, [ticket?.scratchable_areas]);

if (loading) {
return (
<Layout showHeader={false} showFooter={false}>
<div className="flex flex-col overflow-hidden justify-around h-screen">
<div className="px-4 pt-3 w-full bg-[#FF5B04]">
<BackButton
backLabel={"Back to Orders"}
color="white"
icon="arrowLeft"
backUrl="/scratch-orders"
/>
</div>
<div className="flex-grow"></div>
<div className="fixed bottom-0 w-full px-4 pt-2 pb-3">
<button className="w-full h-14 rounded-2xl bg-gradient-to-b from-[#FF5B04] to-[#FFA500] text-white font-medium disabled:bg-opacity-50 disabled:cursor-not-allowed hover:bg-[#FF4B04]/20 transition-colors">
Reveal All
</button>
</div>
</div>
<div className="min-h-screen fixed inset-0 z-40 flex flex-col gap-4 items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in">
<div className="h-12 w-12 rounded-full border-4 border-gray-200 border-t-[#FF5B04] animate-spin" />
<div className="text-xl font-semibold text-white">
Loading your ticket...
</div>
</div>
</Layout>
);
}

if (!ticket) {
return (
<Layout showHeader={false} showFooter={false}>
<div className="min-h-screen flex items-center justify-center">
<div className="text-center">
<div className="text-lg text-gray-600 mb-4">Ticket not found</div>
<button
onClick={() => navigate("/scratch-orders")}
className="px-6 py-2 bg-[#FF5B04] text-white rounded-[14px]"
>
Back to Orders
</button>
</div>
</div>
</Layout>
);
}

const unscratchedImage =
ticket?.frontUnscratchedImage || ticket?.image || null;
const scratchedImage = ticket?.frontScratchedImage || ticket?.image || null;
const canScratch = ticket?.status === "DELIVERED_DIGITALLY" && !isRevealed;
const winnings =
ticket?.winnings ??
(ticket?.prizeAmountCents != null ? ticket.prizeAmountCents / 100 : 0);

// Calculate height: 100vh - back button height (56px) - reveal button height (56px) - padding (32px)
const scratchAreaHeight = "calc(100vh - 196px)";

return (
<Layout showHeader={false} showFooter={false}>
<div
className="flex flex-col overflow-hidden justify-around"
style={{
minHeight: canScratch ? "calc(100vh - 72px)" : "100vh",
}}
>
{/* Back Button */}
<div className="px-4 pt-3 flex-shrink-0 bg-[#FF5B04]">
<div className="flex items-center justify-between">
<BackButton
backLabel={ticket.title}
color="white"
icon="arrowLeft"
backUrl="/scratch-orders"
/>
{/* <button
onClick={() => setShowTicketModal(true)}
className="px-3 py-1.5 rounded-lg bg-gray-100 text-sm text-[#4A5565] hover:bg-gray-200 transition-colors"
>
Info
</button> */}
</div>
</div>

{/* Scratch Ticket Component - Full screen, no scrolling */}
<div className="flex-grow animate-fade-in">
<div
className="w-full h-full flex items-center justify-center relative"
style={{ height: scratchAreaHeight, minHeight: "400px" }}
>
<ScratchTicketComponent
unscratchedImageSrc={unscratchedImage}
scratchedImageSrc={scratchedImage}
overlayText={""}
overlayColor="#B7BDC6"
overlayGrain={0.25}
brushPx={brushPx}
onRevealPercent={canScratch ? handleRevealPercent : undefined}
scratchRegion={scratchRegion} // Bottom half
isRevealed={isRevealed}
onStrokeRecord={canScratch ? handleStrokeRecord : undefined}
/>
{showResultModal && (
<div className="absolute top-0 left-0 w-full h-full bg-black/80 flex items-center justify-center">
<div className="text-white text-2xl font-bold">
{winnings > 0 && (
<div className="flex flex-col items-center justify-center gap-4">
    <div className="h-20 w-20 rounded-full bg-[#00AE81] text-white flex items-center justify-center text-4xl font-bold shadow-[0_4px_6px_-4px_rgba(0,0,0,0.1),0_10px_15px_-3px_rgba(0,0,0,0.1)]">
    ✓
    </div>
    <span className="text-white text-3xl">You won!</span>
    <span className="text-[#00AE81] text-5xl">
    {formatMoneyInt(winnings)}
    </span>
    <span className="text-[#D1D5DC] text-sm">
    Congratulations! 🎉
    </span>
</div>
)}
{winnings === 0 && (
<div className="space-y-2">
    <div className="text-center text-2xl font-bold text-white">
    Sorry, not a winner
    </div>
    <div className="text-center text-sm text-white/80">
    Try again next time!
    </div>
</div>
)}
</div>
</div>
)}
</div>

<div className="h-2 bg-[#E5E7EB]">
<div
className="h-2 bg-gradient-to-r from-[#FF5B04] to-[#FFA500]"
style={{
width: `${Math.round(
Math.min(100, isRevealed ? 100 : revealPercent)
)}%`,
}}
></div>
</div>
<div className="mt-2 text-center text-sm text-[#4A5565]">
{Math.round(Math.min(100, isRevealed ? 100 : revealPercent))}%
</div>
<div className="text-center text-sm text-[#4A5565]">revealed</div>
</div>

{/* Reveal Prize Button */}
{canScratch && (
<div className="px-4 pt-2 pb-3 flex-shrink-0">
<button
onClick={handleRevealPrize}
disabled={submitting}
className="w-full h-14 rounded-2xl bg-gradient-to-b from-[#FF5B04] to-[#FFA500] text-white font-medium disabled:bg-opacity-50 disabled:cursor-not-allowed hover:bg-[#FF4B04]/20 transition-colors"
>
{submitting ? "Revealing..." : "Reveal All"}
</button>
</div>
)}

{/* {!canScratch && (
<div className="px-4 pb-4 flex-shrink-0">
<button
onClick={handleContinue}
disabled={submitting}
className="w-full h-14 rounded-2xl border border-[#FF5B04] text-[#FF5B04] font-medium disabled:bg-opacity-50 disabled:cursor-not-allowed hover:bg-[#FF4B04]/20 transition-colors"
>
Continue
</button>
</div>
)} */}

{!canScratch && (
<div className="px-4 pt-2 pb-3">
<button
onClick={() => setShowActionsSheet(true)}
disabled={submitting}
className="w-full h-14 rounded-2xl bg-[#00AE81] text-white font-medium uppercase"
>
Play Again
</button>
</div>
)}
</div>
{/* Ticket Info Modal */}
<TicketInfoModal
order={ticket}
isOpen={showTicketModal}
onClose={() => setShowTicketModal(false)}
/>

{/* Instruction Modal */}
<ScratchInstructionModal
isOpen={showInstructionModal}
onClose={() => setShowInstructionModal(false)}
message={
isRevealed
? "Your ticket has been revealed!"
: "Swipe here to scratch your ticket"
}
/>

{/* Loading Modal - shows during processing with blur background */}
<ScratchLoadingModal isOpen={processingResult} />

{/* Bottom sheet: Play Again / Back to Games / Share */}
<ScratchGameDraggableBottomSheet
isOpen={showActionsSheet}
onClose={() => setShowActionsSheet(false)}
>
<div className="space-y-1">
<button
onClick={handlePlayAgain}
disabled={submitting || playAgainLoading}
className="w-full h-14 rounded-t-xl bg-[#FF5B04] text-white font-medium disabled:opacity-60 disabled:pointer-events-none"
>
{playAgainLoading ? "Adding…" : "Play Again"}
</button>
<button
onClick={() => {
setShowActionsSheet(false);
navigate("/scratch-orders");
}}
disabled={submitting}
className="w-full h-14 border-2 border-[#D1D5DC] font-medium"
>
Back to Games
</button>
<button
onClick={() => {
handleRevealPrize();
setShowActionsSheet(false);
}}
disabled={submitting}
className="w-full h-14 rounded-b-xl border-2 border-[#D1D5DC] flex items-center justify-center gap-2 font-medium"
>
<Icon name="share" size={20} color="black" />
Share
</button>
</div>
</ScratchGameDraggableBottomSheet>

{/* Scratch Result Modal */}
{/* <ScratchResultModal
isOpen={showResultModal}
onClose={() => setShowResultModal(false)}
onContinue={handleContinue}
winnings={winnings ?? 0}
loading={false}
/> */}
</Layout>
);
}

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
