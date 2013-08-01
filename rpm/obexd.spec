Name:       obexd
Summary:    D-Bus service for Obex Client access
Version:    0.42
Release:    1
Group:      System/Daemons
License:    GPLv2+
URL:        http://www.bluez.org/
Source0:    http://www.kernel.org/pub/linux/bluetooth/obexd-%{version}.tar.gz
Source100:  obexd.yaml
BuildRequires:  pkgconfig(openobex)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(bluez) >= 4.0
BuildRequires:  pkgconfig(libical)

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


%build
./bootstrap

%reconfigure --disable-static \
    --enable-usb --enable-pcsuite

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install


%files
%defattr(-,root,root,-)
%doc README doc/client-api.txt COPYING AUTHORS
%{_libexecdir}/obex-client
%{_datadir}/dbus-1/services/obex-client.service


%files server
%defattr(-,root,root,-)
%{_libexecdir}/obexd
%{_datadir}/dbus-1/services/obexd.service
#%{_libdir}/obex/plugins/*.so


%files devel
%defattr(-,root,root,-)
%doc  doc/client-api.txt
