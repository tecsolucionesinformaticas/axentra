Name:       rustdesk
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     rustdesk <info@rustdesk.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/rustdesk/
mkdir -p %{buildroot}/usr/share/axentra/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/rustdesk %{buildroot}/usr/bin/rustdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/rustdesk/libsciter-gtk.so
install $HBB/res/rustdesk.service %{buildroot}/usr/share/axentra/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/rustdesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/rustdesk.svg
install $HBB/res/axentra.desktop %{buildroot}/usr/share/axentra/files/
install $HBB/res/axentra-link.desktop %{buildroot}/usr/share/axentra/files/

%files
/usr/bin/rustdesk
/usr/share/rustdesk/libsciter-gtk.so
/usr/share/axentra/files/rustdesk.service
/usr/share/icons/hicolor/256x256/apps/rustdesk.png
/usr/share/icons/hicolor/scalable/apps/rustdesk.svg
/usr/share/axentra/files/axentra.desktop
/usr/share/axentra/files/axentra-link.desktop
/usr/share/axentra/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop rustdesk || true
  ;;
esac

%post
cp /usr/share/axentra/files/rustdesk.service /etc/systemd/system/rustdesk.service
cp /usr/share/axentra/files/axentra.desktop /usr/share/applications/
cp /usr/share/axentra/files/axentra-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable rustdesk
systemctl start rustdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop rustdesk || true
    systemctl disable rustdesk || true
    rm /etc/systemd/system/rustdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/axentra.desktop || true
    rm /usr/share/applications/axentra-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
