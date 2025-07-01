#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("Warning: pyperclip not available, clipboard features disabled")

from derive_key import get_key_from_password, load_or_create_salt
from database import create_database, save_password, get_passwords, update_password, delete_password

class PasswordManagerGUI:
    def __init__(self):
        self.master_password = None
        self.key = None
        self.salt = load_or_create_salt()
        self.password_data = {}

        self.root = tk.Tk()
        self.root.title("🔒 Password Manager")
        self.root.geometry("1200x800")
        #self.root.configure(bg='#0D1117')
        self.root.resizable(True, True)

        # Set minimum window size
        self.root.minsize(1000, 700)

        self.setup_styles()
        self.show_login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Clean modern styling
        style.configure('Title.TLabel',
                       font=('SF Pro Display', 20, 'bold'),
                       foreground='#FFFFFF',
                       background='#0D1117')

        style.configure('Subtitle.TLabel',
                       font=('SF Pro Display', 12),
                       foreground='#7D8590',
                       background='#0D1117')

        style.configure('Heading.TLabel',
                       font=('SF Pro Display', 13, 'bold'),
                       foreground='#F0F6FC',
                       background='#161B22')

        # Modern button styles
        style.configure('Primary.TButton',
                       font=('SF Pro Display', 10, 'bold'),
                       padding=(14, 6),
                       focuscolor='none')

        style.map('Primary.TButton',
                 background=[('active', '#2EA043'),
                           ('!active', '#238636')],
                 foreground=[('active', '#FFFFFF'),
                           ('!active', '#FFFFFF')],
                 relief=[('active', 'flat'),
                        ('!active', 'flat')])

        style.configure('Success.TButton',
                       font=('SF Pro Display', 10, 'bold'),
                       padding=(14, 6),
                       focuscolor='none')

        style.map('Success.TButton',
                 background=[('active', '#2EA043'),
                           ('!active', '#238636')],
                 foreground=[('active', '#FFFFFF'),
                           ('!active', '#FFFFFF')],
                 relief=[('active', 'flat'),
                        ('!active', 'flat')])

        style.configure('Danger.TButton',
                       font=('SF Pro Display', 10, 'bold'),
                       padding=(14, 6),
                       focuscolor='none')

        style.map('Danger.TButton',
                 background=[('active', '#F85149'),
                           ('!active', '#DA3633')],
                 foreground=[('active', '#FFFFFF'),
                           ('!active', '#FFFFFF')],
                 relief=[('active', 'flat'),
                        ('!active', 'flat')])

        style.configure('Secondary.TButton',
                       font=('SF Pro Display', 10, 'bold'),
                       padding=(14, 6),
                       focuscolor='none')

        style.map('Secondary.TButton',
                 background=[('active', '#30363D'),
                           ('!active', '#21262D')],
                 foreground=[('active', '#F0F6FC'),
                           ('!active', '#8B949E')],
                 relief=[('active', 'flat'),
                        ('!active', 'flat')])

        style.configure('Warning.TButton',
                       font=('SF Pro Display', 10, 'bold'),
                       padding=(14, 6),
                       focuscolor='none')

        style.map('Warning.TButton',
                 background=[('active', '#FB8500'),
                           ('!active', '#D29922')],
                 foreground=[('active', '#000000'),
                           ('!active', '#000000')],
                 relief=[('active', 'flat'),
                        ('!active', 'flat')])

        # Clean Treeview styling
        style.configure('Clean.Treeview',
                       background='#161B22',
                       foreground='#F0F6FC',
                       fieldbackground='#161B22',
                       font=('SF Pro Display', 10),
                       rowheight=30,
                       borderwidth=0)

        style.configure('Clean.Treeview.Heading',
                       background='#21262D',
                       foreground='#F0F6FC',
                       font=('SF Pro Display', 12, 'bold'),
                       relief='flat',
                       borderwidth=0)

        # Prevent header background changes on hover
        style.map('Clean.Treeview.Heading',
                 background=[('active', '#21262D'),
                           ('!active', '#21262D')],
                 foreground=[('active', '#F0F6FC'),
                           ('!active', '#F0F6FC')])

        style.map('Clean.Treeview',
                 background=[('selected', '#2188FF')])

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Clean login background
        login_frame = tk.Frame(self.root, bg='#0D1117')
        login_frame.pack(expand=True, fill='both')

        center_frame = tk.Frame(login_frame, bg='#0D1117')
        center_frame.pack(expand=True)

        # Header with icon and title
        header_frame = tk.Frame(center_frame, bg='#0D1117')
        header_frame.pack(pady=(0, 40))

        title_label = ttk.Label(header_frame, text="🔒 Password Manager", style='Title.TLabel')
        title_label.pack()

        subtitle_label = ttk.Label(header_frame, text="Secure • Simple • Private", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))

        # Clean login form
        form_frame = tk.Frame(center_frame, bg='#161B22')
        form_frame.pack(padx=25, pady=20, ipadx=35, ipady=30)

        tk.Label(form_frame, text="Master Password",
                font=('SF Pro Display', 12, 'bold'),
                fg='#F0F6FC', bg='#161B22').pack(pady=(0, 10))

        self.master_password_entry = tk.Entry(form_frame,
                                             font=('SF Pro Display', 12),
                                             show='•',
                                             width=28,
                                             relief='flat',
                                             bd=0,
                                             bg='#0D1117',
                                             fg='#F0F6FC',
                                             insertbackground='#238636',
                                             highlightthickness=1,
                                             highlightcolor='#238636',
                                             highlightbackground='#30363D')
        self.master_password_entry.pack(pady=(0, 20), ipady=8)
        self.master_password_entry.bind('<Return>', lambda e: self.login())

        login_btn = ttk.Button(form_frame,
                              text="Unlock",
                              command=self.login,
                              style='Primary.TButton')
        login_btn.pack()

        self.master_password_entry.focus()

    def login(self):
        password = self.master_password_entry.get()

        if not password:
            messagebox.showerror("Authentication Required", "Please enter your master password.")
            return

        try:
            self.master_password = password
            self.key = get_key_from_password(password, self.salt)
            create_database(password)
            self.show_main_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    def show_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Clean main container with better padding
        main_frame = tk.Frame(self.root, bg='#0D1117')
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)

        # Modern header with better spacing
        header_frame = tk.Frame(main_frame, bg='#161B22', relief='flat', bd=0)
        header_frame.pack(fill='x', pady=(0, 25))

        header_content = tk.Frame(header_frame, bg='#161B22')
        header_content.pack(fill='x', padx=25, pady=18)

        # Title with better styling
        title_frame = tk.Frame(header_content, bg='#161B22')
        title_frame.pack(side='left')

        title_label = ttk.Label(title_frame, text="🔐 My Vault",
                               font=('SF Pro Display', 22, 'bold'),
                               foreground='#F0F6FC',
                               background='#161B22')
        title_label.pack()

        subtitle_label = ttk.Label(title_frame, text="Secure Password Storage",
                                  font=('SF Pro Display', 11),
                                  foreground='#7D8590',
                                  background='#161B22')
        subtitle_label.pack(anchor='w', pady=(2, 0))

        # Action buttons in header
        action_header_frame = tk.Frame(header_content, bg='#161B22')
        action_header_frame.pack(side='right')

        add_btn = ttk.Button(action_header_frame,
                            text="✚ New Entry",
                            command=self.show_add_password_dialog,
                            style='Success.TButton')
        add_btn.pack(side='right', padx=(8, 0))

        logout_btn = ttk.Button(action_header_frame,
                               text="Sign Out",
                               command=self.logout,
                               style='Danger.TButton')
        logout_btn.pack(side='right', padx=(8, 0))

        # Main content area with scroll
        content_container = tk.Frame(main_frame, bg='#0D1117')
        content_container.pack(expand=True, fill='both')

        # Create scrollable frame
        self.canvas = tk.Canvas(content_container, bg='#0D1117', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#0D1117')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Improved mousewheel scrolling for trackpad compatibility
        def _on_mousewheel(event):
            # Check if canvas exists and has scrollable content
            try:
                if self.canvas.bbox("all"):
                    # Handle different operating systems and input methods
                    if hasattr(event, 'delta') and event.delta:
                        # Windows and macOS trackpad/mouse wheel
                        delta = int(-1 * (event.delta / 120))
                    elif hasattr(event, 'num'):
                        # Linux scroll events
                        if event.num == 4:
                            delta = -1
                        elif event.num == 5:
                            delta = 1
                        else:
                            delta = 0
                    else:
                        delta = 0

                    if delta != 0:
                        self.canvas.yview_scroll(delta, "units")
                        return "break"  # Prevent event propagation
            except:
                pass

        # Make canvas focusable and bind events directly
        self.canvas.focus_set()
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.canvas.bind("<Button-4>", _on_mousewheel)
        self.canvas.bind("<Button-5>", _on_mousewheel)

        # Bind to content container as well
        content_container.bind("<MouseWheel>", _on_mousewheel)
        content_container.bind("<Button-4>", _on_mousewheel)
        content_container.bind("<Button-5>", _on_mousewheel)

        # Ensure canvas gets focus when mouse enters
        def on_canvas_enter(event):
            self.canvas.focus_set()

        self.canvas.bind("<Enter>", on_canvas_enter)
        content_container.bind("<Enter>", on_canvas_enter)

        # Bind window resize to update layout
        self.root.bind('<Configure>', self.on_window_resize)

        # Stats and search section
        stats_frame = tk.Frame(self.scrollable_frame, bg='#161B22', relief='flat', bd=0)
        stats_frame.pack(fill='x', pady=(0, 20), padx=20)

        stats_content = tk.Frame(stats_frame, bg='#161B22')
        stats_content.pack(fill='x', padx=20, pady=15)

        # Search bar
        search_frame = tk.Frame(stats_content, bg='#161B22')
        search_frame.pack(fill='x', pady=(0, 10))

        tk.Label(search_frame, text="🔍 Search",
                font=('SF Pro Display', 12, 'bold'),
                fg='#F0F6FC', bg='#161B22').pack(side='left')

        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.filter_passwords)

        # Make search entry responsive to window width
        self.search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=('SF Pro Display', 11),
                               relief='flat',
                               bd=0,
                               bg='#0D1117',
                               fg='#F0F6FC',
                               insertbackground='#238636',
                               highlightthickness=1,
                               highlightcolor='#238636',
                               highlightbackground='#30363D')
        self.search_entry.pack(side='right', fill='x', expand=True, ipady=6, padx=(10, 0))

        # Stats display
        self.stats_label = tk.Label(stats_content,
                                   font=('SF Pro Display', 10),
                                   fg='#7D8590', bg='#161B22')
        self.stats_label.pack(anchor='w')

        # Password cards container
        self.cards_frame = tk.Frame(self.scrollable_frame, bg='#0D1117')
        self.cards_frame.pack(fill='both', expand=True, padx=20)

        # Store current passwords for layout updates
        self.current_passwords = []

        self.refresh_passwords()

    def calculate_columns(self):
        """Always return 2 columns as requested"""
        return 2

    def get_card_width(self):
        """Calculate uniform card width for exactly 2 columns"""
        if not hasattr(self, 'canvas'):
            # Use root window width for initial calculation
            canvas_width = self.root.winfo_width() - 70  # Account for padding and scrollbar
            if canvas_width < 100:
                return 400
        else:
            canvas_width = self.canvas.winfo_width()
            if canvas_width < 100:  # Canvas not yet initialized, use root width
                canvas_width = self.root.winfo_width() - 70

        # Fixed 2 columns only
        columns = 2
        total_padding = 60  # 30px padding on each side
        card_spacing = 20   # 10px spacing between cards

        # Calculate available width for cards
        available_width = canvas_width - total_padding
        card_width = (available_width - card_spacing) // columns

        # Ensure minimum width
        return max(350, card_width)

    def on_window_resize(self, event):
        """Handle window resize events to update card layout and search bar"""
        # Only respond to main window resize events
        if event.widget == self.root:
            # Use after_idle to avoid too many rapid updates during resize
            self.root.after_idle(self.update_layout_on_resize)

    def update_layout_on_resize(self):
        """Update both card layout and search bar on window resize"""
        # Update search bar width based on new window size
        if hasattr(self, 'search_entry'):
            # The search entry will automatically adjust due to fill='x', expand=True
            pass

        # Update card layout
        if hasattr(self, 'current_passwords') and self.current_passwords:
            # Recalculate and redisplay cards
            self.display_password_cards(self.current_passwords)

    def update_card_layout(self):
        """Update the card layout based on current window size"""
        if hasattr(self, 'current_passwords') and self.current_passwords:
            # Recalculate and redisplay cards
            self.display_password_cards(self.current_passwords)

    def show_add_password_dialog(self):
        dialog = AddPasswordDialog(self.root, self.save_new_password)

    def save_new_password(self, website, username, password):
        try:
            save_password(website, username, password, self.key, self.master_password)
            messagebox.showinfo("Success", "Password saved successfully!", parent=self.root)
            self.refresh_passwords()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {str(e)}", parent=self.root)

    def update_password_entry(self, old_data, new_website, new_username, new_password):
        """Update an existing password entry"""
        try:
            update_password(old_data['id'], new_website, new_username, new_password, self.key, self.master_password)
            messagebox.showinfo("Success", "Password updated successfully!", parent=self.root)
            self.refresh_passwords()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update password: {str(e)}", parent=self.root)

    def filter_passwords(self, var_name, index, mode):
        """Filter passwords based on search term"""
        search_term = self.search_var.get().lower()

        # Clear current cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Filter and display passwords
        filtered_passwords = []
        try:
            passwords = get_passwords(self.key, self.master_password)
            if search_term:
                filtered_passwords = [pwd for pwd in passwords
                                    if search_term in pwd['website'].lower()
                                    or search_term in pwd['username'].lower()]
            else:
                filtered_passwords = passwords
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passwords: {str(e)}")
            return

        self.display_password_cards(filtered_passwords)
        self.update_stats(len(filtered_passwords), len(passwords) if not search_term else len(passwords))

    def display_password_cards(self, passwords):
        """Display passwords as modern cards with uniform sizing - EXACTLY 2 COLUMNS"""
        # Store current passwords for layout updates
        self.current_passwords = passwords

        if not passwords:
            # Empty state
            empty_frame = tk.Frame(self.cards_frame, bg='#0D1117')
            empty_frame.pack(expand=True, fill='both', pady=50)

            empty_icon = tk.Label(empty_frame, text="🔒",
                                 font=('SF Pro Display', 48),
                                 fg='#30363D', bg='#0D1117')
            empty_icon.pack(pady=(0, 10))

            empty_text = tk.Label(empty_frame,
                                 text="No passwords found" if self.search_var.get() else "No passwords saved yet",
                                 font=('SF Pro Display', 16),
                                 fg='#7D8590', bg='#0D1117')
            empty_text.pack()

            if not self.search_var.get():
                empty_subtitle = tk.Label(empty_frame,
                                         text="Click 'New Entry' to add your first password",
                                         font=('SF Pro Display', 12),
                                         fg='#7D8590', bg='#0D1117')
                empty_subtitle.pack(pady=(10, 0))
            return

        # Clear existing cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Get current window dimensions for proper sizing
        columns = 2
        card_width = self.get_card_width()
        card_height = 200

        # Create grid of cards with IDENTICAL sizing for all cards
        for i, pwd in enumerate(passwords):
            row = i // columns
            col = i % columns

            # Card container - IDENTICAL SIZE FOR ALL CARDS
            card_frame = tk.Frame(self.cards_frame, bg='#161B22', relief='flat', bd=0,
                                 width=card_width, height=card_height)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='')
            card_frame.grid_propagate(False)  # CRITICAL: Prevent size changes
            card_frame.pack_propagate(False)  # CRITICAL: Prevent size changes

            # Configure grid for exactly 2 uniform columns
            self.cards_frame.grid_columnconfigure(col, weight=1, uniform="uniform_card")
            self.cards_frame.grid_rowconfigure(row, weight=0)

            # Card content with IDENTICAL padding for all cards
            card_content = tk.Frame(card_frame, bg='#161B22')
            card_content.pack(fill='both', expand=True, padx=20, pady=18)

            # Website header - UNIFORM height and layout
            header_frame = tk.Frame(card_content, bg='#161B22', height=35)
            header_frame.pack(fill='x', pady=(0, 15))
            header_frame.pack_propagate(False)  # Fixed header height

            # Website name section
            website_frame = tk.Frame(header_frame, bg='#161B22')
            website_frame.pack(side='left', fill='x', expand=True)

            # UNIFORM text truncation based on actual card width
            website_text = pwd['website']
            # Adjust character limit based on card width for better responsiveness
            max_chars = max(15, min(30, card_width // 20))
            if len(website_text) > max_chars:
                website_text = website_text[:max_chars-3] + "..."

            # UNIFORM font size for all cards
            website_label = tk.Label(website_frame, text=f"🌐 {website_text}",
                                   font=('SF Pro Display', 13, 'bold'),
                                   fg='#F0F6FC', bg='#161B22',
                                   anchor='w')
            website_label.pack(fill='x')

            # Quick actions with IDENTICAL sizing
            actions_frame = tk.Frame(header_frame, bg='#161B22')
            actions_frame.pack(side='right')

            # Use ttk.Button with custom style and emoji/icon as text
            copy_pass_btn = ttk.Button(
                actions_frame,
                text="🔑",
                width=3,
                style='Secondary.TButton',
                command=lambda p=pwd['password']: self.copy_to_clipboard(p, "Password")
            )
            copy_pass_btn.pack(side='left', padx=(0, 6))

            copy_user_btn = ttk.Button(
                actions_frame,
                text="👤",
                width=3,
                style='Secondary.TButton',
                command=lambda u=pwd['username']: self.copy_to_clipboard(u, "Username")
            )
            copy_user_btn.pack(side='left', padx=(0, 6))

            more_btn = ttk.Button(
                actions_frame,
                text="⋯",
                width=3,
                style='Secondary.TButton',
                command=lambda p=pwd: self.show_card_menu(p)
            )
            more_btn.pack(side='left')

            # Username section - FIXED height for all cards
            username_frame = tk.Frame(card_content, bg='#161B22', height=45)
            username_frame.pack(fill='x', pady=(0, 10))
            username_frame.pack_propagate(False)  # Fixed section height

            tk.Label(username_frame, text="Username:",
                    font=('SF Pro Display', 9, 'bold'),
                    fg='#7D8590', bg='#161B22').pack(anchor='w')

            # UNIFORM username truncation based on card width
            username_text = pwd['username']
            max_username_chars = max(20, min(35, card_width // 15))
            if len(username_text) > max_username_chars:
                username_text = username_text[:max_username_chars-3] + "..."

            username_display = tk.Label(username_frame, text=username_text,
                                       font=('SF Pro Display', 10),
                                       fg='#F0F6FC', bg='#161B22',
                                       anchor='w')
            username_display.pack(fill='x', pady=(3, 0))

            # Password section - FIXED height for all cards
            password_frame = tk.Frame(card_content, bg='#161B22', height=45)
            password_frame.pack(fill='x')
            password_frame.pack_propagate(False)  # Fixed section height

            tk.Label(password_frame, text="Password:",
                    font=('SF Pro Display', 9, 'bold'),
                    fg='#7D8590', bg='#161B22').pack(anchor='w')

            # UNIFORM password dots for all cards
            password_dots = 12  # Fixed number of dots for all cards
            password_display = tk.Label(password_frame, text='•' * password_dots,
                                       font=('SF Pro Display', 10),
                                       fg='#F0F6FC', bg='#161B22',
                                       anchor='w')
            password_display.pack(fill='x', pady=(3, 0))

        # IMPORTANT: Only configure exactly 2 columns
        self.cards_frame.grid_columnconfigure(0, weight=1, uniform="uniform_card")
        self.cards_frame.grid_columnconfigure(1, weight=1, uniform="uniform_card")

        # Clear any additional columns to prevent layout issues
        for col in range(2, 10):
            self.cards_frame.grid_columnconfigure(col, weight=0)

        # Update canvas scroll region after creating cards
        self.root.after_idle(lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Rebind mousewheel events to new card elements
        if hasattr(self, 'canvas'):
            def _on_mousewheel(event):
                try:
                    if self.canvas.bbox("all"):
                        if hasattr(event, 'delta') and event.delta:
                            delta = int(-1 * (event.delta / 120))
                        elif hasattr(event, 'num'):
                            if event.num == 4:
                                delta = -1
                            elif event.num == 5:
                                delta = 1
                            else:
                                delta = 0
                        else:
                            delta = 0

                        if delta != 0:
                            self.canvas.yview_scroll(delta, "units")
                            return "break"
                except:
                    pass

            # Bind mousewheel to all card widgets and their children
            def bind_to_widget_tree(widget):
                widget.bind("<MouseWheel>", _on_mousewheel)
                widget.bind("<Button-4>", _on_mousewheel)
                widget.bind("<Button-5>", _on_mousewheel)

                # Bind to all children recursively
                for child in widget.winfo_children():
                    bind_to_widget_tree(child)

            # Apply to cards frame and all its contents
            bind_to_widget_tree(self.cards_frame)

            # Also bind to scrollable frame
            bind_to_widget_tree(self.scrollable_frame)

    def show_card_menu(self, password_data):
        """Show context menu for a password card"""
        menu = tk.Menu(self.root, tearoff=0,
                      bg='#21262D', fg='#F0F6FC',
                      activebackground='#238636', activeforeground='#FFFFFF',
                      font=('SF Pro Display', 11),
                      borderwidth=0)

        menu.add_command(label="👁 View Details",
                        command=lambda: self.show_password_details(password_data))
        menu.add_command(label="✏️ Edit Entry",
                        command=lambda: EditPasswordDialog(self.root, self.update_password_entry, password_data))
        menu.add_separator()
        menu.add_command(label="📋 Copy Password",
                        command=lambda: self.copy_to_clipboard(password_data['password'], "Password"))
        menu.add_command(label="👤 Copy Username",
                        command=lambda: self.copy_to_clipboard(password_data['username'], "Username"))
        menu.add_command(label="🌐 Copy Website",
                        command=lambda: self.copy_to_clipboard(password_data['website'], "Website"))
        menu.add_separator()
        menu.add_command(label="🗑 Delete Entry",
                        command=lambda: self.delete_password_card(password_data))

        # Get mouse position and show menu
        x, y = self.root.winfo_pointerxy()
        menu.post(x, y)

    def show_password_details(self, password_data):
        """Show detailed view of password entry"""
        self.create_password_options_dialog_from_data(password_data)

    def create_password_options_dialog_from_data(self, data):
        """Create dialog with password options from card data"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Password Details")
        dialog.geometry("400x350")
        dialog.configure(bg='#0D1117')
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 250, self.root.winfo_rooty() + 200))

        # Clean content
        main_frame = tk.Frame(dialog, bg='#161B22')
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)

        content_frame = tk.Frame(main_frame, bg='#161B22')
        content_frame.pack(expand=True, fill='both', padx=15, pady=15)

        # Website title
        tk.Label(content_frame, text=f"🌐 {data['website']}",
                font=('SF Pro Display', 14, 'bold'),
                fg='#F0F6FC', bg='#161B22').pack(pady=(0, 15))

        # Username section
        username_frame = tk.Frame(content_frame, bg='#161B22')
        username_frame.pack(fill='x', pady=(0, 12))

        tk.Label(username_frame, text="Username",
                font=('SF Pro Display', 10, 'bold'),
                fg='#7D8590', bg='#161B22').pack(anchor='w')

        tk.Label(username_frame, text=data['username'],
                font=('SF Pro Display', 11),
                fg='#F0F6FC', bg='#161B22').pack(anchor='w', pady=(2, 0))

        # Password section
        password_frame = tk.Frame(content_frame, bg='#161B22')
        password_frame.pack(fill='x', pady=(0, 20))

        tk.Label(password_frame, text="Password",
                font=('SF Pro Display', 10, 'bold'),
                fg='#7D8590', bg='#161B22').pack(anchor='w')

        # Password display with improved styling
        self.password_var = tk.StringVar(value='•' * 8)
        self.password_shown = False

        password_display_frame = tk.Frame(password_frame, bg='#21262D', relief='flat', bd=1)
        password_display_frame.pack(fill='x', pady=(2, 0))

        self.password_display_label = tk.Label(password_display_frame,
                                              textvariable=self.password_var,
                                              font=('SF Pro Display', 11),
                                              fg='#F0F6FC', bg='#21262D',
                                              anchor='w')
        self.password_display_label.pack(side='left', padx=10, pady=8, fill='x', expand=True)

        # Improved toggle button
        toggle_btn = tk.Button(password_display_frame,
                               text="👁",
                               font=('SF Pro Display', 12),
                               bg='#6E7681', fg='#F0F6FC',
                               activebackground='#8B949E',
                               activeforeground='#F0F6FC',
                               relief='flat', bd=0,
                               width=3, height=1,
                               cursor='hand2',
                               command=lambda: self.toggle_password_visibility(data['password']))
        toggle_btn.pack(side='right', padx=5, pady=2)

        # Action buttons
        button_frame = tk.Frame(content_frame, bg='#161B22')
        button_frame.pack(fill='x', pady=(20, 0))

        if CLIPBOARD_AVAILABLE:
            copy_btn = ttk.Button(button_frame,
                                 text="📋 Copy Password",
                                 command=lambda: self.copy_password_from_dialog(data['password'], dialog),
                                 style='Primary.TButton')
            copy_btn.pack(side='left', padx=(0, 8))

        close_btn = ttk.Button(button_frame,
                              text="Close",
                              command=dialog.destroy,
                              style='Secondary.TButton')
        close_btn.pack(side='right')

    def delete_password_card(self, password_data):
        """Delete a password from card interface"""
        if messagebox.askyesno("Confirm Delete",
                             f"Are you sure you want to delete the password for {password_data['website']}?",
                             icon='warning'):
            try:
                delete_password(password_data['id'], self.master_password)
                messagebox.showinfo("Success", "Password deleted successfully!")
                self.refresh_passwords()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete password: {str(e)}")

    def update_stats(self, displayed_count, total_count):
        """Update the stats display"""
        if hasattr(self, 'stats_label'):
            if self.search_var.get():
                self.stats_label.config(text=f"Showing {displayed_count} of {total_count} passwords")
            else:
                self.stats_label.config(text=f"Total: {total_count} passwords")

    def refresh_passwords(self):
        # Clear search
        if hasattr(self, 'search_var'):
            self.search_var.set('')

        try:
            passwords = get_passwords(self.key, self.master_password)
            self.display_password_cards(passwords)
            self.update_stats(len(passwords), len(passwords))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passwords: {str(e)}")

    def copy_to_clipboard(self, text, label):
        """Copy text to clipboard and show confirmation"""
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(text)
            messagebox.showinfo("✓ Copied", f"{label} copied to clipboard!", parent=self.root)
        else:
            messagebox.showinfo(f"📋 {label}", f"{label}: {text}", parent=self.root)

    def toggle_password_visibility(self, password):
        """Toggle between showing and hiding password"""
        if self.password_shown:
            self.password_var.set('•' * len(password))
            self.password_shown = False
        else:
            self.password_var.set(password)
            self.password_shown = True

    def copy_password_from_dialog(self, password, dialog):
        """Copy password and close dialog"""
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
            messagebox.showinfo("✓ Copied", "Password copied to clipboard!", parent=dialog)
            dialog.destroy()

    def logout(self):
        self.master_password = None
        self.key = None
        self.show_login_screen()

    def run(self):
        self.root.mainloop()


class AddPasswordDialog:
    def __init__(self, parent, callback):
        self.callback = callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Password")
        self.dialog.geometry("420x380")
        self.dialog.configure(bg='#0D1117')
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 150, parent.winfo_rooty() + 150))

        self.create_form()
        self.website_entry.focus()

    def create_form(self):
        # Clean container
        main_frame = tk.Frame(self.dialog, bg='#161B22')
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)

        content_frame = tk.Frame(main_frame, bg='#161B22')
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        title_label = tk.Label(content_frame,
                              text="Add New Password",
                              font=('SF Pro Display', 16, 'bold'),
                              fg='#F0F6FC',
                              bg='#161B22')
        title_label.pack(pady=(0, 25))

        # Input fields
        self.create_input_field(content_frame, "Website", "website_entry")
        self.create_input_field(content_frame, "Username", "username_entry")
        self.create_input_field(content_frame, "Password", "password_entry", show='•')

        # Buttons
        button_frame = tk.Frame(content_frame, bg='#161B22')
        button_frame.pack(pady=(25, 0))

        save_btn = ttk.Button(button_frame,
                             text="Save Password",
                             command=self.save_password,
                             style='Primary.TButton')
        save_btn.pack(side='left', padx=(0, 8))

        cancel_btn = ttk.Button(button_frame,
                               text="Cancel",
                               command=self.dialog.destroy,
                               style='Secondary.TButton')
        cancel_btn.pack(side='left')

        self.dialog.bind('<Return>', lambda e: self.save_password())

    def create_input_field(self, parent, label_text, field_name, show=None):
        # Label
        tk.Label(parent, text=label_text,
                font=('SF Pro Display', 11, 'bold'),
                fg='#F0F6FC', bg='#161B22').pack(anchor='w', pady=(12, 5))

        # Input field
        entry = tk.Entry(parent,
                        font=('SF Pro Display', 11),
                        width=35,
                        relief='flat',
                        bd=0,
                        bg='#0D1117',
                        fg='#F0F6FC',
                        insertbackground='#238636',
                        highlightthickness=1,
                        highlightcolor='#238636',
                        highlightbackground='#30363D',
                        show=show)
        entry.pack(pady=(0, 5), ipady=6)

        setattr(self, field_name, entry)

    def save_password(self):
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not username or not password:
            messagebox.showerror("Validation Error", "Please fill in all fields.")
            return

        self.callback(website, username, password)
        self.dialog.destroy()


class EditPasswordDialog:
    def __init__(self, parent, callback, existing_data):
        self.callback = callback
        self.existing_data = existing_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Password")
        self.dialog.geometry("420x380")
        self.dialog.configure(bg='#0D1117')
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 150, parent.winfo_rooty() + 150))

        self.create_form()
        self.website_entry.focus()

    def create_form(self):
        # Clean container
        main_frame = tk.Frame(self.dialog, bg='#161B22')
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)

        content_frame = tk.Frame(main_frame, bg='#161B22')
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        title_label = tk.Label(content_frame,
                              text="Edit Password",
                              font=('SF Pro Display', 16, 'bold'),
                              fg='#F0F6FC',
                              bg='#161B22')
        title_label.pack(pady=(0, 25))

        # Input fields with existing data
        self.create_input_field(content_frame, "Website", "website_entry", self.existing_data['website'])
        self.create_input_field(content_frame, "Username", "username_entry", self.existing_data['username'])
        self.create_input_field(content_frame, "Password", "password_entry", self.existing_data['password'], show='•')

        # Buttons
        button_frame = tk.Frame(content_frame, bg='#161B22')
        button_frame.pack(pady=(25, 0))

        update_btn = ttk.Button(button_frame,
                               text="Update Password",
                               command=self.update_password,
                               style='Warning.TButton')
        update_btn.pack(side='left', padx=(0, 8))

        cancel_btn = ttk.Button(button_frame,
                               text="Cancel",
                               command=self.dialog.destroy,
                               style='Secondary.TButton')
        cancel_btn.pack(side='left')

        self.dialog.bind('<Return>', lambda e: self.update_password())

    def create_input_field(self, parent, label_text, field_name, initial_value="", show=None):
        # Label
        tk.Label(parent, text=label_text,
                font=('SF Pro Display', 11, 'bold'),
                fg='#F0F6FC', bg='#161B22').pack(anchor='w', pady=(12, 5))

        # Input field
        entry = tk.Entry(parent,
                        font=('SF Pro Display', 11),
                        width=35,
                        relief='flat',
                        bd=0,
                        bg='#0D1117',
                        fg='#F0F6FC',
                        insertbackground='#238636',
                        highlightthickness=1,
                        highlightcolor='#238636',
                        highlightbackground='#303D3D',
                        show=show)
        entry.pack(pady=(0, 5), ipady=6)
        entry.insert(0, initial_value)

        setattr(self, field_name, entry)

    def update_password(self):
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not username or not password:
            messagebox.showerror("Validation Error", "Please fill in all fields.")
            return

        self.callback(self.existing_data, website, username, password)
        self.dialog.destroy()

if __name__ == "__main__":
    print("Starting Password Manager GUI...")
    try:
        app = PasswordManagerGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import traceback
        traceback.print_exc()
