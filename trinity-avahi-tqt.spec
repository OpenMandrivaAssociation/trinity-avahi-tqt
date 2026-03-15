%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg avahi-tqt

%define libname %mklibname %{tde_pkg}
%define devname %mklibname %{tde_pkg} -d

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.30
Release:	%{?tde_version:%{tde_version}_}6
Summary:	Avahi TQt integration library
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	LGPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	pkgconfig(tqt)

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

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

%package -n %{libname}1
Summary:	Avahi TQt integration library
Group:		System/Libraries

%description -n %{libname}1
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.

%files -n %{libname}1
%defattr(-,root,root,-)
%{_libdir}/libavahi-tqt.so.1
%{_libdir}/libavahi-tqt.so.1.0.0

##########

%package -n %{devname}
Summary:	Avahi TQt integration library (Development Files)
Group:		Development/Libraries/C and C++

Requires:	%{libname}1 = %{EVRD}

%description -n %{devname}
Avahi is a fully LGPL framework for Multicast DNS Service Discovery.
It allows programs to publish and discover services and hosts
running on a local network with no specific configuration. For
example you can plug into a network and instantly find printers to
print to, files to look at and people to talk to.
 .
This library contains the interface to integrate the Avahi libraries
into a TQt main loop application.

%files -n %{devname}
%defattr(-,root,root,-)
%{_includedir}/avahi-tqt/
%{_libdir}/libavahi-tqt.a
%{_libdir}/libavahi-tqt.so
%{_libdir}/libavahi-tqt.la
%{_libdir}/pkgconfig/avahi-tqt.pc

