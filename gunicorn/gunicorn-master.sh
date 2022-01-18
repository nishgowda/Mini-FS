#!/bin/bash
gunicorn  master:app -b 0.0.0.0:3000

