Name:		fermilab-conf_ocsinventory
Version:	2.9.1
Release:	1.1%{?dist}
Summary:	Configure the OCS Inventory client for Fermilab

Group:		Fermilab
License:	MIT
URL:		https://github.com/fermilab-context-rpms/fermilab-conf_ocsinventory

Source0:	30-fermilab-util_ocsinventory.preset

Source1:	Fermilab_Root_CA.pem
Source2:	FERMI_Sub_CA_01.pem
Source3:	SERVICES_Sub_CA_01.pem

BuildArch:	noarch

Requires:	ocsinventory-agent >= 2.9.1-1%{?dist}
Requires:	systemd

Requires(post):	ocsinventory-agent >= 2.9.1-1%{?dist}
Requires(post):	augeas coreutils findutils systemd

BuildRequires:	systemd

# Drop this old name with EL11?
Obsoletes:	fermilab-util_ocsinventory

%define OCSServer https://ocssrv.fnal.gov/ocsinventory/


%description
This RPM will setup OCS Inventory for use at Fermilab.

%prep


%build


%install
%{__install} -D %{SOURCE0} %{buildroot}/%{_presetdir}/30-fermilab-conf_ocsinventory.preset
mkdir -p %{buildroot}/%{_datarootdir}/%{name}/

cat %{SOURCE1} >  %{buildroot}/%{_datarootdir}/%{name}/ocsinventory-agent-cacert.pem
cat %{SOURCE2} >> %{buildroot}/%{_datarootdir}/%{name}/ocsinventory-agent-cacert.pem
cat %{SOURCE3} >> %{buildroot}/%{_datarootdir}/%{name}/ocsinventory-agent-cacert.pem


%post
%systemd_post ocsinventory-agent-daily.timer

TMPFILE=$(mktemp)
cat > ${TMPFILE} <<EOF
set /files/etc/sysconfig/ocsinventory-agent/OCSMODE\[0\] cron
set /files/etc/sysconfig/ocsinventory-agent/OCSSERVER\[0\] %{OCSServer}
save
EOF
augtool < ${TMPFILE} >/dev/null
rm -f ${TMPFILE}

# %{_sysconfdir}/ocsinventory/ocsinventory-agent-cacert.pem added in 2.9.1
cat %{_datarootdir}/%{name}/ocsinventory-agent-cacert.pem >> %{_sysconfdir}/ocsinventory/ocsinventory-agent-cacert.pem

# delete any existing host specific CA certs and let them be rebuilt
find /var/lib/ocsinventory-agent -type f -name cacert.pem -exec rm -f {} \;

systemctl enable ocsinventory-agent-daily.timer
systemctl start ocsinventory-agent-daily.timer

%preun
%systemd_preun ocsinventory-agent-daily.timer

%postun
%systemd_postun_with_restart ocsinventory-agent-daily.timer


%files
%{_presetdir}/30-fermilab-conf_ocsinventory.preset
%config %{_datarootdir}/%{name}/ocsinventory-agent-cacert.pem


%changelog
* Tue Apr 5 2022 Pat Riehecky <riehecky@fnal.gov> 2.9.1-1.1
- Fix requirements typo

* Mon Feb 28 2022 Pat Riehecky <riehecky@fnal.gov> 2.9.1-1
- Initial build for EL9 and OCSInventory 2.9.1
