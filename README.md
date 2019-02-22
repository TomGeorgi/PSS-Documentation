# PSS-Documentation [![Build Status](https://travis-ci.org/TomGeorgi/PSS-Documentation.svg?branch=master)](https://travis-ci.org/TomGeorgi/PSS-Documentation)

This repository contains the documentation of my practical semestre, which I absolved in WS18/19.
Also, the main.pdf will be build via Travis-CI. The newest version can be found in [releases](https://github.com/TomGeorgi/PSS-Documentation/releases).

## Prolog
Thank you to [Lorenz Bung](https://github.com/LorenzBung), who provided a LaTeX-Template.
You want to get a LaTeX template ? Then visit Lorenz Bung for a [Template](https://github.com/LorenzBung/doku-pss/tree/template).

## Content of this repository

### Folders
-  `content/`: This directory contains the file content.
-  `format/`: This directory includes packages, configuration, etc.
	
	> **Note**: If you need to create a new code style, feel free to watch the file **python_code** as example, which is 
	contained in this folder.
	
-  `graphics/`: This directory contains all used graphics.

### Files
- `main.tex`: main LaTeX-file.
- `format/packages.tex`: This file includes all needed packages.
- `format/python_code.tex`:  This file defines a source code environment for python via using the package **lstlistings**.

### Continuous Integration

- `Travis-CI`: pipeline for creating and releasing a PDF-file.
- `Docker`: [Docker Image](https://hub.docker.com/r/dxjoke/tectonic-docker) which I use in Travis-CI to create a PDF-File from LaTeX-Files.

## How to use this repository

If you want to use this repository please go to the template branch and follow the instructions for setup your own **Continuous Integration**.
