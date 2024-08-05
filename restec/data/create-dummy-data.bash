#!/bin/bash
for i in {1..50}
do
  echo "$i: dummy-$i.data"
  fallocate -l 1G dummy-$i.data
done
