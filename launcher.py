#!/usr/bin/env python
"""
Incredible India Data Story - Universal Launcher
===============================================
This launcher provides a completely portable experience with minimal dependencies.
It handles all environment setup, package management, and app launching.

Just run this file and the app will start automatically!
"""
import os
import sys
import subprocess
import platform
import shutil
import tempfile
import time
from pathlib import Path
import threading
from datetime import datetime
import re

# Set UTF-8 mode for better Unicode support
if platform.system() == "Windows":
    os.environ["PYTHONIOENCODING"] = "utf-8"

VERSION = "1.3.0"
APP_NAME = "Incredible India Data Story"
REQUIRED_PYTHON_VERSION = (3, 9)

# Determine if terminal supports Unicode well
def has_unicode_support():
    """Check if the terminal supports Unicode properly"""
    if platform.system() == "Windows":
        # Windows Terminal and some modern terminals do support Unicode
        if "WT_SESSION" in os.environ or "CMDER_ROOT" in os.environ:
            return True
        # Check for PowerShell
        if os.environ.get("PSModulePath") and not os.environ.get("PROMPT"):
            return True
        return False
    return True

# Fallback ASCII characters when Unicode isn't well supported
UNICODE_FALLBACKS = {
    "●": "O",
    "═": "=",
    "║": "|",
    "╔": "+",
    "╗": "+",
    "╚": "+",
    "╝": "+",
    "╠": "+",
    "╣": "+",
    "╦": "+",
    "╩": "+",
    "╬": "+",
    "│": "|",
    "┤": "+",
    "├": "+",
    "┬": "+",
    "┴": "+",
    "┼": "+",
    "─": "-",
    "╭": "/",
    "╮": "\\",
    "╯": "/",
    "╰": "\\",
    "☉": "O",
}

def safe_unicode(text):
    """Convert Unicode to ASCII if needed based on platform support"""
    if not has_unicode_support():
        for unicode_char, fallback in UNICODE_FALLBACKS.items():
            text = text.replace(unicode_char, fallback)
    return text

# Colors for terminal output with enhanced options
class Colors:
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # India flag colors
    SAFFRON = '\033[38;5;208m'
    WHITE_FLAG = '\033[38;5;231m'
    INDIA_GREEN = '\033[38;5;34m'
    NAVY_BLUE = '\033[38;5;19m'
    
    # Text styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    
    # Reset
    END = '\033[0m'

    @staticmethod
    def disable_if_needed():
        # Disable colors on Windows if not supported
        if platform.system() == "Windows" and not (os.environ.get("ANSICON") or "WT_SESSION" in os.environ):
            for attr in dir(Colors):
                if not attr.startswith('__') and isinstance(getattr(Colors, attr), str):
                    setattr(Colors, attr, '')
    
    @staticmethod
    def gradient(text, start_color, end_color, steps=None):
        """Create a gradient effect on text (only works in some terminals)"""
        if steps is None:
            steps = len(text)
        
        # For simplicity, we're only supporting a few color gradients
        gradients = {
            ("red", "yellow"): [f"\033[38;5;{i}m" for i in range(196, 226)],
            ("blue", "cyan"): [f"\033[38;5;{i}m" for i in range(21, 51)],
            ("green", "cyan"): [f"\033[38;5;{i}m" for i in range(34, 51)],
            ("magenta", "blue"): [f"\033[38;5;{i}m" for i in range(201, 21, -5)],
            ("saffron", "green"): [f"\033[38;5;{i}m" for i in range(208, 34, -5)],
        }
        
        gradient_key = (start_color, end_color)
        if gradient_key in gradients:
            colors = gradients[gradient_key]
            result = ""
            for i, char in enumerate(text):
                color_index = min(int(i / len(text) * len(colors)), len(colors) - 1)
                result += f"{colors[color_index]}{char}{Colors.END}"
            return result
        
        # Fallback if gradient not found
        return f"{getattr(Colors, start_color.upper(), '')}{text}{Colors.END}"
    
    @staticmethod
    def india_flag_text(text):
        """Apply India flag colors to text - saffron, white, green"""
        parts = []
        third = len(text) // 3
        parts.append(f"{Colors.SAFFRON}{text[:third]}{Colors.END}")
        parts.append(f"{Colors.WHITE_FLAG}{text[third:2*third]}{Colors.END}")
        parts.append(f"{Colors.INDIA_GREEN}{text[2*third:]}{Colors.END}")
        return "".join(parts)

# Initialize color support
Colors.disable_if_needed()

def center_text(text, width=66, padding_char=" "):
    """Center text in a fixed width with optional padding character"""
    # Strip color codes for length calculation
    plain_text = text
    for attr in dir(Colors):
        if not attr.startswith('__') and isinstance(getattr(Colors, attr), str):
            plain_text = plain_text.replace(getattr(Colors, attr), "")
    
    # Calculate padding
    total_padding = width - len(plain_text)
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    
    return f"{padding_char * left_padding}{text}{padding_char * right_padding}"

