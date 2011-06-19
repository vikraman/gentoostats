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

AUTHFILE="${ROOT}"/etc/gentoostats/auth.cfg

src_compile() {
	cd "client"
	distutils_src_compile
}

src_install() {
	cd "client"
	distutils_src_install
}

pkg_postinst() {
	distutils_pkg_postinst

	if ! [ -f "${AUTHFILE}" ]; then
		elog "Generating uuid and password in ${AUTHFILE}"
		if ! [ -d "$(dirname "${AUTHFILE}")" ]; then
			mkdir "$(dirname "${AUTHFILE}")"
		fi
		touch "${AUTHFILE}"
		echo "[AUTH]" >> "${AUTHFILE}"
		echo -n "UUID : " >> "${AUTHFILE}"
		cat /proc/sys/kernel/random/uuid >> "${AUTHFILE}"
		echo -n "PASSWD : " >> "${AUTHFILE}"
		< /dev/urandom tr -dc a-zA-Z0-9 | head -c16 >> "${AUTHFILE}"
		echo >> "${AUTHFILE}"
	fi
	chmod 0444 "${AUTHFILE}"
}
