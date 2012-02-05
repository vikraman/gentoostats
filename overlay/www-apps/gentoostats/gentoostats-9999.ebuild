# Copyright 1999-2011 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=4

inherit webapp git-2

DESCRIPTION="Package statistics server"
HOMEPAGE="https://soc.dev.gentoo.org/gentoostats/"
SRC_URI=""

EGIT_REPO_URI="git://git.overlays.gentoo.org/proj/gentoostats.git"

LICENSE="GPL-3"
KEYWORDS=""
IUSE=""

DEPEND=""
RDEPEND="${DEPEND}
	>=dev-python/webpy-0.3
	dev-python/mysql-python
	dev-python/matplotlib"

pkg_setup() {
	webapp_pkg_setup
}

src_install() {
	webapp_src_preinst
	pushd "server"

	insinto "${MY_HTDOCSDIR}"
	doins -r .
	webapp_src_install
}

pkg_postinst() {
	webapp_pkg_postinst
}
