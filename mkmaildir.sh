#!/bin/bash

mkdir -p $1/{sieve,.maildir/{cur,new,tmp}}
chown -R mail:mail $1
