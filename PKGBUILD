pkgname=vscode-projects-launcher
pkgver=1.0.0
pkgrel=1
pkgdesc="A GTK Python launcher for your VS Code projects using TOML"
arch=('any')
url="https://github.com/livcl-be/vscode-projects-launcher"
license=('GPL-3')
depends=('python' 'python-gobject' 'python-toml' 'gtk4')
source=("${pkgname}.desktop"
        "icon.png"
        "src/")
md5sums=('SKIP' 'SKIP' 'SKIP')

package() {
  install -d "$pkgdir/usr/share/applications"
  install -Dm644 "$srcdir/${pkgname}.desktop" "$pkgdir/usr/share/applications/${pkgname}.desktop"

  install -d "$pkgdir/usr/share/icons/hicolor/scalable/apps"
  install -Dm644 "$srcdir/icon.png" "$pkgdir/usr/share/icons/hicolor/scalable/apps/${pkgname}.png"

  install -d "$pkgdir/usr/bin"
  echo -e "#!/bin/sh\npython /usr/share/${pkgname}/main.py" > "$pkgdir/usr/bin/${pkgname}"
  chmod +x "$pkgdir/usr/bin/${pkgname}"

  install -d "$pkgdir/usr/share/${pkgname}"
  cp -r "$srcdir/src/vscode_projects_launcher" "$pkgdir/usr/share/${pkgname}/"
}
