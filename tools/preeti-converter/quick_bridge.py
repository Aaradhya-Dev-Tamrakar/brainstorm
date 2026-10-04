"""
Preeti Quick Bridge — Global Hotkey Converter & Floating Widget
================================================================
A lightweight system-tray-resident tool that provides:
  • Global hotkey (Ctrl+Alt+P) to convert clipboard Unicode → Preeti in-place
  • Floating mini-widget (Ctrl+Alt+M) with live preview and copy button
  • Optional system tray icon (via pystray) with context menu

Dependencies:
  Required : keyboard (pip install keyboard)
  Optional : pystray + Pillow (pip install pystray Pillow) — for system tray icon

Author: Aaradhya Dev Tamrakar
"""

import sys
import threading
import tkinter as tk
from tkinter import font as tkfont

# ── Hotkey backend selection (keyboard lib or native Win32 ctypes) ─────────
HAS_KEYBOARD = False
try:
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    pass

import time
import ctypes
from ctypes import wintypes

# ── Optional tray dependencies ───────────────────────────────────────────────
try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False

# ── Project import ───────────────────────────────────────────────────────────
from converter_engine import unicode_to_preeti


# ═════════════════════════════════════════════════════════════════════════════
#  THEME CONSTANTS (Material You Dark — matches main GUI)
# ═════════════════════════════════════════════════════════════════════════════

BG        = "#1C1B1F"
SURFACE   = "#2B2930"
PRIMARY   = "#D0BCFF"
ON_SURFACE = "#E6E1E5"
ON_PRIMARY = "#381E72"
OUTLINE   = "#49454F"
ERROR     = "#F2B8B5"
SUCCESS   = "#A8DB8F"

WIDGET_WIDTH  = 350
WIDGET_HEIGHT = 120
TOAST_DURATION_MS = 1800   # auto-dismiss after 1.8 s


# ═════════════════════════════════════════════════════════════════════════════
#  TOAST NOTIFICATION
# ═════════════════════════════════════════════════════════════════════════════

class ToastNotification:
    """Brief auto-dismissing notification shown near the cursor / bottom-right."""

    def __init__(self, root: tk.Tk):
        self._root = root
        self._win: tk.Toplevel | None = None

    def show(self, message: str, duration_ms: int = TOAST_DURATION_MS) -> None:
        """Display a toast; safe to call from any thread."""
        self._root.after(0, lambda: self._show_impl(message, duration_ms))

    def _show_impl(self, message: str, duration_ms: int) -> None:
        # Dismiss previous toast if still visible
        if self._win is not None:
            try:
                self._win.destroy()
            except tk.TclError:
                pass

        win = tk.Toplevel(self._root)
        win.withdraw()
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.92)
        win.configure(bg=SURFACE)

        frame = tk.Frame(win, bg=SURFACE, padx=14, pady=8)
        frame.pack(fill="both", expand=True)

        lbl = tk.Label(
            frame, text=message, bg=SURFACE, fg=SUCCESS,
            font=("Segoe UI", 10), wraplength=360, justify="left",
        )
        lbl.pack()

        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        w = win.winfo_reqwidth()
        h = win.winfo_reqheight()
        x = sw - w - 20
        y = sh - h - 60
        win.geometry(f"+{x}+{y}")
        win.deiconify()

        self._win = win
        win.after(duration_ms, lambda: self._dismiss(win))

    def _dismiss(self, win: tk.Toplevel) -> None:
        try:
            win.destroy()
        except tk.TclError:
            pass
        if self._win is win:
            self._win = None


# ═════════════════════════════════════════════════════════════════════════════
#  FLOATING MINI-WIDGET
# ═════════════════════════════════════════════════════════════════════════════

