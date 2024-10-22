Name:		qmmp-plugins-freeworld
Version:	2.2.1
Release:	1%{?dist}
Summary:	Plugins for qmmp (Qt-based multimedia player)

Group:		Applications/Multimedia
License:	GPLv2+
URL:		https://qmmp.ylsoftware.com/
Source:		%url/files/qmmp/2.1/qmmp-%{version}.tar.bz2

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	enca-devel
BuildRequires:	faad2-devel
BuildRequires:	libcurl-devel
BuildRequires:	qt6-qtmultimedia-devel
BuildRequires:	qt6-qttools-devel
BuildRequires:	taglib-devel >= 1.10
BuildRequires:	zlib-devel
Requires:	qmmp%{?_isa} = %{version}

Supplements:	qmmp

%global __provides_exclude_from ^%{_libdir}/qmmp/.*\\.so$

%description
Qmmp is an audio-player, written with help of Qt library.
This package contains plugins needed to play AAC and WMA files,
and also the mplayer plugin for video playback.


%prep
%setup -q -n qmmp-%{version}


%build
# the plugin groups, as separated by newlines, are:
# Transport, Input, Output, Effect, Visual, General, File Dialogs
%cmake \
	-D USE_CURL:BOOL=FALSE \
	-D USE_MMS:BOOL=FALSE \
\
	-D USE_FFMPEG:BOOL=FALSE \
	-D USE_FLAC:BOOL=FALSE \
	-D USE_VORBIS:BOOL=FALSE \
	-D USE_MAD:BOOL=FALSE \
	-D USE_MPC:BOOL=FALSE \
	-D USE_XMP:BOOL=FALSE \
	-D USE_SNDFILE:BOOL=FALSE \
	-D USE_WAVPACK:BOOL=FALSE \
	-D USE_CUE:BOOL=FALSE \
	-D USE_CDA:BOOL=FALSE \
	-D USE_MIDI:BOOL=FALSE \
	-D USE_GME:BOOL=FALSE \
	-D USE_OPUS:BOOL=FALSE \
	-D USE_SID:BOOL=FALSE \
	-D USE_ARCHIVE:BOOL=FALSE \
\
	-D USE_ALSA:BOOL=FALSE \
	-D USE_JACK:BOOL=FALSE \
	-D USE_OSS:BOOL=FALSE \
	-D USE_OSS4:BOOL=FALSE \
	-D USE_PULSE:BOOL=FALSE \
	-D USE_NULL:BOOL=FALSE \
	-D USE_WAVEOUT:BOOL=FALSE \
	-D USE_SHOUT:BOOL=FALSE \
\
	-D USE_SRC:BOOL=FALSE \
	-D USE_BS2B:BOOL=FALSE \
	-D USE_LADSPA:BOOL=FALSE \
	-D USE_CROSSFADE:BOOL=FALSE \
	-D USE_STEREO:BOOL=FALSE \
	-D USE_FILEWRITER:BOOL=FALSE \
	-D USE_MONOTOSTEREO:BOOL=FALSE \
\
	-D USE_ANALYZER:BOOL=FALSE \
	-D USE_PROJECTM:BOOL=FALSE \
\
	-D USE_MPRIS:BOOL=FALSE \
	-D USE_SCROBBLER:BOOL=FALSE \
	-D USE_LISTENBRAINZ:BOOL=FALSE \
	-D USE_STATICON:BOOL=FALSE \
	-D USE_NOTIFIER:BOOL=FALSE \
	-D USE_LYRICS:BOOL=FALSE \
	-D USE_HAL:BOOL=FALSE \
	-D USE_UDISKS:BOOL=FALSE \
	-D USE_UDISKS2:BOOL=FALSE \
	-D USE_HOTKEY:BOOL=FALSE \
	-D USE_GNOMEHOTKEY:BOOL=FALSE \
	-D USE_FILEOPS:BOOL=FALSE \
	-D USE_COVER:BOOL=FALSE \
	-D USE_KDENOTIFY:BOOL=FALSE \
	-D USE_CONVERTER:BOOL=FALSE \
	-D USE_RGSCAN:BOOL=FALSE \
	-D USE_SB:BOOL=FALSE \
	-D USE_TRACKCHANGE:BOOL=FALSE \
	-D USE_COPYPASTE:BOOL=FALSE \
	-D USE_HISTORY:BOOL=FALSE \
	-D USE_SLEEPINHIBITOR:BOOL=FALSE \
