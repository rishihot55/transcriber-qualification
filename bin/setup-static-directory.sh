#!/bin/bash

if [ ! -d .git ]; then
  cd ..
  if [ ! -d app ]; then
    echo "You are not in the project directory!"
    exit 1
  fi
  echo "Moved to project root"
fi

echo "Performing bower install for frontend dependencies"
bower install
echo "Bower install complete"

if [ ! -d app/static ]; then
  mkdir app/static
fi

cp -r bower_components/bootstrap/dist/* app/static/
cp bower_components/jquery/dist/jquery.js app/static/js/
cp bower_components/bootstrap-combobox/css/bootstrap-combobox.css app/static/css/
cp bower_components/bootstrap-combobox/js/bootstrap-combobox.js app/static/js/