class FloatingWidget:
    """
    Small always-on-top borderless widget with:
      • Text entry for typing/pasting Unicode
      • Live Preeti preview label
      • Copy button
    """

    def __init__(self, root: tk.Tk, toast: ToastNotification):
        self._root = root
        self._toast = toast
        self._visible = False
        self._drag_data = {"x": 0, "y": 0}

        # ── Build the Toplevel ────────────────────────────────────────────
        self._win = tk.Toplevel(root)
        self._win.withdraw()
        self._win.overrideredirect(True)
        self._win.attributes("-topmost", True)
        self._win.attributes("-alpha", 0.95)
        self._win.configure(bg=BG)
        self._win.protocol("WM_DELETE_WINDOW", self.hide)

        # ── Outer frame with rounded-feel border ─────────────────────────
        outer = tk.Frame(self._win, bg=OUTLINE, padx=1, pady=1)
        outer.pack(fill="both", expand=True)
        container = tk.Frame(outer, bg=BG, padx=10, pady=8)
        container.pack(fill="both", expand=True)

        # ── Title bar (draggable) ────────────────────────────────────────
        title_bar = tk.Frame(container, bg=BG, height=22)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        title_lbl = tk.Label(
            title_bar, text="⚡ Quick Bridge", bg=BG, fg=PRIMARY,
            font=("Segoe UI Semibold", 9), anchor="w",
        )
        title_lbl.pack(side="left", fill="x", expand=True)

        close_btn = tk.Label(
            title_bar, text="✕", bg=BG, fg=ON_SURFACE,
            font=("Segoe UI", 9), cursor="hand2",
        )
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda _: self.hide())

        # Drag bindings on title bar
        for widget in (title_bar, title_lbl):
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._on_drag)

        # ── Unicode input entry ──────────────────────────────────────────
        entry_frame = tk.Frame(container, bg=SURFACE, padx=6, pady=4)
        entry_frame.pack(fill="x", pady=(6, 3))

        self._entry = tk.Entry(
            entry_frame, bg=SURFACE, fg=ON_SURFACE, insertbackground=PRIMARY,
            font=("Nirmala UI", 10), relief="flat", border=0,
        )
        self._entry.pack(fill="x")
        self._entry.bind("<KeyRelease>", self._on_input_change)
        self._entry.bind("<Control-v>", lambda _: self._root.after(50, self._on_input_change))
        self._entry.bind("<Return>", self._copy_result)

        # ── Preview row ──────────────────────────────────────────────────
        preview_frame = tk.Frame(container, bg=BG)
        preview_frame.pack(fill="x", pady=(3, 0))

        self._preview_lbl = tk.Label(
            preview_frame, text="", bg=BG, fg=PRIMARY,
            font=("Preeti", 12), anchor="w",
        )
        self._preview_lbl.pack(side="left", fill="x", expand=True)

        self._copy_btn = tk.Label(
            preview_frame, text=" 📋 Copy ", bg=SURFACE, fg=ON_SURFACE,
            font=("Segoe UI", 9), cursor="hand2", padx=6, pady=2,
        )
        self._copy_btn.pack(side="right")
        self._copy_btn.bind("<Button-1>", self._copy_result)

        # ── Position: center of screen ───────────────────────────────────
        self._win.update_idletasks()
        sw = self._win.winfo_screenwidth()
        sh = self._win.winfo_screenheight()
        x = (sw - WIDGET_WIDTH) // 2
        y = sh // 4
        self._win.geometry(f"{WIDGET_WIDTH}x{WIDGET_HEIGHT}+{x}+{y}")

    # ── Drag helpers ─────────────────────────────────────────────────────
    def _start_drag(self, event: tk.Event) -> None:
        self._drag_data["x"] = event.x_root - self._win.winfo_x()
        self._drag_data["y"] = event.y_root - self._win.winfo_y()

    def _on_drag(self, event: tk.Event) -> None:
        x = event.x_root - self._drag_data["x"]
        y = event.y_root - self._drag_data["y"]
        self._win.geometry(f"+{x}+{y}")

    # ── Live preview ─────────────────────────────────────────────────────
    def _on_input_change(self, event: tk.Event | None = None) -> None:
        unicode_text = self._entry.get().strip()
        if unicode_text:
            preeti = unicode_to_preeti(unicode_text)
            self._preview_lbl.config(text=preeti)
        else:
            self._preview_lbl.config(text="")

    # ── Copy result ──────────────────────────────────────────────────────
    def _copy_result(self, event: tk.Event | None = None) -> None:
        preeti = self._preview_lbl.cget("text")
        if preeti:
            self._root.clipboard_clear()
            self._root.clipboard_append(preeti)
            self._toast.show(f"✓ Copied: {preeti[:50]}")

    # ── Show / Hide / Toggle ─────────────────────────────────────────────
    def show(self) -> None:
        self._root.after(0, self._show_impl)

    def _show_impl(self) -> None:
        self._win.deiconify()
        self._win.lift()
        self._entry.focus_set()
        self._visible = True

    def hide(self) -> None:
        self._root.after(0, self._hide_impl)

    def _hide_impl(self) -> None:
        self._win.withdraw()
        self._visible = False

    def toggle(self) -> None:
        if self._visible:
            self.hide()
        else:
            self.show()

    @property
    def visible(self) -> bool:
        return self._visible


