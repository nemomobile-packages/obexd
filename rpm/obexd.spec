Name:       obexd
Summary:    D-Bus service for Obex Client access
Version:    0.42
Release:    1
Group:      System/Daemons
License:    GPLv2+
URL:        http://www.bluez.org/
Source0:    http://www.kernel.org/pub/linux/bluetooth/obexd-%{version}.tar.gz
Source1:    obexd-wrapper
Source2:    obexd.conf
Patch0:     FTP-fix-directory-creation-failure.patch
Patch1:     OPP-disconnect-request-on-client-exit.patch
Patch2:     OPP-disable-SRM.patch
Patch3:     OPP-supported-format-list.patch
Patch4:     OPP-version.patch
Patch5:     USB-retry-tty.patch
Patch6:     FTP-fix-close-pipe-fds-issue.patch
BuildRequires:  automake, libtool
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(bluez) >= 4.0
BuildRequires:  pkgconfig(libical)
Requires:       obex-capability

%description
obexd contains obex-client, a D-Bus service to allow sending files
using the Obex Push protocol, common on mobile phones and
other Bluetooth-equipped devices.


%package server
Summary:    a server for incoming OBEX connections
Group:      System/Daemons
Requires:   %{name} = %{version}-%{release}

%description server
obexd-server contains a server for receiving OBEX operations.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q -n %{name}-%{version}/%{name}

# FTP-fix-directory-creation-failure.patch
%patch0 -p1
# OPP-disconnect-request-on-client-exit.patch
%patch1 -p1
# OPP-disable-SRM.patch
%patch2 -p1
# OPP-supported-format-list.patch
%patch3 -p1
# OPP-version.patch
%patch4 -p1
# USB-retry-tty.patch
%patch5 -p1
# FTP-fix-close-pipe-fds-issue.patch
%patch6 -p1

%build
./bootstrap
sed -i 's/ovi_suite/pc_suite/' plugins/usb.c
%reconfigure --disable-static \
    --enable-usb --enable-pcsuite

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
install -m755 -D %{SOURCE1} %{buildroot}/%{_libexecdir}/obexd-wrapper
install -m644 -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/obexd.conf
sed -i 's,/usr/libexec/obexd,/usr/libexec/obexd-wrapper,' \
    %{buildroot}/%{_datadir}/dbus-1/services/obexd.service
mkdir -p %{buildroot}/%{_sysconfdir}/obexd/{plugins,noplugins}


%files
%defattr(-,root,root,-)
%doc README doc/client-api.txt COPYING AUTHORS
%{_libexecdir}/obex-client
%{_datadir}/dbus-1/services/obex-client.service


%files server
%defattr(-,root,root,-)
%config %{_sysconfdir}/obexd.conf
%dir %{_sysconfdir}/obexd/
%dir %{_sysconfdir}/obexd/plugins/
%dir %{_sysconfdir}/obexd/noplugins/
%{_libexecdir}/obexd
%{_libexecdir}/obexd-wrapper
%{_datadir}/dbus-1/services/obexd.service


%files devel
%defattr(-,root,root,-)
%doc  doc/client-api.txt
