# Command line configurables

%if 0%{?fedora}%{?rhel} == 0 || 0%{?fedora} >= 5 || 0%{?rhel} >= 5
%bcond_without cracklib
%else
%bcond_with cracklib
%endif

%if 0%{?fedora}%{?rhel} == 0 || 0%{?fedora} >= 7 || 0%{?rhel} >= 6
%bcond_without xdg_utils
%bcond_without cracklib_python
%else
%bcond_with xdg_utils
%bcond_with cracklib_python
%endif

%if 0%{?fedora}%{?rhel} == 0 || 0%{?fedora} >= 8 || 0%{?rhel} >= 6
%bcond_without libuser_python
%else
%bcond_with libuser_python
%endif

%if 0%{?fedora}%{?rhel} == 0 || 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%bcond_without console_util
%else
%bcond_with console_util
%endif

# Enterprise versions pull in docs automatically
%if 0%{?rhel} > 0
%bcond_without require_docs
%else
%bcond_with require_docs
%endif

Summary: A graphical interface for administering users and groups
Name: system-config-users
Version: 1.2.104
Release: 1%{?dist}
URL: http://fedorahosted.org/%{name}
License: GPLv2+
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source: http://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.bz2
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: findutils
# Until version 1.2.81, system-config-users contained online documentation.
# From version 1.2.82 on, online documentation is split off into its own
# package system-config-users-docs. The following ensures that updating from
# earlier versions gives you both the main package and documentation.
Obsoletes: system-config-users < 1.2.82
%if %{with require_docs}
Requires: system-config-users-docs
%endif
%if %{with libuser_python}
Requires: libuser-python >= 0.56
%else
Requires: libuser >= 0.56
%endif
Requires: python >= 2.0
Requires: pygtk2 >= 2.6
Requires: pygtk2-libglade
%if %{with console_util}
Requires: usermode-gtk >= 1.94
%else
Requires: usermode-gtk >= 1.36
%endif
%if %{with xdg_utils}
Requires: xdg-utils
%else
Requires: htmlview
%endif
Requires: rpm-python
Requires: /usr/bin/pgrep
%if %{with cracklib}
%if %{with cracklib_python}
Requires: cracklib-python >= 2.8.6
%else
Requires: cracklib >= 2.8.6
%endif
%endif

BuildRequires: python >= 2.0

%description
system-config-users is a graphical utility for administrating 
users and groups.  It depends on the libuser library.

%prep
%setup -q

%build
make %{?with_console_util:CONSOLE_USE_CONFIG_UTIL=1} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

desktop-file-install --vendor system --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-category X-Red-Hat-Base                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %name
find $RPM_BUILD_ROOT%{_datadir} -name "*.mo" | xargs ./utf8ify-mo

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/system-config-users
%{_datadir}/system-config-users
%{_mandir}/man8/system-config-users*
%{_datadir}/applications/%{name}.desktop
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-users
%config(noreplace) %{_sysconfdir}/pam.d/system-config-users
%config(noreplace) %{_sysconfdir}/sysconfig/system-config-users

%changelog
* Wed Aug 11 2010 Nils Philippsen <nils@redhat.com> - 1.2.104-1
- pick up translation updates

* Wed Aug 11 2010 Nils Philippsen <nils@redhat.com> - 1.2.103-1
- fix python format directives in id.po

* Wed Aug 11 2010 Nils Philippsen <nils@redhat.com> - 1.2.102-1
- pick up translation updates

* Tue Jul 20 2010 Nils Philippsen <nils@redhat.com> - 1.2.101-1
- don't inadvertently add new users to existing groups (#616450)