# ═════════════════════════════════════════════════════════════════════════════
#  CLIPBOARD HOTKEY CONVERTER
# ═════════════════════════════════════════════════════════════════════════════

def convert_clipboard(root: tk.Tk, toast: ToastNotification) -> None:
    """
    Read clipboard, convert Unicode Devanagari → Preeti, write back,
    and show a brief toast notification.  Thread-safe via root.after().
    """
    def _do() -> None:
        try:
            text = root.clipboard_get()
        except tk.TclError:
            toast.show("⚠ Clipboard is empty or unavailable")
            return

        if not text.strip():
            toast.show("⚠ Clipboard is empty")
            return

        result = unicode_to_preeti(text)
        root.clipboard_clear()
        root.clipboard_append(result)

        preview = result[:60] + ("…" if len(result) > 60 else "")
        toast.show(f"✓ Converted to Preeti: {preview}")

    root.after(0, _do)


# ═════════════════════════════════════════════════════════════════════════════
#  SYSTEM TRAY ICON (optional — requires pystray + Pillow)
# ═════════════════════════════════════════════════════════════════════════════

def _create_tray_icon_image() -> "Image.Image":
    """Generate a simple 64×64 tray icon (purple circle with 'P' glyph)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size - 4, size - 4], fill="#D0BCFF")
    try:
        from PIL import ImageFont
        try:
            fnt = ImageFont.truetype("segoeui.ttf", 28)
        except OSError:
            fnt = ImageFont.load_default()
    except ImportError:
        fnt = ImageFont.load_default()

    draw.text((size // 2, size // 2), "P", fill="#381E72", font=fnt, anchor="mm")
    return img


def start_tray_icon(
    root: tk.Tk,
    toast: ToastNotification,
    widget: FloatingWidget,
) -> "pystray.Icon | None":
    """Start the system tray icon in a background thread. Returns the Icon."""
    if not HAS_TRAY:
        return None

    icon_image = _create_tray_icon_image()

    def on_show_widget(icon, item):
        widget.show()

    def on_convert_clipboard(icon, item):
        convert_clipboard(root, toast)

    def on_quit(icon, item):
        icon.stop()
        root.after(0, root.destroy)

    menu = pystray.Menu(
        pystray.MenuItem("Show Widget    (Ctrl+Alt+M)", on_show_widget, default=True),
        pystray.MenuItem("Convert Clipboard (Ctrl+Alt+P)", on_convert_clipboard),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", on_quit),
    )

    icon = pystray.Icon("PreetiQuickBridge", icon_image, "Preeti Quick Bridge", menu)

    tray_thread = threading.Thread(target=icon.run, daemon=True, name="TrayIcon")
    tray_thread.start()
    return icon


# ═════════════════════════════════════════════════════════════════════════════
#  HOTKEY REGISTRATION (Dual backend: keyboard lib + Win32 ctypes fallback)
# ═════════════════════════════════════════════════════════════════════════════

def register_hotkeys(
    root: tk.Tk,
    toast: ToastNotification,
    widget: FloatingWidget,
):
    """
    Register global hotkeys via the `keyboard` library or native Win32 ctypes.
    Returns (backend_name, stop_event).
    """
    if HAS_KEYBOARD:
        try:
            keyboard.add_hotkey(
                "ctrl+alt+p",
                lambda: convert_clipboard(root, toast),
                suppress=True,
            )
            keyboard.add_hotkey(
                "ctrl+alt+m",
                lambda: widget.toggle(),
                suppress=True,
            )
            return ("keyboard", None)
        except Exception as e:
            print(f"keyboard module failed: {e}. Falling back to Win32 RegisterHotKey.")

    if sys.platform == "win32":
        stop_event = threading.Event()

        def win32_hotkey_thread():
            user32 = ctypes.windll.user32
            MOD_ALT = 0x0001
            MOD_CONTROL = 0x0002
            MOD_NOREPEAT = 0x4000
            VK_P = 0x50
            VK_M = 0x4D
            WM_HOTKEY = 0x0312
            WM_QUIT = 0x0012

            HOTKEY_ID_P = 1
            HOTKEY_ID_M = 2

            user32.RegisterHotKey(None, HOTKEY_ID_P, MOD_CONTROL | MOD_ALT | MOD_NOREPEAT, VK_P)
            user32.RegisterHotKey(None, HOTKEY_ID_M, MOD_CONTROL | MOD_ALT | MOD_NOREPEAT, VK_M)

            msg = wintypes.MSG()
            while not stop_event.is_set():
                if user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                    if msg.message == WM_HOTKEY:
                        if msg.wParam == HOTKEY_ID_P:
                            convert_clipboard(root, toast)
                        elif msg.wParam == HOTKEY_ID_M:
                            root.after(0, widget.toggle)
                    elif msg.message == WM_QUIT:
                        break
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))
                else:
                    time.sleep(0.02)

            user32.UnregisterHotKey(None, HOTKEY_ID_P)
            user32.UnregisterHotKey(None, HOTKEY_ID_M)

        t = threading.Thread(target=win32_hotkey_thread, daemon=True, name="Win32Hotkeys")
        t.start()
        return ("win32_ctypes", stop_event)

    return ("none", None)


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN ENTRY
# ═════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Launch Quick Bridge: hotkeys, floating widget, and optional tray icon."""

    # ── Hidden root window (hosts clipboard + event loop) ────────────────
    root = tk.Tk()
    root.withdraw()
    root.title("Preeti Quick Bridge")

    # ── Core components ──────────────────────────────────────────────────
    toast  = ToastNotification(root)
    widget = FloatingWidget(root, toast)

    # ── Register global hotkeys ──────────────────────────────────────────
    backend, stop_event = register_hotkeys(root, toast, widget)

    # ── System tray (graceful fallback if pystray missing) ───────────────
    tray_icon = start_tray_icon(root, toast, widget)

    if HAS_TRAY:
        print(f"Preeti Quick Bridge is running in the system tray (hotkeys via {backend}).")
    else:
        print(f"Preeti Quick Bridge is running (no tray icon — hotkeys via {backend}).")
    print("  Ctrl+Alt+P  →  Convert clipboard (Unicode → Preeti)")
    print("  Ctrl+Alt+M  →  Toggle floating widget")
    print("  Ctrl+C      →  Quit")

    # Show the widget on start so the user sees something
    widget.show()

    # ── Clean shutdown ───────────────────────────────────────────────────
    def shutdown() -> None:
        if backend == "keyboard" and HAS_KEYBOARD:
            try:
                keyboard.unhook_all()
            except Exception:
                pass
        elif backend == "win32_ctypes" and stop_event is not None:
            stop_event.set()

        if tray_icon is not None:
            try:
                tray_icon.stop()
            except Exception:
                pass
        try:
            root.destroy()
        except Exception:
            pass

    root.protocol("WM_DELETE_WINDOW", shutdown)

    # Handle Ctrl+C in terminal
    import signal
    signal.signal(signal.SIGINT, lambda *_: shutdown())

    # ── Run ──────────────────────────────────────────────────────────────
    try:
        root.mainloop()
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()
