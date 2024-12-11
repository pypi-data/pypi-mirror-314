#!/usr/bin/env bash
set -euo pipefail

# https://gitlab.com/odameron/fusekiInstallationUsage/-/blob/main/fusekiInstallationUsage.md?ref_type=heads
#
SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

DEFAULT_VERSION=5.0.0
DEFAULT_HEAP_SIZE=16G
DEFAULT_PATH=$DIR/tmp/fuseki

function show_help()
{
  cat << HELP
SYNOPSIS
  Download the Fuseki server.

USAGE
  ${0##*/} [-h] [-d PATH] [-s INT] [-v VERSION]

OPTIONS
  -h
    Show this help message and exit.

  -d PATH
    Download the files to a directory at PATH.
    Default: $DEFAULT_PATH

  -s SIZE
    Configure the default maximum Java heap size to size.
    Default: $DEFAULT_HEAP_SIZE

  -v VERSION
    Select Fuseki server VERSION.
    Default: $DEFAULT_VERSION
HELP
  exit "$1"
}

fuseki_dir=$DEFAULT_PATH
heap_size=$DEFAULT_HEAP_SIZE
version=$DEFAULT_VERSION
while getopts 'd:h:s:v:' opt
do
  case "$opt" in
    d) fuseki_dir=$OPTARG ;;
    s) heap_size=$OPTARG ;;
    v) version=$OPTARG ;;
    h) show_help 0 ;;
    *) show_help 1 ;;
  esac
done


mkdir -p "$fuseki_dir"
fuseki_dir=$(readlink -f "$fuseki_dir")
pushd "$fuseki_dir"
name=apache-jena-fuseki-$version
# wget -N "https://dlcdn.apache.org/jena/binaries/$name.tar.gz"
wget -N "https://archive.apache.org/dist/jena/binaries/$name.tar.gz"
wget -N "https://archive.apache.org/dist/jena/binaries/$name.tar.gz.sha512"
sha512sum "$name.tar.gz.sha512"
bsdtar -xf "$name.tar.gz"

cat > env.sh <<ENV
#!/bin/bash
if [[ -z \${JVM_ARGS:-} ]]
then
  export JVM_ARGS=-Xmx${heap_size}
fi
export FUSEKI_HOME=${fuseki_dir@Q}/${name@Q}
ENV
popd

echo -e "\nSource $fuseki_dir/env.sh to set the FUSEKI_HOME environment variable."
