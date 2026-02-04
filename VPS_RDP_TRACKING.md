# Hubstaff + Bot on Windows VPS When RDP Is Disconnected

## Important: Mouse/keyboard do not work after tscon on many VPS

On many Windows VPS (headless, no physical display), **after you run tscon** and the session moves to console:

- **Neither `mouse_event` nor `SendInput`** have any effect – the console session does not process injected input.
- So the bot keeps running, but **all mouse moves and clicks (and likely keyboard)** do nothing. Hubstaff may still track if it uses other signals, but the bot cannot interact with the desktop after tscon.

**Recommended:** **Do not use tscon** on such a VPS. **Keep your RDP client connected** (you can minimize the window). The session then stays active, the display and input work, and both the bot and Hubstaff behave normally.

Set **`RUN_TSCON_AT_STARTUP = False`** in `config.py` and leave your RDP window open (minimized is fine).

---

## Why time stops tracking after you disconnect RDP

When you **disconnect** from Remote Desktop (without logging off):

- Your session stays running, but Windows treats it as **disconnected**.
- The **session’s display is no longer active** – nothing is “drawing” the desktop for that session.
- Hubstaff relies on:
  - **Screenshots** (1–3 per 10 minutes) – if the display isn’t updating, screenshots can be blank/frozen or not useful.
  - **Mouse/keyboard activity** (binary: active/inactive) – input from the bot may still be sent, but the session state can make Hubstaff (or Windows) treat the session as idle or inactive.

So: **disconnected RDP session ⇒ display inactive ⇒ no (or wrong) tracking in Hubstaff**, even though the bot and Hubstaff are still running.

---

## What to try on the VPS (in order of practicality)

### 1. Move your RDP session to the “console” (tscon) – try this first

Before you **disconnect**, run this **inside the RDP session** (e.g. in `cmd` as the same user):

```batch
for /f "skip=1 tokens=3" %s in ('query user %USERNAME%') do tscon.exe %s /dest:console
```

- This reattaches your session to the **console** (Session 0). The console session usually keeps a “display” active even when no one is connected via RDP.
- Then you can close the RDP client; the session (and your bot + Hubstaff) keeps running with an active console.
- **Limitation:** On some hosted VPS (e.g. no physical/virtual console), “console” may not exist or may not behave as expected. Still worth trying.

**One-liner for a scheduled task / script (if you use `%USERNAME%`):**

```batch
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do tscon.exe %%s /dest:console
```

(Use `%%s` in a `.bat` file, `%s` in a single command in `cmd`.)

---

### 2. Virtual display / dummy monitor

If the server has **no physical monitor**, the “display” for the session can go inactive when RDP disconnects. A **virtual display** can help:

- Install a **virtual display adapter** or **dummy HDMI** driver so Windows always has at least one “monitor.”
- That can keep a consistent resolution and an active display for the session, which may help Hubstaff’s screenshots and activity detection.

Search for: **“Windows virtual display driver”** or **“dummy HDMI Windows”** and use a solution that works on your Windows Server / Windows version.

---

### 3. Keep the RDP session “alive” (without fully disconnecting)

Some people **minimize** the RDP window instead of disconnecting, or use tools that send periodic input so the session is not considered idle:

- Your **bot already sends mouse/keyboard input**; the problem is usually the **disconnected** state, not just idle timeout.
- So “keep-alive” alone often isn’t enough; the important part is **not disconnecting** (or using tscon / virtual display so the session has an active display after disconnect).

---

### 4. Group Policy – keep disconnected session longer

To avoid the session being ended too soon after disconnect:

- **Computer Configuration** → **Administrative Templates** → **Windows Components** → **Remote Desktop Services** → **Remote Desktop Session Host** → **Session Time Limits**
- Set **“Set time limit for disconnected sessions”** to **“Never”** (or a long time) if allowed by your host.

This doesn’t fix the “display inactive” issue, but it keeps the session around so tscon or other tricks can be used.

---

## Summary

| Approach              | What it does |
|-----------------------|--------------|
| **Don’t disconnect**  | **Best for VPS.** Keep RDP client connected (minimize window). Session stays active, bot and Hubstaff work. Set `RUN_TSCON_AT_STARTUP = False`. |
| **tscon to console** | Reattach session to console then disconnect RDP. On many VPS, **mouse/keyboard injection stops working** after tscon; bot and idle click have no effect. |
| **Virtual display**   | Install dummy/virtual monitor so the session may keep an active display when RDP is gone. May help; does not fix “no input after tscon”. |
| **Session time limits** | Set “disconnected session” limit to Never so the session is not ended too soon. |

**For your VPS:** Use **“Don’t disconnect”** – keep RDP connected (minimized) and leave `RUN_TSCON_AT_STARTUP = False`. That way the bot and Hubstaff both work reliably.


---

```

where tscon

query user

```