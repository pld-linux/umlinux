%define kernel_version 2.4.18
%define utils_version 20020906
Summary:	User Mode Linux
Summary(pl):	Linux w przestrzeni użytkownika
Name:		umlinux
Version:	18
Release:	1
Epoch:		0
License:	GPL
Group:		Applications/Emulators
Source0:	ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-%{kernel_version}.tar.bz2
Source1:	%{name}-config
Source2:	ftp://ftp.sourceforge.net/pub/sourceforge/user-mode-linux/uml_utilities_%{utils_version}.tar.bz2
Source3:	http://user-mode-linux.sourceforge.net/UserModeLinux-HOWTO.html
Patch0:		ftp://ftp.sourceforge.net/pub/sourceforge/user-mode-linux/uml-patch-%{kernel_version}-%{version}.bz2
URL:		http://user-mode-linux.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
User Mode Linux.

%description -l pl
Linux w przestrzeni użytkownika.

%package modules
Summary:	User Mode Linux modules
Summary(pl):	Moduły Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description modules
Modules for User Mode Linux.

%description modules -l pl
Moduły Linuksa w przestrzeni użytkownika.


%package utils
Summary:	User Mode Linux Utilities
Summary(pl):	Narzędzia Perl dla Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description utils
Utilities for User Mode Linux.

%description utils -l pl
Narzędzia do Linuksa w przestrzeni użytkownika.

%package utils-perl
Summary:	User Mode Linux Perl Utilities
Summary(pl):	Narzędzia  dla Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description utils-perl
Perl Utilities for User Mode Linux.

%description utils-perl -l pl
Narzędzia Perl do Linuksa w przestrzeni użytkownika.

%prep
%setup  -q -n linux -a 2 -a 3
%patch0 -p1
cp %{SOURCE1} ./.config

%build
%{__make} ARCH=um oldconfig
%{__make} ARCH=um dep
%{__make} ARCH=um linux
%{__make} ARCH=um modules
cd tools
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_bindir}

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

%doc *.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
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
