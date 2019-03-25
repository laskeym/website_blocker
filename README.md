# Website Blocker

An application written in Python that allows a user to block websites during productivity hours.

Project does what it needs to, but could use some enhancments in the installation field to make running easier than the command line.

## Install

This project uses Python 3.5.3, wxPython and a simple HTTP server.

`git clone https://github.com/laskeym/website_blocker.git`

`pip install -r requirements.txt`

## Usage

A few pre configuration steps to run first:

* Run `sudo visudo` and input `{username}  ALL=(ALL) NOPASSWD: {project_dir}/grant.sh`, as well as `{username}  ALL=(ALL)  NOPASSWD: {project_dir}/revoke.sh`

Currently, this application is run through the command line

`python main.py`

Simply type the URL you wish to block and click 'Add'. 

To remove a URL, just highlight and click 'Remove'.

## To Do

* When running the program, the console asks for the sudo password.  This is because the program is trying to access the `/etc/hosts` file.  I thought that editing `visudo` would fix this, but I was mistken.  Need to take another look at what's in the `visudo` file.
* For the user to see the effect of the block site take place, they need to refresh the browser cache.  One solution could be to use a headless Selenium and gear it towards Chrome/Firefox only.