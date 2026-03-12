#!/usr/bin/bash

set -eo pipefail

# Use grouped output messages
infobegin() {
	echo "::group::${1}"
}
infoend() {
	echo "::endgroup::"
}

# Required packages on Archlinux
requires=(
	ccache # Use ccache to speed up build
)

requires+=(
	autoconf-archive
	clang
	gcc
	git
	gtksourceview4
	libpeas
	make
	mate-common
	pluma
	python-dbus
	python-gobject
	vte3
	yelp-tools
	which
)

infobegin "Update system"
pacman --noconfirm -Syu
infoend

infobegin "Install dependency packages"
pacman --noconfirm -S ${requires[@]}
infoend
