#! /bin/bash

dir="$(dirname "$(readlink -f "$0")")"
echo "Starting Solr in $dir"

solr=/opt/solr/solr-7.0.0
$solr/bin/solr start -s $dir