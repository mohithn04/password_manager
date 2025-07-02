#!/usr/bin/env python3

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("Warning: pyperclip not available, clipboard features disabled")

from derive_key import get_key_from_password, load_or_create_salt
from database import create_database, save_password, get_passwords, update_password, delete_password

# Set appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Enhanced modern color palette - fixed to remove unsupported RGBA colors
COLORS = {
    'bg_primary': '#0f1419',        # Deeper, richer background
    'bg_secondary': '#1a1f2e',      # More sophisticated card background
    'bg_tertiary': '#252b3a',       # Enhanced tertiary background
    'bg_quaternary': '#2d3548',     # Additional depth layer
    'accent': '#667eea',            # More sophisticated blue
    'accent_hover': '#764ba2',      # Purple-blue gradient hover
    'accent_light': '#8b95ff',      # Light accent for highlights (fixed from RGBA)
    'text_primary': '#f8fafc',      # Pure white text
    'text_secondary': '#94a3b8',    # Softer secondary text
    'text_muted': '#64748b',        # More refined muted text
    'success': '#059669',           # Modern green
    'success_hover': "#067E58",     # Darker green hover
    'warning': '#f59e0b',           # Amber warning
    'warning_hover': '#d97706',     # Orange hover
    'danger': '#b81414',            # Modern red
    'danger_hover': "#991010",      # Darker red hover
    'border': '#374151',            # Subtle border
    'shadow': '#1a1f2e',           # Subtle shadow (fixed from RGBA)
    'glow': '#3d4f7a',             # Accent glow effect (fixed from RGBA)
}

# Enhanced typography with bigger font sizes
FONTS = {
    'title': ('SF Pro Display', 32, 'bold'),      # Larger title
    'heading': ('SF Pro Display', 24, 'bold'),    # Enhanced heading
    'subheading': ('SF Pro Display', 18, 'bold'), # Better subheading
    'body': ('SF Pro Display', 14),               # Standard body
    'body_medium': ('SF Pro Display', 15),        # Medium body text
    'small': ('SF Pro Display', 12),              # Small text
    'tiny': ('SF Pro Display', 11),               # Tiny labels
    'button': ('SF Pro Display', 14, 'bold'),     # Button text
    'monospace': ('SF Mono', 13),                 # For passwords
}

# Animation and timing constants
ANIMATION = {
    'fast': 150,
    'medium': 250,
    'slow': 400,
    'fade_steps': 20,
}

