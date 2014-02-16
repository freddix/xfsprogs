Summary:	Tools for the XFS filesystem
Name:		xfsprogs
Version:	3.1.11
Release:	1
License:	LGPL v2.1 (libhandle), GPL v2 (the rest)
Group:		Applications/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/cmd_tars/%{name}-%{version}.tar.gz
# Source0-md5:	de9f1f45026c2f4e0776058d429ff4b6
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	readline-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libxlog.so.* libxcmd.so.*

%description
A set of commands to use the XFS filesystem, including mkfs.xfs.

%package libs
Summary:	XFS libraries
Group:		Libraries

%description libs
XFS libraries.

%package devel
Summary:	Header files and libraries to develop XFS software
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libuuid-devel

%description devel
Header files and libraries to develop software which operates on XFS
filesystems.

%prep
%setup -q

%build
export DEBUG="-DNDEBUG"
export OPTIMIZER="%{rpmcflags}"
%{__aclocal} -I m4
%{__autoconf}
%configure
%{__make} -j1 V=1

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT=$RPM_BUILD_ROOT
DIST_INSTALL=$(pwd)/install.manifest
DIST_INSTALL_DEV=$(pwd)/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV

%{__make} -j1 install \
	DIST_MANIFEST="$DIST_INSTALL"
%{__make} -j1 install-dev \
	DIST_MANIFEST="$DIST_INSTALL_DEV"

mv $RPM_BUILD_ROOT{/%{_lib}/*,%{_libdir}}
mv $RPM_BUILD_ROOT{/sbin/*,%{_sbindir}}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

%find_lang %{name}
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README doc/{CHANGES,CREDITS}
%attr(755,root,root) %{_sbindir}/fsck.xfs
%attr(755,root,root) %{_sbindir}/mkfs.xfs
%attr(755,root,root) %{_sbindir}/xfs_*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libhandle.so.?
%attr(755,root,root) %{_libdir}/libhandle.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhandle.so
%{_includedir}/xfs
%{_mandir}/man3/*.3*

