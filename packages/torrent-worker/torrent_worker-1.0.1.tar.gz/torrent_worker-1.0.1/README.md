# torrent-worker


This torrent worker will:

  * Download torrent source files from a github source
  * Launch a docker instance of a the qbittorrent server
  * Iteratively add torrents as they get completed
  * Display the torrent download information as it's downloading.

Yes, you have to have all the torrents in a github url.

Yes you need to have the docker engine installed.

You can check the progress by either looking at the command line output or else looking at the website at localhost:8080


# Example 1

`torrent-worker --range all --torrent-source https://github.com/author/repo`


# Example 2

This will allow you to use clients on a different computers and distribute the work.

`torrent-worker --range 0-10 --torrent-source https://github.com/author/repo`

# Example 3

  * Docker Image information:
    * https://github.com/linuxserver/docker-qbittorrent
  * Credentials
    * user: admin
    * pass: adminadmin


#### Platform tests

[![MacOS_Tests](https://github.com/zackees/zlib-download/actions/workflows/test_macos.yml/badge.svg)](https://github.com/zackees/zlib-download/actions/workflows/test_macos.yml)
[![Ubuntu_Tests](https://github.com/zackees/zlib-download/actions/workflows/test_ubuntu.yml/badge.svg)](https://github.com/zackees/zlib-download/actions/workflows/test_ubuntu.yml)
[![Win_Tests](https://github.com/zackees/zlib-download/actions/workflows/test_win.yml/badge.svg)](https://github.com/zackees/zlib-download/actions/workflows/test_win.yml)

#### Lint

[![Lint](https://github.com/zackees/zlib-download/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/zlib-download/actions/workflows/lint.yml)

torrent_worker with Docker, ready for Render.com / DigitalOcean

To deploy the test app simply fork the repository and go to Render.com, login with your github account, and select this repo that you forked in your account. It should run without any changes.

# Releases

  * 1.0.1 - Adds lock for the client.
  * 1.0.0 - Initial release.