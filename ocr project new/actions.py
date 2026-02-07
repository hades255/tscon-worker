# =============================================================================
# Auto-bot configuration – edit this file to change behavior
# =============================================================================

# --- Startup ---
START_DELAY_SEC = 20.0  # Seconds to wait before first action
TSCON_DELAY_SEC = 20.0  # Seconds to wait before tscon action

# --- Delays between actions (random in this range) ---
DELAY_MIN_SEC = 3.0 # 0.5
DELAY_MAX_SEC = 6.0 # 2.0

# --- Process names (case-insensitive match on exe name) ---
VS_CODE_PROCESS_NAMES = ["Code.exe"]
CHROME_PROCESS_NAMES = ["chrome.exe"]

# --- VS Code: mouse move region (from_x, from_y, to_x, to_y) in pixels ---
VS_CODE_REGION = (400, 150, 1000, 600)

# --- Chrome: mouse move region (min_x, min_y, max_x, max_y) in pixels ---
CHROME_REGION = (300, 100, 1000, 600)
CHROME_SEARCH_KEYWORDS = [
    "opencv image processing-save byte to png",
    "save image from byte to png cause quality loss",
    "methods to save bytes to png or jpeg without quality lose",
    "remove background from image using opencv",
    "result format of rembg library remove function",
    "rotating and deskewing images using opencv",
    "cropping image to content using opencv",
    "converting png to jpeg with white background using opencv",
    "rotate 90/180/270 jpeg without quality loss using opencv",
    "rotate and re-save losslessly",
    "read image without opencv",
]

# --- After right-click: move this many pixels left, then left-click to close menu ---
CONTEXT_MENU_OFFSET_LEFT_PX = 10

VS_CODE_FILE_NAMES = [
    "apiadmin_router",
    "game_router",
    "gamegamerouter",
    "ticketsrouter",
    "controllersimagecontroller",
    "processorsimagenormalizer",
    "ticketprocessor",
    "servicesimagenotifi",
    "s3manager",
    "gameapiscratchordersrouter",
    "gameapiplayersrouter",
]
# --- Text options for VS Code: list of lines; bot picks 1 to N random lines and types them ---
VS_CODE_TEXTS_LINES_MIN = 1
VS_CODE_TEXTS_LINES_MAX = 10 # 20
VS_CODE_TEXTS = (
    """
base_file_name = file_name.rsplit(".", 1)[0]

if base_file_name.endswith("_READY"):
pass
else:
ready_file_name = f"{base_file_name}_READY"

ext = ""
new_file_name = ""
if "." in file_name:
ext = "." + file_name.rsplit(".", 1)[1]
new_file_name = f"{ready_file_name}{ext}"
else:
new_file_name = f"{ready_file_name}.jpeg"

from ..main import (
app,
)
from rembg import remove
from ..controllers.image_controller import (
crop_to_content,
deskew_png_to_right_angles,
png_to_jpeg_white_bg,
)

s3_manager = getattr(app.state, "s3_manager", None)
if not s3_manager:
return {"status": "error", "reason": "S3 not configured"}

image_bytes = s3_manager.read_file(file_key)
if not image_bytes:
return {"status": "error", "reason": f"Could not read file: {file_key}"}

try:
output = remove(image_bytes)
output = deskew_png_to_right_angles(output)
output = crop_to_content(output, margin_px=0)
output = png_to_jpeg_white_bg(output, quality=88)
except Exception as e:
return {"status": "error", "reason": f"Image processing failed: {e!s}"}

if not _FOLDER_ROLE_PATTERN.match(foldername):
raise HTTPException(
status_code=status.HTTP_400_BAD_REQUEST,
detail="foldername must contain only letters, numbers, underscore, hyphen, period",
)
s3_manager = getattr(request.app.state, "s3_manager", None)
if not s3_manager:
raise HTTPException(
status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
detail="S3 not configured",
)
roles_files = [
("FA", file_fa),
("FB", file_fb),
("B", file_b),
]
uploaded: list[dict[str, str]] = []
s3_manager.create_folder(foldername)
for role, upload in roles_files:
content_type = upload.content_type or ""
if not content_type.startswith("image/"):
raise HTTPException(
status_code=status.HTTP_400_BAD_REQUEST,
detail=f"File for {role} must be an image (got {content_type})",
)
data = upload.file.read()
if not data:
raise HTTPException(
status_code=status.HTTP_400_BAD_REQUEST,
detail=f"File for {role} is empty",
)
ext = _extension_from_filename(upload.filename)
s3_key = f"{foldername}/{foldername}_{role}_READY.{ext}"
ct = _content_type_for_ext(ext)
s3_manager.write_file(s3_key, data, content_type=ct)
uploaded.append({"role": role, "s3_key": s3_key})
return {
"foldername": foldername,
"uploaded": uploaded,
}

arr = np.frombuffer(png_bytes, dtype=np.uint8)
img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
if img is None or img.ndim != 3:
return png_bytes
h, w = img.shape[:2]
if img.shape[2] == 4:
alpha = img[:, :, 3] / 255.0
rgb = img[:, :, :3]
white = np.ones_like(rgb) * 255
blended = (
rgb * alpha[:, :, np.newaxis] + white * (1 - alpha[:, :, np.newaxis])
).astype(np.uint8)
else:
blended = img[:, :, :3]
_, out_bytes = cv2.imencode(".jpg", blended, [cv2.IMWRITE_JPEG_QUALITY, quality])
if out_bytes is None:
return png_bytes
return out_bytes.tobytes()



def _get_best_fit_ratio(self, H: int, W: int) -> list[int, int]:
known_ratios = []
for w_k, h_k in KNOWN_HW:
if h_k == 0:
ratio_k = float("inf")
else:
ratio_k = w_k / h_k
known_ratios.append({"ratio": ratio_k, "pair": [w_k, h_k]})

if H == 0:
R_i = float("inf")
else:
R_i = W / H

min_diff = float("inf")
best_match_pair = [W, H]

for known in known_ratios:
R_k = known["ratio"]
W_k, H_k = known["pair"]

diff_direct = abs(R_i - R_k)

if R_k != 0:
R_k_inv = 1 / R_k
diff_inverse = abs(R_i - R_k_inv)
else:
diff_inverse = float("inf")

if diff_direct < min_diff:
min_diff = diff_direct
best_match_pair = [W_k, H_k]

if diff_inverse < min_diff:
min_diff = diff_inverse

best_match_pair = [H_k, W_k]

ratio = best_match_pair
return [min(ratio), max(ratio)]

def _rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
(h, w) = image.shape[:2]

center = (w // 2, h // 2)

M = cv2.getRotationMatrix2D(center, angle, 1.0)

cos = np.abs(M[0, 0])
sin = np.abs(M[0, 1])

nW = int((h * sin) + (w * cos))
nH = int((h * cos) + (w * sin))

M[0, 2] += (nW / 2) - center[0]
M[1, 2] += (nH / 2) - center[1]

rotated = cv2.warpAffine(image, M, (nW, nH))

return rotated
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
TYPING_DELAY_PER_CHAR = 0.5 # 0.1

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
