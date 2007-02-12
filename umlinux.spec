%define kernel_version 2.4.27
%define utils_version 20040406
Summary:	User Mode Linux
Summary(pl.UTF-8):   Linux w przestrzeni użytkownika
Name:		umlinux
Version:	2
Release:	1.%{kernel_version}.1
Epoch:		0
License:	GPL
Group:		Applications/Emulators
Source0:	ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-%{kernel_version}.tar.bz2
# Source0-md5:	59a2e6fde1d110e2ffa20351ac8b4d9e
Source1:	%{name}-config
Source2:	http://dl.sourceforge.net/user-mode-linux/uml_utilities_%{utils_version}.tar.bz2
# Source2-md5:	2c1ccd9efacbfb39e42d482b89b2550a
Source3:	http://user-mode-linux.sourceforge.net/UserModeLinux-HOWTO.html
# Source3-md5:	781dc3611ebf60ac07814a1cd31c936d
Source4:	%{name}-etc-umltab
Source5:	%{name}-rc-init
Patch0:		http://dl.sourceforge.net/user-mode-linux/uml-patch-%{kernel_version}-1.bz2
Patch1:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-apps/usermode-utilities/files/20040406-CAN-2004-1295.patch
Patch2:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.smbfs.patch
Patch3:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.CAN-2004-1056.patch
Patch4:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources.AF_UNIX.patch
Patch5:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.binfmt_elf.patch
Patch6:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.XDRWrapFix.patch
Patch7:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.78362.patch
Patch8:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.77666.patch
Patch9:		ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.77094.patch
Patch10:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.27.CAN-2004-1295.patch
Patch11:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.78363.patch
Patch12:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.CAN-2004-1137.patch
Patch13:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.CAN-2004-1016.patch
Patch14:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.binfmt_a.out.patch
Patch15:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.brk-locked.patch
Patch16:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.cmdlineLeak.patch
Patch17:	ftp://ftp.linux.ee/pub/gentoo/portage/sys-kernel/usermode-sources/files/usermode-sources-2.4.vma.patch
URL:		http://user-mode-linux.sourceforge.net/
BuildRequires:	libpcap-static
BuildRequires:	modutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
User Mode Linux.

%description -l pl.UTF-8
Linux w przestrzeni użytkownika.

%package modules
Summary:	User Mode Linux modules
Summary(pl.UTF-8):   Moduły Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description modules
Modules for User Mode Linux.

%description modules -l pl.UTF-8
Moduły Linuksa w przestrzeni użytkownika.


%package utils
Summary:	User Mode Linux Utilities
Summary(pl.UTF-8):   Narzędzia dla Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators
Version:	%{utils_version}

%description utils
Utilities for User Mode Linux.

%description utils -l pl.UTF-8
Narzędzia dla Linuksa w przestrzeni użytkownika.

%package utils-perl
Summary:	User Mode Linux Perl Utilities
Summary(pl.UTF-8):   Narzędzia perlowe dla Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators
Version:	%{utils_version}

%description utils-perl
Perl Utilities for User Mode Linux.

%description utils-perl -l pl.UTF-8
Narzędzia perlowe dla Linuksa w przestrzeni użytkownika.

%package init
Summary:	Automagic startup/shutdown User Mode Linux
Summary(pl.UTF-8):   Automagiczy start/stop Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description init
Utilities for automagic startup/shutdown User Mode Linux.

%description init -l pl.UTF-8
Automagiczy start/stop Linuksa w przestrzeni użytkownika.

%prep
%setup  -q -n linux-%{kernel_version} -a 2
%patch0 -p1
cd tools
%patch1 -p1
cd ..
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

cp %{SOURCE1} ./.config
cp %{SOURCE3} .

%build
%{__make} ARCH=um oldconfig
%{__make} ARCH=um dep
# $((0x... )) it's not /bin/sh compatible:
%{__make} ARCH=um SHELL=/bin/bash linux
%{__make} ARCH=um modules
%{__make} -C tools

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/rc.d/init.d}
install %{SOURCE4} $RPM_BUILD_ROOT/etc/umltab
install %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/uml

%{__make} ARCH=um modules_install  INSTALL_MOD_PATH=$RPM_BUILD_ROOT
install linux  $RPM_BUILD_ROOT%{_bindir}/umlinux
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
