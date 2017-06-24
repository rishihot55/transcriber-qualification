#!/bin/bash

if [ ! -d .git ]; then
  cd ..
  if [ ! -d app ]; then
    echo "You are not in the project directory!"
    exit 1
  fi
  echo "Moved to project root"
fi

if [ ! -d app/db ]; then
  echo "Adding base DB"
  mkdir -p app/db
  touch app/db/users.txt
  echo "Added base DB"
fi

if [ ! -d app/hit_db ]; then
  echo "Adding HIT DB"
  mkdir -p app/hit_db
  echo "Added HIT DB"
fi
