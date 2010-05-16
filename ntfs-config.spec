# TODO:
#	binaries names and dirs seems counterintuitive:
#	    /usr/bin/ntfs-config	requires root privilages
#	    /usr/sbin/ntfs-config-root	invokes ntfs-config via gksu/kdesu
#	    /usr/bin/ntfs-config-root	invokes ntfs-config via consolehelper
#
Summary:	A front-end to Enable/disable NTFS write support
Summary(pl.UTF-8):	Frontend do włączania/wyłączania obsługi zapisu na NTFS
Name:		ntfs-config
Version:	1.0.1
Release:	1.9
License:	GPL
Group:		Applications/System
Source0:	http://flomertens.free.fr/ntfs-config/download/source/%{name}-%{version}.tar.gz
# Source0-md5:	d491c8129aa9dad4de28b2b0b2b8f309
Patch0:		%{name}-am.patch
URL:		http://flomertens.free.fr/ntfs-config/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	hal-devel
BuildRequires:	intltool
BuildRequires:	libglade2-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	python-devel > 1:2.4
BuildRequires:	python-pygtk-devel > 2:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires:	ntfs-3g
Requires:	usermode
Suggests:	e2fsprogs
Suggests:	gnome-mount
Suggests:	hal
Suggests:	module-init-tools
Suggests:	mount
Suggests:	udev-core
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ntfs-config will allow you to enable/disable write support for
external and/or internal device with only two click. This will
configure your system to use the new ntfs-3g driver instead of the
current read-only kernel one.

%description -l pl.UTF-8
ntfs-config pozwala włączyć/wyłączyć obsługę zapisu dla zewnętrznego
i/lub wewnętrznego urządzenia za pomocą tylko dwóch kliknięć.
Konfiguruje to system do używania nowego sterownika ntfs-3g zamiast
aktualnego z jądra obsługującego poprawnie tylko odczyt.

%prep
%setup -q
%patch0 -p1

# there's newer pt.po
rm -f po/pt_PT.po
%{__sed} -i s/^pt_PT$// po/LINGUAS

%build
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-force-pam=yes \
	PYTHON=%{__python}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	pyexecdir=%{py_sitescriptdir} \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="install -p -Dm 644"

desktop-file-install					\
	--vendor ""					\
	--dir $RPM_BUILD_ROOT/%{_desktopdir}		\
	--mode 0644					\
	--remove-category=Application			\
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%config(noreplace) /etc/pam.d/%{name}-root
%config(noreplace) /etc/security/console.apps/%{name}-root
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-root
%attr(755,root,root) %{_sbindir}/%{name}-root
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{py_sitescriptdir}/NtfsConfig
%{_mandir}/man8/ntfs-config-root.8*
%{_mandir}/man8/ntfs-config.8*