* Mon Jul 19 2010 Nils Philippsen <nils@redhat.com>
- enforce uids, gids fitting in id_t datatype, also clamp uid, gid to permitted
  value range in UI (#616067)

* Wed Jun 30 2010 Nils Philippsen <nils@redhat.com> - 1.2.100-1
- check if homedirs of new users can be created
- prevent unlocking users with empty passwords
- require docs in enterprise builds

* Fri Jun 11 2010 Nils Philippsen <nils@redhat.com> - 1.2.99-1
- fix exception handling on user removal (#602192)

* Wed May 26 2010 Nils Philippsen <nils@redhat.com> - 1.2.98-1
- revert bad commit which overwrote Greek translations (#590890)
- only delete user or group if really confirmed (#539251)
- make file deletion methods more robust (#539251)

* Mon May 03 2010 Nils Philippsen <nils@redhat.com> - 1.2.97-1
- really require cracklib-python where this is split off (#588462)

* Wed Mar 31 2010 Nils Philippsen <nils@redhat.com> - 1.2.96-1
- use named icons for windows etc., don't require hicolor-theme anymore

* Tue Mar 23 2010 Nils Philippsen <nils@redhat.com> - 1.2.95-1
- pick up translation updates

* Thu Mar 04 2010 Nils Philippsen <nils@redhat.com>
- fix shortcuts in user properties dialog (#570353)

* Thu Jan 21 2010 Nils Philippsen <nils@redhat.com>
- don't obsolete redhat-config-users anymore
- fix conditional for RHEL

* Wed Dec 16 2009 Nils Philippsen <nils@redhat.com>
- use consistent terms for adding users (#343571)
- use strings as keys for user/group check messages
- warn about user names with trailing dollar sign (#486906)

* Mon Sep 28 2009 Nils Philippsen <nils@redhat.com> - 1.2.94-1
- pick up new translations

* Wed Sep 16 2009 Nils Philippsen <nils@redhat.com> - 1.2.93-1
- remove simple files as well as directories
- don't use deprecated gtk.Label.set_use_markup()

* Wed Sep 16 2009 Nils Philippsen <nils@redhat.com> - 1.2.92-1
- fix typo (#523068)

* Mon Sep 14 2009 Nils Philippsen <nils@redhat.com> - 1.2.91-1
- use str.startswith() method (#523068)

* Thu Sep 03 2009 Nils Philippsen <nils@redhat.com> - 1.2.90-1
- import gettext from each module again
- use gtk.ComboBoxEntry instead of gtk.Combo

* Wed Sep 02 2009 Nils Philippsen <nils@redhat.com> - 1.2.89-1
- initialize gettext correctly

* Fri Aug 28 2009 Nils Philippsen <nils@redhat.com> - 1.2.88-1
- initialize gettext at the right place
- get rid of rhpl.iconv, rhpl.executil

* Wed Aug 26 2009 Nils Philippsen <nils@redhat.com>
- explain obsoleting old versions

* Wed Jun 10 2009 Nils Philippsen <nils@redhat.com>
- avoid duplicate shortcuts in main window (#275621)

* Wed Jun 03 2009 Nils Philippsen <nils@redhat.com> - 1.2.87-1
- handle 64bit uids/gids (#503821)

* Thu May 28 2009 Nils Philippsen <nils@redhat.com>
- use simplified source URL

* Tue Apr 14 2009 Nils Philippsen <nils@redhat.com> - 1.2.86-1
- pick up updated translations

* Thu Feb 12 2009 Nils Philippsen <nils@redhat.com> - 1.2.85-1
- cope with new semantics in cracklib >= 2.8.13 (#484303)
- fix ambiguous use of 'str'

* Mon Dec 22 2008 Nils Philippsen <nils@redhat.com> - 1.2.84-1
- use ValueError.message, not .msg to get cracklib error message (#479858)
- pull in updated translations

* Mon Dec 22 2008 Nils Philippsen <nils@redhat.com> - 1.2.83-1
- fix typo in Source0 URL

* Fri Nov 28 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.82-1
- split off documentation

* Thu Oct 30 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.81-1
- require usermode-gtk instead of usermode

* Thu May 08 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.80-1
- handle invalid UTF-8 in passwd information more gracefully (#235533)

* Tue Apr 22 2008 Nils Philippsen <nphilipp@redhat.com>
- fix duplicate shortcut (#439717)

* Tue Apr 08 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.79-1
- pick up updated translations

* Mon Mar 31 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.78-1
- fix focus target for "Account expires" label (#439717)
- fix French translator credits so msgfmt doesn't complain

* Tue Mar 25 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.77-1
- use hard links to avoid excessive disk space requirements

* Thu Jan 31 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.76-1
- migrate online help to yelp/Docbook XML

* Fri Jan 11 2008 Nils Philippsen <nphilipp@redhat.com> - 1.2.75-1
- use config-util for userhelper configuration from Fedora 9 on (#428403)

* Thu Dec 27 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.74-1
- rename sr@Latn to sr@latin (#426592)

* Mon Dec 10 2007 Nils Philippsen <nphilipp@redhat.com>
- allow setting but not creating of home directories when creating a user
  (#416421)

* Wed Dec 05 2007 Nils Philippsen <nphilipp@redhat.com>
- overwrite *.pot and *.po files only on real changes

* Wed Dec 05 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.73-1
- use libuser defaults for password and account expiration when creating users
  (#185097)

* Wed Nov 07 2007 Nils Philippsen <nphilipp@redhat.com>
- update copyright terms, admit complicity in source files
- display shadow information from LDAP directories (#185907, fix by Ed van
  Gasteren, modified)
- use libuser defaults for home directories (#204707, fix by Miloslav Trmac)
- use gtk.AboutDialog for about dialog (#202963)

* Tue Oct 16 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.72-1
- make /usr/share/system-config-users/system-config-users.py executable again

* Mon Oct 15 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.71-1
- add release tags to changelog entries to appease rpmlint
- remove "ExclusiveOS: Linux"
- use xdg-open if available
- change hicolor-icon-theme requirement to be "uncolored" (without
  "(post)"/"(postun)")
- obsolete explicit version of redhat-config-users
- use "%%defattr(-,root,root,-)"
- don't use %%attr
- use "%%config(noreplace)"
- use macros instead of hardcoded directories
- don't let gtk-update-icon-cache fail scriptlets
- remove obsolete no.po translation file (#332431)
- use "make %%{?_smp_mflags}"

* Mon Oct 08 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.70-1
- add "make diff" ("dif") and "make shortdiff" ("sdif")
- pull in updated translations

* Thu Oct 02 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.69-1
- prohibit home directories which are not absolute paths or contain path
  components which are empty, ".", ".." or too long (#303971)

* Tue Oct 02 2007 Nils Philippsen <nphilipp@redhat.com>
- limit username and groupname entries to their respective maximum lengths
  (#303931)

* Mon Oct 01 2007 Nils Philippsen <nphilipp@redhat.com>
- limit homedir entry to maximum path length (#304011)

* Fri Sep 28 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.68-1
- remove po/POTFILES.in to appease transifex (#299811)
- pick up updated translations

* Sun Sep 16 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.67-1
- pick up updated translations

* Sat Sep 15 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.66-1
- pick up updated translations

* Mon Sep 10 2007 Nils Philippsen <nphilipp@redhat.com>
- make use of force tagging (since mercurial 0.9.4)

* Sat Aug 18 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.65-1
- avoid more duplicate shortcuts (#253319)

* Fri Aug 17 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.64-1
- keep account expiration date stable (#251760)

* Thu Aug 16 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.63-1
- change license tag to GPLv2+
- make accounts without home directory work (#251076)

* Wed Aug 15 2007 Nils Philippsen <nphilipp@redhat.com>
- require libuser-python from Fedora 8 on
- check password expiration values for validity (#251762)

* Mon Aug 13 2007 Nils Philippsen <nphilipp@redhat.com>
- avoid duplicate shortcuts in preferences dialog (#251766)

* Fri Aug 10 2007 Nils Philippsen <nphilipp@redhat.com>
- avoid duplicate user/group names when editing properties (#251584, #251588)

* Tue Aug 07 2007 Nils Philippsen <nphilipp@redhat.com>
- fix typo that prevented colons as the first character to be found (#251081)

* Tue Jul 24 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.62-1
- pull in updated translations

* Mon Jul 23 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.61-1
- make "make archive" work with Hg

* Fri Jul 20 2007 Nils Philippsen <nphilipp@redhat.com>
- fix exception syntax, catch only IndexErrors caused by group inconsistencies
  (#243217)
- list users and/or groups found to be inconsistent (#243217)

* Thu Jul 19 2007 Nils Philippsen <nphilipp@redhat.com>
- catch IndexErrors caused by group inconsistencies (#243217)

* Wed Jul 18 2007 Nils Philippsen <nphilipp@redhat.com>
- don't delete preferences toplevel window when closing via window manager
  (#248686)
- barf even less on inconsistent groups (#243217)

* Thu Jun 28 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.60-1
- don't barf on inconsistent groups
- use integers instead of strings for various user parameters (#226976, patch
  by Miloslav Trmac)

* Wed Jun 27 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.59-1
- fix desktop file category (#245876)

* Tue Jun 26 2007 Nils Philippsen <nphilipp@redhat.com>
- try not to barf if encountering inconsistencies between /etc/passwd,
  /etc/group, /etc/shadow and /etc/gshadow

* Wed Jun 13 2007 Nils Philippsen <nphilipp@redhat.com>
- fix English language oddity

* Fri Jun 08 2007 Nils Philippsen <nphilipp@redhat.com>
- split up map/filter statement in userGroupFind.py to make debugging easier
  (#243217)

* Thu May 24 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.58-1
- avoid traceback when creating a new user with a specific group id (#240129)

* Wed Apr 25 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.57-1
- pick up updated translations

* Fri Mar 30 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.56-1
- check whether password and confirmed password match before checking weakness
  etc.

* Fri Mar 30 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.55-1
- don't check both password and confirmed password to avoid duplicate error
  dialogs (#234182)

* Mon Mar 26 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.54-1
- fix plural specification for German (#233781)

* Thu Mar 22 2007 Nils Philippsen <nphilipp@redhat.com>
- update URL

* Tue Mar 20 2007 Nils Philippsen <nphilipp@redhat.com>
- mention that we are upstream
- use preferred buildroot
- use Category: ... System; ... in desktop file
- clean buildroot before installing
- fix licensing blurb in PO files
- require/BR python >= 2.0 instead of python2
- recode spec file to UTF-8

* Mon Mar 19 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.53-1
- some UI cleanup
- when adding new users, let gid be set manually (#201500)

* Mon Feb 05 2007 Nils Philippsen <nphilipp@redhat.com>
- fix erroneous tooltips (#227205)
- mark python files as utf-8 (#226772)

* Thu Feb 01 2007 Nils Philippsen <nphilipp@redhat.com>
- use named arguments in translatable format strings
- use ngettext to allow proper pluralization

* Thu Feb 01 2007 Nils Philippsen <nphilipp@redhat.com> - 1.2.52-1
- fix BR: find-utils -> findutils
- fix syntax error in Makefile

* Wed Jan 31 2007 Nils Philippsen <nphilipp@redhat.com>
- use "install -m" to install a lot of files without executable bits (#222580)

* Tue Jan 30 2007 Nils Philippsen <nphilipp@redhat.com>
- fix warning about all-digit usernames

* Mon Jan 29 2007 Nils Philippsen <nphilipp@redhat.com>
- fix typos (#217247, #224444)

* Thu Jan 25 2007 Nils Philippsen <nphilipp@redhat.com>
- check passwords with cracklib if available (#82723)

* Wed Jan 10 2007 Nils Philippsen <nphilipp@redhat.com>
- add BR: find-utils

* Thu Dec 21 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.51-1
- pick up updated translations (#216396)

* Wed Dec 13 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.50-1
- pick up updated translations (#216396)

* Fri Nov 24 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.49-1
- pick up updated translations (#216396)

* Sat Oct 14 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.48-1
- pick up updated translations

* Sat Oct 14 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.47-1
- pick up updated translations (#210731)

* Mon Jul 24 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.46-1
- ask user when hitting duplicate group name or gid (#199836)

* Mon Jul 17 2006 Nils Philippsen <nphilipp@redhat.com>
- clarify comments, add new variables in /etc/sysconfig/system-config-users
- use new method to choose GID when creating groups as well
- actually set new user's GID
- remove debugging statements

* Thu Jul 13 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.45-1
- revamp uid/gid number selection to honor preferences and avoid primary
  group/created group discrepancies (#198152)
- use disttag if available

* Mon Jun 12 2006 Nils Philippsen <nphilipp@redhat.com>
- detect inconsistencies between /etc/group and /etc/gshadow at startup
  (#174716)

* Wed Jun 07 2006 Nils Philippsen <nphilipp@redhat.com>
- change some label texts
- fix indentation

* Tue May 16 2006 Nils Philippsen <nphilipp@redhat.com>
- fix localization markings (#191846, patch by Roozbeh Pournader)

* Fri May 05 2006 Nils Philippsen <nphilipp@redhat.com>
- pull out preferences handling into Preferences class
- implement preferences dialog

* Wed Apr 05 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.44-1
- rephrase some error messages to ease translation (#154204)

* Mon Mar 27 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.43-1
- pick up translation updates

* Fri Mar 03 2006 Nils Philippsen <nphilipp@redhat.com> - 1.2.42-1
- require hicolor-icon-theme (#182882, #182883)

* Fri Oct 14 2005 Nils Philippsen <nphilipp@redhat.com>
- don't use pam_stack (#170649)

* Tue Oct 04 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.41-1
- fix variable names to prevent hangs when adding a group (#169730)

* Fri Sep 30 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.40-1
- initialize shadow variables only if shadow passwords are used
  (#168524, #168529, patch by Josef Whiter)

* Fri Sep 23 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.39-1
- require rhpl (#168921)

* Fri Jun 10 2005 Nils Philippsen <nphilipp@redhat.com>
- allow punctation in user names (#141273)

* Mon May 09 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.38-1
- pick up updated translations

* Fri May 06 2005 Nils Philippsen <nphilipp@redhat.com>
- make desktop file rebuild consistently

* Fri May 06 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.37-1
- make About menu entry translate (#156793)

* Fri May 06 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.36-1
- use DESTDIR consistently

* Wed May 04 2005 Nils Philippsen <nphilipp@redhat.com>
- make desktop file translatable (#156793)

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 1.2.35-2
- silence %%post

* Thu Apr 07 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.35-1
- correct setting shadow values if password doesn't expire

* Mon Apr 04 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.34-1
- don't crash when displaying non-shadow accounts (#152960)

* Mon Apr 04 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.33-1
- don't use GNOME stock stuff for About menu entry (#153227)

* Fri Apr 01 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.32-1
- don't require gnome (#152960)
- revive about dialog

* Fri Apr 01 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.31-1
- fix deprecation warnings (#153054) with (modified) patch by Colin Charles

* Wed Mar 30 2005 Nils Philippsen <nphilipp@redhat.com> - 1.2.30-1
- use os.lstat() to test ownership of files to be deleted
- update the GTK+ theme icon cache on (un)install

* Fri Dec 03 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.29-1
- use variable max length for user/group names (prepare fix for #141273)

* Wed Nov 10 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.28-1
- check for running processes of a user about to be deleted (#132902)

* Mon Nov 08 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.27-1
- some sanity testing to avoid deleting system directories when deleting a user
  (#138093)
- eventually delete mail spool (#102637) and temporary files (#126756)

* Fri Nov 05 2004 Nils Philippsen <nphilipp@redhat.com>
- set password and confirm password entries (in)sensitive based on whether
  account is locked or not (#131180)

* Tue Nov 02 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.26-1
- use libuser defaults for password aging (#130379, original patch by Dave
  Lehman)

* Wed Oct 13 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.25-1
- when renaming users, ensure that groups forget about the old user name
  (#135280)

* Mon Oct 11 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.24-1
- use user/group names for indexing, avoid unnecessary user/group lookups
  (#135223, original patch by Miloslav Trmac)
- remove some debugging statements
- updated translations

* Fri Oct 08 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.23-1
- try to fix 32bit uids/gids (#134803)
- fix gtk.main*() related DeprecationWarnings
- byte-compile python files in "make install"
- updated translations

* Mon Oct 04 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.22-1
- updated translations

* Sun Sep 26 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.21-1
- updated translations

* Fri Sep 24 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.20-1
- allow UTF-8 in user's full name (#133137)
- require new libuser version so that fix for #80624 doesn't throw exception
  (#133479)
- admit complicity

* Wed Sep 15 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.19-1
- try to use gid as specified in /etc/libuser.conf, only if that fails use next
  free (#80624)

* Mon Sep 13 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.18-1
- use F1 instead of Ctrl+H as accelerator for Help/Contents (#132163)
- use "mkdir -p" to fix make install glitch
- use absolute paths in *.glade to fix pygtk/pyglade subtleties

* Sun Sep 05 2004 Nils Philippsen <nphilipp@redhat.com> - 1.2.15-1
- add manpage (Chris Spencer, #115316)
- add Slovenian translation to desktop file (Roman Maurer, #131835)

* Mon Jun 21 2004 Brent Fox <bfox@redhat.com> - 1.2.14-1
- fix password expiration bug (bug #125234)

* Wed Apr 21 2004 Brent Fox <bfox@redhat.com> 1.2.13-1
- allow columns to be resized (bug #121174)

* Tue Apr 20 2004 Brent Fox <bfox@redhat.com> 1.2.12-5
- call self.ready() if no is clicked (bug #121364)

* Mon Apr 19 2004 Brent Fox <bfox@redhat.com> 1.2.12-4
- apply patch from bug #72058 to localize pw last changed time

* Mon Apr 19 2004 Brent Fox <bfox@redhat.com> 1.2.12-3
- hide SELinux widgets for now (bug #119941)

* Mon Apr 19 2004 Brent Fox <bfox@redhat.com> 1.2.12-2
- remove *pyc files on ininstall

* Thu Apr 15 2004 Brent Fox <bfox@redhat.com> 1.2.12-1
- fix bug #120669

* Tue Apr 13 2004 Brent Fox <bfox@redhat.com> 1.2.11-6
- remove print statements in mainWindow.py

* Mon Apr 12 2004 Brent Fox <bfox@redhat.com> 1.2.11-5
- fix icon path (bug #120186)

* Wed Apr  7 2004 Brent Fox <bfox@redhat.com> 1.2.11-4
- disable SELinux widgets if it isn't running or isn't enabled (bug #120193)

* Tue Apr  6 2004 Brent Fox <bfox@redhat.com> 1.2.11-3
- remove Requires on policy-sources and setools (bug #120193)

* Mon Apr  5 2004 Brent Fox <bfox@redhat.com> 1.2.11-2
- rebuild for SELinux 
- add Requires on policy-sources

* Wed Mar 31 2004 Brent Fox <bfox@redhat.com> 1.2.11-1
- first stab at SELinux bits

* Wed Mar 24 2004 Brent Fox <bfox@redhat.com> 1.2.10-1
- reset user home dir check button (bug #119068)

* Tue Feb  3 2004 Brent Fox <bfox@redhat.com> 1.2.9-1
- remove comparison to gtk.TRUE (bug #114266)

* Mon Jan 12 2004 Brent Fox <bfox@redhat.com> 1.2.8-1
- rename redhat-config-users.png to system-config-users.png (bug #113311)

* Mon Dec  1 2003 Brent Fox <bfox@redhat.com> 1.2.7-1
- preserve existing group selection in userProperties.py (bug #111199)
- handle munged config file (bug #108400)

* Mon Nov 24 2003 Brent Fox <bfox@redhat.com> 1.2.6-1
- remove Red Hat reference in the window title

* Wed Nov 19 2003 Brent Fox <bfox@redhat.com> 1.2.5-1
- rename from redhat-config-users
- add Obsoletes for redhat-config-users
- make changes for Python2.3

* Mon Oct 27 2003 Brent Fox <bfox@redhat.com> 1.2.4-1
- call self.ready() if the user clicks cancel in the existing group dialog (bug #107991)

* Mon Oct 20 2003 Brent Fox <bfox@redhat.com> 1.2.3-1
- use htmlview to find default browser (bug #107604)

* Mon Oct  6 2003 Brent Fox <bfox@redhat.com> 1.2.2-1
- don't allow the root's username to be changed (bug #105632)

* Tue Sep 23 2003 Brent Fox <bfox@redhat.com> 1.2.1-1
- rebuild with latest docs

* Tue Sep 16 2003 Brent Fox <bfox@redhat.com> 1.1.17-4
- bump release

* Tue Sep 16 2003 Brent Fox <bfox@redhat.com> 1.1.17-3
- turn off SELinux

* Tue Sep 16 2003 Brent Fox <bfox@redhat.com> 1.1.17-2
- bump release

* Tue Sep 16 2003 Brent Fox <bfox@redhat.com> 1.1.17-1
- if shadow passwords are not enabled, do not show certain widgets (bug #104536)
- don't modify password expiration data by accident (bug #88190)

* Thu Sep 4 2003 Dan Walsh <dwalsh@redhat.com> 1.1.16-3
- Turn off SELinux 

* Thu Sep 4 2003 Dan Walsh <dwalsh@redhat.com> 1.1.16-2.sel
- add SELinux support

* Thu Aug 14 2003 Brent Fox <bfox@redhat.com> 1.1.16-1
- clarify error dialog message (bug #101607)
- allow underscores and dashes in usernames and groupnames (bug #99115)

* Thu Aug 14 2003 Brent Fox <bfox@redhat.com> 1.1.15-1
- tag on every build

* Wed Aug 13 2003 Brent Fox <bfox@redhat.com> 1.1.14-2
- bump relnum and rebuild

* Wed Aug 13 2003 Brent Fox <bfox@redhat.com> 1.1.14-1
- use UTC instead of GMT (bug #102251)

* Wed Aug 13 2003 Brent Fox <bfox@redhat.com> 1.1.13-1
- add BuildRequires on gettext

* Wed Jul 23 2003 Brent Fox <bfox@redhat.com> 1.1.12-2
- bump relnum and rebuild

* Wed Jul 23 2003 Brent Fox <bfox@redhat.com> 1.1.12-1
- use GMT time on password last changed (bug #89759)

* Wed Jul 23 2003 Brent Fox <bfox@redhat.com> 1.1.11-2
- bump relnum and rebuild

* Wed Jul 23 2003 Brent Fox <bfox@redhat.com> 1.1.11-1
- don't create new user with an existing uid (bug #90911)
- use the messageDialog module in groupWindow.py
- don't create group with an existing gid (bug #90911)

* Fri Jul 11 2003 Brent Fox <bfox@redhat.com> 1.1.10-2
- bump relnum and rebuild

* Fri Jul 11 2003 Brent Fox <bfox@redhat.com> 1.1.10-1
- display an error if no X server is running (bug #97148)

* Mon Jun  2 2003 Brent Fox <bfox@redhat.com> 1.1.9-1
- popup a confirmation dialog when deleting groups
- popup a confirmation dialog when deleting users

* Tue May 27 2003 Brent Fox <bfox@redhat.com> 1.1.8-1
- don't require a full user name (bug #91718)

* Fri May 23 2003 Brent Fox <bfox@redhat.com> 1.1.7-1
- don't allow colons in username or homedir names (bug #90481)
- check for zero length in usernames, groupnames, gecos, and homedirs

* Thu May 22 2003 Brent Fox <bfox@redhat.com> 1.1.6-1
- change label in glade file (bug #86323)

* Mon May 19 2003 Brent Fox <bfox@redhat.com> 1.1.5-9
- create a 'users' group if a new user is getting added to a non-existing users group (bug #89895)

* Thu Apr  3 2003 Brent Fox <bfox@redhat.com> 1.1.5-8
- don't automatically delete system groups (bug #78620)

* Wed Feb 26 2003 Jeremy Katz <katzj@redhat.com> 1.1.5-7
- use rm for rmrf instead (#85175)

* Mon Feb 17 2003 Brent Fox <bfox@redhat.com> 1.1.5-6
- update desktop file (bug #84360)

* Thu Feb 13 2003 Brent Fox <bfox@redhat.com> 1.1.5-5
- make double-click launch properties box (#84231)

* Tue Feb 11 2003 Brent Fox <bfox@redhat.com> 1.1.5-4
- call self.rmrf

* Mon Feb 10 2003 Brent Fox <bfox@redhat.com> 1.1.5-3
- rebuild to pull in fix for bug #83341

* Fri Feb  7 2003 Brent Fox <bfox@redhat.com> 1.1.5-2
- fix bug #83341 for real this time

* Wed Feb  5 2003 Brent Fox <bfox@redhat.com> 1.1.5-1
- don't allow root account to be locked
- make default values for SHADOW* on user creation so we can do password aging properly later

* Tue Feb  4 2003 Brent Fox <bfox@redhat.com> 1.1.4-2
- fix bug with deleting user homeDir (bug #83341)

* Thu Jan 30 2003 Brent Fox <bfox@redhat.com> 1.1.4-1
- bump and build

* Fri Jan 24 2003 Brent Fox <bfox@redhat.com> 1.1.3-4
- better error checking for user names and group names (bug #82607)
* Thu Jan 16 2003 Brent Fox <bfox@redhat.com> 1.1.3-3
- force ascii input (bug #74058)
- make sure that groupWindow calls self.ready() after showing dialogs
- remove sentence hacks in asciiCheck.py (bug #82015)
- fix typo in about box (bug #82016)
- do not create homedir if they user doesn't want to
- only offer to delete homedirs if they actually exist  (bug #78619)
- if the user is the only member of their group, delete the group automatically (bug #78620)
* Wed Jan 15 2003 Brent Fox <bfox@redhat.com> 1.1.3-1
- don't try to delete the group if the groupEnt is None (bug #68950)
* Tue Jan 14 2003 Tammy Fox <tfox@redhat.com> 1.1.2-2
- update help with new screenshots and tweak content
* Wed Jan  8 2003 Brent Fox <bfox@redhat.com> 1.1.2-1
- ask if they want to delete the home directory
* Tue Jan  7 2003 Brent Fox <bfox@redhat.com> 1.1.1-9
- handle window delete-events correctly
- call ready() after dialog is destroyed (bug #80625)
- if a deleted user is the only user in his primary group, offer to delete the group too (bug #78620)
* Mon Dec 23 2002 Brent Fox <bfox@redhat.com> 1.1.1-6
- replace some message dialogs with calls to show_message_dialog
* Tue Dec 17 2002 Brent Fox <bfox@redhat.com> 1.1.1-5
- Do a lot of input checking on the userWindow.py and userProperties.py (bug #79246)
* Tue Nov 12 2002 Brent Fox <bfox@redhat.com> 1.1.1-4
- Rebuild with latest translations
* Thu Oct 10 2002 Brent Fox <bfox@redhat.com> 1.1.1-3
- Make the upper limit on UIDs and GIDs  (pow(2, 32)).  Fixes bug 75605
* Mon Sep 16 2002 Brent Fox <bfox@redhat.com>
- groupWindow.py, groupProperties.py, userProperties.py...desensitize when performing actions
* Fri Sep 13 2002 Brent Fox <bfox@redhat.com>
- Make the window insensitive when adding a user to prevent double clicks
* Tue Sep 10 2002 Brent Fox <bfox@redhat.com> 
- Applied patch for Norwegian translation to desktop file
* Tue Sep 03 2002 Brent Fox <bfox@redhat.com> 1.1.1-2
- Pull in latest translations
* Thu Aug 29 2002 Brent Fox <bfox@redhat.com> 1.1.1-1
- Pull in latest translations
* Thu Aug 22 2002 Dan Walsh <dwalsh@redhat.com> 1.1-16
- Fix traceback bug, caused by unitialized variable
- Fix traceback bug, caused by primary gid missing from /etc/group
* Tue Aug 20 2002 Brent Fox <bfox@redhat.com> 1.1-15
- Convert desktop file to UTF8
- Pull in new translations into desktop file
* Mon Aug 19 2002 Brent Fox <bfox@redhat.com> 1.1-14
- Apply patch from twaugh to fix bug 68778
- Change widths on account expriation widgets
* Thu Aug 15 2002 Brent Fox <bfox@redhat.com> 1.1-13
- enlarge window startup size for verbose langs
* Wed Aug 14 2002 Brent Fox <bfox@redhat.com> 1.1-12
- rebuild to pull in latest translations
* Mon Aug 12 2002 Tammy Fox <tfox@redhat.com> 1.1-11
- replace System with SystemSetup in desktop file categories
* Wed Aug 07 2002 Tammy Fox <tfox@redhat.com>
- UI tweaks
* Tue Aug 06 2002 Brent Fox <bfox@redhat.com> 1.1-10
- Increase default window size
* Tue Aug 06 2002 Brent Fox <bfox@redhat.com> 1.1-9
- fix bug 70783
* Fri Aug 02 2002 Brent Fox <bfox@redhat.com> 1.1-8
- Use new pam timestamp rules
* Wed Jul 24 2002 Brent Fox <bfox@redhat.com> 1.1-7
- Use new icons from garrett
* Wed Jul 24 2002 Brent Fox <bfox@redhat.com> 1.1-6
- Fix glade path typo
* Wed Jul 24 2002 Tammy Fox <tfox@redhat.com> 1.1-4
- Fix desktop file (bug #69488)
* Thu Jul 18 2002 Karsten Hopp <karsten@redhat.de> 1.1-3
- prepare for new pygtk2
* Sat Jul 13 2002 Brent Fox <bfox@redhat.com> 1.1-2
- Fixed bug #68639
- Make properties and delete widgets desensitized when necessary
* Fri Jul 12 2002 Tammy Fox <tfox@redhat.com>
- Updated docs
- Moved desktop file to /usr/share/applications only
* Thu Jul 11 2002 Brent Fox <bfox@redhat.com> 1.1-1
- Add a "Search Filter" label
* Fri Jun 14 2002 Brent Fox <bfox@redhat.com> 1.0.2-3
- Typo bug on my part
* Thu Jun 13 2002 Brent Fox <bfox@redhat.com> 1.0.2-1
- Use spiffy new toolbar icons
* Thu May 2 2002 Brent Fox <bfox@redhat.com> 1.0.1-7
- Update translations
* Mon Apr 22 2002 Brent Fox <bfox@redhat.com> 1.0.1-6
- Bring in the latest translations and rebuild in the latest dist
* Thu Apr 18 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-5
- Convert .mo files to UTF-8 at install-time, fixing #63815 correctly (probably)
* Thu Apr 18 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-4
- Don't bail on LookupErrors when recoding strings, just punt (#63815)
* Tue Apr 16 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-3
- Don't bail on IOErrors when saving preferences to /etc/sysconfig
* Tue Apr 16 2002 Brent Fox <bfox@redhat.com> 1.0.1-2
- Add set_transient_for calls to bring dialogs to the front in KDE (#61590)
* Tue Apr 16 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-1
- Handle cases where translations are encoded in non-UTF8 encodings (#63334)
* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0-14
- Update translations
* Tue Apr 09 2002 Brent Fox <bfox@redhat.com>
- Added workaround for bug 62919
* Fri Apr 05 2002 Brent Fox <bfox@redhat.com>
- Added changes to use a new icon
* Thu Mar 28 2002 Brent Fox <bfox@redhat.com>
- Finished port to Python2.2/Gtk2
* Wed Feb 27 2002 Brent Fox <bfox@redhat.com> 
- Added sortable columns
* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.2-7
- rebuild for completeness
* Wed Aug 29 2001 Brent Fox <bfox@redhat.com>
- Fixed desktop file problem
- Nakai added Japanese support to the desktop file
* Thu Aug 9 2001 Tammy Fox <tfox@redhat.com>
- added documentation
* Thu Aug 9 2001 Nalin Dahyabhai <nalin@redhat.com>
- Attempt to minimize enumerations where possible
- Always use defined constants for attribute names
* Thu Aug 9 2001 Brent Fox <bfox@redhat.com>
- fixes for password aging
* Wed Aug  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- byte-compile python modules in %%install and include them in the package
* Wed Jul 26 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese translation
* Wed Jul 26 2001  Yukihiro Nakai <ynakai@redhat.com>
- Directory restructure for i18n
* Tue Jul 10 2001 Brent Fox <bfox@redhat.com>
- some glade fixups and packaging work
* Mon Jul 09 2001 Tammy Fox <tfox@redhat.com>
- added usermode files to spec file
* Tue Jul 05 2001 Brent Fox <bfox@redhat.com>
- initial packaging
* Wed Jun 13 2001 Brent Fox <bfox@redhat.com>
- mainWindow.glade: Changed GUI per jrb's recommendations
- mainWindow.py: added interfacing with libuser backend
* Wed Jun 6 2001 Jonathan Blandford  <jrb@redhat.com>
- mainWindow.glade: Cleaned up glade file a bunch.
- mainWindow.py: modified to deal with updated glade.


