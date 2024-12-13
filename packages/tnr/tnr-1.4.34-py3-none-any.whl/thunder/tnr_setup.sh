__find_tnr() {
    TNR_PATH=$(which tnr)
    if [ -z "$TNR_PATH" ]; then
        TNR_PATH=$(find ~/.local/bin /usr/local/bin -name tnr -type f -print -quit 2>/dev/null)
    fi
    echo "$TNR_PATH"
}

__define_tnr_activated() {
    tnr() {
        if [ -z "${__TNR_BINARY_PATH}" ]; then
            export __TNR_BINARY_PATH=$(__find_tnr)
        fi
        if [ "$1" = "device" ]; then
            if [ $# -eq 1 ]; then
                # Handle the case for 'tnr device' with no additional arguments
                "$__TNR_BINARY_PATH" "$@"
            elif [ "$(echo "$2" | tr '[:upper:]' '[:lower:]')" = "cpu" ]; then
                # Handle the case for 'tnr device cpu'
                "$__TNR_BINARY_PATH" "$@"
                unset LD_PRELOAD
                PS1="(⚡CPU) $__DEFAULT_PS1"
            else
                # Handle other 'tnr device' commands
                "$__TNR_BINARY_PATH" "$@"
                if [ $? -eq 0 ]; then
                    case "${2,,}" in
                        h100|t4|v100|a100|l4|p4|p100)
                            export LD_PRELOAD=`readlink -f ~/.thunder/libthunder.so`
                            PS1="(⚡$($__TNR_BINARY_PATH device --raw)) $__DEFAULT_PS1"
                            ;;
                        *)
                            ;;
                    esac
                fi

            fi
        elif [ "$1" = "deactivate" ]; then
            unset __TNR_RUN
            PS1="$__DEFAULT_PS1"
            unset LD_PRELOAD
            __define_tnr_deactivated
        else
            # Forward the command to the actual tnr binary for all other cases
            "$__TNR_BINARY_PATH" "$@"
        fi
    }
}

__define_tnr_deactivated() {
    tnr() {
        if [ -z "${__TNR_BINARY_PATH}" ]; then
            export __TNR_BINARY_PATH=$(__find_tnr)
        fi
        if [ "$1" = "activate" ]; then
            output=$($__TNR_BINARY_PATH creds)
            exit_code=$?

            if [ $exit_code -eq 0 ]; then
                IFS=',' read -r token uid <<< "$output"
                export SESSION_USERNAME=$uid
                export TOKEN=$token
                export __TNR_RUN=true
                export __DEFAULT_PS1=$PS1
                device=$($__TNR_BINARY_PATH device --raw)
                PS1="(⚡$device) $__DEFAULT_PS1"
                if [ "$device" != "CPU" ]; then
                    export LD_PRELOAD=`readlink -f ~/.thunder/libthunder.so`
                fi
                __define_tnr_activated
            else 
                echo "Failed to activate Thunder. Please ensure you are logged in and try again."
            fi
        else
            # Forward the command to the actual tnr binary for all other cases
            "$__TNR_BINARY_PATH" "$@"
        fi
    }
}

__tnr_setup() {
    if [ -z "${__TNR_BINARY_PATH}" ]; then
        export __TNR_BINARY_PATH=$(__find_tnr)
    fi

    if [ -z "${__DEFAULT_PS1}" ]; then
        export __DEFAULT_PS1=$PS1
    fi

    if [[ "${__TNR_RUN}" != "true" ]]; then
        # We aren't running in a thunder shell
        __define_tnr_deactivated
    else
        PS1="(⚡$($__TNR_BINARY_PATH device --raw)) $__DEFAULT_PS1"
        __define_tnr_activated
    fi
}

__tnr_setup