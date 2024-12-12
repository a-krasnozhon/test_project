#!/usr/bin/env sh
if ! pytest;then /usr/games/cowsay -f eyes "!!!!!!!! YOUR TESTS FAILED !!!!!!!!"; exit 1; fi