# Ultra-minimal banner for Incredible India
BANNER = safe_unicode(f"""
{Colors.BOLD}{Colors.WHITE}╭{'─' * 66}╮{Colors.END}
{Colors.BOLD}{Colors.WHITE}│{Colors.END}{center_text(f"{Colors.BOLD}{Colors.SAFFRON}INCREDIBLE {Colors.WHITE_FLAG}INDIA {Colors.INDIA_GREEN}DATA STORY{Colors.END}", 66)}{Colors.BOLD}{Colors.WHITE}│{Colors.END}
{Colors.BOLD}{Colors.WHITE}│{Colors.END}{center_text(f"{Colors.BOLD}{Colors.CYAN}A DATA-DRIVEN JOURNEY{Colors.END}", 66)}{Colors.BOLD}{Colors.WHITE}│{Colors.END}
{Colors.BOLD}{Colors.WHITE}╰{'─' * 66}╯{Colors.END}
""")

# Ultra-minimal flag symbol with improved alignment
FLAG_SYMBOL = safe_unicode(f"""
{center_text(f"{Colors.SAFFRON}▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔{Colors.END}", 66)}
{center_text(f"{Colors.WHITE_FLAG}▔▔▔▔▔▔{Colors.NAVY_BLUE}●{Colors.WHITE_FLAG}▔▔▔▔▔▔{Colors.END}", 66)}
{center_text(f"{Colors.INDIA_GREEN}▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔{Colors.END}", 66)}
""")

