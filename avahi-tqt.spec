#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg avahi-tqt

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libavahi %{_lib}avahi
%else
%define libavahi libavahi
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.30
Release:	%{?tde_version}_%{?!preversion:2}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Avahi TQt integration library
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	LGPL-2.0+
%else
License:	LGPLv2+
%endif

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:   cmake make

BuildRequires:	libtqt4-devel >= %{tde_epoch}:4.2.0

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	libtool

# GLIB2 support
BuildRequires:	pkgconfig(glib-2.0)

# GETTEXT support
BuildRequires:	gettext-devel

# Xi support
BuildRequires:  pkgconfig(xi)

# DBUS support
BuildRequires:  pkgconfig(dbus-1)

# PCAP support
BuildRequires:	pkgconfig(libcap)

# AVAHI support
BuildRequires:  pkgconfig(avahi-client)

# EXPAT support
BuildRequires:  pkgconfig(expat)

# NAS support
# no updates since 2022
# %if 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion}
# define with_nas 1
# BuildRequires: nas-devel
# %endif

# XT support
BuildRequires:  pkgconfig(xt)

%description
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.

##########

%package -n %{libavahi}-tqt1
Summary:	Avahi TQt integration library
Group:		System/Libraries
Provides:	libavahi-tqt1 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:		trinity-avahi-tqt < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-avahi-tqt = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libavahi}-tqt1
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.

%post -n %{libavahi}-tqt1
/sbin/ldconfig || :

%postun -n %{libavahi}-tqt1
/sbin/ldconfig || :

%files -n %{libavahi}-tqt1
%defattr(-,root,root,-)
%{_libdir}/libavahi-tqt.so.1
%{_libdir}/libavahi-tqt.so.1.0.0

##########

%package -n %{libavahi}-tqt-devel
Summary:	Avahi TQt integration library (Development Files)
Group:		Development/Libraries/C and C++
Provides:	libavahi-tqt-devel = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:	%{libavahi}-tqt1 = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	libtqt4-devel >= %{tde_epoch}:4.2.0
%{?avahi_devel:Requires: %{avahi_devel}}

Obsoletes:		trinity-avahi-tqt-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-avahi-tqt-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libavahi}-tqt-devel
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.

%post -n %{libavahi}-tqt-devel
/sbin/ldconfig || :

%postun -n %{libavahi}-tqt-devel
/sbin/ldconfig || :

%files -n %{libavahi}-tqt-devel
%defattr(-,root,root,-)
%{_includedir}/avahi-tqt/
%{_libdir}/libavahi-tqt.a
%{_libdir}/libavahi-tqt.so
%{_libdir}/libavahi-tqt.la
%{_libdir}/pkgconfig/avahi-tqt.pc

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DLIB_INSTALL_DIR="%{_libdir}" \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install DESTDIR="%{?buildroot}" -C build

