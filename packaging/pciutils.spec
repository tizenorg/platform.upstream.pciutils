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
make %{?_smp_mflags} OPT="%{optflags} -Wall" PREFIX=%{_prefix} LIBDIR=%{_libdir} SBINDIR=%{_sbindir} STRIP="" SHARED="yes"

%install
make install PREFIX=%{buildroot}%{_prefix} SBINDIR=%{buildroot}%{_sbindir} \
             ROOT=%{buildroot}/ MANDIR=%{buildroot}/%{_mandir} STRIP="" \
	     SHARED="yes" LIBDIR=%{buildroot}/%{_libdir}
mkdir -p %{buildroot}%{_includedir}/pci
cp -p lib/{pci,header,config,types}.h %{buildroot}%{_includedir}/pci/
rm -rf %{buildroot}%{_datadir}/pci.ids*
install -D -m 0644 lib/libpci.pc %{buildroot}%{_libdir}/pkgconfig/libpci.pc

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%docs_package

%files
%defattr(-, root, root)
%doc COPYING
%{_sbindir}/*

%files -n %lname
%defattr(-,root,root)
%{_libdir}/libpci.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/pci/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpci.pc

%changelog
