[![wercker status](https://app.wercker.com/status/4f7193bea2bccc9333c83ae0727c2392/m/ "wercker status")](https://app.wercker.com/project/byKey/4f7193bea2bccc9333c83ae0727c2392)

# Transmission Post Processor

When configured in Transmission, Transmission Post Processor runs every time a download finishes.
It will detect if the download contains archived content or not.
If if does contain archived content, transmission post processor will try to extract it and then move the extracted content together with the remaining content to the configured destination.
If it does not contain archived content, it will move every file that was downloaded "as is" to the destination directory. 

## Transmission Parameters

Transmission provides the following parameters:
* TR_APP_VERSION = 2.92
* TR_TIME_LOCALTIME = Tue Aug  9 16:02:17 2016
* TR_TORRENT_DIR = /downloads/complete
* TR_TORRENT_HASH = fb204ba60db50be3ea21d025f4cddc385468ab91
* TR_TORRENT_ID = 41
* TR_TORRENT_NAME = UbuntuLinux

# Post Processor Parameters

Transmission Post Processor requires the following parameters:
* File destination directory


## Operation modes

Install the python egg into your system.
```bash
python setyp.py sdist
```

### Command Line (cmdline)

Run the tool from command line.
```bash
# python -m trdone cmdline --help
python -m trdone cmdline -t <TORRENT> -d <DESTINATION>
```

The source repository contains a script (`trdone.sh`) that can be used to execute straight from transmission.
It basically links the environment variables exported by transmission to the command needed to run the tool.
It still needs a destination to where it should process the torrents.
Since you cannot configure transmission to pass arguments to the script, the destination directory must be hardcoded in the script.

### API (api)

Run the tool as a service.
```bash
# python -m trdone api --help
python -m trdone api -p <port>
```

Once the tool is running on a given port, use a web client to post to it.
Make a script with the following content and confiure transmission to run that.
Replace `/DESTINATION_DIR`, `HOST` and `PORT` accordingly.
```bash
#! /bin/bash
curl -X POST -d '{"torrent":"'"${TR_TORRENT_DIR}/${TR_TORRENT_NAME}"'","destination":"/DESTINATION_DIR"}' http://HOST:PORT
```

### API Docker Container

This repo is linked to Docker Hub and a container is build on every commit.
To decouple the volumes mapped in the container from the real paths that transmission uses (maybe even the volumes that are mapped in a transmission container), the API mode
provides and option to define a path mapping.
In order to have set the correct permissions on the mounted volumes, `puid` and `guid` of the appropriate user need to be set.
Such a mapping relates the torrent paths as transmission sees them the paths that the API container knows.
```
docker create --name=trdone \
    -e "torrent_external=some_path" \
    -e "torrent_internal=another_path" \
    -e puid=<user_id> \
    -e pgid=<group_id> \
    -p <port>:8080 \
    -v <path_to_downloaded_torrents_dir>:/downloads \
    -v <path_to_processed_torrents_destination>:/processed \
    miguelaferreira/transmission-postprocess 
```