\
	-D USE_QMMP_DIALOG:BOOL=FALSE \
	-D USE_TWO_PANEL_DIALOG:BOOL=FALSE \
\
	-D CMAKE_INSTALL_PREFIX=/usr \
	-D LIB_DIR=%{_lib} \
	-D PLUGIN_DIR=%{_lib}/qmmp

make VERBOSE=1 %{?_smp_mflags} -C %{_vpath_builddir}/src/plugins/Engines/mplayer
make VERBOSE=1 %{?_smp_mflags} -C %{_vpath_builddir}/src/plugins/Input/aac


%install
make DESTDIR=%{buildroot} install -C %{_vpath_builddir}/src/plugins/Engines/mplayer
make DESTDIR=%{buildroot} install -C %{_vpath_builddir}/src/plugins/Input/aac
## install .desktop files for MimeType associations
mkdir -p %{buildroot}/%{_datadir}/applications/
# aac
sed -e "/MimeType/c\MimeType=audio/aac;audio/aacp;audio/x-aac;audio/m4a;audio/x-m4a;" -e "/Actions/,$ c\NoDisplay=true" \
    src/app/qmmp.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-aac.desktop
sed -e "/MimeType/c\MimeType=audio/aac;audio/aacp;audio/x-aac;audio/m4a;audio/x-m4a;" \
    src/app/qmmp-enqueue.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-aac-enqueue.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-aac.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-aac-enqueue.desktop


