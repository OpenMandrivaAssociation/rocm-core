# Tiny TheRock component: ROCm version/path helpers (librocm-core).
# RCCL, HIP, and others call getROCmVersion() from this library.

Name:		rocm-core
Version:	10.1.0
Release:	1
Summary:	ROCm version and install-path helpers
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-systems
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-10.1/rocm-core.tar.gz#/rocm-core-%{version}.tar.gz

BuildSystem:	cmake
BuildRequires:	cmake
BuildRequires:	ninja
BuildOption:	-DROCM_VERSION=%{version}
BuildOption:	-DDISABLE_CPACK=ON
BuildOption:	-DBUILD_SHARED_LIBS=ON
BuildOption:	-DCMAKE_INSTALL_LIBDIR=%{_lib}

# rdhc + runpath_to_rpath.py
Requires:	python
Requires:	python%{pyver}dist(prettytable)
Requires:	python%{pyver}dist(pyyaml)

%description
librocm-core reports the ROCm release version (getROCmVersion) and the
install prefix. Official ROCm packages depend on it; OpenMandriva
previously only stubbed the header.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{EVRD}

%description devel
Headers and CMake package for librocm-core.

%prep
%autosetup -n rocm-core -p1
# Current python, not a frozen python3.
sed -i '1s|#!.*python3|#!%{_bindir}/python|' rdhc/rdhc.py runpath_to_rpath.py
# Do not plant /usr/.info/version
sed -i -e 's|DESTINATION .info|DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/rocm-core|' CMakeLists.txt

%files
%license LICENSE.md
%doc README.md CHANGELOG.md
%{_libdir}/librocm-core.so.1{,.*}
%{_libdir}/rocmmod
%{_bindir}/rdhc
%{_libexecdir}/rocm-core/
%{_datadir}/rdhc/
%{_datadir}/rocm-core/

%files devel
%{_includedir}/rocm-core/
%{_libdir}/librocm-core.so
%{_libdir}/cmake/rocm-core/
