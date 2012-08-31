Name:       pocketsphinx
Version:    0.7
Release:    1
Group:      System/Libraries
License:    BSD
URL:        http://www.pocketsphinx.org/
Summary:    Speech Recognition Engine
Source:     http://sourceforge.net/projects/cmusphinx/files/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:     0001-pocketsphinx-0.7-fix_build_error_with_stdio.patch
BuildRequires:  pkgconfig(gstreamer-0.10)
BuildRequires:  pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:  pkgconfig(sphinxbase)
BuildRequires:  pkgconfig(python)
BuildRequires:  python-setuptools

%description
PocketSphinx is a version of the open-source Sphinx-II speech recognition
system which is able to recognize speech in real-time.  While it may be
somewhat less accurate than the offline speech recognizers, it is lightweight
enough to run on handheld and embedded devices.

%package devel
Summary:        Header files for developing with pocketsphinx
Group:          Applications/Multimedia
Requires:       %{name}-libs = %{version}-%{release}, pkgconfig
Requires:       sphinxbase-devel

%description devel
Header files for developing with pocketsphinx.

%package libs
Summary:        Shared libraries for pocketsphinx executables
Group:          Applications/Multimedia

%description libs
Shared libraries for pocketsphinx executables.

%package plugin
Summary:        Pocketsphinx gstreamer plugin
Group:          Applications/Multimedia
Requires:       %{name}-libs = %{version}-%{release}, gst-plugins-base

%description plugin
A gstreamer plugin for pocketsphinx.

%package python
Summary:        Python interface to pocketsphinx
Group:          Applications/Multimedia
Requires:       %{name}-libs = %{version}-%{release}, sphinxbase-python

%description python
Python interface to pocketsphinx.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static


make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{python_sitearch}
make install DESTDIR=$RPM_BUILD_ROOT

# Install the man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -p doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# Get rid of files we don't want packaged
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/*.la
rm -f doc/html/installdox

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/pocketsphinx
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/pocketsphinx
%{_libdir}/libpocketsphinx.so
%{_libdir}/pkgconfig/pocketsphinx.pc

%files libs
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libpocketsphinx.so.*

%files plugin
%defattr(-,root,root,-)
%{_libdir}/gstreamer-0.10/*

%files python
%defattr(-,root,root,-)
%{python_sitearch}/*
%changelog
