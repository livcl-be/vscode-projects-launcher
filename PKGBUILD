pkgname=vscode-projects-launcher
pkgver=1.0.0
pkgrel=1
pkgdesc="A GTK Python launcher for your VS Code projects using TOML"
arch=('any')
url="https://github.com/livcl-be/vscode-projects-launcher"
license=('GPL-3')
depends=('gtk4')
source=("${pkgname}.desktop"
        "requirements.txt"
        "icon.png"
        "main.py"
        "projects.toml")
md5sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

build() {
  cd "$srcdir"

  # Create a virtual environment just for build
  python -m venv venv
  source venv/bin/activate

  # Install dependencies locally with pip
  pip install --upgrade pip
  pip install -r requirements.txt

  # Build the app using PyInstaller
  pyinstaller --noconfirm --onefile --name vscode-projects-launcher main.py

  deactivate
}

package() {
  install -Dm755 "$srcdir/dist/vscode-projects-launcher" \
    "$pkgdir/usr/bin/vscode-projects-launcher"

  install -Dm755 "$srcdir/projects.toml" \
    "$pkgdir/usr/bin/projects.toml"

  install -Dm644 "$srcdir/vscode-projects-launcher.desktop" \
    "$pkgdir/usr/share/applications/vscode-projects-launcher.desktop"

  install -Dm644 "$srcdir/icon.png" \
    "$pkgdir/usr/share/icons/hicolor/256x256/apps/vscode-projects-launcher.png"
}