# Enhanced Spinner class for loading animations
class Spinner:
    def __init__(self, message="Loading...", style="dots"):
        self.message = message
        self.running = False
        self.spinner_thread = None
        
        # Ultra-minimal spinner styles
        self.styles = {
            "dots": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
            "line": "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁",
            "india": "▰▱",
            "bounce": "▁▂▃▂▁",
            "pulse": "▉▊▋▌▍▎▏▎▍▌▋▊▉",
            "clock": "◐◓◑◒"
        }
        
        self.spinner_chars = self.styles.get(style, self.styles["dots"])
        
        # Refined color options for spinner
        self.colors = [
            Colors.SAFFRON,
            Colors.WHITE,
            Colors.INDIA_GREEN
        ]

    def spin(self):
        i = 0
        while self.running:
            i = (i + 1) % len(self.spinner_chars)
            color = self.colors[i % len(self.colors)]
            sys.stdout.write(f"\r{color}{self.spinner_chars[i]}{Colors.END} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()

    def start(self):
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop(self):
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
            
    def update_message(self, message):
        """Update the spinner message while it's running"""
        self.message = message

# Enhanced Progress bar class for visual progress display
class ProgressBar:
    def __init__(self, total=100, width=40, style="default"):
        self.total = total
        self.width = width
        
        # Ultra-minimal progress bar styles
        self.styles = {
            "default": {"fill": "▰", "empty": "▱", "brackets": ["│", "│"]},
            "block": {"fill": "▰", "empty": "▱", "brackets": ["▕", "▏"]},
            "arrow": {"fill": "─", "empty": "─", "head": "▶", "brackets": ["┫", "┣"]},
            "india": {"fill": "▰", "empty": "▱", "brackets": ["▕", "▏"]},
            "elegant": {"fill": "▰", "empty": "▱", "brackets": ["┃", "┃"]},
            "modern": {"fill": "─", "empty": "╌", "brackets": ["┣", "┫"]},
            "pulse": {"fill": "▉", "pulse": "▊▋▌▍▎▏", "empty": " ", "brackets": ["▕", "▏"]}
        }
        
        style_config = self.styles.get(style, self.styles["default"])
        self.fill = style_config.get("fill", "▰")
        self.empty = style_config.get("empty", "▱")
        self.brackets = style_config.get("brackets", ["│", "│"])
        self.head = style_config.get("head", "")
        self.pulse_chars = style_config.get("pulse", "")
        
        # Animation state
        self.animation_frame = 0
        self.last_update = 0
        
    def update(self, progress, description="", elapsed_time=None):
        filled_width = int(self.width * progress / self.total)
        empty_width = self.width - filled_width - (1 if self.head else 0)
        
        # Make sure we don't have negative widths
        filled_width = max(0, filled_width)
        empty_width = max(0, empty_width)
        
        # Add pulsing effect on the edge of the bar
        if self.pulse_chars and time.time() - self.last_update > 0.1:
            self.animation_frame = (self.animation_frame + 1) % len(self.pulse_chars)
            self.last_update = time.time()
            pulse_char = self.pulse_chars[self.animation_frame]
        else:
            pulse_char = ""
            
        # Build the bar
        if self.head and filled_width > 0:
            bar = f"{self.fill * (filled_width-1)}{self.head}{self.empty * empty_width}"
        elif pulse_char:
            bar = f"{self.fill * filled_width}{pulse_char}{self.empty * (empty_width-1)}"
        else:
            bar = f"{self.fill * filled_width}{self.empty * empty_width}"
        
        percent = int(100 * progress / self.total)
        
        # Add elapsed time display if provided
        time_display = ""
        if elapsed_time is not None:
            time_display = f" {Colors.CYAN}[{elapsed_time:.1f}s]{Colors.END}"
            
        # Show different colors based on progress - web-inspired gradient
        if percent < 30:
            color = Colors.RED
        elif percent < 50:
            color = Colors.YELLOW
        elif percent < 75:
            color = Colors.SAFFRON
        else:
            color = Colors.GREEN
            
        # Create a web-inspired progress indicator
        percent_display = f"{percent}%"
        
        # Return a well-formatted progress bar
        return f"{color}{self.brackets[0]}{bar}{self.brackets[1]}{Colors.END} {Colors.BOLD}{percent_display}{Colors.END}{time_display} {description}"
        
    def make_indeterminate(self, width=40, description="", frame=None):
        """Create an indeterminate (animated) progress bar"""
        if frame is None:
            frame = int(time.time() * 10) % width
            
        bar = ""
        for i in range(width):
            if (i + width - frame) % 10 == 0:
                bar += f"{Colors.SAFFRON}━{Colors.END}"
            elif (i + width - frame) % 10 == 3:
                bar += f"{Colors.WHITE}━{Colors.END}"
            elif (i + width - frame) % 10 == 6:
                bar += f"{Colors.INDIA_GREEN}━{Colors.END}"
            else:
                bar += "╌"
                
        return f"{Colors.BLUE}┃{bar}┃{Colors.END} {description}"

def visible_len(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return len(ansi_escape.sub('', text))

def print_header():
    """Print a minimal header for the launcher"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    width = 90
    # Print banner with consistent spacing
    print(f"\n{Colors.BOLD}{Colors.WHITE}╭{'─' * width}╮{Colors.END}")
    banner_line = f'{Colors.BOLD}{Colors.SAFFRON}INCREDIBLE {Colors.WHITE_FLAG}INDIA {Colors.INDIA_GREEN}DATA STORY{Colors.END}'
    pad = width - visible_len(banner_line)
    print(f"{Colors.BOLD}{Colors.WHITE}│{Colors.END}{banner_line}{' ' * pad}{Colors.BOLD}{Colors.WHITE}│{Colors.END}")
    subtitle = f'{Colors.BOLD}{Colors.CYAN}A DATA-DRIVEN JOURNEY{Colors.END}'
    pad = width - visible_len(subtitle)
    print(f"{Colors.BOLD}{Colors.WHITE}│{Colors.END}{subtitle}{' ' * pad}{Colors.BOLD}{Colors.WHITE}│{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}╰{'─' * width}╯{Colors.END}\n")
    # Print version and system info in a minimal box
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info = [
        [f"{Colors.YELLOW}◆{Colors.END}", f"Launcher v{VERSION} | {Colors.india_flag_text('Made with ♥ in India')}"],
        [f"{Colors.BLUE}◆{Colors.END}", f"Python {platform.python_version()} on {platform.system()} {platform.release()}"],
        [f"{Colors.MAGENTA}◆{Colors.END}", f"Started at: {current_time}"]
    ]
    print(f"{Colors.CYAN}╭{'─' * width}╮{Colors.END}")
    for icon, line in info:
        content = f"{icon}  {line}"
        pad = width - visible_len(content)
        print(f"{Colors.CYAN}│{Colors.END}{content}{' ' * pad}{Colors.CYAN}│{Colors.END}")
    print(f"{Colors.CYAN}╰{'─' * width}╯{Colors.END}")
    # Add a minimal welcome message with improved alignment
    print(f"\n{Colors.CYAN}╭{'─' * width}╮{Colors.END}")
    welcome_msg = f"Welcome to Incredible India Data Story Experience"
    welcome_colored = Colors.gradient(welcome_msg, 'saffron', 'green')
    pad = width - visible_len(welcome_msg)
    print(f"{Colors.CYAN}│{Colors.END}{welcome_colored}{' ' * pad}{Colors.CYAN}│{Colors.END}")
    journey_msg = "Preparing your journey..."
    pad = width - visible_len(journey_msg)
    print(f"{Colors.CYAN}│{Colors.END}{Colors.BOLD}{journey_msg}{Colors.END}{' ' * pad}{Colors.CYAN}│{Colors.END}")
    print(f"{Colors.CYAN}╰{'─' * width}╯{Colors.END}\n")

def print_step(step_number, total_steps, step_name):
    """Print a formatted step indicator with enhanced visuals and strict alignment"""
    width = 90
    inner_width = width - 2
    progress_bar = ProgressBar(total=total_steps, width=70, style="elegant")
    bar = progress_bar.update(step_number)
    elapsed = time.time() - startup_time
    elapsed_text = f"{Colors.YELLOW}[{elapsed:.1f}s]{Colors.END}"
    print(f"\n{Colors.BOLD}{Colors.CYAN}╭{'─' * inner_width}╮{Colors.END}")
    step_indicator = f"{Colors.BOLD}{Colors.YELLOW}●{Colors.END}"
    step_text = f"{Colors.BOLD}STEP {step_number}/{total_steps}:{Colors.END} {Colors.BOLD}{Colors.WHITE}{step_name}{Colors.END}"
    content = f"{step_indicator} {step_text}"
    pad = inner_width - visible_len(content)
    print(f"{Colors.BOLD}{Colors.CYAN}│{Colors.END}{content}{' ' * pad}{Colors.BOLD}{Colors.CYAN}│{Colors.END}")
    bar_content = f"{bar}{elapsed_text}"
    pad = inner_width - visible_len(bar_content)
    print(f"{Colors.BOLD}{Colors.CYAN}│{Colors.END}{bar}{' ' * pad}{elapsed_text}{Colors.BOLD}{Colors.CYAN}│{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╰{'─' * inner_width}╯{Colors.END}")

# Global variables for tracking timing
startup_time = time.time()
step_start_times = {}

def check_python_version():
    """Check if Python version meets requirements"""
    spinner = Spinner("Checking Python version compatibility...", style="india")
    spinner.start()
    time.sleep(1.5)  # For visual effect
    current_version = sys.version_info
    spinner.stop()
    
    if current_version < REQUIRED_PYTHON_VERSION:
        print(f"{Colors.RED}✘ Error: Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]} or higher is required.{Colors.END}")
        print(f"{Colors.RED}  You are using Python {current_version.major}.{current_version.minor}.{current_version.micro}{Colors.END}")
        print(f"\n{Colors.YELLOW}  Please install a compatible Python version to continue.{Colors.END}")
        input(f"\n{Colors.MAGENTA}Press Enter to exit...{Colors.END}")
        return False
    
    # Create a more attractive version display with color coding
    version_parts = [str(current_version.major), str(current_version.minor), str(current_version.micro)]
    colored_version = f"{Colors.CYAN}{version_parts[0]}{Colors.END}.{Colors.GREEN}{version_parts[1]}{Colors.END}.{Colors.YELLOW}{version_parts[2]}{Colors.END}"
    
    print(f"{Colors.GREEN}✓ Python version {colored_version} is compatible{Colors.END}")
    print(f"  {Colors.CYAN}Minimum required: {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}{Colors.END}")
    return True

def create_virtual_environment():
    """Create a project-specific virtual environment"""
    step_start_times['venv'] = time.time()
    venv_dir = Path(".venv")
    
    # Check if venv already exists
    if venv_dir.exists():
        elapsed = time.time() - step_start_times['venv']
        print(f"{Colors.YELLOW}➤ Using existing virtual environment at {Colors.UNDERLINE}{venv_dir.absolute()}{Colors.END}")
        print(f"  {Colors.CYAN}└─ Environment detected in {elapsed:.2f}s{Colors.END}")
        return True
    
    # Show indeterminate progress while creating venv
    spinner = Spinner("Creating virtual environment (this may take a minute)...", style="pulse")
    spinner.start()
    
    # Visual progress indicator
#     indeterminate_bar = ProgressBar(style="pulse")  # Unused variable
    progress_thread = threading.Thread(target=lambda: _show_indeterminate_progress(
        "Creating isolated Python environment...",
        lambda: spinner.running
    ))
    progress_thread.daemon = True
    progress_thread.start()
    
    try:
        subprocess.check_call([sys.executable, "-m", "venv", ".venv"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        spinner.stop()
        elapsed = time.time() - step_start_times['venv']
        
        # Print success with a bit more flair
        print(f"\r{' ' * 80}\r", end="")  # Clear progress line
        print(f"{Colors.GREEN}✓ Virtual environment created successfully {Colors.YELLOW}({elapsed:.1f}s){Colors.END}")
        print(f"  {Colors.CYAN}└─ Location: {Colors.UNDERLINE}{venv_dir.absolute()}{Colors.END}")
        return True
    except subprocess.CalledProcessError as e:
        spinner.stop()
        print(f"\r{' ' * 80}\r", end="")  # Clear progress line
        print(f"{Colors.RED}✘ Failed to create virtual environment: {e}{Colors.END}")
        print(f"  {Colors.YELLOW}└─ Will attempt to use system Python instead{Colors.END}")
        return False

def _show_indeterminate_progress(message, should_continue):
    """Helper to show an animated progress bar during long-running tasks"""
    bar = ProgressBar()
    frame = 0
    while should_continue():
        progress = bar.make_indeterminate(width=40, description=message, frame=frame)
        sys.stdout.write(f"\r{progress}")
        sys.stdout.flush()
        frame = (frame + 1) % 40
        time.sleep(0.1)
    sys.stdout.write(f"\r{' ' * 80}\r")
    sys.stdout.flush()

def get_venv_python():
    """Get path to Python executable in virtual environment"""
    if platform.system() == "Windows":
        return os.path.abspath(".venv/Scripts/python.exe")
    return os.path.abspath(".venv/bin/python")

def install_requirements(venv_python):
    """Install required packages in the virtual environment"""
    step_start_times['deps'] = time.time()
    
    print(f"{Colors.BOLD}{Colors.BLUE}➤ Preparing dependency installation...{Colors.END}")
    
    requirements = [
        "streamlit>=1.30.0",
        "pandas>=2.1.1",
        "numpy>=1.26.0",
        "altair>=5.1.2",
        "plotly==5.18.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "pillow>=10.0.1",
        "requests>=2.31.0",
        "typing-extensions>=4.9.0"
    ]
    
    # Display packages in a more attractive format
    print(f"  {Colors.CYAN}Packages to install:{Colors.END}")
    for i, req in enumerate(requirements):
        # Extract package name and version for more attractive display
        parts = req.split(">=")
        if len(parts) == 1:
            parts = req.split("==")
        
        if len(parts) == 2:
            pkg, ver = parts
            print(f"    {Colors.GREEN}▸ {Colors.BOLD}{pkg}{Colors.END}{Colors.YELLOW} {ver}{Colors.END}")
        else:
            print(f"    {Colors.GREEN}▸ {Colors.BOLD}{req}{Colors.END}")
    
    print()  # Add spacing
    
    # Create a temporary requirements file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp:
        temp.write('\n'.join(requirements))
        temp_name = temp.name
    
    try:
        # Update pip first
        spinner = Spinner("Updating pip to latest version...", style="dots")
        spinner.start()
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        spinner.stop()
        print(f"{Colors.GREEN}✓ Pip updated successfully{Colors.END}")
        
        # Install requirements with progress tracking
        print(f"\n  {Colors.CYAN}Installing packages (this may take a few minutes)...{Colors.END}")
        
        # Start spinner and progress animation
        spinner = Spinner("", style="india")
        spinner.start()
        
        # Show animated progress bar
        progress_thread = threading.Thread(target=lambda: _show_package_installation_progress(
            requirements, lambda: spinner.running
        ))
        progress_thread.daemon = True
        progress_thread.start()
        
        # Actually install packages
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", temp_name],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        
        spinner.stop()
        elapsed = time.time() - step_start_times['deps']
        
        # Success message with timing info
        print(f"\r{' ' * 80}\r", end="")  # Clear progress line
        print(f"{Colors.GREEN}✓ All packages installed successfully! {Colors.YELLOW}({elapsed:.1f}s){Colors.END}")
        print(f"  {Colors.CYAN}└─ {len(requirements)} packages are ready to use{Colors.END}")
        return True
    except subprocess.CalledProcessError as e:
        spinner.stop()
        print(f"\r{' ' * 80}\r", end="")  # Clear progress line
        print(f"{Colors.RED}✘ Failed to install packages: {e}{Colors.END}")
        print(f"  {Colors.YELLOW}Try running manually: {venv_python} -m pip install -r requirements.txt{Colors.END}")
        return False
    finally:
        # Clean up temp file
        os.unlink(temp_name)

def _show_package_installation_progress(packages, should_continue):
    """Show animated progress for package installation"""
    bar = ProgressBar(style="elegant")
    pkg_names = [p.split(">=")[0].split("==")[0] for p in packages]
    total_pkgs = len(pkg_names)
    
    i = 0
    while should_continue():
        # Cycle through package names in animation
        pkg_idx = i % total_pkgs
        pkg_name = pkg_names[pkg_idx]
        
        # Simulate progress
        progress_val = (i % 100) + 1
        progress = bar.update(progress_val, f"Installing {Colors.BOLD}{pkg_name}{Colors.END}...")
        
        sys.stdout.write(f"\r{progress}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.2)
    
    sys.stdout.write(f"\r{' ' * 80}\r")
    sys.stdout.flush()

def create_streamlit_config():
    """Create a basic Streamlit config if it doesn't exist"""
    step_start_times['config'] = time.time()
    
    config_dir = Path(".streamlit")
    config_file = config_dir / "config.toml"
    
    if not config_dir.exists():
        config_dir.mkdir()
    
    if not config_file.exists():
        spinner = Spinner("Creating Streamlit configuration...", style="clock")
        spinner.start()
        time.sleep(1.5)  # For visual effect
        
        with open(config_file, 'w') as f:
            f.write("""[theme]
primaryColor = "#FF9933"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1E2129"
textColor = "#FAFAFA"
font = "sans serif"

[server]
runOnSave = true
""")
        spinner.stop()
        elapsed = time.time() - step_start_times['config']
        
        print(f"{Colors.GREEN}✓ Streamlit configuration created {Colors.YELLOW}({elapsed:.1f}s){Colors.END}")
        # Display the theme colors as a preview
        print(f"  {Colors.CYAN}Theme colors:{Colors.END}")
        print(f"    {Colors.SAFFRON}■{Colors.END} Primary: #FF9933 (Saffron)")
        print(f"    {Colors.BG_BLUE}{Colors.WHITE} ■ {Colors.END} Background: #0E1117 (Dark)")
        print(f"    {Colors.WHITE}■{Colors.END} Text: #FAFAFA (White)")

def print_section_divider(title=""):
    """Print a section divider with optional title"""
    width = 70
    
    if title:
        print(f"\n{Colors.MAGENTA}┌{'─' * (width - 2)}┐{Colors.END}")
        print(f"{Colors.MAGENTA}│{Colors.END}{center_text(title, width - 2)}{Colors.MAGENTA}│{Colors.END}")
        print(f"{Colors.MAGENTA}└{'─' * (width - 2)}┘{Colors.END}")
    else:
        print(f"\n{Colors.MAGENTA}┌{'─' * (width - 2)}┐{Colors.END}")
        print(f"{Colors.MAGENTA}└{'─' * (width - 2)}┘{Colors.END}")

def launch_app(venv_python):
    """Launch the Streamlit app with enhanced visuals"""
    step_start_times['launch'] = time.time()
    
    # Create a modern section divider
    width = 66
    print(f"\n{Colors.MAGENTA}╭{'─' * (width - 2)}╮{Colors.END}")
    print(f"{Colors.MAGENTA}│{Colors.END}{center_text('LAUNCHING APPLICATION', width - 2)}{Colors.MAGENTA}│{Colors.END}")
    print(f"{Colors.MAGENTA}╰{'─' * (width - 2)}╯{Colors.END}\n")
    
    # Create a modern launch box
    print(f"{Colors.GREEN}╭{'─' * (width - 2)}╮{Colors.END}")
    launch_msg = f"{Colors.BOLD}The app will launch momentarily in your web browser{Colors.END}"
    launch_padding = max(0, width - len("The app will launch momentarily in your web browser") - 2)
    print(f"{Colors.GREEN}│{Colors.END} {launch_msg}{' ' * launch_padding}{Colors.GREEN}│{Colors.END}")
    
    ctrl_msg = f"{Colors.YELLOW}Press Ctrl+C to stop the app when you're done{Colors.END}"
    ctrl_padding = max(0, width - len("Press Ctrl+C to stop the app when you're done") - 2)
    print(f"{Colors.GREEN}│{Colors.END} {ctrl_msg}{' ' * ctrl_padding}{Colors.GREEN}│{Colors.END}")
    print(f"{Colors.GREEN}╰{'─' * (width - 2)}╯{Colors.END}")
    
    # Show a minimal loading animation
#     chars = "◜◠◝◞◡◟"  # Unused variable
    colors = [Colors.SAFFRON, Colors.WHITE, Colors.INDIA_GREEN]
    
    # Multi-line loading animation with consistent styling
    lines = [
        "Starting Incredible India journey",
        "Loading visualization modules",
        "Preparing data storytelling experience"
    ]
    
    for line_idx, line in enumerate(lines):
        # Use a different color for each line
        color = colors[line_idx % len(colors)]
        sys.stdout.write(f"\n{color}  ")
        
        # Animated typing effect
        for char_idx, char in enumerate(line):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.02)  # Slightly faster for better UX
        
        # Add animated dots
        for _ in range(3):
            for dot in range(1, 4):
                sys.stdout.write(f"\r{color}  {line}{'.' * dot}{' ' * (3-dot)}{Colors.END}")
                sys.stdout.flush()
                time.sleep(0.15)  # Slightly faster for better UX
    
    print("\n")
    
    # Fix for character encoding issues
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if platform.system() == "Windows":
        env["PYTHONUTF8"] = "1"
        # Fix for 'charmap' codec errors on Windows
        env["PYTHONLEGACYWINDOWSSTDIO"] = "utf-8"
    
    # Final countdown with animated styling
    print(f"{Colors.CYAN}  Starting server in:{Colors.END}")
    
    for i in range(3, 0, -1):
        countdown_char = "○" if i == 3 else "◎" if i == 2 else "●"
        sys.stdout.write(f"\r{Colors.CYAN}  {countdown_char} {i}...{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.5)
    
    sys.stdout.write(f"\r{Colors.GREEN}  ✓ Launching now!{Colors.END}\n\n")
    sys.stdout.flush()
    
    # Run streamlit in the virtual environment
    try:
        subprocess.run([venv_python, "-m", "streamlit", "run", "app.py"], env=env)
        return True
    except KeyboardInterrupt:
        elapsed = time.time() - step_start_times['launch']
        print(f"\n{Colors.YELLOW}✓ App stopped by user after {elapsed:.1f}s of runtime.{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✘ Error launching app: {e}{Colors.END}")
        return False

def check_data_encoding():
    """Check data files for encoding issues and fix if possible"""
    step_start_times['data'] = time.time()
    
    spinner = Spinner("Checking data files for encoding issues...", style="dots")
    spinner.start()
    
    try:
        data_dir = Path("data")
        fixed_files = 0
        total_files = 0
        
        if data_dir.exists() and data_dir.is_dir():
            for file_path in data_dir.glob("*.csv"):
                total_files += 1
                try:
                    # Try to read the file with utf-8 encoding
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # If utf-8 fails, try to read with another encoding and save as utf-8
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                        
                        # Write back as UTF-8
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        # Update the spinner message to show progress
                        spinner.update_message(f"Fixed encoding in {file_path.name}...")
                        fixed_files += 1
                        time.sleep(0.3)  # Slight delay to show the message
                    except Exception:
                        # If that fails too, just skip the file
                        pass
        
        spinner.stop()
        elapsed = time.time() - step_start_times['data']
        
        if fixed_files > 0:
            print(f"{Colors.GREEN}✓ Fixed encoding in {fixed_files} of {total_files} data file(s) {Colors.YELLOW}({elapsed:.1f}s){Colors.END}")
        else:
            print(f"{Colors.GREEN}✓ All {total_files} data files have correct encoding {Colors.YELLOW}({elapsed:.1f}s){Colors.END}")
    except Exception as e:
        spinner.stop()
        print(f"{Colors.YELLOW}⚠ Could not check data files: {e}{Colors.END}")

def clean_unnecessary_files():
    """Clean up unnecessary files like cache and temp files"""
    step_start_times['clean'] = time.time()
    
    print(f"{Colors.BLUE}➤ Cleaning up unnecessary files...{Colors.END}")
    
    try:
        # List of patterns for files/dirs to remove
        patterns_to_clean = [
            "**/__pycache__",
            "**/*.pyc",
            "**/.DS_Store",
            ".streamlit/cache",
            ".streamlit/logs",
            "**/*.bak",
            "**/*.tmp"
        ]
        
        cleaned_items = 0
        spinner = Spinner("Scanning for unnecessary files...", style="dots")
        spinner.start()
        
        # Group patterns into categories for better reporting
        categories = {
            "Cache files": ["**/__pycache__", "**/*.pyc", ".streamlit/cache"],
            "System files": ["**/.DS_Store"],
            "Temporary files": ["**/*.bak", "**/*.tmp", ".streamlit/logs"]
        }
        
        results = {category: 0 for category in categories}
        
        for pattern in patterns_to_clean:
            # Determine which category this pattern belongs to
            pattern_category = next((cat for cat, patterns in categories.items() 
                                  if pattern in patterns), "Other")
            
            # Use Path.glob to find matching files/dirs
            for path in Path('.').glob(pattern):
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)
                cleaned_items += 1
                results[pattern_category] += 1
                
                # Update spinner message occasionally
                if cleaned_items % 5 == 0:
                    spinner.update_message(f"Removing {pattern_category.lower()}...")
        
        spinner.stop()
        elapsed = time.time() - step_start_times['clean']
        
        if cleaned_items > 0:
            print(f"{Colors.GREEN}✓ Cleaned up {cleaned_items} unnecessary files/directories {Colors.YELLOW}({elapsed:.1f}s){Colors.END}")
            
            # Print breakdown of cleaned items by category
            print(f"  {Colors.CYAN}Summary of cleanup:{Colors.END}")
            for category, count in results.items():
                if count > 0:
                    print(f"    {Colors.GREEN}▸ {Colors.BOLD}{category}{Colors.END}: {count} items")
        else:
            print(f"{Colors.GREEN}✓ Project is already clean {Colors.YELLOW}({elapsed:.1f}s){Colors.END}")
            
    except Exception as e:
        print(f"{Colors.YELLOW}⚠ Error during cleanup: {e}{Colors.END}")

def main():
    """Main entry point"""
    # Initialize global timing
    global startup_time
    startup_time = time.time()
    
    # Print a fancy welcome header
    print_header()
    
    # Define steps with proper 0-based indexing
    TOTAL_STEPS = 6
    steps = [
        {"name": "Cleaning Project", "function": clean_unnecessary_files},
        {"name": "Checking Environment Compatibility", "function": check_python_version},
        {"name": "Setting Up Isolated Environment", "function": create_virtual_environment},
        {"name": "Installing Dependencies", "function": lambda venv: install_requirements(venv)},
        {"name": "Configuring Application", "function": create_streamlit_config},
        {"name": "Verifying Data Integrity", "function": check_data_encoding},
        {"name": "Launching Incredible India Experience", "function": lambda venv: launch_app(venv)}
    ]
    
    # Track process success
#     success = True  # Unused variable
    venv_python = None
    
    # Run steps 1-6
    for i in range(6):
        # Show progress
        print_step(i+1, TOTAL_STEPS, steps[i]["name"])
        
        # Execute step function
        if i == 0:
            # Cleaning step
            steps[i]["function"]()
        elif i == 1:
            # Python version check
            if not steps[i]["function"]():
                print(f"\n{Colors.RED}Setup cannot continue with incompatible Python version.{Colors.END}")
                print(f"\n{Colors.YELLOW}Please install Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]} or higher and try again.{Colors.END}")
                input(f"\n{Colors.MAGENTA}Press Enter to exit...{Colors.END}")
                return
        elif i == 2:
            # Virtual environment setup
            if not steps[i]["function"]():
                print(f"{Colors.YELLOW}⚠ Continuing with system Python...{Colors.END}")
                venv_python = sys.executable
            else:
                venv_python = get_venv_python()
        elif i == 3:
            # Install dependencies
            if not steps[i]["function"](venv_python):
                print(f"\n{Colors.RED}Failed to install required packages.{Colors.END}")
                print(f"{Colors.YELLOW}Please try running manually: pip install -r requirements.txt{Colors.END}")
                input(f"\n{Colors.MAGENTA}Press Enter to exit...{Colors.END}")
                return
        else:
            # Other steps (configuring, data verification)
            steps[i]["function"]()
    
    # Final step - Launch app (calling with different step number)
    print_step(TOTAL_STEPS, TOTAL_STEPS, steps[6]["name"])
    steps[6]["function"](venv_python)
    
    # Print elapsed time
    total_elapsed = time.time() - startup_time
    print(f"\n{Colors.BLUE}Total setup time: {Colors.BOLD}{Colors.YELLOW}{total_elapsed:.2f}s{Colors.END}")

if __name__ == "__main__":
    try:
        # Check for debug flag
        if len(sys.argv) > 1 and sys.argv[1] == "--debug":
            print(f"{Colors.YELLOW}Running in debug mode - configuration check only{Colors.END}")
            print(f"{Colors.CYAN}Python version: {sys.version}{Colors.END}")
            print(f"{Colors.CYAN}System: {platform.system()} {platform.release()}{Colors.END}")
            print(f"{Colors.CYAN}Terminal color support: {'Yes' if os.environ.get('ANSICON') or platform.system() != 'Windows' else 'Limited'}{Colors.END}")
            print(f"{Colors.CYAN}Launcher version: {VERSION}{Colors.END}")
            
            # Create a debug section box
            width = 70
            print(f"\n{Colors.YELLOW}┌────────────────────────────────────────────────────────────────────┐{Colors.END}")
            print(f"{Colors.YELLOW}│{Colors.END}{center_text('Debug Information', width - 2)}{Colors.YELLOW}│{Colors.END}")
            print(f"{Colors.YELLOW}└────────────────────────────────────────────────────────────────────┘{Colors.END}")
            
            # Test color display
            print("\nColor test:")
            for color_name in dir(Colors):
                if not color_name.startswith('__') and not callable(getattr(Colors, color_name)) and isinstance(getattr(Colors, color_name), str):
                    color_code = getattr(Colors, color_name)
                    print(f"  {color_code}■ {color_name}{Colors.END}")
            
            # Test India flag colors specifically
            print(f"\n{Colors.BOLD}Tricolor Test:{Colors.END}")
            print(f"  {Colors.SAFFRON}████████████████████{Colors.END}")
            print(f"  {Colors.WHITE}████████████████████{Colors.END}")
            print(f"  {Colors.INDIA_GREEN}████████████████████{Colors.END}")
            
            # Test spinner animation for 2 seconds
            print("\nSpinner test:")
            spinner = Spinner("Testing spinner animation...", "india")
            spinner.start()
            time.sleep(2)
            spinner.stop()
            print(f"{Colors.GREEN}✓ Spinner test complete{Colors.END}")
            
            # Test progress bar
            print("\nProgress bar test:")
            for style in ["default", "elegant", "modern", "arrow", "pulse"]:
                bar = ProgressBar(total=100, width=40, style=style)
                progress = bar.update(70, f"Style: {style}")
                print(f"  {progress}")
            
            # Show sample indeterminate progress
            bar = ProgressBar()
            progress = bar.make_indeterminate(40, "Processing...")
            print(f"\n  {progress}")
            
            # Show the ASCII art options in a consistent box
            print(f"\n{Colors.BOLD}{Colors.CYAN}┌────────────────────────────────────────────────────────────────────┐{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}│{Colors.END}{center_text('Available ASCII Art Options', width - 2)}{Colors.BOLD}{Colors.CYAN}│{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}└────────────────────────────────────────────────────────────────────┘{Colors.END}")
            
            print(f"\n{Colors.BOLD}1. Main Banner:{Colors.END}")
            print(BANNER)
            
            print(f"\n{Colors.BOLD}2. Flag Symbol:{Colors.END}")
            print(FLAG_SYMBOL)
            
            # Show color gradient test
            print(f"\n{Colors.BOLD}Color Gradient Test:{Colors.END}")
            gradient_text = "INCREDIBLE INDIA - THE LAND OF DIVERSITY AND UNITY"
            print(f"  {Colors.gradient(gradient_text, 'saffron', 'green')}")
            
            # Random quotes test in a box
            print(f"\n{Colors.BOLD}{Colors.GREEN}┌────────────────────────────────────────────────────────────────────┐{Colors.END}")
            print(f"{Colors.BOLD}{Colors.GREEN}│{Colors.END}{center_text('Inspirational Quotes', width - 2)}{Colors.BOLD}{Colors.GREEN}│{Colors.END}")
            print(f"{Colors.BOLD}{Colors.GREEN}└────────────────────────────────────────────────────────────────────┘{Colors.END}\n")
            
            quotes = [
                "{Colors.ITALIC}\"India is not a nation, nor a country. It is a subcontinent of nationalities.\" - Muhammad Ali Jinnah{Colors.END}",
                "{Colors.ITALIC}\"We owe a lot to the Indians, who taught us how to count, without which no worthwhile scientific discovery could have been made.\" - Albert Einstein{Colors.END}",
                "{Colors.ITALIC}\"India is the cradle of the human race, the birthplace of human speech, the mother of history, the grandmother of legend.\" - Mark Twain{Colors.END}",
                "{Colors.ITALIC}\"If there is one place where all dreams have found a home, it is India.\" - Romain Rolland{Colors.END}",
                "{Colors.ITALIC}\"In India, the oldest and most profound spiritual tradition on Earth still thrives.\" - Jack Kornfield{Colors.END}",
            ]
            for i, quote in enumerate(quotes):
                print(f"  {Colors.YELLOW}{i+1}.{Colors.END} {quote}")
            
            sys.exit(0)
            
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup interrupted by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}An unexpected error occurred: {e}{Colors.END}")
        print(f"{Colors.YELLOW}Please report this issue with the details above.{Colors.END}")
        sys.exit(1) 