class PasswordManagerGUI:
    def __init__(self):
        self.master_password = None
        self.key = None
        self.salt = load_or_create_salt()
        self.current_passwords = []

        # Animation state
        self.fade_alpha = 0.0
        self.is_animating = False

        # Create main window with enhanced styling
        self.root = ctk.CTk()
        self.root.title("🔒 Password Manager")
        self.root.geometry("1300x850")  # Slightly larger for better breathing room
        self.root.minsize(1100, 750)

        # Configure for better performance
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Remove transparency fade-in - make window fully opaque
        try:
            self.root.attributes('-alpha', 1.0)  # Fully opaque window
        except:
            pass

        self.show_login_screen()

    def fade_in_window(self):
        """Removed fade-in animation - window stays fully opaque"""
        pass  # No fade animation

    def show_login_screen(self):
        """Enhanced login screen with gradient-like effects and animations"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container with enhanced background
        main_frame = ctk.CTkFrame(self.root, fg_color=COLORS['bg_primary'])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Background accent frame for subtle depth
        bg_accent = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=0
        )
        bg_accent.place(relx=0.6, rely=0.0, relwidth=0.4, relheight=1.0)

        # Center container
        center_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        center_frame.grid(row=0, column=0, sticky="")

        # Enhanced login card with subtle shadow effect
        login_card = ctk.CTkFrame(
            center_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=24,  # More rounded corners
            width=450,         # Slightly wider
            height=520,        # Taller for better proportions
            border_width=1,
            border_color=COLORS['border']
        )
        login_card.pack(padx=50, pady=50)
        login_card.pack_propagate(False)

        # Subtle accent line instead of glow effect (compatible with CustomTkinter)
        accent_line = ctk.CTkFrame(
            login_card,
            fg_color=COLORS['accent'],
            corner_radius=20,
            height=3
        )
        accent_line.pack(fill="x", padx=20, pady=(20, 0))

        # Enhanced header section
        header_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        header_frame.pack(pady=(30, 25))

        # Animated lock icon with accent color
        lock_label = ctk.CTkLabel(
            header_frame,
            text="🔐",
            font=('SF Pro Display', 56),  # Larger icon
            text_color=COLORS['accent']
        )
        lock_label.pack()

        # Enhanced title with better spacing
        title_label = ctk.CTkLabel(
            header_frame,
            text="Password Manager",
            font=FONTS['title'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(15, 8))

        # Styled subtitle with better color
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Secure • Simple • Private",
            font=FONTS['body_medium'],
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack()

        # Enhanced form section
        form_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        form_frame.pack(pady=(25, 45), padx=45, fill="x")

        # Password label with better styling
        password_label = ctk.CTkLabel(
            form_frame,
            text="Master Password",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 12))

        # Enhanced password entry with better styling
        self.master_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your master password",
            font=FONTS['body_medium'],
            height=50,  # Taller for better touch targets
            corner_radius=12,
            border_width=2,
            border_color=COLORS['border'],
            fg_color=COLORS['bg_tertiary'],
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_muted'],
            show="•"
        )
        self.master_password_entry.pack(fill="x", pady=(0, 30))
        self.master_password_entry.bind('<Return>', lambda e: self.login())

        # Add focus animations
        self.master_password_entry.bind('<FocusIn>', self.on_entry_focus)
        self.master_password_entry.bind('<FocusOut>', self.on_entry_blur)

        # Enhanced login button with gradient-like effect
        login_btn = ctk.CTkButton(
            form_frame,
            text="🔓 Unlock Vault",  # Enhanced button text with icon
            font=FONTS['button'],
            height=50,
            corner_radius=12,
            fg_color=COLORS['accent'],
            hover_color=COLORS['accent_hover'],
            command=self.login,
            cursor="hand2"
        )
        login_btn.pack(fill="x")

        # Focus and no fade in (removed fade_in_window call)
        self.master_password_entry.focus()

    def on_entry_focus(self, event):
        """Add focus animation to entry fields - fixed for CustomTkinter"""
        # Use CustomTkinter's configure method correctly
        if hasattr(event.widget, 'configure'):
            try:
                event.widget.configure(border_color=COLORS['accent'])
            except:
                # Fallback if border_color isn't supported
                pass

    def on_entry_blur(self, event):
        """Remove focus animation from entry fields - fixed for CustomTkinter"""
        # Use CustomTkinter's configure method correctly
        if hasattr(event.widget, 'configure'):
            try:
                event.widget.configure(border_color=COLORS['border'])
            except:
                # Fallback if border_color isn't supported
                pass

    def login(self):
        """Handle login authentication"""
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
        """Enhanced main screen with better visual hierarchy"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container with enhanced styling
        main_frame = ctk.CTkFrame(self.root, fg_color=COLORS['bg_primary'])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Enhanced header
        self.create_enhanced_header(main_frame)

        # Content area with better spacing
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        # Enhanced search section
        self.create_enhanced_search_section(content_frame)

        # Enhanced scrollable cards area
        self.cards_container = ctk.CTkScrollableFrame(
            content_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=20,
            scrollbar_button_color=COLORS['bg_tertiary'],
            scrollbar_button_hover_color=COLORS['accent'],
            border_width=1,
            border_color=COLORS['border']
        )
        self.cards_container.grid(row=1, column=0, sticky="nsew", pady=(20, 0))
        self.cards_container.grid_columnconfigure((0, 1), weight=1, uniform="cards")

        self.refresh_passwords()

    def create_enhanced_header(self, parent):
        """Enhanced header with gradient-like styling and better button design"""
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_secondary'],
            corner_radius=18,
            height=120,  # Taller header
            border_width=1,
            border_color=COLORS['border']
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.pack_propagate(False)

        # Accent line at top
        accent_line = ctk.CTkFrame(
            header_frame,
            fg_color=COLORS['accent'],
            corner_radius=0,
            height=3
        )
        accent_line.pack(fill="x", padx=10, pady=(15, 0))

        # Header content
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=20)

        # Enhanced left side - Title with better hierarchy
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="y")

        title_label = ctk.CTkLabel(
            title_frame,
            text="🔐 My Vault",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Secure Password Storage",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # Enhanced right side - Action buttons with better styling
        actions_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        actions_frame.pack(side="right", fill="y")

        # Enhanced New Entry button
        new_btn = ctk.CTkButton(
            actions_frame,
            text="➕ New Entry",  # Better icon
            font=FONTS['button'],
            height=40,
            width=120,
            corner_radius=10,
            fg_color=COLORS['success'],
            hover_color=COLORS['success_hover'],
            command=self.show_add_password_dialog,
            cursor="hand2"
        )
        new_btn.pack(side="right", padx=(12, 0))

        # Enhanced Sign Out button
        signout_btn = ctk.CTkButton(
            actions_frame,
            text="✌🏽 Sign Out",  # Better icon
            font=FONTS['button'],
            height=40,
            width=100,
            corner_radius=10,
            fg_color=COLORS['danger'],
            hover_color=COLORS['danger_hover'],
            command=self.logout,
            cursor="hand2"
        )
        signout_btn.pack(side="right")

    def create_enhanced_search_section(self, parent):
        """Enhanced search section with better visual appeal"""
        search_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_secondary'],
            corner_radius=18,
            height=100,  # Slightly taller
            border_width=1,
            border_color=COLORS['border']
        )
        search_frame.grid(row=0, column=0, sticky="ew")
        search_frame.pack_propagate(False)

        # Search content with better padding
        search_content = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_content.pack(fill="both", expand=True, padx=30, pady=10)

        # Enhanced search label
        search_label = ctk.CTkLabel(
            search_content,
            text="🔍 Search Passwords",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        search_label.pack(anchor="w", pady=(0, 10))

        # Enhanced search entry
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.filter_passwords)

        self.search_entry = ctk.CTkEntry(
            search_content,
            textvariable=self.search_var,
            placeholder_text="Type to search by website or username...",
            font=FONTS['body_medium'],
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=COLORS['border'],
            fg_color=COLORS['bg_tertiary'],
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_muted']
        )
        self.search_entry.pack(fill="x", pady=(0, 10))
        self.search_entry.bind('<FocusIn>', self.on_entry_focus)
        self.search_entry.bind('<FocusOut>', self.on_entry_blur)

        # Enhanced stats label
        self.stats_label = ctk.CTkLabel(
            search_content,
            text="Total: 0 passwords",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        self.stats_label.pack(anchor="w")

    def display_password_cards(self, passwords):
        """Display password cards in a 2-column grid"""
        # Clear existing cards
        for widget in self.cards_container.winfo_children():
            widget.destroy()

        self.current_passwords = passwords

        if not passwords:
            self.show_empty_state()
            return

        # Create cards in 2-column grid
        for i, pwd in enumerate(passwords):
            row = i // 2
            col = i % 2

            self.create_password_card(pwd, row, col)

    def create_password_card(self, password_data, row, col):
        """Enhanced password card with better visual hierarchy and hover effects"""
        card = ctk.CTkFrame(
            self.cards_container,
            fg_color=COLORS['bg_tertiary'],
            corner_radius=16,  # More rounded
            height=210,        # Taller cards
            border_width=1,
            border_color=COLORS['border']
        )
        card.grid(row=row, column=col, padx=12, pady=12, sticky="ew")
        card.pack_propagate(False)

        # Subtle top accent line
        accent_line = ctk.CTkFrame(
            card,
            fg_color=COLORS['accent'],
            corner_radius=0,
            height=2
        )
        accent_line.pack(fill="x", padx=15, pady=(15, 0))

        # Card content with better padding
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=15)

        # Enhanced header with website and actions
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        # Enhanced website name with favicon-like styling
        website_text = password_data['website']
        if len(website_text) > 22:
            website_text = website_text[:19] + "..."

        website_label = ctk.CTkLabel(
            header_frame,
            text=f"🌐 {website_text}",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        website_label.pack(side="left", fill="x", expand=True)

        # Enhanced action buttons with better spacing
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        # Copy password button with tooltip-like styling
        copy_btn = ctk.CTkButton(
            actions_frame,
            text="🔑",
            width=32,
            height=32,
            corner_radius=8,
            font=('SF Pro Display', 16),
            fg_color=COLORS['bg_quaternary'],
            hover_color=COLORS['accent'],
            command=lambda: self.copy_to_clipboard(password_data['password'], "Password"),
            cursor="hand2"
        )
        copy_btn.pack(side="left", padx=(0, 6))

        # Copy username button
        copy_user_btn = ctk.CTkButton(
            actions_frame,
            text="👤",
            width=32,
            height=32,
            corner_radius=8,
            font=('SF Pro Display', 16),
            fg_color=COLORS['bg_quaternary'],
            hover_color=COLORS['accent'],
            command=lambda: self.copy_to_clipboard(password_data['username'], "Username"),
            cursor="hand2"
        )
        copy_user_btn.pack(side="left", padx=(0, 6))

        # More options button
        more_btn = ctk.CTkButton(
            actions_frame,
            text="⋯",
            width=32,
            height=32,
            corner_radius=8,
            font=('SF Pro Display', 18, 'bold'),
            fg_color=COLORS['bg_quaternary'],
            hover_color=COLORS['accent'],
            command=lambda: self.show_card_menu(password_data, more_btn),
            cursor="hand2"
        )
        more_btn.pack(side="left")

        # Enhanced username section
        username_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        username_frame.pack(fill="x")

        username_title = ctk.CTkLabel(
            username_frame,
            text="Username:",
            font=FONTS['body_medium'],
            text_color=COLORS['text_muted']
        )
        username_title.pack(anchor="w")

        username_text = password_data['username']
        if len(username_text) > 32:
            username_text = username_text[:29] + "..."

        username_value = ctk.CTkLabel(
            username_frame,
            text=username_text,
            font=FONTS['body_medium'],
            text_color=COLORS['text_primary']
        )
        username_value.pack(anchor="w")

        # Enhanced password section
        password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        password_frame.pack(fill="x")

        password_title = ctk.CTkLabel(
            password_frame,
            text="Password:",
            font=FONTS['body_medium'],
            text_color=COLORS['text_muted']
        )
        password_title.pack(anchor="w")

        # Styled password dots with monospace font
        password_dots = ctk.CTkLabel(
            password_frame,
            text="●●●●●●●●●●●●",  # Different bullet style
            font=FONTS['monospace'],
            text_color=COLORS['text_secondary']
        )
        password_dots.pack(anchor="w", pady=(4, 7))

    def show_empty_state(self):
        """Enhanced empty state with better visual appeal"""
        empty_frame = ctk.CTkFrame(self.cards_container, fg_color="transparent")
        empty_frame.pack(expand=True, fill="both", pady=80)

        # Enhanced empty state card
        empty_card = ctk.CTkFrame(
            empty_frame,
            fg_color=COLORS['bg_tertiary'],
            corner_radius=20,
            border_width=2,
            border_color=COLORS['border']
        )
        empty_card.pack(padx=100, pady=40)

        # Large icon with better styling
        empty_icon = ctk.CTkLabel(
            empty_card,
            text="🔒",
            font=('SF Pro Display', 72),
            text_color=COLORS['text_muted']
        )
        empty_icon.pack(pady=(40, 10))

        # Enhanced empty text
        empty_text = ctk.CTkLabel(
            empty_card,
            text="No passwords found" if self.search_var.get() else "Your vault is empty",
            font=FONTS['heading'],
            text_color=COLORS['text_secondary']
        )
        empty_text.pack(padx=30, pady=(0, 30)) if self.search_var.get() else empty_text.pack(padx=30, pady=(0, 10))

        if not self.search_var.get():
            empty_subtitle = ctk.CTkLabel(
                empty_card,
                text="Click '➕ New Entry' to add your first password",
                font=FONTS['body_medium'],
                text_color=COLORS['text_muted']
            )
            empty_subtitle.pack(padx=15, pady=(0, 40))

    def show_card_menu(self, password_data, button):
        """Show context menu for password card"""
        # Create popup menu
        menu = tk.Menu(self.root, tearoff=0,
                      bg=COLORS['bg_tertiary'], fg=COLORS['text_primary'],
                      activebackground=COLORS['accent'], activeforeground='white',
                      font=FONTS['body'], borderwidth=0)

        menu.add_command(label="👁 View Details",
                        command=lambda: self.show_password_details(password_data))
        menu.add_command(label="✏️ Edit Entry",
                        command=lambda: self.show_edit_password_dialog(password_data))
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

        # Show menu at button position
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()
        menu.post(x, y)

    def show_password_details(self, password_data):
        """Show password details dialog"""
        dialog = PasswordDetailsDialog(self.root, password_data, self.copy_to_clipboard)

    def show_add_password_dialog(self):
        """Show add password dialog"""
        dialog = AddPasswordDialog(self.root, self.save_new_password)

    def show_edit_password_dialog(self, password_data):
        """Show edit password dialog"""
        dialog = EditPasswordDialog(self.root, self.update_password_entry, password_data)

    def save_new_password(self, website, username, password):
        """Save new password to database"""
        try:
            save_password(website, username, password, self.key, self.master_password)
            messagebox.showinfo("Success", "Password saved successfully!")
            self.refresh_passwords()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {str(e)}")

    def update_password_entry(self, old_data, new_website, new_username, new_password):
        """Update existing password entry"""
        try:
            update_password(old_data['id'], new_website, new_username, new_password, self.key, self.master_password)
            messagebox.showinfo("Success", "Password updated successfully!")
            self.refresh_passwords()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update password: {str(e)}")

    def delete_password_card(self, password_data):
        """Delete password with confirmation"""
        if messagebox.askyesno("Confirm Delete",
                             f"Are you sure you want to delete the password for {password_data['website']}?",
                             icon='warning'):
            try:
                delete_password(password_data['id'], self.master_password)
                messagebox.showinfo("Success", "Password deleted successfully!")
                self.refresh_passwords()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete password: {str(e)}")

    def filter_passwords(self, var_name, index, mode):
        """Filter passwords based on search term"""
        search_term = self.search_var.get().lower()

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
        self.update_stats(len(filtered_passwords), len(passwords))

    def update_stats(self, displayed_count, total_count):
        """Update stats display"""
        if self.search_var.get():
            self.stats_label.configure(text=f"Showing {displayed_count} of {total_count} passwords")
        else:
            self.stats_label.configure(text=f"Total: {total_count} passwords")

    def refresh_passwords(self):
        """Refresh password display"""
        if hasattr(self, 'search_var'):
            self.search_var.set('')

        try:
            passwords = get_passwords(self.key, self.master_password)
            self.display_password_cards(passwords)
            self.update_stats(len(passwords), len(passwords))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passwords: {str(e)}")

    def copy_to_clipboard(self, text, label):
        """Enhanced clipboard copy with better notification"""
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(text)
            # Create a custom notification instead of basic messagebox
            self.show_toast_notification(f"✓ {label} copied to clipboard!")
        else:
            messagebox.showinfo(f"📋 {label}", f"{label}: {text}")

    def show_toast_notification(self, message):
        """Show a modern toast notification"""
        toast = ctk.CTkToplevel(self.root)
        toast.geometry("300x60")
        toast.overrideredirect(True)
        toast.attributes('-topmost', True)

        # Position in bottom right
        x = self.root.winfo_x() + self.root.winfo_width() - 320
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        toast.geometry(f"+{x}+{y}")

        # Toast content
        toast_frame = ctk.CTkFrame(
            toast,
            fg_color=COLORS['success'],
            corner_radius=12
        )
        toast_frame.pack(fill="both", expand=True, padx=8, pady=8)

        toast_label = ctk.CTkLabel(
            toast_frame,
            text=message,
            font=FONTS['body_medium'],
            text_color="white"
        )
        toast_label.pack(expand=True)

        # Auto-dismiss after 2 seconds
        toast.after(2000, toast.destroy)

    def logout(self):
        """Logout and return to login screen"""
        self.master_password = None
        self.key = None
        self.show_login_screen()

    def run(self):
        """Start the application"""
        self.root.mainloop()


class PasswordDetailsDialog:
    def __init__(self, parent, password_data, copy_callback):
        self.password_data = password_data
        self.copy_callback = copy_callback
        self.password_shown = False

        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Password Details")
        self.dialog.geometry("500x450")  # Slightly larger for bigger text
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.geometry(f"+{parent.winfo_rootx() + 200}+{parent.winfo_rooty() + 150}")

        self.create_dialog()

    def create_dialog(self):
        # Main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color=COLORS['bg_secondary'], corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Content frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=f"🌐 {self.password_data['website']}",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(0, 25))

        # Username section
        username_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        username_frame.pack(fill="x", pady=(0, 20))

        username_label = ctk.CTkLabel(
            username_frame,
            text="Username",
            font=FONTS['subheading'],
            text_color=COLORS['text_secondary']
        )
        username_label.pack(anchor="w")

        username_value = ctk.CTkLabel(
            username_frame,
            text=self.password_data['username'],
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        username_value.pack(anchor="w", pady=(5, 0))

        # Password section
        password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 30))

        password_label = ctk.CTkLabel(
            password_frame,
            text="Password",
            font=FONTS['subheading'],
            text_color=COLORS['text_secondary']
        )
        password_label.pack(anchor="w")

        # Password display frame
        password_display_frame = ctk.CTkFrame(password_frame, fg_color=COLORS['bg_tertiary'], corner_radius=8)
        password_display_frame.pack(fill="x", pady=(5, 0))

        self.password_var = tk.StringVar(value="•" * 12)
        self.password_display = ctk.CTkLabel(
            password_display_frame,
            textvariable=self.password_var,
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        self.password_display.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        # Toggle button
        self.toggle_btn = ctk.CTkButton(
            password_display_frame,
            text="👁",
            width=40,
            height=30,
            corner_radius=6,
            fg_color=COLORS['bg_secondary'],
            hover_color=COLORS['border'],
            command=self.toggle_password_visibility
        )
        self.toggle_btn.pack(side="right", padx=10, pady=5)

        # Action buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))

        if CLIPBOARD_AVAILABLE:
            copy_btn = ctk.CTkButton(
                button_frame,
                text="📋 Copy Password",
                font=FONTS['button'],
                height=40,
                corner_radius=10,
                fg_color=COLORS['accent'],
                hover_color=COLORS['accent_hover'],
                command=self.copy_password
            )
            copy_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            font=FONTS['button'],
            height=40,
            corner_radius=10,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['border'],
            command=self.dialog.destroy
        )
        close_btn.pack(side="right", padx=(10, 0) if CLIPBOARD_AVAILABLE else (0, 0))

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_shown:
            self.password_var.set("•" * 12)
            self.password_shown = False
        else:
            self.password_var.set(self.password_data['password'])
            self.password_shown = True

    def copy_password(self):
        """Copy password and close dialog"""
        self.copy_callback(self.password_data['password'], "Password")
        self.dialog.destroy()


