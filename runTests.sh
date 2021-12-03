#!/bin/bash

. setEnv.sh

coverage run -m unittest
coverage report
coverage html