#! /bin/bash

set -xe

if [ -z $(grep abc /etc/passwd) ]; then
  addgroup --gid ${pgid} abc
  adduser --home /trdone --disabled-password --uid ${puid} --gid ${pgid} \
    --gecos "First Last,RoomNumber,WorkPhone,HomePhone" abc
  chown -R abc:abc /trdone
fi

touch /root/.bash_profile
chmod 777 /root/.*

su --preserve-environment -l abc \
      -c "UNRAR_LIB_PATH=/usr/lib/libunrar.so python trdone api -p 8080 -te ${torrent_external} -ti ${torrent_internal}"
