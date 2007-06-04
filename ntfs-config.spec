%define	_pre	RC3
Summary:	A front-end to Enable/disable NTFS write support
Name:		ntfs-config
Version:	1.0
Release:	0.%{_pre}.1
License:	GPL
Group:		Applications/System
Source0:	http://flomertens.free.fr/ntfs-config/download/source/%{name}-%{version}-%{_pre}.tar.gz
# Source0-md5:	cce97389f402e1cc325c47952eaec3df
URL:		http://flomertens.free.fr/ntfs-config
BuildRequires:	gettext
BuildRequires:	perl-XML-Parser
BuildRequires:	python-devel > 2.4
BuildRequires:	python-pygtk-devel > 2.6
Buildrequires:	hal-devel
Buildrequires:	libglade2-devel
BuildRequires:	desktop-file-utils
Requires:	ntfs-3g
#Requires:	usermode
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ntfs-config will allow you to enable/disable write support for
external and/or internal device with only two click. This will
configure your system to use the new ntfs-3g driver instead of the
current read-only kernel one.

%prep
%setup -q -n %{name}-%{version}-%{_pre}

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure PYTHON=%{_bindir}/python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/{pam.d,security/console.apps}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="install -p -Dm 644"

desktop-file-install					\
	--vendor ""					\
	--dir $RPM_BUILD_ROOT/%{_desktopdir}		\
	--mode 0644					\
	--remove-category=Application			\
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

install data/pam/ntfs-config.pam $RPM_BUILD_ROOT/etc/pam.d/%{name}-root
install data/pam/ntfs-config.consolhelper $RPM_BUILD_ROOT/etc/security/console.apps/%{name}-root

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%config(noreplace) /etc/pam.d/%{name}-root
%config(noreplace) /etc/security/console.apps/%{name}-root
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}-root
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{py_sitedir}/NtfsConfig
