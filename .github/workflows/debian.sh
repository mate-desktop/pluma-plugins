#!/usr/bin/bash

set -eo pipefail

# Use grouped output messages
infobegin() {
	echo "::group::${1}"
}
infoend() {
	echo "::endgroup::"
}

# Required packages on Debian
requires=(
	ccache # Use ccache to speed up build
)

requires+=(
	autopoint
	gcc
	git
	libgtk-3-dev
	libgtksourceview-4-dev
	libpeas-dev
	libvte-2.91-dev
	make
	mate-common
	pluma-dev
	python3-dev
	python3-dbus
	python3-gi
	yelp-tools
	libenchant-2-dev
)

infobegin "Update system"
apt-get update -qq
infoend

infobegin "Install dependency packages"
env DEBIAN_FRONTEND=noninteractive \
	apt-get install --assume-yes \
	${requires[@]}
infoend
