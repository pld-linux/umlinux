%define basever 2.6.27
%define postver .3
Summary:	User Mode Linux
Summary(pl.UTF-8):	Linux w przestrzeni użytkownika
Name:		umlinux
Version:	%{basever}%{postver}
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/Emulators
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{basever}.tar.bz2
# Source0-md5:  b3e78977aa79d3754cb7f8143d7ddabd
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:  4f0dc89b4989619c616d40507b5f7f34
Source2:	%{name}-config
Source3:	http://user-mode-linux.sourceforge.net/UserModeLinux-HOWTO.html
# Source3-md5:	781dc3611ebf60ac07814a1cd31c936d
Source4:	%{name}-etc-umltab
Source5:	%{name}-rc-init
URL:		http://user-mode-linux.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
User Mode Linux.

%description -l pl.UTF-8
Linux w przestrzeni użytkownika.

%package modules
Summary:	User Mode Linux modules
Summary(pl.UTF-8):	Moduły Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description modules
Modules for User Mode Linux.

%description modules -l pl.UTF-8
Moduły Linuksa w przestrzeni użytkownika.

%package init
Summary:	Automagic startup/shutdown User Mode Linux
Summary(pl.UTF-8):	Automagiczy start/stop Linuksa w przestrzeni użytkownika
Group:		Applications/Emulators

%description init
Utilities for automagic startup/shutdown User Mode Linux.

%description init -l pl.UTF-8
Automagiczy start/stop Linuksa w przestrzeni użytkownika.

%prep
%setup -qc

cd linux-%{basever}
%if "%{postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | %{__patch} -p1 -s
%endif

cp %{SOURCE2} ./.config
cp %{SOURCE3} .

%build
cd linux-%{basever}
#%{__make} ARCH=um oldconfig
%{__make} ARCH=um LDFLAGS=-L/lib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/rc.d/init.d}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/umltab
install %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/uml

cd linux-%{basever}
install linux $RPM_BUILD_ROOT%{_bindir}/linux
%{__make} ARCH=um modules_install  INSTALL_MOD_PATH=$RPM_BUILD_ROOT

%post modules
%depmod %{version}

%postun modules
%depmod %{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc linux-%{basever}/UserModeLinux-HOWTO.html
%attr(755,root,root) %{_bindir}/linux

%files modules
%defattr(644,root,root,755)
/lib/modules/%{basever}%{postver}

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/uml
%{_sysconfdir}/umltab
