#!/bin/bash
# Simple script to generate a random alphabetic API key
# Outputs the key to STDOUT

# Generate 32 random alphabetic characters
tr -dc 'A-Za-z' </dev/urandom | head -c 32
printf "\n"
