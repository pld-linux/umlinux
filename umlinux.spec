#%define kernel_version 2.6.11.1
%define kernel_version 2.6.12.1
%define	uml_patch 2.6.11.8-bs6
#%define	uml_patch 2.6.11.8-bs5
#%define	uml_patch 2.6.11-bs4
#%define	skas_patch 2.6.11-v9-pre2
%define	skas_patch 2.6.12-rc4-v9-pre2
Summary:	User Mode Linux
Summary(pl.UTF-8):   Linux w przestrzeni użytkownika
Name:		umlinux
Version:	2
Release:	1.1
Epoch:		0
License:	GPL
Group:		Applications/Emulators
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{kernel_version}.tar.bz2
# Source0-md5:	542d5aa1657f8da60b41d4d08b098841
Source1:	%{name}-config
Source2:	http://user-mode-linux.sourceforge.net/UserModeLinux-HOWTO.html
# Source2-md5:	781dc3611ebf60ac07814a1cd31c936d
Source3:	%{name}-etc-umltab
Source4:	%{name}-rc-init
Patch0:		http://www.user-mode-linux.org/~blaisorblade/patches/guest/uml-%{uml_patch}/uml-%{uml_patch}.patch.bz2
Patch1:		http://www.user-mode-linux.org/~blaisorblade/patches/skas3-2.6/skas-%{skas_patch}/skas-%{skas_patch}.patch.bz2
URL:		http://user-mode-linux.sourceforge.net/
BuildRequires:	libpcap-static
BuildRequires:	modutils
BuildRequires:	readline-devel
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

%package init
Summary:	Automagic startup/shutdown User Mode Linux
Summary(pl.UTF-8):   Automagiczy start/stop Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description init
Utilities for automagic startup/shutdown User Mode Linux.

%description init -l pl.UTF-8
Automagiczy start/stop Linuksa w przestrzeni użytkownika.

%prep
%setup  -q -n linux-%{kernel_version}
#%patch0 -p1
#patch1 -p1

cp %{SOURCE1} ./.config
cp %{SOURCE2} .

%build
%{__make} ARCH=um oldconfig
# $((0x... )) it's not /bin/sh compatible:
%{__make} ARCH=um SHELL=/bin/bash linux
%{__make} ARCH=um modules

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/rc.d/init.d}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/umltab
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/uml

%{__make} ARCH=um modules_install  INSTALL_MOD_PATH=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.html
%attr(755,root,root) %{_bindir}/umlinux

%files modules
%defattr(644,root,root,755)
/lib/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/uml
/etc/umltab
