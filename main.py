import toml
import subprocess
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk

CONFIG_FILE = "projects.toml"


class ProjectLauncher(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.ProjectLauncher")
        self.projects = []

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_activate(self):
        self.load_projects()

        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title("VS Code Project Launcher")
        self.window.set_default_size(700, 500)

        # Header bar
        header = Gtk.HeaderBar()
        title_label = Gtk.Label(label="VS Code Project Launcher")
        title_label.get_style_context().add_class("title")
        header.set_title_widget(title_label)
        self.window.set_titlebar(header)

        # Add gear button to top-left
        gear_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="emblem-system-symbolic")  # gear icon
        image = Gtk.Image.new_from_gicon(icon)
        gear_button.set_child(image)
        gear_button.set_tooltip_text("Settings")
        gear_button.connect("clicked", self.open_settings_window)
        header.pack_start(gear_button)

        # Scrollable area
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.window.set_child(scrolled)

        # FlowBox for 2-column layout
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_max_children_per_line(2)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.set_child(self.flowbox)

        for project in self.projects:
            button = self.create_button(project)
            self.flowbox.append(button)

        self.window.present()
    
    def refresh_projects(self):
        # Load file again
        self.load_projects()

        # Remove all children from grid
        self.flowbox.remove_all()
        
        # Re-add buttons
        for project in self.projects:
            button = self.create_button(project)
            self.flowbox.append(button)

        self.window.present()

    def create_button(self, project):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(25)
        box.set_margin_bottom(25)
        box.set_margin_start(25)
        box.set_margin_end(25)
        box.set_valign(Gtk.Align.CENTER)

        # Project Name
        name_label = Gtk.Label(label=project.get("name", "Unnamed"))
        name_label.set_wrap(True)
        name_label.set_justify(Gtk.Justification.CENTER)
        name_label.set_xalign(0.5)
        name_label.set_margin_bottom(4)
        name_label.set_css_classes(["title"])

        # Profile Subtext
        profile_label = Gtk.Label(label=f"Profile: {project.get('profile', '')}")
        profile_label.set_xalign(0.5)
        profile_label.set_opacity(0.6)
        profile_label.set_margin_bottom(6)

        box.append(name_label)
        box.append(profile_label)

        # Clickable area
        button = Gtk.Button()
        button.set_child(box)
        button.set_hexpand(True)
        button.set_margin_top(20)
        button.set_margin_bottom(20)
        button.set_margin_start(20)
        button.set_margin_end(20)
        button.set_vexpand(True)
        button.set_size_request(250, 100)
        button.connect("clicked", self.launch_project, project)

        return button

    def open_settings_window(self, button):
        settings_window = Gtk.Window(
            title="Edit Projects",
            transient_for=self.window,
            modal=True
        )
        settings_window.set_default_size(700, 500)
        settings_window.set_destroy_with_parent(True)

        # Vertical layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        settings_window.set_child(vbox)

        # TextView
        textview = Gtk.TextView()
        textbuffer = textview.get_buffer()

        try:
            with open(CONFIG_FILE, "r") as f:
                toml_text = f.read()
        except FileNotFoundError:
            toml_text = ""

        textbuffer.set_text(toml_text)

        scroll = Gtk.ScrolledWindow()
        scroll.set_min_content_height(400)
        scroll.set_child(textview)
        vbox.append(scroll)

        # Save and Cancel buttons
        button_box = Gtk.Box(spacing=10)
        save_btn = Gtk.Button(label="Save")
        cancel_btn = Gtk.Button(label="Cancel")
        button_box.append(save_btn)
        button_box.append(cancel_btn)
        vbox.append(button_box)

        # Cancel: just close the window
        cancel_btn.connect("clicked", lambda b: settings_window.close())

        # Save: validate TOML and update file
        def on_save_clicked(button):
            start = textbuffer.get_start_iter()
            end = textbuffer.get_end_iter()
            new_text = textbuffer.get_text(start, end, True)
            try:
                toml.loads(new_text)  # Validate
                with open(CONFIG_FILE, "w") as f:
                    f.write(new_text)
                self.load_projects()
                self.refresh_projects()
                settings_window.close()
            except Exception as e:
                error_win = Gtk.Window(transient_for=settings_window, modal=True, title="Error")
                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                box.set_margin_top(10)
                box.set_margin_bottom(10)
                box.set_margin_start(10)
                box.set_margin_end(10)
                error_win.set_child(box)
                label = Gtk.Label(label=f"Invalid TOML:\n{e}")
                box.append(label)
                close = Gtk.Button(label="Close")
                close.connect("clicked", lambda _: error_win.close())
                box.append(close)
                error_win.present()

        save_btn.connect("clicked", on_save_clicked)

        settings_window.present()


    def load_projects(self):
        try:
            config = toml.load(CONFIG_FILE)
            self.projects = config.get("projects", [])
        except Exception as e:
            print(f"Error loading config: {e}")
            self.projects = []

    def launch_project(self, button, project):
        location = project.get("location", "")
        profile = project.get("profile", "")
        try:
            subprocess.Popen(["code", "--profile", profile, location])
        except Exception as e:
            print(f"Failed to launch project: {e}")


if __name__ == "__main__":
    import sys

    app = ProjectLauncher()
    app.run(sys.argv)
