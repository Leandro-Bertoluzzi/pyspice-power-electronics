<!--
<div align="center" id="top"> 
  <img src="logo.gif" alt="Pyspice Power Electronics" />
  &#xa0;
</div>
-->

<h1 align="center">Pyspice Power Electronics</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/Leandro-Bertoluzzi/pyspice-power-electronics?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/Leandro-Bertoluzzi/pyspice-power-electronics?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/Leandro-Bertoluzzi/pyspice-power-electronics?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/Leandro-Bertoluzzi/pyspice-power-electronics?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/Leandro-Bertoluzzi/pyspice-power-electronics?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/Leandro-Bertoluzzi/pyspice-power-electronics?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/Leandro-Bertoluzzi/pyspice-power-electronics?color=56BEB8" /> -->
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Pyspice Power Electronics 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/Leandro-Bertoluzzi" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

Collection of scripts with the definition and simulation of circuits used in power electronics, written in Python using the module PySpice to interact with NgSpice and Matplotlib to graph the results from the simulations.

## :rocket: Technologies ##

The following tools were used in this project:

- [PySpice](https://pyspice.fabrice-salvaire.fr/)
- [NgSpice](http://ngspice.sourceforge.net/)
- [Matplotlib](https://matplotlib.org/)
- [Numpy](https://numpy.org/)
- [Docker](https://www.docker.com/)

## :white_check_mark: Requirements ##

- If you want to use the docker container, you need to [install Docker](https://www.docker.com/get-started) and, optionally, [Docker Compose](https://docs.docker.com/compose/install/) in your machine.

- If you decide to not use docker, you need to install [PySpice](https://pyspice.fabrice-salvaire.fr/). The version currently used is [v1.5](https://pyspice.fabrice-salvaire.fr/releases/v1.5/installation.html). In the same docs you are taught how to install NgSpice.

If you choose the second option, local setup, and you are a Windows user, I highly recommend installing it via Anaconda or Miniconda.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/Leandro-Bertoluzzi/pyspice-power-electronics

# Access the project folder
$ cd pyspice-power-electronics

# Option 1: Using Docker container through docker-compose
docker-compose run --rm pyspice the_folder/the_file.py

# Option 2: Using Docker container without docker-compose
## Before running it for the first time and every time you modify the scripts, build the docker container
docker build -t pyspice .
## Run the Docker container with the script as a parameter
docker run --rm -v %cd%/results:/root/results pyspice the_folder/the_file.py

# Option 3: Installing PySpice in local machine
## Enter any of the folders and run a script
$ cd the_folder
$ python the_file.py
```

**Note:** If you chose option 2, to get the current directory you must use:
- Windows (cmd): %cd%
- Windows (PowerShell): ${PWD}
- Linux: $(pwd)
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.

Made with :heart: by <a href="https://github.com/Leandro-Bertoluzzi" target="_blank">Leandro Bertoluzzi</a>

&#xa0;

<a href="#top">Back to top</a>
