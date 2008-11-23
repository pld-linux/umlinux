# TODO
# - does it make sens to package module-build for umlinux? Is it possible?
# - package docs

%define basever 2.6.27
%define postver .7
%define alt_kernel uml
Summary:	User Mode Linux
Summary(pl.UTF-8):	Linux w przestrzeni użytkownika
Name:		umlinux
Version:	%{basever}%{postver}
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/Emulators
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{basever}.tar.bz2
# Source0-md5:	b3e78977aa79d3754cb7f8143d7ddabd
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:	1d0e83c620f3960d4d1e813f186b39f6
Source2:	%{name}-config
URL:		http://user-mode-linux.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		localversion %{release}
%define         kernel_release %{version}-%{alt_kernel}-%{localversion}

%define         defconfig       arch/um/defconfig

%define         topdir          %{_builddir}/%{name}-%{version}
%define         srcdir          %{topdir}/linux-%{basever}

%define         CommonOpts      HOSTCC="%{kgcc}" HOSTCFLAGS="-Wall -Wstrict-prototypes %{rpmcflags} -fomit-frame-pointer"
%define		MakeOpts	%{CommonOpts} ARCH=um CC="%{kgcc}" LDFLAGS=-L/lib
%define		DepMod		/bin/true

%define CrossOpts ARCH=um LDFLAGS=-L/lib CC="%{__cc}"

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

%prep
%setup -qc

cd linux-%{basever}

%if "%{postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | patch -p1 -s
%endif

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{postver}-%{alt_kernel}#g' Makefile

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' -o -name '.gitignore' ')' -print0 | xargs -0 -r -l512 rm -f

%build

cd linux-%{basever}

BuildConfig() {
	%{?debug:set -x}
	cat $RPM_SOURCE_DIR/umlinux-config > %{defconfig}

%{?debug:sed -i "s:# CONFIG_DEBUG_SLAB is not set:CONFIG_DEBUG_SLAB=y:" %{defconfig}}
%{?debug:sed -i "s:# CONFIG_DEBUG_PREEMPT is not set:CONFIG_DEBUG_PREEMPT=y:" %{defconfig}}
%{?debug:sed -i "s:# CONFIG_RT_DEADLOCK_DETECT is not set:CONFIG_RT_DEADLOCK_DETECT=y:" %{defconfig}}

}

BuildKernel() {
	%{?debug:set -x}
	echo "Building kernel $1 ..."
	%{__make} %CrossOpts mrproper \
		RCS_FIND_IGNORE='-name build-done -prune -o'
	ln -sf %{defconfig} .config

	%{__make} %CrossOpts clean \
		RCS_FIND_IGNORE='-name build-done -prune -o'
	%{__make} %CrossOpts include/linux/version.h \
		%{?with_verbose:V=1}

	%{__make} %CrossOpts scripts/mkcompile_h \
		%{?with_verbose:V=1}

	%{__make} %CrossOpts \
		%{?with_verbose:V=1}
}

PreInstallKernel() {
	%{__make} %CrossOpts modules_install \
		%{?with_verbose:V=1} \
		DEPMOD=%DepMod \
		INSTALL_MOD_PATH=$KERNEL_INSTALL_DIR \
		KERNELRELEASE=%{kernel_release}

	# You'd probabelly want to make it somewhat different
	install -d $KERNEL_INSTALL_DIR%{_kernelsrcdir}
	install Module.symvers $KERNEL_INSTALL_DIR%{_kernelsrcdir}/Module.symvers-dist

	echo "CHECKING DEPENDENCIES FOR KERNEL MODULES"
	if [ %DepMod = /sbin/depmod ]; then
		/sbin/depmod --basedir $KERNEL_INSTALL_DIR -ae -F $KERNEL_INSTALL_DIR/boot/System.map-%{kernel_release} -r %{kernel_release} || :
	fi
	touch $KERNEL_INSTALL_DIR/lib/modules/%{kernel_release}/modules.dep
	echo "KERNEL RELEASE %{kernel_release} DONE"
}

KERNEL_BUILD_DIR=`pwd`
echo "-%{localversion}" > localversion

KERNEL_INSTALL_DIR="$KERNEL_BUILD_DIR/build-done/kernel"
rm -rf $KERNEL_INSTALL_DIR
BuildConfig
ln -sf %{defconfig} .config
install -d $KERNEL_INSTALL_DIR%{_kernelsrcdir}/include/linux
rm -f include/linux/autoconf.h
%{__make} %CrossOpts include/linux/autoconf.h
install include/linux/autoconf.h \
	$KERNEL_INSTALL_DIR%{_kernelsrcdir}/include/linux/autoconf-dist.h
install .config \
	$KERNEL_INSTALL_DIR%{_kernelsrcdir}/config-dist
BuildKernel
PreInstallKernel

%{__make} %CrossOpts include/linux/utsrelease.h
cp include/linux/utsrelease.h{,.save}
cp include/linux/version.h{,.save}
cp scripts/mkcompile_h{,.save}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},/lib/modules/%{kernel_release}/misc}

cd linux-%{basever}
install linux $RPM_BUILD_ROOT%{_bindir}/linux
%{__make} ARCH=um modules_install INSTALL_MOD_PATH=$RPM_BUILD_ROOT

cd %{topdir}/linux-%{basever}

%post modules
%depmod %{kernel_release}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/linux

%files modules
%defattr(644,root,root,755)
%dir /lib/modules/%{kernel_release}
/lib/modules/%{kernel_release}/kernel
/lib/modules/%{kernel_release}/misc
%ghost /lib/modules/%{kernel_release}/modules.*
%if 0
# symlinks pointing to kernelsrcdir
%ghost /lib/modules/%{kernel_release}/build
%ghost /lib/modules/%{kernel_release}/source
%endif

%if 0
%files doc
%defattr(644,root,root,755)
%{_prefix}/src/linux-%{version}/Documentation
%endif
