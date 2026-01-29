#!/usr/bin/bash

set -eo pipefail

# Use grouped output messages
infobegin() {
	echo "::group::${1}"
}
infoend() {
	echo "::endgroup::"
}

# Required packages on Fedora
requires=(
	ccache # Use ccache to speed up build
)

requires+=(
	autoconf-archive
	python3-dbus
	gcc
	git
	gtk3-devel
	gtksourceview4-devel
	libpeas-devel
	make
	mate-common
	pluma-devel
	python3-devel
	vte291-devel
	yelp-tools
	enchant2-devel
	iso-codes-devel
	libSM-devel
)

infobegin "Update system"
dnf update -y
infoend

infobegin "Install dependency packages"
dnf install -y ${requires[@]}
infoend
