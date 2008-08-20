Name:		qmmp-plugins-freeworld
Version:	0.2.0
Release:	6%{?dist}
Summary:	Plugins for qmmp (Qt-based multimedia player)

Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://qmmp.ylsoftware.com/index_en.html
Source:		http://qmmp.ylsoftware.com/files/qmmp-%{version}.tar.bz2
Source2:	qmmp-filter-provides.sh
%define		_use_internal_dependency_generator 0
%define		__find_provides %{_builddir}/%{buildsubdir}/qmmp-filter-provides.sh

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	cmake ffmpeg-devel < 0.4.9-0.8 libmad-devel qt4-devel >= 4.2
BuildRequires:	taglib-devel curl-devel
BuildRequires:	qmmp = %{version}
Requires:	qmmp = %{version}


%description
Qmmp is an audio-player, written with help of Qt library.
This package contains plugins needed to play MPEG (.mp3) and WMA files.


%prep
%setup -q -n qmmp-%{version}
cp %{SOURCE2} .
chmod +x qmmp-filter-provides.sh


%build
%cmake \
	-D USE_FLAC:BOOL=FALSE \
	-D USE_VORBIS:BOOL=FALSE \
	-D USE_MPC:BOOL=FALSE \
	-D USE_MODPLUG:BOOL=FALSE \
	-D USE_SNDFILE:BOOL=FALSE \
	-D USE_WAVPACK:BOOL=FALSE \
	-D USE_ALSA:BOOL=FALSE \
	-D USE_OSS:BOOL=FALSE \
	-D USE_JACK:BOOL=FALSE \
	-D USE_PULSE:BOOL=FALSE \
	-D USE_SRC:BOOL=FALSE \
	-D USE_ANALYZER:BOOL=FALSE \
	-D USE_DBUS:BOOL=FALSE \
	-D USE_SCROBBLER:BOOL=FALSE \
	-D USE_STATICON:BOOL=FALSE \
	-D USE_NOTIFIER:BOOL=FALSE \
	-D USE_QMMP_DIALOG:BOOL=FALSE \
	-D CMAKE_INSTALL_PREFIX=/usr \
	-D LIB_DIR=%{_lib} \
	./
make VERBOSE=1 %{?_smp_mflags} -C src/plugins/Input/ffmpeg
make VERBOSE=1 %{?_smp_mflags} -C src/plugins/Input/mad


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install -C src/plugins/Input/ffmpeg
make DESTDIR=%{buildroot} install -C src/plugins/Input/mad


%clean
rm -rf %{buildroot}


%files
%defattr(0755,root,root,0755)
%dir %{_libdir}/qmmp/Input
%{_libdir}/qmmp/Input/*.so


%post -p /sbin/ldconfig
 
%postun -p /sbin/ldconfig


%changelog
* Wed Aug 20 2008 Karel Volny <kvolny@redhat.com> 0.2.0-6
- reverted previous change, the new ffmpeg is not released in this branch

* Tue Aug 19 2008 Karel Volny <kvolny@redhat.com> 0.2.0-5
- adjusted includes for the header move in latest ffmpeg
- upgraded ffmpeg-devel dependency

* Fri Aug 08 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.2.0-4
- rebuild for RPM Fusion

* Fri Aug 08 2008 Karel Volny <kvolny@redhat.com> 0.2.0-3
- fix BuildRequires: qt4-devel instead of qt-devel

* Mon Aug 04 2008 Karel Volny <kvolny@redhat.com> 0.2.0-2
- added BuildRequires: curl-devel

* Thu Jul 31 2008 Karel Volny <kvolny@redhat.com> 0.2.0-1
- version bump

* Tue May 13 2008 Karel Volny <kvolny@redhat.com> 0.1.6-1
- version bump

* Mon Jan 21 2008 Karel Volny <kvolny@redhat.com> 0.1.5-2
- fixed permissions issue for the helper sript qmmp-filter-provides.sh

* Mon Jan 14 2008 Karel Volny <kvolny@redhat.com> 0.1.5-1
- package renamed to match conventions (from "qmmp-plugins")
- added "BuildRequires: qmmp = %%{version}"

* Mon Dec 10 2007 Karel Volny <kvolny@redhat.com> 0.1.5-1
- version bump
- simplified setting of the libraries destination

* Wed Sep 12 2007 Karel Volny <kvolny@redhat.com> 0.1.4-2
- specfile improvements (Fedora bug #280751 comment #4)

* Tue Sep 11 2007 Karel Volny <kvolny@redhat.com> 0.1.4-1
- initial release of separate plugins, as suggested in comment #1 to (Livna) bug #1631
