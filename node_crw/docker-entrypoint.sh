#!/bin/bash
# Copyright (c) 2018 The Crown developers
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

systemnode=false
masternode=false
help=false
install=false
unknown=()
appname=$(basename "$0")

print_help()
{
echo "Usage: $(basename "$0") [OPTION]...
Setup crown server or update existing one

  -m, --masternode                  create a masternode
  -s, --systemnode                  create a systemnode
  -p, --privkey=privkey             set private key
  -h, --help                        display this help and exit

"
}

handle_arguments()
{
    while [[ $# -gt 0 ]]
    do
        key="$1"
        case $key in
            -h|--help)
                help=true
                shift
                ;;
            -m|--masternode)
                masternode=true
                shift
                ;;
            -s|--systemnode)
                systemnode=true
                shift
                ;;
            -p|--privkey)
                privkey="$2"
                shift
                shift
                ;;
            --privkey=*)
                privkey="${key#*=}"
                shift
                ;;
            *)    # unknown option
                unknown+=("$1") # save it in an array
                shift
                ;;
        esac
    done
    if [ "$help" = true ] ; then
        print_help
        exit 0
    fi

    # Check if there are unknown arguments
    if [ ${#unknown[@]} -gt 0 ] ; then
        printf "$appname: unrecognized option '${unknown[0]}'\nTry '$appname --help' for more information.\n"
        exit 1
    fi

    # Check if only one of the options is set
    if [ "$masternode" = true ] && [ "$systemnode" = true ] ; then
        echo "'-m|masternode' and '-s|--systemnode' options are mutually exclusive."
        exit 1
    fi

    # Check if private key is set and not empty
    if [ ! -z ${privkey+x} ] && [ -z "$privkey" ]; then
        printf "$appname: option '-p|--privkey' requires an argument'\nTry '$appname --help' for more information.\n"
        exit 1
    fi

    # Check if '-m' or '-s' option is set with '-p'
    if [ ! -z "$privkey" ] && [ "$masternode" != true ] && [ "$systemnode" != true ] ; then
        printf "$appname: If private key is set '-m' or '-s' option is mandatory'\nTry '$appname --help' for more information.\n"
        exit 1
    fi

    # If private key is set then install otherwise update
    if [ ! -z "$privkey" ]; then
        install=true
    fi
}


configure_conf() {
    echo "========================CROWN=============================="
    cd $HOME
    mkdir -p .crown
    # mv .crown/crown.conf .crown/crown.bak
    touch .crown/crown.conf
    IP=$(curl http://checkip.amazonaws.com/)
    PW=$(date +%s | sha256sum | base64 | head -c 32 ;)

    pwd
    echo "rpcallowip=127.0.0.1" > /crown/.crown/crown.conf 
    echo "rpcuser=crowncoinrpc">> /crown/.crown/crown.conf 
    echo "rpcpassword="$PW >> /crown/.crown/crown.conf 
    echo "listen=1" >> /crown/.crown/crown.conf 
    echo "server=1" >> /crown/.crown/crown.conf 
    echo "externalip="$IP >> /crown/.crown/crown.conf 

    echo "printtoconsole=1" >> /crown/.crown/crown.conf
    cat /crown/.crown/crown.conf
    echo "==========================================================="
}

main() {
    configure_conf
}

handle_arguments "$@"
main
exec crownd
