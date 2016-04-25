#!/bin/sh

echo "ENV:" 1>&2
echo `env` 1>&2

echo "ARGS!" 1>&2
for word in "$@"; do echo "$word" 1>&2; done
echo "DONE ARGS!" 1>&2

echo '{"feedback":"Hello world.","fractionalScore":1.0}'
