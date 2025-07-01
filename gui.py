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
        self.root.configure(bg='#0D1117')
        self.root.resizable(True, True)

        # Set minimum window size
        self.root.minsize(1000, 700)

        self.setup_styles()
        self.show_login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Dark theme styling with modern aesthetics
        style.configure('Title.TLabel',
                       font=('SF Pro Display', 24, 'bold'),
                       foreground='#F0F6FC',
                       background='#0D1117')

        style.configure('Subtitle.TLabel',
                       font=('SF Pro Display', 14, 'normal'),
                       foreground='#8B949E',
                       background='#0D1117')

        style.configure('Heading.TLabel',
                       font=('SF Pro Display', 14, 'bold'),
                       foreground='#F0F6FC',
                       background='#21262D')

        # Modern button styles with subtle gradients
        style.configure('Primary.TButton',
                       font=('SF Pro Display', 11, 'bold'),
                       padding=(16, 8))

        style.map('Primary.TButton',
                 background=[('active', '#1F6FEB'),
                           ('!active', '#238636')],
                 foreground=[('active', '#FFFFFF'),
                           ('!active', '#FFFFFF')])

        style.configure('Success.TButton',
                       font=('SF Pro Display', 11, 'bold'),
                       padding=(16, 8))

        style.map('Success.TButton',
                 background=[('active', '#2EA043'),
                           ('!active', '#238636')],
                 foreground=[('active', '#FFFFFF'),
                           ('!active', '#FFFFFF')])

        style.configure('Danger.TButton',
                       font=('SF Pro Display', 11, 'bold'),
                       padding=(16, 8))

        style.map('Danger.TButton',
                 background=[('active', '#DA3633'),
                           ('!active', '#F85149')],
                 foreground=[('active', '#FFFFFF'),
                           ('!active', '#FFFFFF')])

        style.configure('Secondary.TButton',
                       font=('SF Pro Display', 11, 'bold'),
                       padding=(16, 8))

        style.map('Secondary.TButton',
                 background=[('active', '#30363D'),
                           ('!active', '#21262D')],
                 foreground=[('active', '#F0F6FC'),
                           ('!active', '#8B949E')])

        style.configure('Warning.TButton',
                       font=('SF Pro Display', 11, 'bold'),
                       padding=(16, 8))

        style.map('Warning.TButton',
                 background=[('active', '#BB8009'),
                           ('!active', '#D29922')],
                 foreground=[('active', '#000000'),
                           ('!active', '#000000')])

        # Modern dark Treeview styling with centered text
        style.configure('Dark.Treeview',
                       background='#0D1117',
                       foreground='#F0F6FC',
                       fieldbackground='#0D1117',
                       font=('SF Pro Display', 11),
                       rowheight=36,
                       borderwidth=0,
                       anchor='center')

        style.configure('Dark.Treeview.Heading',
                       background='#21262D',
                       foreground='#F0F6FC',
                       font=('SF Pro Display', 11, 'bold'),
                       relief='flat',
                       borderwidth=1,
                       anchor='center')

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Dark background
        login_frame = tk.Frame(self.root, bg='#0D1117')
        login_frame.pack(expand=True, fill='both')

        # Center container
        center_frame = tk.Frame(login_frame, bg='#0D1117')
        center_frame.pack(expand=True)

        # Modern title
        title_label = ttk.Label(center_frame, text="🔒 Password Manager", style='Title.TLabel')
        title_label.pack(pady=(0, 8))

        subtitle_label = ttk.Label(center_frame, text="Secure • Simple • Private", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 40))

        # Modern dark form card with subtle border
        form_frame = tk.Frame(center_frame, bg='#21262D', relief='solid', bd=1)
        form_frame.pack(padx=40, pady=20, ipadx=40, ipady=30)

        tk.Label(form_frame, text="Master Password",
                font=('SF Pro Display', 14, 'bold'),
                fg='#F0F6FC', bg='#21262D').pack(pady=(0, 8))

        self.master_password_entry = tk.Entry(form_frame,
                                             font=('SF Pro Display', 14),
                                             show='•',
                                             width=30,
                                             relief='solid',
                                             bd=1,
                                             bg='#0D1117',
                                             fg='#F0F6FC',
                                             insertbackground='#238636',
                                             highlightthickness=2,
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

        # Dark main container
        main_frame = tk.Frame(self.root, bg='#0D1117')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)

        # Modern dark header
        header_frame = tk.Frame(main_frame, bg='#21262D', relief='solid', bd=1)
        header_frame.pack(fill='x', pady=(0, 20))

        header_content = tk.Frame(header_frame, bg='#21262D')
        header_content.pack(fill='x', padx=25, pady=15)

        title_label = ttk.Label(header_content, text="🔒 Password Manager", style='Title.TLabel')
        title_label.pack(side='left')

        logout_btn = ttk.Button(header_content,
                               text="Sign Out",
                               command=self.logout,
                               style='Danger.TButton')
        logout_btn.pack(side='right')

        # Action buttons with dark theme
        action_frame = tk.Frame(main_frame, bg='#21262D', relief='solid', bd=1)
        action_frame.pack(fill='x', pady=(0, 20))

        action_content = tk.Frame(action_frame, bg='#21262D')
        action_content.pack(fill='x', padx=25, pady=15)

        add_btn = ttk.Button(action_content,
                            text="+ Add Password",
                            command=self.show_add_password_dialog,
                            style='Success.TButton')
        add_btn.pack(side='left', padx=(0, 10))

        refresh_btn = ttk.Button(action_content,
                               text="⟳ Refresh",
                               command=self.refresh_passwords,
                               style='Secondary.TButton')
        refresh_btn.pack(side='left')

        # Dark password list
        list_frame = tk.Frame(main_frame, bg='#21262D', relief='solid', bd=1)
        list_frame.pack(expand=True, fill='both')

        list_content = tk.Frame(list_frame, bg='#21262D')
        list_content.pack(expand=True, fill='both', padx=25, pady=20)

        ttk.Label(list_content, text="Saved Passwords", style='Heading.TLabel').pack(anchor='w', pady=(0, 15))

        # Modern dark treeview
        tree_container = tk.Frame(list_content, bg='#0D1117', relief='solid', bd=1)
        tree_container.pack(expand=True, fill='both')

        columns = ('Website', 'Username', 'Password', 'Actions')
        self.password_tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                         height=15, style='Dark.Treeview')

        self.password_tree.heading('Website', text='Website')
        self.password_tree.heading('Username', text='Username')
        self.password_tree.heading('Password', text='Password')
        self.password_tree.heading('Actions', text='Actions')

        self.password_tree.column('Website', width=250, minwidth=200)
        self.password_tree.column('Username', width=250, minwidth=200)
        self.password_tree.column('Password', width=150, minwidth=100)
        self.password_tree.column('Actions', width=200, minwidth=150)

        scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.password_tree.yview)
        self.password_tree.configure(yscrollcommand=scrollbar.set)

        self.password_tree.pack(side='left', expand=True, fill='both', padx=2, pady=2)
        scrollbar.pack(side='right', fill='y', padx=(0, 2), pady=2)

        # Use single click for Actions column to show context menu
        self.password_tree.bind('<Double-1>', self.on_treeview_click)

        self.create_context_menu()
        self.password_tree.bind('<Button-2>', self.show_context_menu)
        self.password_tree.bind('<Button-3>', self.show_context_menu)

        self.refresh_passwords()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0,
                                   bg='#21262D', fg='#F0F6FC',
                                   activebackground='#238636', activeforeground='#FFFFFF',
                                   font=('SF Pro Display', 11),
                                   borderwidth=0)
        self.context_menu.add_command(label="👁 Show Password", command=self.show_password_options)
        self.context_menu.add_command(label="✏️ Edit Entry", command=self.edit_password_entry)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy Password", command=self.copy_password)
        self.context_menu.add_command(label="👤 Copy Username", command=self.copy_username)
        self.context_menu.add_command(label="🌐 Copy Website", command=self.copy_website)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑 Delete Entry", command=self.delete_password)

    def show_context_menu(self, event):
        item = self.password_tree.identify_row(event.y)
        if item:
            self.password_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def edit_password_entry(self):
        """Edit an existing password entry"""
        selection = self.password_tree.selection()
        if selection:
            item_id = selection[0]
            if item_id in self.password_data:
                data = self.password_data[item_id]
                dialog = EditPasswordDialog(self.root, self.update_password_entry, data)

    def copy_to_clipboard(self, text, label):
        """Copy text to clipboard and show confirmation"""
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(text)
            messagebox.showinfo("✓ Copied", f"{label} copied to clipboard!", parent=self.root)
        else:
            messagebox.showinfo(f"📋 {label}", f"{label}: {text}", parent=self.root)

    def copy_password(self, event=None):
        selection = self.password_tree.selection()
        if selection:
            item_id = selection[0]
            if item_id in self.password_data:
                password = self.password_data[item_id]['password']
                self.copy_to_clipboard(password, "Password")

    def copy_username(self):
        selection = self.password_tree.selection()
        if selection:
            item_id = selection[0]
            if item_id in self.password_data:
                username = self.password_data[item_id]['username']
                self.copy_to_clipboard(username, "Username")

    def copy_website(self):
        selection = self.password_tree.selection()
        if selection:
            item_id = selection[0]
            if item_id in self.password_data:
                website = self.password_data[item_id]['website']
                self.copy_to_clipboard(website, "Website")

    def delete_password(self):
        selection = self.password_tree.selection()
        if selection:
            item_id = selection[0]
            if item_id in self.password_data:
                data = self.password_data[item_id]
                if messagebox.askyesno("Confirm Delete",
                                     f"Are you sure you want to delete the password for {data['website']}?",
                                     icon='warning'):
                    try:
                        delete_password(data['id'], self.master_password)
                        messagebox.showinfo("Success", "Password deleted successfully!")
                        self.refresh_passwords()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete password: {str(e)}")

    def show_password_options(self, event=None):
        """Show options to copy or reveal password"""
        selection = self.password_tree.selection()
        if selection:
            item_id = selection[0]
            if item_id in self.password_data:
                self.create_password_options_dialog(item_id)

    def on_treeview_click(self, event):
        """Handle clicks on the treeview for copying and options"""
        region = self.password_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.password_tree.identify_column(event.x)
            item = self.password_tree.identify_row(event.y)

            if item and item in self.password_data:
                self.password_tree.selection_set(item)
                data = self.password_data[item]

                if column == '#1':  # Website column
                    self.copy_to_clipboard(data['website'], "Website")
                elif column == '#2':  # Username column
                    self.copy_to_clipboard(data['username'], "Username")
                elif column == '#3':  # Password column
                    self.copy_to_clipboard(data['password'], "Password")
                elif column == '#4':  # Actions column
                    # Use the same context menu as right-click
                    self.context_menu.post(event.x_root, event.y_root)

    def create_password_options_dialog(self, item_id):
        """Create dialog with password options"""
        data = self.password_data[item_id]

        dialog = tk.Toplevel(self.root)
        dialog.title("Password Options")
        dialog.geometry("450x400")
        dialog.configure(bg='#0D1117')
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, self.root.winfo_rooty() + 200))

        # Main content with dark theme
        main_frame = tk.Frame(dialog, bg='#21262D', relief='solid', bd=1)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        content_frame = tk.Frame(main_frame, bg='#21262D')
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        tk.Label(content_frame, text=f"🔒 {data['website']}",
                font=('SF Pro Display', 16, 'bold'),
                fg='#F0F6FC', bg='#21262D').pack(pady=(0, 20))

        # Username
        tk.Label(content_frame, text=f"Username: {data['username']}",
                font=('SF Pro Display', 12),
                fg='#8B949E', bg='#21262D').pack(pady=(0, 20))

        # Password section
        password_frame = tk.Frame(content_frame, bg='#21262D')
        password_frame.pack(fill='x', pady=(0, 20))

        tk.Label(password_frame, text="Password:",
                font=('SF Pro Display', 12, 'bold'),
                fg='#F0F6FC', bg='#21262D').pack(anchor='w')

        # Password display with toggle
        self.password_var = tk.StringVar(value='•' * len(data['password']))
        self.password_shown = False

        password_display_frame = tk.Frame(password_frame, bg='#0D1117', relief='solid', bd=1)
        password_display_frame.pack(fill='x', pady=(5, 10))

        self.password_display_label = tk.Label(password_display_frame,
                                              textvariable=self.password_var,
                                              font=('SF Pro Display', 12),
                                              fg='#F0F6FC', bg='#0D1117',
                                              anchor='w')
        self.password_display_label.pack(side='left', padx=10, pady=8, fill='x', expand=True)

        toggle_btn = ttk.Button(password_display_frame,
                               text="👁",
                               command=lambda: self.toggle_password_visibility(data['password']),
                               style='Secondary.TButton')
        toggle_btn.pack(side='right', padx=5, pady=2)

        # Action buttons
        button_frame = tk.Frame(content_frame, bg='#21262D')
        button_frame.pack(fill='x', pady=(10, 0))

        if CLIPBOARD_AVAILABLE:
            copy_btn = ttk.Button(button_frame,
                                 text="📋 Copy Password",
                                 command=lambda: self.copy_password_from_dialog(data['password'], dialog),
                                 style='Primary.TButton')
            copy_btn.pack(side='left', padx=(0, 10))

        close_btn = ttk.Button(button_frame,
                              text="Close",
                              command=dialog.destroy,
                              style='Secondary.TButton')
        close_btn.pack(side='right')

    def edit_from_dialog(self, data, dialog):
        """Edit password entry from the password options dialog"""
        dialog.destroy()  # Close the options dialog first
        # Find the item_id for this data
        for item_id, item_data in self.password_data.items():
            if item_data['id'] == data['id']:
                self.password_tree.selection_set(item_id)
                break
        # Open edit dialog
        EditPasswordDialog(self.root, self.update_password_entry, data)

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

    def refresh_passwords(self):
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)
        self.password_data.clear()

        try:
            passwords = get_passwords(self.key, self.master_password)
            for pwd in passwords:
                masked_password = '•' * 8
                item_id = self.password_tree.insert('', 'end', values=(
                    pwd['website'],
                    pwd['username'],
                    masked_password,
                    "⚙️ Options"
                ))
                self.password_data[item_id] = {
                    'id': pwd['id'],
                    'website': pwd['website'],
                    'username': pwd['username'],
                    'password': pwd['password']
                }

                # Center the text in all columns
                for col in ['Website', 'Username', 'Password', 'Actions']:
                    self.password_tree.set(item_id, col, self.password_tree.set(item_id, col))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passwords: {str(e)}", parent=self.root)

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
        self.dialog.geometry("500x450")
        self.dialog.configure(bg='#0D1117')
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))

        self.create_form()
        self.website_entry.focus()

    def create_form(self):
        # Dark main container
        main_frame = tk.Frame(self.dialog, bg='#21262D', relief='solid', bd=1)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        content_frame = tk.Frame(main_frame, bg='#21262D')
        content_frame.pack(expand=True, fill='both', padx=30, pady=30)

        # Dark theme title
        title_label = tk.Label(content_frame,
                              text="Add New Password",
                              font=('SF Pro Display', 18, 'bold'),
                              fg='#F0F6FC',
                              bg='#21262D')
        title_label.pack(pady=(0, 30))

        # Dark input fields
        self.create_input_field(content_frame, "Website", "website_entry")
        self.create_input_field(content_frame, "Username", "username_entry")
        self.create_input_field(content_frame, "Password", "password_entry", show='•')

        # Button container
        button_frame = tk.Frame(content_frame, bg='#21262D')
        button_frame.pack(pady=(30, 0))

        # Dark theme buttons
        save_btn = ttk.Button(button_frame,
                             text="Save Password",
                             command=self.save_password,
                             style='Primary.TButton')
        save_btn.pack(side='left', padx=(0, 10))

        cancel_btn = ttk.Button(button_frame,
                               text="Cancel",
                               command=self.dialog.destroy,
                               style='Secondary.TButton')
        cancel_btn.pack(side='left')

        self.dialog.bind('<Return>', lambda e: self.save_password())

    def create_input_field(self, parent, label_text, field_name, show=None):
        # Dark theme label
        tk.Label(parent, text=label_text,
                font=('SF Pro Display', 12, 'bold'),
                fg='#F0F6FC', bg='#21262D').pack(anchor='w', pady=(15, 5))

        # Dark theme input field
        entry = tk.Entry(parent,
                        font=('SF Pro Display', 12),
                        width=40,
                        relief='solid',
                        bd=1,
                        bg='#0D1117',
                        fg='#F0F6FC',
                        insertbackground='#238636',
                        highlightthickness=2,
                        highlightcolor='#238636',
                        highlightbackground='#30363D',
                        show=show)
        entry.pack(pady=(0, 5), ipady=8)

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
        self.dialog.geometry("500x450")
        self.dialog.configure(bg='#0D1117')
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))

        self.create_form()
        self.website_entry.focus()

    def create_form(self):
        # Dark main container
        main_frame = tk.Frame(self.dialog, bg='#21262D', relief='solid', bd=1)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        content_frame = tk.Frame(main_frame, bg='#21262D')
        content_frame.pack(expand=True, fill='both', padx=30, pady=30)

        # Dark theme title
        title_label = tk.Label(content_frame,
                              text="Edit Password",
                              font=('SF Pro Display', 18, 'bold'),
                              fg='#F0F6FC',
                              bg='#21262D')
        title_label.pack(pady=(0, 30))

        # Dark input fields with existing data
        self.create_input_field(content_frame, "Website", "website_entry", self.existing_data['website'])
        self.create_input_field(content_frame, "Username", "username_entry", self.existing_data['username'])
        self.create_input_field(content_frame, "Password", "password_entry", self.existing_data['password'], show='•')

        # Button container
        button_frame = tk.Frame(content_frame, bg='#21262D')
        button_frame.pack(pady=(30, 0))

        # Dark theme buttons
        update_btn = ttk.Button(button_frame,
                               text="Update Password",
                               command=self.update_password,
                               style='Warning.TButton')
        update_btn.pack(side='left', padx=(0, 10))

        cancel_btn = ttk.Button(button_frame,
                               text="Cancel",
                               command=self.dialog.destroy,
                               style='Secondary.TButton')
        cancel_btn.pack(side='left')

        self.dialog.bind('<Return>', lambda e: self.update_password())

    def create_input_field(self, parent, label_text, field_name, initial_value="", show=None):
        # Dark theme label
        tk.Label(parent, text=label_text,
                font=('SF Pro Display', 12, 'bold'),
                fg='#F0F6FC', bg='#21262D').pack(anchor='w', pady=(15, 5))

        # Dark theme input field
        entry = tk.Entry(parent,
                        font=('SF Pro Display', 12),
                        width=40,
                        relief='solid',
                        bd=1,
                        bg='#0D1117',
                        fg='#F0F6FC',
                        insertbackground='#238636',
                        highlightthickness=2,
                        highlightcolor='#238636',
                        highlightbackground='#30363D',
                        show=show)
        entry.pack(pady=(0, 5), ipady=8)
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
