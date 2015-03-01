Name:           4ti2
Version:        1.3.2
Release:        4
Summary:        A software package for problems on linear spaces

Group:          Sciences/Mathematics
License:        GPLv2+
URL:            http://www.4ti2.de/
Source0:        http://www.4ti2.de/version_%{version}/%{name}-%{version}.tar.gz
Source1:        http://www.4ti2.de/4ti2_manual.pdf
Patch0:         4ti2-1.3.2-gcc47.patch
BuildRequires:  gmp-devel
BuildRequires:  glpk-devel

%description
A software package for algebraic, geometric and combinatorial
problems on linear spaces.

This package uses Environment Modules, to load the binaries onto
your PATH you will need to run module load %{name}-%{_arch}

%prep
%setup -q
cp -p %{SOURCE1} .
%patch0 -p1 -b .gcc47

%build
export LDFLAGS="%{ldflags} -lglpk"

CXXFLAGS="%{optflags} -I%{_includedir}/glpk" \
CFLAGS="%{optflags} -I%{_includedir}/glpk" \
%configure2_5x --disable-shared --disable-static
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool
%make 

%install
make install-exec DESTDIR=%{buildroot}

# The libraries are not really fit for use outside the package.
rm -rf %{buildroot}/%{_libdir}

%check
make check

%files
%doc COPYING TODO 4ti2_manual.pdf
%{_bindir}/*


%changelog
* Wed Aug 15 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.3.2-1
+ Revision: 814879
- Import 4ti2 package (based on fedora package)
- Import 4ti2 package (based on fedora package)

