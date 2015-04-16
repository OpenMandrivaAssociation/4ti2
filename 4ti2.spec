%define major		0
%define libname		%mklibname %{name}- %{major}
%define libzsolve	%mklibname zsolve %{major}
%define devname		%mklibname %{name} -d
%define _libexecdir	/usr/libexec
%define debug_package	%{nil}
# docs
%define _files_listed_twice_terminate_build 0
#

Name:           4ti2
Version:        1.6.2
Release:        2
Summary:        A software package for problems on linear spaces

Group:          Sciences/Mathematics
License:        GPLv2+
URL:            http://www.4ti2.de/
Source0:        http://www.4ti2.de/version_%{version}/%{name}-%{version}.tar.gz
Source1:        http://www.4ti2.de/4ti2_manual.pdf
Patch0:         4ti2-1.3.2-gcc47.patch
Patch1:         4ti2-missing-libs.diff
Patch2:         4ti2-docdir.diff
BuildRequires:  gmp-devel
BuildRequires:  glpk-devel
BuildRequires:	gcc-c++, gcc, gcc-cpp

%description
A software package for algebraic, geometric and combinatorial
problems on linear spaces.

This package uses Environment Modules, to load the binaries onto
your PATH you will need to run module load %{name}-%{_arch}.

%files
%doc COPYING AUTHORS TODO NEWS README 4ti2_manual.pdf
%{_bindir}/*
%{_libexecdir}/%{name}/
%{_docdir}/%{name}/
#--------------------------------------------------------
%package  -n %{libname}

Summary:	Library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the 4ti2 program library, which comes in three
flavors:
- 32-bit precision integers
- 64-bit precision integers
- arbitrary precision integer support through use of GNU MP.

%files -n %{libname}
%doc COPYING AUTHORS TODO NEWS README
#%%{_libdir}/lib4ti2gmp.so.0*
%{_libdir}/lib4ti2int32.so.0*
%{_libdir}/lib4ti2int64.so.0*
%{_libdir}/lib4ti2common.so.0*
%{_libdir}/lib4ti2util.so.0*
#--------------------------------------------------------
%package  -n %{libzsolve}

Summary:	Library for solving linear systems over integers for 4ti2
Group:		System/Libraries

%description -n %{libzsolve}
This package contains the 4ti2 library for solving systems linear systems over
integers (\mathbb{Z}).

%files -n %{libzsolve}
%doc COPYING AUTHORS TODO NEWS README
%{_libdir}/libzsolve.so.0*
#--------------------------------------------------------
%package -n %{devname}

Summary:	Development files for %{name}
Group:		Development/C
Requires:       %{libname} = %{EVRD}
Requires:       %{libzsolve} = %{EVRD}

%description -n %{devname}
This subpackage contains the include files and library links for
developing against 4ti2's libraries.

%files  -n %{devname}
%doc COPYING AUTHORS TODO NEWS README
%{_includedir}/pkg/
%{_libdir}/lib*.so
#--------------------------------------------------------

%prep
%setup -q
cp -p %{SOURCE1} .
#patch0 -p1 -b .gcc47
%patch1 -p1
%patch2 -p1

%build
export CC=gcc
export CXX=g++

autoreconf -fi;
%configure --enable-shared --disable-static \
	--includedir="%_includedir/pkg/%{name}" --docdir="%_docdir/%{name}"

%make 

%install
make install DESTDIR=%{buildroot}
cp COPYING doc/* "%{buildroot}/%{_docdir}/%{name}/"
mkdir -p "%{buildroot}/%{_bindir}" "%{buildroot}/%{_libexecdir}/%{name}";
mv "%{buildroot}/%{_bindir}"/* "%{buildroot}/%{_libexecdir}/%{name}/";
pushd "%{buildroot}/%{_libexecdir}/%{name}";
for i in *; do
	ln -s "%{_libexecdir}/%{name}/$i" "%{buildroot}/%{_bindir}/4ti2_$i";
done;




