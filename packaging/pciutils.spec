Name:           pciutils
Version:        3.2.1
Release:        0
License:        GPL-2.0+
Summary:        PCI utilities for Kernel version 2
Url:            http://atrey.karlin.mff.cuni.cz/~mj/pciutils.shtml
Group:          Base/Device Management
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	pciutils.manifest
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

%package -n libpci
Summary:        PCI utility library
Group:          Base/Device Management

%description -n libpci
libpci offers access to the PCI configuration space.

%package devel
Summary:        Library and Include Files of the PCI utilities
Group:          Development/Libraries
Requires:       libpci = %{version}

%description devel
This package contains the files that are necessary for software
development using the PCI utilities.

%prep
%setup -q
cp %{SOURCE1001} .

%build
make %{?_smp_mflags} OPT="%{optflags} -Wall" PREFIX=%{_prefix} LIBDIR=%{_libdir} SBINDIR=%{_sbindir} STRIP="" SHARED="yes" IDSDIR=%{_datadir}/hwdata

%install
make install PREFIX=%{buildroot}%{_prefix} SBINDIR=%{buildroot}%{_sbindir} \
             ROOT=%{buildroot}/ MANDIR=%{buildroot}/%{_mandir} STRIP="" \
	     SHARED="yes" LIBDIR=%{buildroot}/%{_libdir} IDSDIR=%{buildroot}/%{_datadir}/hwdata
mkdir -p %{buildroot}%{_includedir}/pci
cp -p lib/{pci,header,config,types}.h %{buildroot}%{_includedir}/pci/
rm -rf %{buildroot}%{_datadir}/hwdata/pci.ids*
install -D -m 0644 lib/libpci.pc %{buildroot}%{_libdir}/pkgconfig/libpci.pc
ln -sf libpci.so.3 %{buildroot}%{_libdir}/libpci.so

%post -n libpci -p /sbin/ldconfig

%postun -n libpci -p /sbin/ldconfig

%docs_package

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_sbindir}/*

%files -n libpci
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libpci.so.*

%files devel
%manifest %{name}.manifest
%defattr(-, root, root)
%{_includedir}/pci/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpci.pc

%changelog
