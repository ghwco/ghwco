#!/usr/bin/env bash
#
# Assembles the publishable site into dist/.
#
# Why this exists: Cloudflare Pages publishes whatever directory you point it
# at. Pointing it at the repo root worked fine for a no-build deploy, but once
# `npm install` runs there, node_modules sits in the publish root — tens of
# thousands of files against Pages' 20,000-file cap, and none of them belong
# on the web. Copying the real site into dist/ and publishing that keeps the
# output to exactly what should be served.
#
# Run by `npm run build`, after the generators and `tinacms build`.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

rm -rf dist
mkdir -p dist

# Pages, assets and the Tina editor
cp -R assets dist/
cp -R content dist/          # Tina reads these at runtime in the editor
[ -d admin ] && cp -R admin dist/
cp ./*.html dist/

# Root-level files that must be served verbatim
for f in robots.txt sitemap.xml llms.txt _redirects _headers; do
  [ -f "$f" ] && cp "$f" dist/
done

# Never ship the build machinery or the working files
rm -f dist/logo-options.html dist/type-options.html dist/v1.html

echo "→ dist/ assembled: $(find dist -type f | wc -l | tr -d ' ') files"
