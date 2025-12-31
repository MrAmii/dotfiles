#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '
export EDITOR=nano

# Wake/shutdown/check mainframe
mainframe() {
    case "$1" in
        on)
            echo "SENDING WAKE PACKET TO MAINFRAME..."
            wol 00:02:e3:3f:1a:04 > /dev/null 2>&1
            echo "WAKING UP..."
            echo "WAITING FOR MAINFRAME TO BOOT... (PRESS CTRL+C TO CANCEL)"
            while true; do
                if ping -c 1 -W 1 192.168.1.64 &>/dev/null; then
                    echo "✓ MAINFRAME IS ONLINE! ($(date +%T))"
                    echo "CONNECTING VIA SSH..."
                    ssh mainframe
                    return 0
                fi
                sleep 2
            done
            ;;
        off)
            echo "SHUTTING DOWN MAINFRAME..."
            ssh mainframe "sudo shutdown now"
            echo "✓ SHUTDOWN COMMAND SENT!"
            ;;
        "")
            echo "CHECKING MAINFRAME STATUS..."
            if ping -c 1 -W 1 192.168.1.64 &>/dev/null; then
                echo "✓ MAINFRAME IS ONLINE"
            else
                echo "✗ MAINFRAME IS OFFLINE"
            fi
            ;;
        *)
            echo "USAGE: MAINFRAME [ON|OFF]"
            echo "       MAINFRAME (CHECK STATUS)"
            ;;
    esac
}

# S24 Ultra SSH alias
alias s24='ssh -p 8022 192.168.1.185'

# Midnight Commander with remote filesystem mounting
mc() {
    if [ "$1" = "s24" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📱 MOUNTING S24 ULTRA FILESYSTEM..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        mkdir -p ~/mnt/s24
        
        echo "➤  ESTABLISHING SSHFS CONNECTION"
        if sshfs -p 8022 -o Ciphers=aes128-ctr,Compression=no 192.168.1.185:/storage/emulated/0 ~/mnt/s24 2>/dev/null; then
            echo "✓  FILESYSTEM MOUNTED AT ~/mnt/s24"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🗂  LAUNCHING MIDNIGHT COMMANDER"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            
            /usr/bin/mc ~/mnt/s24
            
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "⚡ UNMOUNTING S24 FILESYSTEM..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            
            fusermount -u ~/mnt/s24
            echo "✓  S24 FILESYSTEM UNMOUNTED"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        else
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "✗  FAILED TO MOUNT S24 FILESYSTEM"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        fi
        
    elif [ "$1" = "mainframe" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🖥  MOUNTING MAINFRAME FILESYSTEM..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        mkdir -p ~/mnt/mainframe
        
        echo "➤  ESTABLISHING SSHFS CONNECTION"
        if sshfs -o Ciphers=aes128-ctr,Compression=no mainframe.local:/ ~/mnt/mainframe 2>/dev/null; then
            echo "✓  FILESYSTEM MOUNTED AT ~/mnt/mainframe"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🗂  LAUNCHING MIDNIGHT COMMANDER"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            
            /usr/bin/mc ~/mnt/mainframe
            
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "⚡ UNMOUNTING MAINFRAME FILESYSTEM..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            
            fusermount -u ~/mnt/mainframe
            echo "✓  MAINFRAME FILESYSTEM UNMOUNTED"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        else
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "✗  FAILED TO MOUNT MAINFRAME FILESYSTEM"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        fi
        
    else
        /usr/bin/mc "$@"
    fi
}

######### AC CONTROL ##########

ac() {
    if [ "$1" = "control" ]; then
        python ~/scripts/ac-control.py
    else
        python ~/scripts/ac-control.py "$@"
    fi
}
