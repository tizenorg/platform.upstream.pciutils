#
# spec file for package pciutils
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           pciutils
%define lname	libpci
Version:        3.1.9
Release:        0
License:        GPL-2.0+
Summary:        PCI utilities for Kernel version 2
Url:            http://atrey.karlin.mff.cuni.cz/~mj/pciutils.shtml
Group:          Hardware/Other
Source:         %{name}-%{version}.tar.bz2
Source1:        COPYING
Source2:        baselibs.conf
Patch0:         update-pciutils-dist
Patch1:         %{name}-%{version}_pkgconfig.patch
Patch2:         pciutils-ocloexec.patch
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
Requires:       pciutils-ids
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
lspci: This program displays detailed information about all PCI busses
and devices in the system, replacing the original /proc/pci interface.

setpci: This program allows reading from and writing to PCI device
configuration registers. For example, you can adjust the latency timers
with it.

update-pciids: This program downloads the current version of the
pci.ids file.

%package -n %lname
Summary:        PCI utility library
Group:          System/Libraries

%description -n %lname
libpci offers access to the PCI configuration space.

%package devel
Summary:        Library and Include Files of the PCI utilities
Group:          Development/Libraries/C and C++
Requires:       %lname = %{version}

%description devel
This package contains the files that are necessary for software
development using the PCI utilities.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make %{?_smp_mflags} OPT="%{optflags} -Wall" PREFIX=%{_prefix} LIBDIR=/%{_lib} SBINDIR=/sbin STRIP="" SHARED="yes"

%install
make install PREFIX=%{buildroot}%{_prefix} SBINDIR=%{buildroot}/sbin \
             ROOT=%{buildroot}/ MANDIR=%{buildroot}/%{_mandir} STRIP="" \
	     SHARED="yes" LIBDIR=%{buildroot}/%{_lib}
mkdir -p %{buildroot}%{_includedir}/pci
cp -p lib/{pci,header,config,types}.h %{buildroot}%{_includedir}/pci/
rm -rf %{buildroot}%{_datadir}/pci.ids*
install -D -m 0644 lib/libpci.pc %{buildroot}%{_libdir}/pkgconfig/libpci.pc
ln -sf /%{_lib}/libpci.so.3 %{buildroot}%{_libdir}/libpci.so

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README COPYING
%doc %{_mandir}/man?/*
/sbin/*

%files -n %lname
%defattr(-,root,root)
/%{_lib}/libpci.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/pci/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpci.pc

%changelog
