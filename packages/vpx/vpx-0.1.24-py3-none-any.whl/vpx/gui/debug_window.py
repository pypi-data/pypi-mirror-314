try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, filedialog, messagebox
except ImportError:
    raise ImportError(
        "Tkinter is not available. Please install python3-tk:\n"
        "For Ubuntu/Debian: sudo apt-get install python3-tk\n"
        "For macOS: brew install python-tk@3.9\n"
        "For Windows: Reinstall Python with tcl/tk option checked"
    )

from typing import Optional, Dict, Any, List, Tuple
import json
from ..diann.helper_agents import DesignVerifier, TestCase, TestType
from .rtl_visualizer import RTLVisualizer
import tempfile
import os
import webbrowser
import re
import datetime
import svgwrite
from svgwrite import cm, mm
from PIL import Image, ImageTk
import cairosvg  # For SVG to PNG conversion
import vcd
from math import cos, sin, sqrt
import subprocess

class ModulePort:
    def __init__(self, name: str, direction: str, width: int = 1):
        self.name = name
        self.direction = direction
        self.width = width

class DebugWindow(tk.Tk):
    COLORS = {
        'output': ('#ffcdd2', '#c62828'),     # Light red, Dark red
        'input': ('#c8e6c9', '#2e7d32'),      # Light green, Dark green
        'flop': ('#bbdefb', '#1565c0'),       # Light blue, Dark blue
        'combinational': ('#fff3e0', '#e65100'),  # Light orange, Dark orange
        'parameter': ('#e1bee7', '#6a1b9a'),   # Light purple, Dark purple
        'constant': ('#b2dfdb', '#00695c'),    # Light teal, Dark teal
        'clock': ('#ffe0b2', '#e65100'),      # Light amber, Dark amber
        'reset': ('#ffccbc', '#bf360c'),      # Light deep orange, Dark deep orange
        'default': ('#ffffff', '#000000')      # White, Black
    }

    def __init__(self, verbose: bool = False):
        super().__init__()
        self.title("VPX Verification")
        self.geometry("1400x800")
        self.verbose = verbose
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(expand=True, fill='both')
        
        # Create horizontal paned window
        self.h_paned = ttk.PanedWindow(self.main_container, orient=tk.HORIZONTAL)
        self.h_paned.pack(expand=True, fill='both')
        
        # Create verification frame (left side)
        self.verification_frame = self._create_verification_frame()
        self.h_paned.add(self.verification_frame, weight=3)
        
        # Create file hierarchy frame (right side)
        self.hierarchy_frame = self._create_hierarchy_frame()
        self.h_paned.add(self.hierarchy_frame, weight=1)
        
        # Set initial sash position (75% left, 25% right)
        self.after(100, lambda: self.h_paned.sashpos(0, int(self.winfo_width() * 0.75)))

    def _create_verification_frame(self) -> ttk.Frame:
        """Create verification frame with test list and detail view"""
        # Create paned window to split test list and details
        paned = ttk.PanedWindow(self.main_container, orient=tk.VERTICAL)
        
        # Top frame for test list
        top_frame = ttk.Frame(paned)
        
        # Add progress bar and status
        progress_frame = ttk.Frame(top_frame)
        progress_frame.pack(fill='x', padx=5, pady=5)
        
        # Add status label first
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(fill='x', padx=5, pady=2)
        
        # Then progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.pack(fill='x', padx=5, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(side='right', padx=5)
        
        # Add progress text widget
        self.progress_text = scrolledtext.ScrolledText(
            top_frame,
            wrap=tk.WORD,
            width=80,
            height=5,  # Reduced height
            font=('Courier', 10)
        )
        self.progress_text.pack(fill='x', padx=5, pady=5)
        
        # Add test results tree
        self.test_tree = ttk.Treeview(
            top_frame, 
            columns=('type', 'status', 'inputs', 'coverage', 'vcd', 'description', 'error', 'test_case'),  # Add test_case column
            show='headings',
            height=10  # Reduced height to make room for details
        )
        
        # Configure columns
        self.test_tree.heading('type', text='Type')
        self.test_tree.heading('status', text='Status')
        self.test_tree.heading('inputs', text='Inputs')
        self.test_tree.heading('coverage', text='Coverage')
        self.test_tree.heading('vcd', text='VCD?')
        self.test_tree.heading('description', text='Description')
        self.test_tree.heading('error', text='Error')
        self.test_tree.heading('test_case', text='')  # Hidden column for test case object
        
        # Configure column widths
        self.test_tree.column('type', width=100)
        self.test_tree.column('status', width=70)
        self.test_tree.column('inputs', width=300)
        self.test_tree.column('coverage', width=200)
        self.test_tree.column('vcd', width=150)
        self.test_tree.column('description', width=300)
        self.test_tree.column('error', width=200)
        self.test_tree.column('test_case', width=0, stretch=False)  # Hide test_case column
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(top_frame, orient="vertical", command=self.test_tree.yview)
        x_scroll = ttk.Scrollbar(top_frame, orient="horizontal", command=self.test_tree.xview)
        self.test_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Pack scrollbars and tree
        y_scroll.pack(side='right', fill='y')
        x_scroll.pack(side='bottom', fill='x')
        self.test_tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Configure tag for failed tests
        self.test_tree.tag_configure('failed', background='#ef9a9a')
        
        # Add double-click handler
        self.test_tree.bind('<Double-1>', self._on_test_double_click)
        
        # Bottom frame for test details
        self.detail_frame = ttk.Frame(paned)
        
        # Create notebook for detail tabs
        self.detail_notebook = ttk.Notebook(self.detail_frame)
        self.detail_notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create detail tabs
        self.log_tab = self._create_log_tab()
        self.compare_tab = self._create_compare_tab()
        self.wave_tab = self._create_wave_tab()
        
        # Add tabs to notebook
        self.detail_notebook.add(self.log_tab, text="Compilation Log")
        self.detail_notebook.add(self.compare_tab, text="Expected vs Actual")
        self.detail_notebook.add(self.wave_tab, text="Waveform")
        
        # Add frames to paned window
        paned.add(top_frame, weight=1)
        paned.add(self.detail_frame, weight=1)
        
        return paned

    def _create_log_tab(self) -> ttk.Frame:
        """Create tab for compilation log"""
        frame = ttk.Frame(self.detail_notebook)
        
        # Add text widget with scrollbar
        self.log_text = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Courier', 10)
        )
        self.log_text.pack(expand=True, fill='both', padx=5, pady=5)
        
        return frame

    def _create_compare_tab(self) -> ttk.Frame:
        """Create tab for expected vs actual comparison"""
        frame = ttk.Frame(self.detail_notebook)
        
        # Create two side-by-side text widgets
        left_frame = ttk.LabelFrame(frame, text="Expected Outputs")
        left_frame.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        
        # Add headers for expected outputs
        headers_frame = ttk.Frame(left_frame)
        headers_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(headers_frame, text="Signal", width=20).pack(side='left')
        ttk.Label(headers_frame, text="Value", width=20).pack(side='left')
        ttk.Label(headers_frame, text="Width", width=10).pack(side='left')
        
        # Create treeview for expected outputs
        self.expected_tree = ttk.Treeview(
            left_frame,
            columns=('value', 'width'),
            show='tree headings',
            selectmode='none'
        )
        self.expected_tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Configure columns
        self.expected_tree.column('#0', width=150)  # Signal name
        self.expected_tree.column('value', width=150)
        self.expected_tree.column('width', width=80)
        
        right_frame = ttk.LabelFrame(frame, text="Actual Outputs")
        right_frame.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        
        # Add headers for actual outputs
        headers_frame = ttk.Frame(right_frame)
        headers_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(headers_frame, text="Signal", width=20).pack(side='left')
        ttk.Label(headers_frame, text="Value", width=20).pack(side='left')
        ttk.Label(headers_frame, text="Width", width=10).pack(side='left')
        
        # Create treeview for actual outputs
        self.actual_tree = ttk.Treeview(
            right_frame,
            columns=('value', 'width'),
            show='tree headings',
            selectmode='none'
        )
        self.actual_tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Configure columns
        self.actual_tree.column('#0', width=150)  # Signal name
        self.actual_tree.column('value', width=150)
        self.actual_tree.column('width', width=80)
        
        return frame

    def _create_wave_tab(self) -> ttk.Frame:
        """Create tab for waveform display"""
        frame = ttk.Frame(self.detail_notebook)
        
        # Add canvas for waveform
        self.wave_canvas = tk.Canvas(
            frame,
            background='white'
        )
        self.wave_canvas.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Add "Open in GTKWave" button
        self.gtkwave_btn = ttk.Button(
            frame,
            text="Open in GTKWave",
            command=self._open_current_vcd
        )
        self.gtkwave_btn.pack(side='bottom', pady=5)
        
        return frame

    def _on_test_double_click(self, event):
        """Handle double-click on test case"""
        selection = self.test_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        test_name = self.test_tree.item(item)['text']  # Get test name from item text
        test_case = self.verifier.get_test_case(test_name) if hasattr(self, 'verifier') else None
        
        # Load compilation log
        log_file = os.path.join("vpx_outputs", f"{test_name}_compile.log")
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                self.log_text.delete('1.0', tk.END)
                self.log_text.insert('1.0', f.read())
        
        # Update expected vs actual comparison
        if test_case:
            # Clear previous data
            for tree in [self.expected_tree, self.actual_tree]:
                for item in tree.get_children():
                    tree.delete(item)
            
            # Get port info from verifier
            port_info = self.verifier._get_cached_module_info()['ports']
            
            # Add expected outputs
            for port in port_info:
                if port['direction'] == 'output':
                    name = port['name']
                    width = port['width']
                    expected_value = test_case.expected.get(name, 'x')
                    
                    # Format value based on width
                    if isinstance(width, int) and width > 1:
                        value_str = f"{width}'h{expected_value:x}" if isinstance(expected_value, int) else expected_value
                    else:
                        value_str = str(expected_value)
                    
                    # Add to expected tree with proper formatting
                    self.expected_tree.insert(
                        '', 'end',
                        text=name,
                        values=(value_str, width)
                    )
            
            # Add actual outputs
            if hasattr(test_case, 'actual'):
                for port in port_info:
                    if port['direction'] == 'output':
                        name = port['name']
                        width = port['width']
                        actual_value = test_case.actual.get(name, 'x')
                        
                        # Format value based on width
                        if isinstance(width, int) and width > 1:
                            value_str = f"{width}'h{actual_value:x}" if isinstance(actual_value, int) else actual_value
                        else:
                            value_str = str(actual_value)
                        
                        # Add to actual tree with proper formatting
                        self.actual_tree.insert(
                            '', 'end',
                            text=name,
                            values=(value_str, width)
                        )
        
        # Load and render waveform
        vcd_file = os.path.join("vpx_outputs", f"{test_name}.vcd")  # Use test_name instead of test_case.name
        if os.path.exists(vcd_file):
            self._render_waveform(vcd_file)
            self.gtkwave_btn.configure(state='normal')
            self.current_vcd = vcd_file
        else:
            self.wave_canvas.delete('all')
            self.wave_canvas.create_text(
                self.wave_canvas.winfo_width()/2,
                self.wave_canvas.winfo_height()/2,
                text="No waveform available",
                anchor='center'
            )
            self.gtkwave_btn.configure(state='disabled')
            self.current_vcd = None
        
        # Switch to detail view
        self.detail_notebook.select(0)  # Show log tab first

    def _render_waveform(self, vcd_file: str):
        """Render basic waveform visualization from VCD file"""
        try:
            # Clear canvas
            self.wave_canvas.delete('all')
            
            # Parse VCD file
            signals = {}
            current_time = 0
            with open(vcd_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Parse timestamp
                    if line.startswith('#'):
                        current_time = int(line[1:])
                        continue
                        
                    # Parse signal value changes
                    if line and line[0] in '01xz':
                        value = line[0]
                        signal = line[1:].strip()
                        if signal not in signals:
                            signals[signal] = []
                        signals[signal].append((current_time, value))
            
            # Draw waveforms
            y_spacing = 30
            x_scale = self.wave_canvas.winfo_width() / max(t for s in signals.values() for t,_ in s)
            
            for i, (signal_name, changes) in enumerate(signals.items()):
                y = (i + 1) * y_spacing
                
                # Draw signal name
                self.wave_canvas.create_text(10, y, text=signal_name, anchor='w')
                
                # Draw waveform
                prev_x = 50  # Start after signal name
                prev_y = y
                prev_value = '0'
                
                for time, value in changes:
                    x = 50 + time * x_scale
                    
                    # Draw vertical line for value change
                    if value != prev_value:
                        self.wave_canvas.create_line(x, y-10, x, y+10)
                    
                    # Draw horizontal line
                    y_offset = -10 if value == '1' else 10
                    self.wave_canvas.create_line(prev_x, prev_y + y_offset, x, y + y_offset)
                    
                    prev_x = x
                    prev_y = y
                    prev_value = value
            
            # Update canvas scroll region
            self.wave_canvas.configure(scrollregion=self.wave_canvas.bbox('all'))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to render waveform: {str(e)}")

    def _open_current_vcd(self):
        """Open current VCD file in GTKWave"""
        if self.current_vcd and os.path.exists(self.current_vcd):
            self._open_vcd_in_gtkwave(self.current_vcd)

    def _create_file_explorer(self) -> ttk.Frame:
        """Create file explorer panel"""
        frame = ttk.Frame(self.h_paned)
        
        # Add controls at top
        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(
            controls,
            text="↑ Up",
            command=self._go_up_directory
        ).pack(side='left', padx=2)
        
        ttk.Button(
            controls,
            text="⟳ Refresh",
            command=self._refresh_files
        ).pack(side='left', padx=2)
        
        self.path_var = tk.StringVar(value=os.getcwd())
        path_entry = ttk.Entry(controls, textvariable=self.path_var)
        path_entry.pack(side='left', fill='x', expand=True, padx=2)
        path_entry.bind('<Return>', lambda e: self._refresh_files())
        
        # Create treeview for files
        self.file_tree = ttk.Treeview(frame, selectmode='browse')
        self.file_tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.file_tree.yview)
        scrollbar.pack(fill='y', side='right')
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.file_tree["columns"] = ("size", "modified")
        self.file_tree.column("#0", width=200)  # Name column
        self.file_tree.column("size", width=70)
        self.file_tree.column("modified", width=120)
        
        self.file_tree.heading("#0", text="Name")
        self.file_tree.heading("size", text="Size")
        self.file_tree.heading("modified", text="Modified")
        
        # Bind double-click
        self.file_tree.bind('<Double-1>', self._on_file_double_click)
        
        # Initial file population
        self._refresh_files()
        
        return frame

    def _go_up_directory(self):
        """Navigate to parent directory"""
        current = self.path_var.get()
        parent = os.path.dirname(current)
        
        # Don't allow going above vpx_outputs
        vpx_outputs_path = os.path.join(os.getcwd(), "vpx_outputs")
        if parent.startswith(vpx_outputs_path):
            self.path_var.set(parent)
            self._refresh_files()

    def _refresh_files(self):
        """Refresh file list"""
        try:
            path = self.path_var.get()
            if not os.path.exists(path):
                return
                
            # Only allow navigation within vpx_outputs
            vpx_outputs_path = os.path.join(os.getcwd(), "vpx_outputs")
            if not path.startswith(vpx_outputs_path):
                self.path_var.set(vpx_outputs_path)
                path = vpx_outputs_path

            # Clear existing items
            self.file_tree.delete(*self.file_tree.get_children())
            
            # Add parent directory entry only if we're in a subdirectory of vpx_outputs
            if path != vpx_outputs_path:
                self.file_tree.insert(
                    "", 0,
                    text="..",
                    values=("", ""),
                    tags=("directory",)
                )
            
            # Get all items in directory
            items = sorted(os.listdir(path))
            
            # Add directories first
            for item in items:
                full_path = os.path.join(path, item)
                try:
                    stats = os.stat(full_path)
                    modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                    
                    if os.path.isdir(full_path):
                        self.file_tree.insert(
                            "", "end",
                            text=item,
                            values=("", modified),
                            tags=("directory",)
                        )
                except Exception:
                    continue
            
            # Then add files
            for item in items:
                full_path = os.path.join(path, item)
                try:
                    if os.path.isfile(full_path) and full_path.endswith(('.v', '.sv', '.vcd', '.log')):
                        stats = os.stat(full_path)
                        size = f"{stats.st_size/1024:.1f}K" if stats.st_size >= 1024 else f"{stats.st_size}B"
                        modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                        
                        self.file_tree.insert(
                            "", "end",
                            text=item,
                            values=(size, modified),
                            tags=("file",)
                        )
                except Exception:
                    continue
                    
            # Configure tags
            self.file_tree.tag_configure("directory", foreground="blue")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh files: {str(e)}")

    def _on_file_double_click(self, event):
        """Handle double-click on file tree item"""
        item = self.file_tree.selection()[0]
        text = self.file_tree.item(item, "text")
        
        if text == "..":
            self._go_up_directory()
            return
            
        path = os.path.join(self.path_var.get(), text)
        
        if os.path.isdir(path):
            self.path_var.set(path)
            self._refresh_files()
        elif os.path.isfile(path):
            if path.endswith('.vcd'):
                self._open_vcd_in_gtkwave(path)
            elif path.endswith(('.v', '.sv')):
                self.load_rtl_file(path)

    def _open_vcd_in_gtkwave(self, vcd_file: str):
        """Open VCD file in GTKWave"""
        try:
            # Check if GTKWave is installed
            try:
                subprocess.run(['gtkwave', '--version'], capture_output=True)
                gtkwave_installed = True
            except FileNotFoundError:
                gtkwave_installed = False

            if not gtkwave_installed:
                # Try to install GTKWave
                if messagebox.askyesno(
                    "GTKWave Not Found",
                    "GTKWave is not installed. Would you like to install it now?"
                ):
                    try:
                        # Detect OS and install accordingly
                        if os.name == 'posix':  # Linux/Unix/macOS
                            if os.path.exists('/usr/bin/apt'):  # Debian/Ubuntu
                                cmd = ['sudo', 'apt-get', 'install', '-y', 'gtkwave']
                                install_process = subprocess.Popen(
                                    cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                )
                            elif os.path.exists('/usr/bin/brew'):  # macOS with Homebrew
                                cmd = ['brew', 'install', 'gtkwave']
                                install_process = subprocess.Popen(
                                    cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                )
                            else:
                                messagebox.showerror(
                                    "Installation Failed",
                                    "Automatic installation is only supported on Debian/Ubuntu or macOS with Homebrew.\n"
                                    "Please install GTKWave manually."
                                )
                                return
                                
                            # Show installation progress
                            progress = ttk.Progressbar(
                                self,
                                mode='indeterminate'
                            )
                            progress.pack(fill='x', padx=20, pady=10)
                            progress.start()
                            
                            # Wait for installation to complete
                            stdout, stderr = install_process.communicate()
                            progress.stop()
                            progress.destroy()
                            
                            if install_process.returncode != 0:
                                messagebox.showerror(
                                    "Installation Failed",
                                    f"Failed to install GTKWave:\n{stderr.decode()}"
                                )
                                return
                                
                            messagebox.showinfo(
                                "Installation Complete",
                                "GTKWave has been installed successfully!"
                            )
                            gtkwave_installed = True
                            
                        elif os.name == 'nt':  # Windows
                            messagebox.showinfo(
                                "Manual Installation Required",
                                "Please download and install GTKWave from:\n"
                                "https://sourceforge.net/projects/gtkwave/files/\n\n"
                                "After installation, you may need to restart the application."
                            )
                            webbrowser.open('https://sourceforge.net/projects/gtkwave/files/')
                            return
                            
                        else:
                            messagebox.showerror(
                                "Unsupported OS",
                                "GTKWave installation is not supported on this operating system."
                            )
                            return
                    except Exception as e:
                        messagebox.showerror(
                            "Installation Failed",
                            f"Failed to install GTKWave:\n{str(e)}"
                        )
                        return
                else:
                    return

            # Create a save file for GTKWave
            gtkw_file = vcd_file.replace('.vcd', '.gtkw')
            with open(gtkw_file, 'w') as f:
                f.write(f"""[*]
[*] GTKWave Analyzer
[*] 
[dumpfile] "{os.path.abspath(vcd_file)}"
[dumpfile_mtime] "{os.path.getmtime(vcd_file)}"
[dumpfile_size] {os.path.getsize(vcd_file)}
[savefile] "{os.path.abspath(gtkw_file)}"
[timestart] 0
[size] 1200 600
[pos] -1 -1
*-16.000000 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
[sst_width] 200
[signals_width] 150
[sst_expanded] 1
[sst_vpaned_height] 150
""")
            
            # Launch GTKWave with save file
            subprocess.Popen(['gtkwave', '-a', gtkw_file, os.path.abspath(vcd_file)])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open VCD file: {str(e)}")

    def _load_rtl_dialog(self):
        filename = filedialog.askopenfilename(
            title="Open RTL File",
            filetypes=[("SystemVerilog Files", "*.sv"), ("Verilog Files", "*.v"), ("All Files", "*.*")]
        )
        if filename:
            self.load_rtl_file(filename)

    def _create_rtl_view_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        
        # Create horizontal paned window
        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(expand=True, fill='both')
        
        # Left side: RTL Text with line numbers
        left_frame = ttk.Frame(paned)
        
        # Create container for nav and search
        self.nav_container = ttk.Frame(left_frame)
        self.nav_container.pack(fill='x', padx=5, pady=2)
        
        # Navigation buttons in their own frame
        self.nav_frame = ttk.Frame(self.nav_container)
        self.nav_frame.pack(fill='x', side='top')
        
        ttk.Button(self.nav_frame, text="⟳", width=3, command=self._refresh_rtl).pack(side='left', padx=2)
        ttk.Button(self.nav_frame, text="⌕", width=3, command=self._show_search).pack(side='left', padx=2)
        
        # Search frame (hidden by default)
        self.search_frame = ttk.Frame(self.nav_container)
        ttk.Label(self.search_frame, text="Find:").pack(side='left', padx=2)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=2)
        search_entry.bind('<Return>', self._find_next)
        search_entry.bind('<Escape>', lambda e: self._hide_search())
        ttk.Button(self.search_frame, text="Next", command=self._find_next).pack(side='left', padx=2)
        ttk.Button(self.search_frame, text="×", width=3, 
                  command=self._hide_search).pack(side='left', padx=2)
        
        # Create text widget with line numbers
        text_frame = ttk.Frame(left_frame)
        text_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Line numbers text widget
        self.line_numbers = tk.Text(text_frame, width=6, padx=3, takefocus=0,
                                  border=0, background='lightgray',
                                  state='disabled')
        self.line_numbers.pack(side='left', fill='y')
        
        # Main text widget with scrollbar
        text_with_scroll = ttk.Frame(text_frame)
        text_with_scroll.pack(side='left', fill='both', expand=True)
        
        self.rtl_text = scrolledtext.ScrolledText(
            text_with_scroll, 
            wrap=tk.NONE,
            width=60, 
            height=30,
            font=('Courier', 10)
        )
        self.rtl_text.pack(expand=True, fill='both')
        
        # Configure tag for output signal highlighting - remove foreground color
        self.rtl_text.tag_configure('output_hover', background='#E0FFE0')  # Light green without alpha
        self.rtl_text.tag_configure('output_signal')  # No default color change
        
        # Add bindings for output signal interaction
        self.rtl_text.tag_bind('output_signal', '<Enter>', self._on_output_enter)
        self.rtl_text.tag_bind('output_signal', '<Leave>', self._on_output_leave)
        self.rtl_text.tag_bind('output_signal', '<Button-1>', self._on_output_click)
        
        # Add horizontal scrollbar
        h_scroll = ttk.Scrollbar(text_with_scroll, orient='horizontal', command=self.rtl_text.xview)
        h_scroll.pack(fill='x', side='bottom')
        self.rtl_text.configure(xscrollcommand=h_scroll.set)
        
        # Bind events for line numbers
        self.rtl_text.bind('<KeyRelease>', self._update_line_numbers)
        self.rtl_text.bind('<MouseWheel>', self._update_line_numbers)
        
        # Synchronize line numbers scroll with main text
        self.rtl_text.bind('<Configure>', self._update_line_numbers)
        self.rtl_text.bind('<<Modified>>', self._on_text_scroll)
        self.rtl_text.bind('<MouseWheel>', self._on_text_scroll)
        # Add bindings for Linux mouse wheel
        self.rtl_text.bind('<Button-4>', self._on_text_scroll)
        self.rtl_text.bind('<Button-5>', self._on_text_scroll)
        
        paned.add(left_frame)
        
        # Right side: Module Visualization
        right_frame = ttk.Frame(paned)
        
        # Add zoom controls
        zoom_frame = ttk.Frame(right_frame)
        zoom_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(zoom_frame, text="Zoom:").pack(side='left', padx=5)
        self.zoom_scale = ttk.Scale(
            zoom_frame, 
            from_=0.1, 
            to=2.0, 
            orient='horizontal',
            value=1.0,
            command=self._on_zoom_change
        )
        self.zoom_scale.pack(side='left', expand=True, fill='x', padx=5)
        
        # Reset view button
        ttk.Button(
            zoom_frame,
            text="Reset View",
            command=self._reset_view
        ).pack(side='left', padx=5)
        
        # Create canvas with scrollbars
        canvas_frame = ttk.Frame(right_frame)
        canvas_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        self.module_canvas = tk.Canvas(
            canvas_frame,
            background='white',
            scrollregion=(0, 0, 1000, 1000)  # Initial scroll region
        )
        
        # Add scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient='horizontal', command=self.module_canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.module_canvas.yview)
        
        # Configure canvas scrolling
        self.module_canvas.configure(
            xscrollcommand=h_scrollbar.set,
            yscrollcommand=v_scrollbar.set
        )
        
        # Grid layout for canvas and scrollbars
        self.module_canvas.grid(row=0, column=0, sticky='nsew')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Configure grid weights
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize view transform variables
        self.zoom_factor = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0
        
        # Bind mouse events for panning
        self.module_canvas.bind('<ButtonPress-1>', self._start_pan)
        self.module_canvas.bind('<B1-Motion>', self._pan)
        self.module_canvas.bind('<MouseWheel>', self._mouse_wheel)  # Windows/macOS
        self.module_canvas.bind('<Button-4>', self._mouse_wheel)    # Linux up
        self.module_canvas.bind('<Button-5>', self._mouse_wheel)    # Linux down
        
        paned.add(right_frame)
        return frame

    def _draw_grid(self):
        """Draw background grid"""
        # Clear existing grid
        self.module_canvas.delete('grid')
        
        # Get canvas dimensions
        width = self.module_canvas.winfo_width()
        height = self.module_canvas.winfo_height()
        
        # Calculate grid size based on zoom
        grid_size = 20 * self.zoom_factor
        
        # Draw vertical lines
        for x in range(0, width, int(grid_size)):
            self.module_canvas.create_line(
                x, 0, x, height,
                fill='#EEEEEE',
                tags='grid'
            )
            
        # Draw horizontal lines
        for y in range(0, height, int(grid_size)):
            self.module_canvas.create_line(
                0, y, width, y,
                fill='#EEEEEE',
                tags='grid'
            )

    def _start_pan(self, event):
        """Start panning"""
        self.module_canvas.scan_mark(event.x, event.y)
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def _pan(self, event):
        """Handle panning"""
        self.module_canvas.scan_dragto(event.x, event.y, gain=1)
        
    def _mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        if event.num == 5 or event.delta < 0:  # Zoom out
            self.zoom_factor = max(0.1, self.zoom_factor - 0.1)
        else:  # Zoom in
            self.zoom_factor = min(2.0, self.zoom_factor + 0.1)
            
        self.zoom_scale.set(self.zoom_factor)
        self._update_module_visualization()

    def _on_zoom_change(self, value):
        """Handle zoom slider change"""
        self.zoom_factor = float(value)
        self._update_module_visualization()

    def _reset_view(self):
        """Reset view to original position and zoom"""
        self.zoom_factor = 1.0
        self.zoom_scale.set(1.0)
        self.module_canvas.xview_moveto(0)
        self.module_canvas.yview_moveto(0)
        self._update_module_visualization()

    def _extract_module_ports(self, rtl_content: str) -> List[ModulePort]:
        ports = []
        # Find module declaration
        module_match = re.search(r'module\s+\w+\s*\((.*?)\);', rtl_content, re.DOTALL)
        if not module_match:
            return ports
            
        port_list = module_match.group(1)
        port_declarations = [p.strip() for p in port_list.split(',')]
        
        for decl in port_declarations:
            parts = decl.strip().split()
            if not parts:
                continue
                
            direction = parts[0] if parts[0] in ['input', 'output', 'inout'] else None
            if not direction:
                continue
                
            # Handle vector ports
            width = 1
            name = parts[-1].replace(';', '')
            width_match = re.search(r'\[(\d+):0\]', decl)
            if width_match:
                width = int(width_match.group(1)) + 1
                
            ports.append(ModulePort(name, direction, width))
            
        return ports

    def _update_module_visualization(self):
        """Draw module visualization directly on the canvas"""
        try:
            # Clear canvas
            self.module_canvas.delete('all')
            
            # Draw grid first
            self._draw_grid()
            
            # Get canvas dimensions
            canvas_width = self.module_canvas.winfo_width()
            canvas_height = self.module_canvas.winfo_height()
            
            # Extract and organize ports
            ports = self._extract_module_ports(self.rtl_text.get('1.0', tk.END))
            inputs = [p for p in ports if p.direction == 'input']
            outputs = [p for p in ports if p.direction == 'output']
            
            # Calculate dimensions based on number of ports
            num_ports = max(len(inputs), len(outputs))
            min_port_spacing = 25 * self.zoom_factor  # Reduced spacing
            required_height = (num_ports + 1) * min_port_spacing
            
            # Calculate scaling factor if needed
            scale = min(1.0, (canvas_height - 60) / required_height) * self.zoom_factor
            
            # Module box margins and dimensions
            margin_x = 60 * scale  # Reduced margins
            margin_y = 40 * scale
            box_width = min(canvas_width - 2 * margin_x, 300 * scale)  # Reduced width
            box_height = min(required_height * scale, canvas_height - 2 * margin_y)
            
            # Center the diagram
            x_offset = (canvas_width - box_width) / 2
            y_offset = (canvas_height - box_height) / 2
            
            # Get module name
            module_match = re.search(r'module\s+(\w+)', self.rtl_text.get('1.0', tk.END))
            module_name = module_match.group(1) if module_match else "Unknown Module"
            
            # Draw module box with name banner
            banner_height = 20 * scale  # Reduced banner height
            
            # Module box
            self.module_canvas.create_rectangle(
                x_offset, y_offset + banner_height,
                x_offset + box_width, y_offset + box_height,
                fill='white', outline='black', width=2
            )
            
            # Module name in center (instead of top)
            self.module_canvas.create_text(
                x_offset + box_width/2,  # Center X
                y_offset + banner_height + box_height/2,  # Center Y
                text=module_name,
                anchor='c',  # Center anchor
                font=('TkDefaultFont', min(14, int(14 * scale))),  # Slightly larger font
                fill='black'
            )
            
            # Calculate pin spacing
            pin_spacing = (box_height - banner_height) / (max(len(inputs), len(outputs)) + 1)
            
            # Draw input pins
            for i, port in enumerate(inputs, 1):
                y = y_offset + banner_height + i * pin_spacing
                
                # Pin circle
                pin_radius = 3 * scale
                self.module_canvas.create_oval(
                    x_offset - pin_radius, y - pin_radius,
                    x_offset + pin_radius, y + pin_radius,
                    fill='black'
                )
                
                # Connection line
                self.module_canvas.create_line(
                    x_offset - margin_x/2, y,
                    x_offset - pin_radius, y,
                    fill='black', width=1
                )
                
                # Port name (above line, made black)
                name_y = y - 12 * scale
                self.module_canvas.create_text(
                    x_offset - margin_x/4, name_y,
                    text=port.name,
                    anchor='s',
                    font=('TkDefaultFont', min(9, int(9 * scale))),
                    fill='black'  # Added explicit black color
                )
                
                # Width indicator (if needed)
                if port.width > 1:
                    self.module_canvas.create_text(
                        x_offset - margin_x/4, name_y - 10 * scale,
                        text=f'[{port.width-1}:0]',
                        anchor='s',
                        font=('TkDefaultFont', min(7, int(7 * scale))),
                        fill='blue'  # Keep width indicators blue for distinction
                    )
            
            # Draw output pins with clickable behavior
            for i, port in enumerate(outputs, 1):
                y = y_offset + banner_height + i * pin_spacing
                
                # Pin circle - make it clickable
                pin_radius = 3 * scale
                pin_id = self.module_canvas.create_oval(
                    x_offset + box_width - pin_radius, y - pin_radius,
                    x_offset + box_width + pin_radius, y + pin_radius,
                    fill='black',
                    tags=('pin', f'port_{port.name}')  # Add tags for identification
                )
                
                # Make the text clickable too
                name_y = y - 12 * scale
                text_id = self.module_canvas.create_text(
                    x_offset + box_width + margin_x/4, name_y,
                    text=port.name,
                    anchor='s',
                    font=('TkDefaultFont', min(9, int(9 * scale))),
                    fill='black',
                    tags=('pin', f'port_{port.name}')  # Add tags for identification
                )
                
                # Add hover effect and click handler
                for item_id in (pin_id, text_id):
                    self.module_canvas.tag_bind(f'port_{port.name}', '<Enter>', 
                        lambda e, p=port.name: self._highlight_port(p))
                    self.module_canvas.tag_bind(f'port_{port.name}', '<Leave>', 
                        lambda e, p=port.name: self._unhighlight_port(p))
                    self.module_canvas.tag_bind(f'port_{port.name}', '<Button-1>', 
                        lambda e, p=port.name: self._show_logic_cone_for_port(p))
                
                # Connection line
                self.module_canvas.create_line(
                    x_offset + box_width + pin_radius, y,
                    x_offset + box_width + margin_x/2, y,
                    fill='black', width=1
                )
                
                # Port name (above line, made black)
                name_y = y - 12 * scale
                self.module_canvas.create_text(
                    x_offset + box_width + margin_x/4, name_y,
                    text=port.name,
                    anchor='s',
                    font=('TkDefaultFont', min(9, int(9 * scale))),
                    fill='black'  # Added explicit black color
                )
                
                # Width indicator (if needed)
                if port.width > 1:
                    self.module_canvas.create_text(
                        x_offset + box_width + margin_x/4, name_y - 10 * scale,
                        text=f'[{port.width-1}:0]',
                        anchor='s',
                        font=('TkDefaultFont', min(7, int(7 * scale))),
                        fill='blue'  # Keep width indicators blue for distinction
                    )
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw module visualization: {str(e)}")

    def _highlight_port(self, port_name: str):
        """Highlight port on hover"""
        self.module_canvas.itemconfig(f'port_{port_name}', fill='red')

    def _unhighlight_port(self, port_name: str):
        """Remove highlight from port"""
        self.module_canvas.itemconfig(f'port_{port_name}', fill='black')

    
    def _show_logic_cone_for_port(self, port_name: str):
        """Show logic cone analysis as a detailed technical circuit diagram"""
        try:
            canvas_width = self.module_canvas.winfo_width()
            canvas_height = self.module_canvas.winfo_height()
            result = self.verifier.analyze_logic_cone(port_name)
            result['target_output'] = port_name

            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp_svg:
                dwg = svgwrite.Drawing(tmp_svg.name, size=(f"{canvas_width}px", f"{canvas_height}px"))
                
                # Technical diagram styling
                dwg.defs.add(dwg.style("""
                    .diagram-frame { stroke: #333; stroke-width: 1; fill: none; }
                    .grid { stroke: #eee; stroke-width: 0.5; }
                    .node { fill: white; stroke: #333; stroke-width: 1; }
                    .node-sequential { stroke-dasharray: 5,3; }
                    .node-title { font-family: "Courier New"; font-size: 12px; }
                    .node-details { font-family: "Courier New"; font-size: 10px; }
                    .timing-info { font-family: "Courier New"; font-size: 9px; fill: #666; }
                    .signal-path { stroke: #333; stroke-width: 1; fill: none; marker-end: url(#arrow); }
                    .signal-path-clk { stroke: #2196F3; stroke-dasharray: 5,3; }
                    .signal-path-rst { stroke: #F44336; stroke-dasharray: 2,2; }
                    .signal-label { font-family: "Courier New"; font-size: 10px; }
                    .vector-info { font-family: "Courier New"; font-size: 9px; fill: #666; }
                    .timing-marker { stroke: #666; stroke-width: 0.5; }
                    .propagation-delay { font-family: "Courier New"; font-size: 8px; fill: #666; }
                """))

                # Create technical arrow markers
                for marker_id, color in [('arrow', '#333'), ('arrow-clk', '#2196F3'), ('arrow-rst', '#F44336')]:
                    marker = dwg.marker(id=marker_id, insert=(0,0), size=(8,8), orient='auto')
                    marker.add(dwg.path(d='M0,0 L8,4 L0,8 z', fill=color))
                    dwg.defs.add(marker)

                # Draw reference grid
                grid_size = 20
                grid_group = dwg.g(class_='grid')
                for x in range(0, canvas_width, grid_size):
                    grid_group.add(dwg.line(start=(x, 0), end=(x, canvas_height)))
                for y in range(0, canvas_height, grid_size):
                    grid_group.add(dwg.line(start=(0, y), end=(canvas_width, y)))
                dwg.add(grid_group)

                # Organize nodes into technical layers
                MARGIN = 60
                USABLE_WIDTH = canvas_width - 2*MARGIN
                USABLE_HEIGHT = canvas_height - 2*MARGIN
                NODE_WIDTH = 180
                NODE_HEIGHT = 80

                layers = {
                    0: {  # Input layer
                        'nodes': result.get('inputs', {}).get('primary', []),
                        'title': 'Primary Inputs'
                    },
                    1: {  # Clock/Reset layer
                        'nodes': (result.get('inputs', {}).get('clocks', []) + 
                                result.get('inputs', {}).get('resets', [])),
                        'title': 'Clock/Reset Domain'
                    },
                    2: {  # Sequential layer
                        'nodes': result.get('trace', {}).get('sequential_elements', []),
                        'title': 'Sequential Logic'
                    },
                    3: {  # Combinational layer
                        'nodes': result.get('trace', {}).get('combinational_elements', []),
                        'title': 'Combinational Logic'
                    },
                    4: {  # Output layer
                        'nodes': [port_name],
                        'title': 'Output'
                    }
                }

                # Remove empty layers and calculate positions
                active_layers = {k: v for k, v in layers.items() if v['nodes']}
                layer_count = len(active_layers)
                LAYER_GAP = USABLE_HEIGHT / (layer_count + 1)

                # Store node positions for connections
                node_positions = {}

                # Draw technical layer labels and nodes
                for idx, (layer_num, layer_info) in enumerate(active_layers.items(), 1):
                    layer_y = MARGIN + idx * LAYER_GAP
                    
                    # Layer title with technical details
                    dwg.add(dwg.text(
                        layer_info['title'],
                        insert=(MARGIN/2, layer_y),
                        class_='node-title',
                        transform=f'rotate(-90, {MARGIN/2}, {layer_y})'
                    ))

                    # Position nodes in layer
                    nodes = sorted(set(layer_info['nodes']))
                    node_spacing = USABLE_WIDTH / (len(nodes) + 1)
                    
                    for i, node_id in enumerate(nodes, 1):
                        node_x = MARGIN + i * node_spacing
                        
                        # Create detailed technical node
                        node_group = self._create_technical_node(
                            dwg, node_id, node_x, layer_y, 
                            NODE_WIDTH, NODE_HEIGHT, result
                        )
                        dwg.add(node_group)
                        
                        # Store position for connections
                        node_positions[node_id] = {
                            'x': node_x,
                            'y': layer_y,
                            'layer': layer_num
                        }

                # Draw technical connections with timing information
                self._draw_technical_connections(
                    dwg, node_positions, result, LAYER_GAP
                )

                # Add technical diagram frame
                dwg.add(dwg.rect(
                    insert=(MARGIN/2, MARGIN/2),
                    size=(canvas_width - MARGIN, canvas_height - MARGIN),
                    class_='diagram-frame'
                ))

                # Add technical legend
                self._add_technical_legend(dwg, MARGIN, USABLE_HEIGHT + MARGIN)

                # Generate and display
                dwg.save()
                
                # Convert to PNG and display
                png_data = cairosvg.svg2png(url=tmp_svg.name)
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_png:
                    tmp_png.write(png_data)
                    tmp_png.flush()
                    
                    image = Image.open(tmp_png.name)
                    image = image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    self.module_canvas.delete('all')
                    self.module_canvas.create_image(0, 0, image=photo, anchor='nw')
                    self.module_canvas.image = photo
                    
                    self.module_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze logic cone: {str(e)}")
            raise

    def _create_technical_node(self, dwg, node_id: str, x: float, y: float, 
                            width: float, height: float, result: Dict) -> svgwrite.container.Group:
        """Create a detailed technical node with comprehensive information"""
        node = dwg.g(class_='node')
        
        # Determine node properties
        is_sequential = node_id in result.get('trace', {}).get('sequential_elements', [])
        deps = result.get('propagation', {}).get('dependencies', {}).get(node_id, {})
        vector_info = result.get('trace', {}).get('vector_dependencies', {}).get(node_id)
        
        # Create node rectangle
        rect_class = 'node node-sequential' if is_sequential else 'node'
        node.add(dwg.rect(
            insert=(x - width/2, y - height/2),
            size=(width, height),
            rx=2, ry=2,
            class_=rect_class
        ))
        
        # Add node title
        node.add(dwg.text(
            node_id,
            insert=(x, y - height/4),
            text_anchor='middle',
            class_='node-title'
        ))
        
        # Add comprehensive technical details
        details = []
        
        # Vector width information
        if vector_info:
            details.append(f"Width: {vector_info}")
        
        # Clock domain
        if deps.get('clk_deps'):
            details.append(f"Clock: {', '.join(deps['clk_deps'])}")
        
        # Reset signals
        if deps.get('rst_deps'):
            details.append(f"Reset: {', '.join(deps['rst_deps'])}")
        
        # Dependencies count
        if deps.get('deps'):
            details.append(f"Deps: {len(deps['deps'])}")
        
        # Add all details
        for i, detail in enumerate(details):
            node.add(dwg.text(
                detail,
                insert=(x, y + (i-len(details)/2)*12),
                text_anchor='middle',
                class_='node-details'
            ))
        
        return node

    def _draw_technical_connections(self, dwg, node_positions: Dict, 
                                result: Dict, layer_gap: float):
        """Draw technical connections with timing and signal information"""
        drawn = set()
        
        for target, info in result.get('propagation', {}).get('dependencies', {}).items():
            if target not in node_positions:
                continue
                
            target_pos = node_positions[target]
            
            for dep in info.get('deps', []):
                if dep not in node_positions or (dep, target) in drawn:
                    continue
                    
                source_pos = node_positions[dep]
                
                # Determine connection type
                is_clock = dep in info.get('clk_deps', [])
                is_reset = dep in info.get('rst_deps', [])
                
                # Calculate control points for proper technical routing
                path = self._calculate_technical_path(
                    source_pos, target_pos, layer_gap
                )
                
                # Add connection with appropriate style
                class_name = ('signal-path-clk' if is_clock else
                            'signal-path-rst' if is_reset else
                            'signal-path')
                
                marker_id = ('arrow-clk' if is_clock else
                            'arrow-rst' if is_reset else
                            'arrow')
                
                dwg.add(dwg.path(
                    d=path,
                    class_=class_name,
                    marker_end=f'url(#{marker_id})'
                ))
                
                # Add timing information if available
                if 'timing' in result:
                    self._add_timing_marker(
                        dwg, source_pos, target_pos, result['timing']
                    )
                
                drawn.add((dep, target))

    def _calculate_technical_path(self, source: Dict, target: Dict, 
                                layer_gap: float) -> str:
        """Calculate technical path with proper routing"""
        x1, y1 = source['x'], source['y']
        x2, y2 = target['x'], target['y']
        
        # Calculate control points for proper routing
        if abs(y2 - y1) > layer_gap:
            # Route with vertical segments
            return (f"M {x1},{y1} "
                    f"V {y1 + (y2-y1)/2} "
                    f"H {x2} "
                    f"V {y2}")
        else:
            # Direct diagonal route
            return f"M {x1},{y1} L {x2},{y2}"

    def _add_timing_marker(self, dwg, source: Dict, target: Dict, 
                        timing_info: Dict):
        """Add timing information to connection"""
        x1, y1 = source['x'], source['y']
        x2, y2 = target['x'], target['y']
        
        # Calculate midpoint
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        
        # Add timing marker
        dwg.add(dwg.circle(
            center=(mx, my),
            r=3,
            class_='timing-marker'
        ))
        
        # Add propagation delay if available
        if 'levels' in timing_info:
            delay = f"t={timing_info['levels']}Δ"
            dwg.add(dwg.text(
                delay,
                insert=(mx + 5, my - 5),
                class_='propagation-delay'
            ))

    def _add_technical_legend(self, dwg, x: float, y: float):
        """Add comprehensive technical legend"""
        legend = dwg.g(transform=f'translate({x}, {y})')
        
        items = [
            ("Sequential Logic", "node node-sequential"),
            ("Combinational Logic", "node"),
            ("Clock Domain", "signal-path-clk"),
            ("Reset Signal", "signal-path-rst"),
            ("Data Path", "signal-path"),
            ("Timing Marker", "timing-marker")
        ]
        
        for i, (label, class_name) in enumerate(items):
            legend.add(dwg.text(
                label,
                insert=(60, i*20),
                class_='node-details'
            ))
            
            if 'node' in class_name:
                legend.add(dwg.rect(
                    insert=(10, i*20-10),
                    size=(40, 15),
                    class_=class_name
                ))
            elif 'signal-path' in class_name:
                legend.add(dwg.line(
                    start=(10, i*20-5),
                    end=(50, i*20-5),
                    class_=class_name
                ))
            elif class_name == 'timing-marker':
                legend.add(dwg.circle(
                    center=(30, i*20-5),
                    r=3,
                    class_=class_name
                ))
        
        dwg.add(legend)

    def _get_node_style(self, node_id: str, result: Dict) -> Dict[str, str]:
        """Get the style information for a node based on its type"""
        styles = {
            'clock': {
                'fill': '#e3f2fd',
                'stroke': '#0277bd'
            },
            'reset': {
                'fill': '#ffebee',
                'stroke': '#c62828'
            },
            'sequential': {
                'fill': '#e8eaf6',
                'stroke': '#3f51b5'
            },
            'combinational': {
                'fill': '#e8f5e9',
                'stroke': '#2e7d32'
            },
            'input': {
                'fill': '#f3e5f5',
                'stroke': '#6a1b9a'
            },
            'output': {
                'fill': '#fff3e0',
                'stroke': '#e65100'
            },
            'default': {
                'fill': '#f5f5f5',
                'stroke': '#616161'
            }
        }
        
        try:
            # Safely get critical path
            critical_path = result.get('propagation', {}).get('critical_path', [])
            
            # Check node type
            if node_id in result.get('inputs', {}).get('clocks', []):
                return styles['clock']
            elif node_id in result.get('inputs', {}).get('resets', []):
                return styles['reset']
            elif node_id in result.get('inputs', {}).get('primary', []):
                return styles['input']
            elif node_id in result.get('trace', {}).get('sequential_elements', []):
                return styles['sequential']
            elif node_id in result.get('trace', {}).get('combinational_elements', []):
                return styles['combinational']
            elif critical_path and node_id == critical_path[-1]:
                return styles['output']
            
            # If it's the original port we're analyzing, mark it as output
            elif node_id == result.get('target_output', '') or node_id in result.get('outputs', []):
                return styles['output']
                
        except Exception as e:
            print(f"Warning: Error determining node style for {node_id}: {str(e)}")
        
        return styles['default']

    def _draw_svg_node(self, dwg, x: float, y: float, signal: str, node_type: str, 
                      deps: Dict[str, Any], width: float, height: float) -> svgwrite.container.Group:
        """Draw a single node in the logic cone with detailed dependency info"""
        bg_color, text_color = self.COLORS.get(node_type, self.COLORS['default'])
        
        node = dwg.g(class_='node')
        
        # Draw node box
        node.add(dwg.rect(
            insert=(x, y),
            size=(width, height),
            fill=bg_color,
            stroke=text_color,
            class_='node'
        ))
        
        # Add signal name
        node.add(dwg.text(
            signal,
            insert=(x + width/2, y + height/4),
            text_anchor='middle',
            fill=text_color,
            class_='node-title'
        ))
        
        # Add dependency info
        y_offset = y + height/2
        line_height = height/4
        
        if deps:
            # Show clock dependencies
            if deps.get('clk_deps'):
                clk_text = f"CLK: {', '.join(deps['clk_deps'])}"
                node.add(dwg.text(
                    clk_text,
                    insert=(x + width/2, y_offset),
                    text_anchor='middle',
                    class_='dep-info',
                    fill='blue'
                ))
                y_offset += line_height
            
            # Show reset dependencies
            if deps.get('rst_deps'):
                rst_text = f"RST: {', '.join(deps['rst_deps'])}"
                node.add(dwg.text(
                    rst_text,
                    insert=(x + width/2, y_offset),
                    text_anchor='middle',
                    class_='dep-info',
                    fill='red'
                ))
                y_offset += line_height
            
            # Show vector dependencies if any
            if deps.get('vector_deps'):
                vec_deps = [f"{d}[{i}]" for d, i in deps['vector_deps']]
                if vec_deps:
                    vec_text = f"Vec: {', '.join(vec_deps)}"
                    node.add(dwg.text(
                        vec_text,
                        insert=(x + width/2, y_offset),
                        text_anchor='middle',
                        class_='dep-info',
                        fill=text_color
                    ))
        
        return node

    def _draw_svg_connection(self, dwg, start: Tuple[float, float], end: Tuple[float, float], 
                            conn_type: str, vector_idx: Optional[str] = None):
        """Draw a connection between nodes with improved routing and highlighting"""
        x1, y1 = start
        x2, y2 = end
        
        # Calculate intermediate points for better routing
        mid_y = y1 - (y1 - y2) * 0.5
        
        # Create path with clean orthogonal routing
        path_data = [
            'M', x1, y1,           # Start
            'L', x1, mid_y,        # Go up
            'L', x2, mid_y,        # Go across
            'L', x2, y2            # Go up to target
        ]
        
        # Add highlight effect for the connection
        if conn_type != 'data-arrow':
            # Add glow effect for clock and reset connections
            glow_color = 'rgba(0,0,255,0.2)' if conn_type == 'clock-arrow' else 'rgba(255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2)'
            glow = dwg.path(
                d=' '.join(str(x) for x in path_data),
                class_='connection-glow',
                stroke=glow_color,
                stroke_width='6px',
                fill='none'
            )
            dwg.add(glow)
        
        # Draw main connection
        path = dwg.path(
            d=' '.join(str(x) for x in path_data),
            class_=f'arrow {conn_type}',
            fill='none'
        )
        dwg.add(path)
        
        # Add vector index if present
        if vector_idx is not None:
            # Create background for better visibility
            dwg.add(dwg.rect(
                insert=(x1 + (x2 - x1)/2 - 15, mid_y - 12),
                size=(30, 16),
                fill='white',
                stroke=path.get_style('stroke')
            ))
            # Add vector index text
            dwg.add(dwg.text(
                f'[{vector_idx}]',
                insert=(x1 + (x2 - x1)/2, mid_y - 2),
                text_anchor='middle',
                class_='vector-index'
            ))

    def _create_test_vectors_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        
        # Controls
        controls_frame = ttk.LabelFrame(frame, text="Generation Controls")
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Number of Vectors:").pack(side='left', padx=5)
        self.num_vectors = ttk.Spinbox(controls_frame, from_=1, to=100, width=5)
        self.num_vectors.set(20)
        self.num_vectors.pack(side='left', padx=5)
        
        ttk.Button(controls_frame, text="Generate", command=self._generate_test_vectors).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Save...", command=self._save_test_vectors).pack(side='left', padx=5)
        
        # Vectors Table
        table_frame = ttk.LabelFrame(frame, text="Generated Vectors")
        table_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create treeview for vectors
        self.vectors_tree = ttk.Treeview(table_frame)
        self.vectors_tree.pack(expand=True, fill='both', side='left')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.vectors_tree.yview)
        scrollbar.pack(fill='y', side='right')
        self.vectors_tree.configure(yscrollcommand=scrollbar.set)
        
        return frame

    def _create_testbench_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        
        # Controls
        controls_frame = ttk.LabelFrame(frame, text="Testbench Controls")
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Load Vectors...", command=self._load_test_vectors).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Generate", command=self._generate_testbench).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Save...", command=self._save_testbench).pack(side='left', padx=5)
        
        # Testbench View
        tb_frame = ttk.LabelFrame(frame, text="Generated Testbench")
        tb_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        self.testbench_text = scrolledtext.ScrolledText(tb_frame, wrap=tk.WORD, width=80, height=25)
        self.testbench_text.pack(expand=True, fill='both', padx=5, pady=5)
        
        return frame

    def _load_rtl(self):
        filename = filedialog.askopenfilename(
            title="Open RTL File",
            filetypes=[("SystemVerilog Files", "*.sv"), ("Verilog Files", "*.v"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    rtl_content = f.read()
                self.rtl_file = filename
                self.rtl_text.delete('1.0', tk.END)
                self.rtl_text.insert('1.0', rtl_content)
                
                # Ask user if they want to import Python model
                if messagebox.askyesno(
                    "Import Python Model",
                    "Would you like to import a Python model of the RTL for model-based checking?"
                ):
                    # Open file dialog for Python file selection
                    py_file = filedialog.askopenfilename(
                        title="Select Python Model File",
                        filetypes=[("Python files", "*.py"), ("All files", "*.*")]
                    )
                    py_model_path = py_file if py_file else None
                else:
                    py_model_path = None
                
                # Initialize verifier
                self.verifier = DesignVerifier(
                    context=None,
                    rtl=rtl_content,
                    verbose=True,
                    py_model_file_path=py_model_path
                )
                
                messagebox.showinfo("Success", "RTL file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load RTL file: {str(e)}")

    def _generate_test_vectors(self):
        if not self.verifier:
            messagebox.showerror("Error", "Please load an RTL file first!")
            return
            
        try:
            num = int(self.num_vectors.get())
            vectors = self.verifier.generate_test_vectors(num)
            
            # Clear existing items
            self.vectors_tree.delete(*self.vectors_tree.get_children())
            
            # Configure columns
            if vectors:
                # Get all signal names from first vector
                signals = list(vectors[0].keys())
                self.vectors_tree["columns"] = signals
                
                # Configure columns
                self.vectors_tree.column("#0", width=80, stretch=tk.NO)  # Vector number column
                self.vectors_tree.heading("#0", text="Vector #")
                
                for signal in signals:
                    self.vectors_tree.column(signal, width=100)
                    self.vectors_tree.heading(signal, text=signal)
                
                # Add vectors to tree
                for i, vector in enumerate(vectors, 1):
                    values = [vector[signal] for signal in signals]
                    self.vectors_tree.insert("", "end", text=f"Vector {i}", values=values)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate test vectors: {str(e)}")

    def _save_test_vectors(self):
        if not self.vectors_tree.get_children():
            messagebox.showerror("Error", "No test vectors to save!")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Test Vectors",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            try:
                # Get column headers
                headers = self.vectors_tree["columns"]
                
                # Get all vectors
                vectors = []
                for item in self.vectors_tree.get_children():
                    values = self.vectors_tree.item(item)["values"]
                    vectors.append(dict(zip(headers, values)))
                
                # Save as CSV
                import csv
                with open(filename, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(vectors)
                    
                messagebox.showinfo("Success", "Test vectors saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save test vectors: {str(e)}")

    def _load_test_vectors(self):
        filename = filedialog.askopenfilename(
            title="Load Test Vectors",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                # TODO: Parse test vectors file format
                messagebox.showinfo("Success", "Test vectors loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load test vectors: {str(e)}")

    def _generate_testbench(self):
        if not self.verifier:
            messagebox.showerror("Error", "Please load an RTL file first!")
            return
            
        try:
            # Generate a single test vector if none loaded
            test_vector = self.verifier.generate_test_vectors(1)[0]
            testbench = self.verifier.generate_testbench(test_vector)
            log = self.verifier.generate_test_log(test_vector)
            
            self.testbench_text.delete('1.0', tk.END)
            self.testbench_text.insert('1.0', testbench)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate testbench: {str(e)}")

    def _save_testbench(self):
        content = self.testbench_text.get('1.0', tk.END).strip()
        if not content:
            messagebox.showerror("Error", "No testbench to save!")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Testbench",
            defaultextension=".sv",
            filetypes=[("SystemVerilog Files", "*.sv"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                messagebox.showinfo("Success", "Testbench saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save testbench: {str(e)}")

    def _show_test_vectors_tab(self):
        self.notebook.select(self.test_vectors_tab)

    def _show_testbench_tab(self):
        self.notebook.select(self.testbench_tab) 

    def load_rtl_file(self, filename: str):
        """Load an RTL file programmatically"""
        try:
            with open(filename, 'r') as f:
                rtl_content = f.read()
            self.rtl_file = filename
            self.rtl_text.delete('1.0', tk.END)
            self.rtl_text.insert('1.0', rtl_content)
            
            # Ask user if they want to import Python model
            if messagebox.askyesno(
                "Import Python Model",
                "Would you like to import a Python model of the RTL for model-based checking?"
            ):
                # Open file dialog for Python file selection
                py_file = filedialog.askopenfilename(
                    title="Select Python Model File",
                    filetypes=[("Python files", "*.py"), ("All files", "*.*")]
                )
                py_model_path = py_file if py_file else None
            else:
                py_model_path = None
            
            # Initialize verifier with verbose=True
            self.verifier = DesignVerifier(
                context=None, 
                rtl=rtl_content,
                verbose=True,  # Set verbose to True
                py_model_file_path=py_model_path
            )
            
            # Highlight output signals
            self._highlight_output_signals()
            
            # Update module visualization
            self._update_module_visualization()
            
            # Update file label
            self.file_label.config(text=f"Loaded: {os.path.basename(filename)}")
            
            # Switch to RTL view tab
            self.notebook.select(self.rtl_view_tab)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load RTL file: {str(e)}")

    def set_explorer_path(self, path: str):
        """Set the file explorer path"""
        if os.path.exists(path):
            self.path_var.set(path)
            self._refresh_files()

    def set_explorer_filter(self, filter_paths: List[str]):
        """Set files to show in explorer"""
        self.filter_paths = set(os.path.abspath(p) for p in filter_paths)
        self._refresh_files()

    def _update_line_numbers(self, event=None):
        """Update line numbers"""
        def count_lines(widget):
            text = widget.get('1.0', 'end-1c')
            return len(text.split('\n'))
            
        final_index = self.rtl_text.index('end-1c')
        num_lines = int(final_index.split('.')[0])
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        for i in range(1, num_lines + 1):
            self.line_numbers.insert(tk.END, f'{i}\n')
        self.line_numbers.config(state='disabled')
        
        # Synchronize scroll position
        self.line_numbers.yview_moveto(self.rtl_text.yview()[0])

    def _on_text_scroll(self, *args):
        """Synchronize line numbers scroll with main text"""
        self.line_numbers.yview_moveto(self.rtl_text.yview()[0])

    def _show_search(self):
        """Show search bar"""
        self.search_frame.pack(fill='x', side='top')
        self.search_frame.focus_set()

    def _hide_search(self, event=None):
        """Hide search bar"""
        self.search_frame.pack_forget()
        self.rtl_text.focus_set()

    def _find_next(self, event=None):
        """Find next occurrence of search text"""
        search_text = self.search_var.get()
        if not search_text:
            return
            
        # Remove previous highlights
        self.rtl_text.tag_remove('search', '1.0', tk.END)
        
        # Start from current cursor position
        start_pos = self.rtl_text.index(tk.INSERT)
        pos = self.rtl_text.search(search_text, start_pos, tk.END)
        
        if not pos:
            # If not found from cursor, try from beginning
            pos = self.rtl_text.search(search_text, '1.0', tk.END)
            
        if pos:
            # Calculate end position
            line, col = pos.split('.')
            end_pos = f'{line}.{int(col) + len(search_text)}'
            
            # Highlight found text
            self.rtl_text.tag_add('search', pos, end_pos)
            self.rtl_text.tag_config('search', background='yellow')
            
            # Move cursor and ensure visible
            self.rtl_text.mark_set(tk.INSERT, end_pos)
            self.rtl_text.see(pos)
            
            # Set focus back to search entry
            self.search_frame.focus_set()
        else:
            messagebox.showinfo("Not Found", f"No occurrences of '{search_text}' found.")

    def _refresh_rtl(self):
        """Refresh RTL view"""
        if self.rtl_file and os.path.exists(self.rtl_file):
            self.load_rtl_file(self.rtl_file)

    def _highlight_output_signals(self):
        """Find and highlight output signals in RTL text"""
        # Clear existing tags
        self.rtl_text.tag_remove('output_signal', '1.0', tk.END)
        self.rtl_text.tag_remove('output_hover', '1.0', tk.END)
        
        # Find output declarations - modified pattern to catch more cases
        content = self.rtl_text.get('1.0', tk.END)
        output_pattern = r'^.*\boutput\b.*?(\w+)\s*(?:,|;|$)'  # Match entire line with output
        
        for line_num, line in enumerate(content.split('\n'), 1):
            matches = re.finditer(output_pattern, line, re.MULTILINE)
            for match in matches:
                signal_name = match.group(1)
                # Add tag to entire line without changing color
                line_start = f"{line_num}.0"
                line_end = f"{line_num}.end"
                self.rtl_text.tag_add('output_signal', line_start, line_end)

    def _on_output_enter(self, event):
        """Handle mouse enter on output signal"""
        index = self.rtl_text.index(f"@{event.x},{event.y}")
        line_start = self.rtl_text.index(f"{index} linestart")
        line_end = self.rtl_text.index(f"{index} lineend")
        
        # Check if line has output_signal tag
        if 'output_signal' in self.rtl_text.tag_names(index):
            # Add hover highlight to entire line
            self.rtl_text.tag_add('output_hover', line_start, line_end)

    def _on_output_leave(self, event):
        """Handle mouse leave from output signal"""
        # Remove hover highlight
        self.rtl_text.tag_remove('output_hover', '1.0', tk.END)

    def _on_output_click(self, event):
        """Handle click on output signal"""
        index = self.rtl_text.index(f"@{event.x},{event.y}")
        if 'output_signal' in self.rtl_text.tag_names(index):
            # Extract signal name from the line
            line = self.rtl_text.get(f"{index} linestart", f"{index} lineend")
            match = re.search(r'\boutput\b.*?(\w+)\s*(?:,|;|$)', line)
            if match:
                signal_name = match.group(1)
                self._show_logic_cone_for_port(signal_name)

    def _draw_legend_item(self, x: int, y: int, text: str, node_type: str):
        """Draw a legend item with consistent styling"""
        bg_color, text_color = self.COLORS.get(node_type, self.COLORS['default'])
        
        # Draw small rectangle for legend
        LEGEND_WIDTH = 120
        LEGEND_HEIGHT = 30
        
        self.module_canvas.create_rectangle(
            x, y, 
            x + LEGEND_WIDTH, y + LEGEND_HEIGHT,
            fill=bg_color, outline=text_color,
            width=2
        )
        
        # Add text
        self.module_canvas.create_text(
            x + LEGEND_WIDTH/2, y + LEGEND_HEIGHT/2,
            text=text,
            fill=text_color,
            font=('TkDefaultFont', 8, 'bold')
        )

    def load_implementation_context(self, context):
        """Load implementation context from Diann"""
        if not context:
            return
            
        # Create new tab for implementation details
        self.impl_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.impl_tab, text="Implementation")
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(self.impl_tab)
        text_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        self.impl_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=('Courier', 10)
        )
        self.impl_text.pack(expand=True, fill='both')
        
        # Format and display implementation details
        self._display_implementation_details(context)
        
        # Switch to implementation tab
        self.notebook.select(self.impl_tab)

    def _display_implementation_details(self, context):
        """Format and display implementation details"""
        self.impl_text.delete('1.0', tk.END)
        
        # Module Interface
        if context.requirements and context.requirements.module_interface:
            self.impl_text.insert(tk.END, "=== Module Interface ===\n\n")
            self.impl_text.insert(tk.END, context.requirements.module_interface)
            self.impl_text.insert(tk.END, "\n\n")
        
        # Components
        if context.requirements and context.requirements.components:
            self.impl_text.insert(tk.END, "=== Components ===\n\n")
            self.impl_text.insert(tk.END, context.requirements.components)
            self.impl_text.insert(tk.END, "\n\n")
        
        # Timing
        if context.timing_plan:
            self.impl_text.insert(tk.END, "=== Timing ===\n\n")
            if context.timing_plan.cycle_diagram:
                self.impl_text.insert(tk.END, "Cycle Diagram:\n")
                self.impl_text.insert(tk.END, context.timing_plan.cycle_diagram)
                self.impl_text.insert(tk.END, "\n\n")
            if context.timing_plan.register_deps:
                self.impl_text.insert(tk.END, "Register Dependencies:\n")
                self.impl_text.insert(tk.END, context.timing_plan.register_deps)
                self.impl_text.insert(tk.END, "\n\n")
            if context.timing_plan.critical_paths:
                self.impl_text.insert(tk.END, "Critical Paths:\n")
                self.impl_text.insert(tk.END, context.timing_plan.critical_paths)
                self.impl_text.insert(tk.END, "\n\n")
        
        # FSM
        if context.fsm_plan:
            self.impl_text.insert(tk.END, "=== FSM ===\n\n")
            if context.fsm_plan.state_info:
                self.impl_text.insert(tk.END, "State Information:\n")
                self.impl_text.insert(tk.END, context.fsm_plan.state_info)
                self.impl_text.insert(tk.END, "\n\n")
            if context.fsm_plan.output_logic:
                self.impl_text.insert(tk.END, "Output Logic:\n")
                self.impl_text.insert(tk.END, context.fsm_plan.output_logic)
                self.impl_text.insert(tk.END, "\n\n")
        
        # Make text read-only
        self.impl_text.configure(state='disabled')

    def generate_timing_vcd(self, timing_plan) -> Optional[str]:
        """Generate VCD file from timing plan"""
        if not timing_plan or not timing_plan.cycle_diagram:
            return None
            
        try:
            # Create temporary VCD file
            vcd_file = tempfile.NamedTemporaryFile(suffix='.vcd', delete=False)
            
            # Parse timing diagram
            signals = self._parse_timing_diagram(timing_plan.cycle_diagram)
            
            # Write VCD file
            with vcd.VCDWriter(vcd_file, timescale='1 ns', date=datetime.now()) as writer:
                # Register signals
                var_ids = {}
                for signal_name in signals.keys():
                    var_ids[signal_name] = writer.register_var(
                        scope='top',
                        name=signal_name,
                        var_type='wire',
                        size=1,
                        init=0
                    )
                
                # Write signal changes
                timestamp = 0
                first_signal = next(iter(signals.values()))  # Get first signal's values
                for i in range(len(first_signal)):  # Use length of first signal
                    for signal_name, values in signals.items():
                        writer.change(var_ids[signal_name], timestamp, values[i])
                    timestamp += 10  # 10ns per cycle
            
            return vcd_file.name
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate VCD file: {str(e)}")
            return None

    def _parse_timing_diagram(self, diagram: str) -> Dict[str, List[int]]:
        """Parse timing diagram into signal values"""
        signals = {}
        
        # Split into lines and process each signal
        lines = diagram.strip().split('\n')
        for line in lines:
            if '|' not in line:
                continue
                
            # Extract signal name and values
            parts = line.split('|')
            if len(parts) < 2:
                continue
                
            signal_name = parts[0].strip()
            if not signal_name:
                continue
                
            # Convert waveform to values
            values = []
            for char in ''.join(parts[1:]):
                if char in '01':
                    values.append(int(char))
                elif char == 'x':
                    values.append(0)  # Treat x as 0 for VCD
            
            if values:
                signals[signal_name] = values
                
        return signals

    def update_verification_progress(self, stage: str, details: Dict[str, Any]):
        """Update verification progress in GUI"""
        # Update status
        self.status_var.set(f"Stage: {stage}")
        
        # Update progress text
        if details.get('status'):
            self.progress_text.insert(tk.END, f"\n[{stage}] {details['status']}\n")
            self.progress_text.see(tk.END)
        
        # Handle test case updates
        if details.get('action') == 'start_test':
            test = details['test']
            self.progress_text.insert(tk.END, f"Running test: {test.name}\n")
            self.progress_text.see(tk.END)
            
        elif details.get('action') == 'test_complete':
            test = details['test']
            result = details['result']
            
            # Format coverage info
            coverage = result.get('coverage', {})
            coverage_str = f"L:{coverage.get('line', 0):.0f}% B:{coverage.get('branch', 0):.0f}% "
            coverage_str += f"F:{coverage.get('fsm', 0):.0f}% T:{coverage.get('toggle', 0):.0f}%"
            
            # Check if VCD file exists
            vcd_file = os.path.join("vpx_outputs", f"{test.name}.vcd")
            vcd_status = "Found" if os.path.exists(vcd_file) else "Not found"
            
            # Add to test results tree
            item_id = self.test_tree.insert(
                '',
                'end',
                text=test.name,
                values=(
                    test.type.name if hasattr(test.type, 'name') else str(test.type),
                    '✓' if result.get('passed', False) else '✗',
                    self.format_dict(test.inputs),
                    coverage_str,
                    vcd_status,
                    test.description,
                    result.get('error', ''),
                    ''  # Empty value for test_case column
                ),
                tags=('failed',) if not result.get('passed', False) else ()
            )
            
            # Store test case object in tree item
            self.test_tree.set(item_id, 'test_case', test)
            
            # Auto-scroll to bottom
            self.test_tree.see(item_id)
        
        # Update hierarchy if new files are generated
        if details.get('file_generated'):
            for item in self.hierarchy_tree.get_children():
                if self.hierarchy_tree.item(item)["text"] == "VCD Files":
                    vcd_node = item
                    # Add new VCD file
                    basename = os.path.basename(details['file_generated'])
                    if basename.endswith('.vcd'):
                        self.hierarchy_tree.insert(vcd_node, "end", text=basename, values=("file",))
                    break
        
        # Update GUI
        self.update()

    def format_dict(self, d: Dict) -> str:
        """Format dictionary values as comma-separated string"""
        if not d:
            return ""
        return ", ".join(str(v) for v in d.values())

    def load_rtl_files(self, files: List[str]):
        """Load multiple RTL files"""
        try:
            # Combine RTL content
            rtl_content = ""
            for file in files:
                with open(file, 'r') as f:
                    rtl_content += f.read() + "\n"
                    
            # Initialize verifier
            self.verifier = DesignVerifier(
                context=None,
                rtl=rtl_content,
                verbose=True
            )
                
            # Update status
            self.status_var.set(f"Loaded {len(files)} RTL files")
            
            # Clear any previous results
            if hasattr(self, 'test_tree'):
                for item in self.test_tree.get_children():
                    self.test_tree.delete(item)
            
            if hasattr(self, 'progress_text'):
                self.progress_text.delete('1.0', tk.END)
                self.progress_text.insert(tk.END, f"Loaded RTL files:\n")
                for file in files:
                    self.progress_text.insert(tk.END, f"- {os.path.basename(file)}\n")
                
            # Update file hierarchy
            self._update_hierarchy(files)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load RTL files: {str(e)}")

    def _update_hierarchy(self, files: List[str]):
        """Update file hierarchy tree"""
        # Clear existing items
        for item in self.hierarchy_tree.get_children():
            self.hierarchy_tree.delete(item)
        
        # Add root node for project
        project_node = self.hierarchy_tree.insert("", "end", text="Project", values=("project",))
        
        # Add RTL files
        rtl_node = self.hierarchy_tree.insert(project_node, "end", text="RTL Files", values=("folder",))
        for file in files:
            basename = os.path.basename(file)
            self.hierarchy_tree.insert(rtl_node, "end", text=basename, values=("file",))
        
        # Add outputs node
        outputs_node = self.hierarchy_tree.insert(project_node, "end", text="Outputs", values=("folder",))
        
        # Add VCD files node
        vcd_node = self.hierarchy_tree.insert(outputs_node, "end", text="VCD Files", values=("folder",))
        
        # Expand all nodes
        self.hierarchy_tree.item(project_node, open=True)
        self.hierarchy_tree.item(rtl_node, open=True)
        self.hierarchy_tree.item(outputs_node, open=True)
        self.hierarchy_tree.item(vcd_node, open=True)

    def _create_hierarchy_frame(self) -> ttk.Frame:
        """Create file hierarchy panel"""
        frame = ttk.Frame(self.h_paned)
        
        # Add label
        ttk.Label(frame, text="File Hierarchy", font=('TkDefaultFont', 10, 'bold')).pack(fill='x', padx=5, pady=5)
        
        # Create treeview for hierarchy
        self.hierarchy_tree = ttk.Treeview(frame, selectmode='browse')
        self.hierarchy_tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.hierarchy_tree.yview)
        scrollbar.pack(fill='y', side='right')
        self.hierarchy_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.hierarchy_tree["columns"] = ("type",)
        self.hierarchy_tree.column("#0", width=200)  # Name column
        self.hierarchy_tree.column("type", width=100)
        
        self.hierarchy_tree.heading("#0", text="Name")
        self.hierarchy_tree.heading("type", text="Type")
        
        # Add double-click handler
        self.hierarchy_tree.bind('<Double-1>', self._on_hierarchy_double_click)
        
        return frame

    def _on_hierarchy_double_click(self, event):
        """Handle double-click on hierarchy item"""
        item = self.hierarchy_tree.selection()[0]
        item_type = self.hierarchy_tree.item(item)["values"][0]
        item_text = self.hierarchy_tree.item(item)["text"]
        
        if item_type == "file":
            # If it's a VCD file, try to open in GTKWave
            if item_text.endswith('.vcd'):
                vcd_path = os.path.join("vpx_outputs", item_text)
                if os.path.exists(vcd_path):
                    try:
                        subprocess.Popen(['gtkwave', vcd_path])
                    except FileNotFoundError:
                        messagebox.showwarning(
                            "GTKWave not found",
                            "GTKWave is not installed. Please install GTKWave to view waveforms."
                        )