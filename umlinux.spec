%define kernel_version 2.4.18
Summary:	User Mode Linux
Summary(pl):	Linux w przestrzeni u¿ytkownika
Name:		umlinux
Version:	18
Release:	1
Epoch:		0
License:	GPL
Group:		Aplications/Dupa
Source0:	linux-%{kernel_version}.tar.bz2
Source1:	umlinux-config
Patch0:		uml-patch-%{kernel_version}-%{version}.bz2 
URL:		http://ftp.sourceforge.org/uml 
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%package modules
Summary:	User Mode Linux modules
Group:		Aplications/Dupa

%description
User Mode Linux 

%description modules
Modules for User Mode Linux

%prep
%setup  -q -n linux
%patch0 -p1
cp %{SOURCE1} ./.config

%build
%{__make} ARCH=um oldconfig
%{__make} ARCH=um dep
%{__make} ARCH=um linux
%{__make} ARCH=um modules


%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_bindir}

%{__make} ARCH=um modules_install  INSTALL_MOD_PATH=$RPM_BUILD_ROOT
install linux  ${RPM_BUILD_ROOT}/usr/bin/umlinux

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/umlinux

%files modules
%defattr(644,root,root,755)
/lib/*
