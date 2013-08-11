
Summary: Portable Computing Language
Name: pocl
Version: 0.8
Release: 0.1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://pocl.sourceforge.net
Source0: pocl-0.8-pre.tar.gz

BuildRequires: pkgconfig automake autoconf libtool
BuildRequires: opencl-headers ocl-icd-devel clang

Requires: clang
Requires: %{name}-libs = %{version}-%{release}

%description
Portable Computing Language runtime

%package libs
Summary: Portable Computing Lanugage library files
Requires: ocl-icd

%description libs
Portable Computing Lanugage runtime library files

%package devel
Summary: Portable Computing Lanugage development files
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
Requires: opencl-headers

%description devel
Portable Computing Lanugage development files

%prep
%setup -q -b0 -n %{name}-%{version}-pre

%build
autoreconf -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/pocl-standalone
%{_datadir}/pocl/pocl-build
%{_datadir}/pocl/pocl-kernel
%{_datadir}/pocl/pocl-workgroup

%files libs
%defattr(-,root,root,-)
%{_sysconfdir}/OpenCL/vendors/pocl.icd
%{_libdir}/libpocl.so.1.1.0
%{_libdir}/libpocl.so.1
%{_libdir}/libpoclu.so.1.1.0
%{_libdir}/libpoclu.so.1
#woah
%{_libdir}/pocl/x86_64/kernel-x86_64-redhat-linux-gnu.bc
%{_libdir}/pocl/llvmopencl.so.1
%{_libdir}/pocl/llvmopencl.so.1.1.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/pocl.pc
%{_libdir}/pocl/llvmopencl.so
%{_libdir}/libpocl.so
%{_libdir}/libpoclu.so
%{_includedir}/pocl/_kernel.h
%{_includedir}/pocl/pocl.h
%{_includedir}/pocl/pocl_device.h
%{_includedir}/pocl/arm/types.h
%{_includedir}/pocl/tce/types.h
%{_includedir}/pocl/x86_64/types.h
%{_includedir}/poclu.h

%changelog
* Wed Feb 27 2013 Dave Airlie <airlied@redhat.com> 2.0.2-1
- first import


