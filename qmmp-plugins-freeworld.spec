Name:		qmmp-plugins-freeworld
Version:	0.2.3
Release:	3%{?dist}
Summary:	Plugins for qmmp (Qt-based multimedia player)

Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://qmmp.ylsoftware.com/index_en.html
Source:		http://qmmp.ylsoftware.com/files/qmmp-%{version}.tar.bz2
Source2:	qmmp-filter-provides.sh
%define		_use_internal_dependency_generator 0
%define		__find_provides %{_builddir}/%{buildsubdir}/qmmp-filter-provides.sh
# Patch to compile with Qt4-4.2 (as upstream requires Qt >= 4.3)
Patch:          qmmp-plugins-0.2.3-qt42.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	cmake ffmpeg-devel >= 0.4.9-0.51.20080908 libmad-devel qt4-devel >= 4.2
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
# adjust includes for the header move in latest ffmpeg
sed -i \
	-e 's|<avcodec.h|<libavcodec/avcodec.h|g' \
	-e 's|g/avcodec.h|g/libavcodec/avcodec.h|g' \
	-e 's|<avformat.h|<libavformat/avformat.h|g' \
	-e 's|g/avformat.h|g/libavformat/avformat.h|g' \
	src/plugins/Input/ffmpeg/decoder_ffmpeg.h \
	src/plugins/Input/ffmpeg/decoderffmpegfactory.cpp \
	src/plugins/Input/ffmpeg/detailsdialog.cpp
# patch for Qt4 4.2
%patch -p1


%build
export QTDIR="%{_libdir}/qt4/"
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
* Tue Jan 20 2009 Karel Volny <kvolny@redhat.com> 0.2.3-3
- version for EPEL
- adjusted BuildRequires to match EPEL
- patched for using qt4-4.2

* Sat Dec 20 2008 Dominik Mierzejewski <rpm@greysector.net> 0.2.3-2
- rebuild against new ffmpeg

* Mon Dec 08 2008 Karel Volny <kvolny@redhat.com> 0.2.3-1
- version bump

* Fri Sep 05 2008 Karel Volny <kvolny@redhat.com> 0.2.2-1
- version bump

* Wed Aug 20 2008 Karel Volny <kvolny@redhat.com> 0.2.0-4
- adjusted includes for the header move in latest ffmpeg
- upgraded ffmpeg-devel dependency

* Fri Aug 08 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.2.0-3
- rebuild

* Mon Aug 04 2008 Karel Volny <kvolny@redhat.com> 0.2.0-2
- added BuildRequires: libcurl-devel

* Thu Jul 31 2008 Karel Volny <kvolny@redhat.com> 0.2.0-1
- version bump

* Tue May 13 2008 Karel Volny <kvolny@redhat.com> 0.1.6-1
- version bump

* Sat Mar 15 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 0.1.5-3
- rebuild for new ffmpeg

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