class AddPasswordDialog:
    def __init__(self, parent, callback):
        self.callback = callback

        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add New Password")
        self.dialog.geometry("500x550")  # Slightly larger for bigger text
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.geometry(f"+{parent.winfo_rootx() + 200}+{parent.winfo_rooty() + 150}")

        self.create_dialog()

    def create_dialog(self):
        # Main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color=COLORS['bg_secondary'], corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Content frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text="Add New Password",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(0, 30))

        # Website field
        self.website_entry = self.create_input_field(content_frame, "Website")

        # Username field
        self.username_entry = self.create_input_field(content_frame, "Username")

        # Password field
        self.password_entry = self.create_input_field(content_frame, "Password", show="•")

        # Buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(30, 0))

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Password",
            font=FONTS['button'],
            height=50,  # Taller buttons for bigger text
            corner_radius=10,
            fg_color=COLORS['success'],
            hover_color="#16a34a",
            command=self.save_password
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=FONTS['button'],
            height=50,  # Taller buttons for bigger text
            corner_radius=10,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['border'],
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="right")

        # Focus on first field
        self.website_entry.focus()

    def create_input_field(self, parent, label_text, show=None):
        """Create a labeled input field"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=(0, 20))

        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        label.pack(anchor="w", pady=(0, 8))

        entry = ctk.CTkEntry(
            field_frame,
            font=FONTS['body_medium'],  # Bigger font for input
            height=45,  # Taller input fields
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border'],
            fg_color=COLORS['bg_tertiary'],
            text_color=COLORS['text_primary'],
            show=show
        )
        entry.pack(fill="x")

        return entry

    def save_password(self):
        """Save the password"""
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

        # Create dialog
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Edit Password")
        self.dialog.geometry("500x500")  # Slightly larger for bigger text
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.geometry(f"+{parent.winfo_rootx() + 200}+{parent.winfo_rooty() + 150}")

        self.create_dialog()

    def create_dialog(self):
        # Main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color=COLORS['bg_secondary'], corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Content frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text="Edit Password",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(0, 20))

        # Website field
        self.website_entry = self.create_input_field(content_frame, "Website", self.existing_data['website'])

        # Username field
        self.username_entry = self.create_input_field(content_frame, "Username", self.existing_data['username'])

        # Password field
        self.password_entry = self.create_input_field(content_frame, "Password", self.existing_data['password'], show="•")

        # Buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(7, 0))

        update_btn = ctk.CTkButton(
            button_frame,
            text="Update Password",
            font=FONTS['button'],
            height=50,  # Taller buttons for bigger text
            corner_radius=10,
            fg_color=COLORS['warning'],
            hover_color="#d97706",
            command=self.update_password
        )
        update_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=FONTS['button'],
            height=50,  # Taller buttons for bigger text
            corner_radius=10,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['border'],
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="right")

        # Focus on first field
        self.website_entry.focus()

    def create_input_field(self, parent, label_text, initial_value="", show=None):
        """Create a labeled input field with initial value"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=(0, 20))

        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        label.pack(anchor="w", pady=(0, 8))

        entry = ctk.CTkEntry(
            field_frame,
            font=FONTS['body_medium'],  # Bigger font for input
            height=45,  # Taller input fields
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border'],
            fg_color=COLORS['bg_tertiary'],
            text_color=COLORS['text_primary'],
            show=show
        )
        entry.pack(fill="x")
        entry.insert(0, initial_value)

        return entry

    def update_password(self):
        """Update the password"""
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
