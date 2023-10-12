#!/bin/bash

function onFinish {
  if [ -x "$(command -v deactivate)" ]; then
      deactivate > /dev/null 2>&1
  fi
}

trap onFinish EXIT
trap onFinish ERR
trap onFinish SIGINT

cd venv/Scripts
. activate > /dev/null 2>&1
cd ../..