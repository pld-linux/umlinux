%define kernel_version 2.4.24
%define utils_version 20040406
Summary:	User Mode Linux
Summary(pl):	Linux w przestrzeni u¿ytkownika
Name:		umlinux
Version:	2
Release:	1.1
Epoch:		0
License:	GPL
Group:		Applications/Emulators
Source0:	ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-%{kernel_version}.tar.bz2
# Source0-md5:	1e055c42921b2396a559d84df4c3d9aa
Source1:	%{name}-config
Source2:	http://dl.sourceforge.net/user-mode-linux/uml_utilities_%{utils_version}.tar.bz2
# Source2-md5:	2c1ccd9efacbfb39e42d482b89b2550a
Source3:	http://user-mode-linux.sourceforge.net/UserModeLinux-HOWTO.html
# Source3-md5:	781dc3611ebf60ac07814a1cd31c936d
Source4:	%{name}-etc-umltab
Source5:	%{name}-rc-init
Patch0:		http://dl.sourceforge.net/user-mode-linux/uml-patch-%{kernel_version}-%{version}.bz2
URL:		http://user-mode-linux.sourceforge.net/
BuildRequires:	libpcap-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
User Mode Linux.

%description -l pl
Linux w przestrzeni u¿ytkownika.

%package modules
Summary:	User Mode Linux modules
Summary(pl):	Modu³y Linuksa w przestrzeni u¿ytkownika
Group:		Applications/Emulators

%description modules
Modules for User Mode Linux.

%description modules -l pl
Modu³y Linuksa w przestrzeni u¿ytkownika.


%package utils
Summary:	User Mode Linux Utilities
Summary(pl):	Narzêdzia dla Linuksa w przestrzeni u¿ytkownika
Group:		Applications/Emulators

%description utils
Utilities for User Mode Linux.

%description utils -l pl
Narzêdzia dla Linuksa w przestrzeni u¿ytkownika.

%package utils-perl
Summary:	User Mode Linux Perl Utilities
Summary(pl):	Narzêdzia perlowe dla Linuksa w przestrzeni u¿ytkownika
Group:		Applications/Emulators

%description utils-perl
Perl Utilities for User Mode Linux.

%description utils-perl -l pl
Narzêdzia perlowe dla Linuksa w przestrzeni u¿ytkownika.

%package init
Summary:	Automagic startup/shutdown User Mode Linux
Summary(pl):	Automagiczy start/stop Linuksa w przestrzeni u¿ytkownika
Group:		Applications/Emulators

%description init
Utilities for automagic startup/shutdown User Mode Linux.

%description init -l pl
Automagiczy start/stop Linuksa w przestrzeni u¿ytkownika.

%prep
%setup  -q -n linux-%{kernel_version} -a 2
%patch0 -p1
cp %{SOURCE1} ./.config
cp %{SOURCE3} .

%build
%{__make} ARCH=um oldconfig
%{__make} ARCH=um dep
# $((0x... )) it's not /bin/sh compatible:
%{__make} ARCH=um SHELL=/bin/bash linux
%{__make} ARCH=um modules
cd tools
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -d ${RPM_BUILD_ROOT}/etc/rc.d/init.d/
install %{SOURCE4} ${RPM_BUILD_ROOT}/etc/umltab
install %{SOURCE5} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/uml

%{__make} ARCH=um modules_install  INSTALL_MOD_PATH=$RPM_BUILD_ROOT
install linux  ${RPM_BUILD_ROOT}%{_bindir}/umlinux
install tools/moo/uml_moo $RPM_BUILD_ROOT%{_bindir}
install tools/umlgdb/umlgdb $RPM_BUILD_ROOT%{_bindir}
install tools/port-helper/port-helper $RPM_BUILD_ROOT%{_bindir}
install tools/uml_net/uml_net $RPM_BUILD_ROOT%{_bindir}
install tools/uml_router/uml_switch $RPM_BUILD_ROOT%{_bindir}
install tools/watchdog/uml_watchdog $RPM_BUILD_ROOT%{_bindir}
install tools/jail/jailer.pl $RPM_BUILD_ROOT%{_bindir}
install tools/jailtest/jailtest $RPM_BUILD_ROOT%{_bindir}
install tools/tunctl/tunctl $RPM_BUILD_ROOT%{_bindir}
install tools/honeypot/honeypot.pl $RPM_BUILD_ROOT%{_bindir}
# install tools/honeypot/hppfslib.pm ?
# install tools/honeypot/hppfs.pm ?

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.html
%attr(755,root,root) %{_bindir}/umlinux

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jailtest
%attr(755,root,root) %{_bindir}/port-helper
%attr(755,root,root) %{_bindir}/tunctl
%attr(755,root,root) %{_bindir}/umlgdb
%attr(755,root,root) %{_bindir}/uml_moo
%attr(755,root,root) %{_bindir}/uml_net
%attr(755,root,root) %{_bindir}/uml_switch
%attr(755,root,root) %{_bindir}/uml_watchdog

%files utils-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/honeypot.pl
%attr(755,root,root) %{_bindir}/jailer.pl
# honeypot/hppfslib.pm ?
# honeypot/hppfs.pm ?

%files modules
%defattr(644,root,root,755)
/lib/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/uml
/etc/umltab
