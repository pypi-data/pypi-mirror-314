# Debian packages

Debian packages are avaiable at https://deb.rkslot.nl/:

  * [music-client-python](https://codeberg.org/raphson/music-client-python) as `python3-raphson-music-client`
  * [music-headless](https://codeberg.org/raphson/music-headless) as `raphson-music-headless`


## Building packages

If you are not on Debian or on a different version, use distrobox:
```
distrobox create --image debian:bookworm --name debian
distrobox enter debian
```

Install build dependencies:
```
sudo apt install dpkg-dev debhelper dh-python pybuild-plugin-pyproject python3-hatchling
dpkg-buildpackage -tc
```

The -tc option ensures temporary data is deleted after building. The built package is placed in the parent directory of the repository.

You must have a GPG key in order to sign the package.
