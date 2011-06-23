# Copyright 1999-2011 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=3

inherit distutils python git

DESCRIPTION="Package statistics client"
HOMEPAGE="http://soc.dev.gentoo.org/gentoostats"
SRC_URI=""

EGIT_REPO_URI="git://git.overlays.gentoo.org/proj/gentoostats.git"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS=""
IUSE=""

DEPEND=""
RDEPEND="${DEPEND}
	sys-apps/portage
    >=app-portage/gentoolkit-0.3.0.2
	dev-python/simplejson"

src_compile() {
	cd "client"
	distutils_src_compile
}

src_install() {
	cd "client"
	distutils_src_install

	dodir /etc/gentoostats || die
	insinto /etc/gentoostats
	doins payload.cfg || die

	# this doesn't work, why ?
	fowners root:portage /etc/gentoostats/payload.cfg || die
	fperms 0640 /etc/gentoostats/payload.cfg || die
}

pkg_postinst() {
	distutils_pkg_postinst

	AUTHFILE="${ROOT}/etc/gentoostats/auth.cfg"
	if ! [ -f "${AUTHFILE}" ]; then
		elog "Generating uuid and password in ${AUTHFILE}"
		touch "${AUTHFILE}"
		echo "[AUTH]" >> "${AUTHFILE}"
		echo -n "UUID : " >> "${AUTHFILE}"
		cat /proc/sys/kernel/random/uuid >> "${AUTHFILE}"
		echo -n "PASSWD : " >> "${AUTHFILE}"
		< /dev/urandom tr -dc a-zA-Z0-9 | head -c16 >> "${AUTHFILE}"
	fi
	chown root:portage "${AUTHFILE}"
	chmod 0640 "${AUTHFILE}"
}
