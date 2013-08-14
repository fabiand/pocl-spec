
Summary:  Portable Computing Language
Name:     pocl
Version:  0.8
Release:  3%{?dist}
License:  MIT
Group:    System Environment/Libraries
URL:      http://pocl.sourceforge.net
Source0:  http://pocl.sourceforge.net/downloads/pocl-%{version}.tar.gz

# Only armv7l is supported
ExcludeArch: armv7hl
# PPC support is currently broken, due to path problems
ExcludeArch: ppc
ExcludeArch: ppc64

BuildRequires: pkgconfig automake autoconf libtool libtool-ltdl-devel
BuildRequires: opencl-headers ocl-icd-devel 
BuildRequires: mesa-libGL-devel
BuildRequires: llvm-devel clang
BuildRequires: hwloc-devel

Requires: clang
Requires: %{name}-libs = %{version}-%{release}


%description
Pocl's goal is to become an efficient open source (MIT-licensed) implementation
of the OpenCL 1.2 (and soon OpenCL 2.0) standard.

In addition to producing an easily portable open-source OpenCL implementation,
another major goal of this project is improving performance portability of
OpenCL programs with compiler optimizations, reducing the need for
target-dependent manual optimizations.

At the core of pocl is the kernel compiler that consists of a set of LLVM
passes used to statically transform kernels into work-group functions with
multiple work-items, even in the presence of work-group barriers. These
functions are suitable for parallelization in multiple ways (SIMD, VLIW,
superscalar,...).


%package libs
Summary:  Portable Computing Lanugage library files
Requires: ocl-icd


%description libs
Portable Computing Lanugage runtime library files


%package devel
Summary:  Portable Computing Lanugage development files
Group:    Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
Requires: opencl-headers


%description devel
Portable Computing Lanugage development files


%prep
%setup -q


%build
%configure --disable-static \
    --enable-icd --enable-tests-with-icd=default
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :


%check
make check


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%doc README
%{_bindir}/pocl-standalone
%{_datadir}/pocl/


%files libs
%{_sysconfdir}/OpenCL/vendors/pocl.icd
%{_libdir}/libpocl.so.1.1.0
%{_libdir}/libpocl.so.1
%{_libdir}/libpoclu.so.1.1.0
%{_libdir}/libpoclu.so.1
%{_libdir}/pocl/


%files devel
%{_libdir}/libpoclu.so
%{_libdir}/libpocl.so
%{_libdir}/pocl/llvmopencl.so
%{_libdir}/pkgconfig/pocl.pc
%{_includedir}/pocl/
%{_includedir}/poclu.h


%changelog
* Wed Aug 14 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.8-3
- Add check
- Enforce ICD usage
- Fix duplicate file warnings

* Tue Aug 13 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.8-2
- Own some dirs
- Fix -devel libraries
- Add hwloc, llvm, mesa-libGL BR
- Glob for bc and type files
- ExcludeArch armv7hl

* Mon Aug 12 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.8-1
- Update to 0.8
- Better description
- Fix SourceUrl

* Sun Aug 11 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.8pre-0.2
- Updated bzr snapshot

* Wed Feb 27 2013 Dave Airlie <airlied@redhat.com> - 0.8pre-0.1
- first import