%files
# there's only mplayer plugin now, so own the directory
%dir %{_libdir}/qmmp/Engines
%{_libdir}/qmmp/Engines/*.so
# Input & Transports dirs are owned by qmmp already
%{_libdir}/qmmp/Input/*.so
%{_datadir}/applications/%{name}-aac.desktop
%{_datadir}/applications/%{name}-aac-enqueue.desktop


%changelog
* Tue Oct 22 2024 Karel Volný <kvolny@redhat.com> 2.2.1-1
- version bump to 2.2.1

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 05 2024 Karel Volný <kvolny@redhat.com> 2.1.8-1
- version bump to 2.1.8

* Thu Apr 18 2024 Karel Volný <kvolny@redhat.com> 2.1.7-1
- version bump to 2.1.7
- removed ldconfig

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 08 2023 Leigh Scott <leigh123linux@gmail.com> - 2.1.5-2
- Rebuild for new faad2 version

* Fri Sep 01 2023 Karel Volný <kvolny@redhat.com> 2.1.5-1
- version bump to 2.1.5
- drop MMS transport as it is in Fedora now (rhbz#2235608)

* Fri Aug 11 2023 Leigh Scott <leigh123linux@gmail.com> - 2.1.4-1
- Update qmmp-plugins-freeworld to 2.1.4

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 27 2023 Karel Volný <kvolny@redhat.com> 2.1.2-2
- disable ffmpeg as ffmpeg-free is now in Fedora

* Sat Feb 25 2023 Sérgio Basto <sergio@serjux.com> - 2.1.2-1
- Update qmmp-plugins-freeworld to 2.1.2

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Tue Jun 14 2022 Karel Volný <kvolny@redhat.com> 2.1.1-1
- version bump to 2.1.1

* Thu May 19 2022 Karel Volný <kvolny@redhat.com> 2.1.0-1
- version bump to 2.1.0

* Fri Apr 08 2022 Karel Volný <kvolny@redhat.com> 2.0.4-1
- version bump to 2.0.4
- uses Qt6
- fix provides filtering
- update cmake usage

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-3
- Rebuilt for new ffmpeg snapshot

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Karel Volný <kvolny@redhat.com> 1.5.1-1
- version bump to 1.5.1

* Tue Jun 08 2021 Karel Volný <kvolny@redhat.com> 1.5.0-1
- version bump to 1.5.0

* Wed May 12 2021 Karel Volný <kvolny@redhat.com> 1.4.6-1
- version bump to 1.4.6

* Thu Apr 29 2021 Karel Volný <kvolny@redhat.com> 1.4.5-1
- version bump to 1.4.5
- fixes GCC 11 issue, patch removed

* Tue Feb 23 2021 Karel Volný <kvolny@redhat.com> 1.4.4-1
- version bump to 1.4.4

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
- Add GCC patch from Fedora proper
- Sync with Fedora proper

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 1.4.2-2
- Rebuilt for new ffmpeg snapshot

* Mon Sep 21 2020 Karel Volný <kvolny@redhat.com> 1.4.2-1
- version bump to 1.4.2

* Tue Aug 18 2020 Karel Volný <kvolny@redhat.com> 1.4.1-1
- version bump to 1.4.1
- adapted to F33 System-Wide Change: CMake to do out-of-source builds

* Tue Mar 31 2020 Karel Volný <kvolny@redhat.com> 1.3.7-1
- version bump to 1.3.7

* Tue Mar 10 2020 leigh123linux <leigh123linux@googlemail.com> - 1.3.6-1
- version bump to 1.3.6
- Remove obsolete scriptlets

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.5-3
- Rebuild for ffmpeg-4.3 git

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 28 2019 Karel Volný <kvolny@redhat.com> 1.3.5-1
- version bump to 1.3.5

* Wed Aug 14 2019 Karel Volný <kvolny@redhat.com> 1.3.3-1
- version bump to 1.3.3

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2.4-3
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Karel Volný <kvolny@redhat.com> 1.2.4-1
- version bump to 1.2.4

* Thu Jul 26 2018 Karel Volný <kvolny@redhat.com> 1.2.3-1
- version bump to 1.2.3

* Mon Jun 04 2018 Karel Volný <kvolny@redhat.com> 1.2.2-1
- version bump to 1.2.2

* Fri Apr 20 2018 Karel Volný <kvolny@redhat.com> 1.2.1-1
- version bump to 1.2.1
- removed patch to compile with newer ffmpeg (ffmpeg35_buildfix.patch)

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.1.12-4
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.12-2
- Rebuilt for ffmpeg-3.5 git

* Wed Nov 15 2017 Karel Volný <kvolny@redhat.com> 1.1.12-1
- version bump to 1.1.12
- add audio/* mimetypes filtered out from qmmp package

* Tue Aug 08 2017 Karel Volný <kvolny@redhat.com> 1.1.10-1
- version bump to 1.1.10

* Fri Jun 09 2017 Karel Volný <kvolny@redhat.com> 1.1.9-1
- version bump to 1.1.9
- add weak backwards dependency on qmmp (see also rhbz#1450271)

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.8-2
- Rebuild for ffmpeg update

* Tue Mar 28 2017 Karel Volný <kvolny@redhat.com> 1.1.8-1
- version bump to 1.1.8

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 06 2017 Karel Volný <kvolny@redhat.com> 1.1.7-1
- version bump to 1.1.7

* Tue Jan 17 2017 Karel Volný <kvolny@redhat.com> 1.1.6-1
- version bump to 1.1.6
- dropped MAD plugin, now in Fedora (rhbz#1400109)

* Wed Oct 05 2016 Karel Volný <kvolny@redhat.com> 1.1.4-1
- version bump to 1.1.4

* Thu Sep 08 2016 Sérgio Basto <sergio@serjux.com> - 1.1.2-1
- Sync to 1.1.2

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.1.1-2
- Rebuilt for ffmpeg-3.1.1

* Mon Jul 11 2016 Karel Volný <kvolny@redhat.com> 1.1.1-1
- version bump to 1.1.1

* Fri Jun 24 2016 Karel Volný <kvolny@redhat.com> 1.1.0-1
- version bump to 1.1.0
- uses Qt5
- disabled build of some more plugins present in base qmmp

* Tue Jan 12 2016 Karel Volný <kvolny@redhat.com> 0.9.6-1
- version bump
- updated provides filtering
- add separate .desktop file for each plugin for MimeType associations
- spec cleanups as per newer guidelines
 - removed BuildRoot definition
 - no longer remove buildroot, dropped clean section
 - removed defattr

* Mon Jan 04 2016 Karel Volný <kvolny@redhat.com> 0.9.5-1
- version bump

* Mon Jun 29 2015 Karel Volný <kvolny@redhat.com> 0.8.3-1
- version bump

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.7.7-4
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.7-3
- Rebuilt for FFmpeg 2.4.x

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.7.7-2
- Rebuilt for ffmpeg-2.3

* Thu Jun 12 2014 Karel Volný <kvolny@redhat.com> 0.7.7-1
- version bump

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 0.7.4-2
- Rebuilt for ffmpeg-2.2

* Wed Dec 11 2013 Karel Volný <kvolny@redhat.com> 0.7.4-1
- version bump

* Wed Dec 11 2013 Karel Volný <kvolny@redhat.com> 0.7.3-1
- version bump

* Wed Oct 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-2
- Rebuilt

* Wed Aug 28 2013 Karel Volný <kvolny@redhat.com> 0.7.2-1
- version bump

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.1-2
- Rebuilt for FFmpeg 2.0.x

* Fri Jun 21 2013 Karel Volný <kvolny@redhat.com> 0.7.1-1
- version bump

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.0-2
- Rebuilt for x264/FFmpeg

* Thu May 02 2013 Karel Volný <kvolny@redhat.com> 0.7.0-1
- version bump
- project URLs changed

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.6.8-2
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Apr 02 2013 Karel Volný <kvolny@redhat.com> 0.6.8-1
- version bump

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.6.6-2
- Rebuilt for ffmpeg

* Tue Jan 29 2013 Karel Volný <kvolny@redhat.com> 0.6.6-1
- version bump

* Tue Dec 11 2012 Karel Volný <kvolny@redhat.com> 0.6.5-1
- version bump

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.6.4-2
- Rebuilt for FFmpeg 1.0

* Tue Nov 06 2012 Karel Volný <kvolny@redhat.com> 0.6.4-1
- version bump

* Mon Jul 30 2012 Karel Volný <kvolny@redhat.com> 0.6.3-1
- version bump

* Mon Jul 30 2012 Karel Volný <kvolny@redhat.com> 0.6.2-1
- version bump

* Mon Jul 30 2012 Karel Volný <kvolny@redhat.com> 0.6.1-1
- version bump

* Tue Jul 03 2012 Karel Volný <kvolny@redhat.com> 0.6.0-1
- version bump

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.6-2
- Rebuilt for FFmpeg

* Mon Jun 18 2012 Karel Volný <kvolny@redhat.com> 0.5.6-1
- version bump
- adds support for ffmpeg-0.11

* Fri Jun 08 2012 Karel Volný <kvolny@redhat.com> 0.5.5-1
- version bump

* Fri Mar 02 2012 Karel Volný <kvolny@redhat.com> 0.5.4-1
- version bump
- removed patch to include usleep from QThread (qmmp-0.5.3-mms-include-usleep.patch)

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.3-3
- Rebuilt for c++ ABI breakage

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.3-2
- Rebuilt for x264/FFmpeg

* Mon Jan 23 2012 Karel Volný <kvolny@redhat.com> 0.5.3-1
- version bump
- patch to include usleep from QThread (qmmp-0.5.3-mms-include-usleep.patch)

* Wed Nov 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-3
- Rebuilt for libcdio

* Thu Sep 08 2011 Karel Volný <kvolny@redhat.com> 0.5.1-2
- rebuild for new ffmpeg

* Fri Jun 24 2011 Karel Volný <kvolny@redhat.com> 0.5.1-1
- version bump

* Wed Dec 15 2010 Karel Volný <kvolny@redhat.com> 0.4.3-1
- version bump

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.2-2
- Rebuilt for gcc bug

* Thu Sep 16 2010 Karel Volný <kvolny@redhat.com> 0.4.2-1
- version bump
- fixes possible freezes with mplayer plugin

* Fri Jul 02 2010 Karel Volný <kvolny@redhat.com> 0.4.1-1
- version bump
- fixes in flv playback and mplayer support

* Tue Jun 15 2010 Karel Volný <kvolny@redhat.com> 0.4.0-1
- version bump
- new MMS transport plugin
- BuildRequires libmms-devel for MMS support
- BuildRequires enca-devel for encoding detection

* Tue Apr 20 2010 Karel Volný <kvolny@redhat.com> 0.3.4-1
- version bump

* Thu Jan 14 2010 Karel Volný <kvolny@redhat.com> 0.3.2-1
- version bump

* Fri Dec 04 2009 Karel Volný <kvolny@redhat.com> 0.3.1-2
- add %%{?_isa} to require architecture match (wrt Fedora bug #543963)

* Thu Nov 05 2009 Karel Volný <kvolny@redhat.com> 0.3.1-1
- version bump

* Tue Aug 25 2009 Karel Volný <kvolny@redhat.com> 0.3.0-1
- version bump
- new plugins aac and mplayer
- BuildRequires faad2-devel for AAC support

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2.3-3
- rebuild for new F11 features

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
