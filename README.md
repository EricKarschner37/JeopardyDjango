# NOTE:

This repo is now _deprecated_. Please see [this repo](https://github.com/EricKasrchner37/Jeopardy) instead.

# Jeopardy

A self-hosted open source Jeopardy! game. This project uses the [Jeopardy! Buzzer App](https://github.com/EricKarschner37/JeopardyApp) to manage players.

## Overview

Jeopardy is built using Python and Django on the backend with a React.JS front end. It uses [Django Channels](https://channels.readthedocs.io/en/latest/) to manage a WebSocket server to communicate with the buzzer app. This project would not be possible without [J-archive](http://www.j-archive.com/), which holds transcripts of every past Jeopardy game.

## Features

Jeopardy currently supports a basic game of Jeopardy, played through the Jeopardy! Buzzer App.

**Game retrieval**

Games can be added to the Jeopardy database on-demand from the J-archive website.

**Buzzers**

Using the Jeopardy! Buzzer App, players can experience a fully-featured buzzer system, complete with host controls to manage the buzzers.

**Score tracking**

After a user has buzzed in, the host can report whether or not they were correct to automatically keep track of each player's score.

## Planned Features

The following features are planned for future development:

* Custom Game Creation
* iOS Application
* Improved Final Jeopardy
