# VS Code Projects Launcher

A minimal GTK4 Python application that lets you manage and launch your VS Code projects with their own profiles.

<p align="center">
  <img src="homescreen.png" alt="Homescreen" width="45%"/>
  <img src="settings.png" alt="Settings" width="45%"/>
</p>

## 🧩 Features

- Read projects from a simple `projects.toml` file
- Launch VS Code with `--profile` and project path in one click
- Clean GTK4 UI with a native look
- Edit the TOML file directly via the built-in settings screen
- Responsive layout with dark/light theme support
- Optional `.desktop` integration and launcher icon



## 🛠 Requirements

- Python ≥ 3.10
- [GTK 4](https://docs.gtk.org/gtk4/) & PyGObject
- `code` (VS Code CLI must be in PATH)

Install dependencies on Arch:

```bash
sudo pacman -S gtk4 python-gobject
pip install toml
````



## 📁 TOML Configuration

Create a `projects.toml` file in the working directory like this:

```toml
[[projects]]
name = "CAST"
location = "/home/liv/projects/cast"
profile = "CAST"

[[projects]]
name = "Side Project"
location = "/home/liv/projects/side"
profile = "Default"
```



## 🚀 Running

```bash
python src/vscode_projects_launcher/main.py
```

or if you’ve installed it:

```bash
vscode-projects-launcher
```



## 🖥️ Desktop Launcher (optional)

If you install via AUR or manually place the `.desktop` file and icon:

```bash
cp vscode-projects-launcher.desktop ~/.local/share/applications/
cp icon.png ~/.local/share/icons/hicolor/256x256/apps/vscode-projects-launcher.png
```

Then launch it from GNOME/KDE menu!



## 📦 AUR Packaging

To install from source:

```bash
makepkg -si
```

To publish to AUR, see [Arch Wiki - AUR submission](https://wiki.archlinux.org/title/Arch_User_Repository#Submitting_packages).



## 📄 License

GPL-3 License. See [LICENSE](LICENSE).



## 🤝 Contributing

PRs welcome! Bug reports and ideas too.
