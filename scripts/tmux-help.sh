#!/bin/bash

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
RESET='\033[0m'
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}"
cat << 'EOF'
╭─────────────────────────────────────────────────────────────╮
│                    TMUX CHEAT SHEET                         │
│                     Prefix: Ctrl-b                          │
╰─────────────────────────────────────────────────────────────╯
EOF
echo -e "${RESET}"

echo -e "${GREEN}╭─────────────────────────────────────────────────────────────╮"
echo -e "│ ${BOLD}SESSIONS${RESET}${GREEN}                                                    │"
echo -e "├─────────────────────────────────────────────────────────────┤${RESET}"
echo -e "${GREEN}│${RESET} ${YELLOW}d${RESET}       Detach from session                              ${GREEN}${RESET}"
echo -e "${GREEN}│${RESET} ${YELLOW}s${RESET}       List/switch sessions                             ${GREEN}${RESET}"
echo -e "${GREEN}│${RESET} ${YELLOW}\$${RESET}       Rename current session                          ${GREEN}${RESET}"
echo -e "${GREEN}╰─────────────────────────────────────────────────────────────╯${RESET}"
echo ""

echo -e "${BLUE}╭─────────────────────────────────────────────────────────────╮"
echo -e "│ ${BOLD}WINDOWS (tabs)${RESET}${BLUE}                                              │"
echo -e "├─────────────────────────────────────────────────────────────┤${RESET}"
echo -e "${BLUE}│${RESET} ${YELLOW}c${RESET}       Create new window                                 ${BLUE}${RESET}"
echo -e "${BLUE}│${RESET} ${YELLOW},${RESET}       Rename current window                             ${BLUE}${RESET}"
echo -e "${BLUE}│${RESET} ${YELLOW}n / p${RESET}   Next / Previous window                            ${BLUE}${RESET}"
echo -e "${BLUE}│${RESET} ${YELLOW}0-9${RESET}     Switch to window by number                        ${BLUE}${RESET}"
echo -e "${BLUE}│${RESET} ${YELLOW}w${RESET}       List all windows                                  ${BLUE}${RESET}"
echo -e "${BLUE}│${RESET} ${YELLOW}&${RESET}       Kill current window                               ${BLUE}${RESET}"
echo -e "${BLUE}╰─────────────────────────────────────────────────────────────╯${RESET}"
echo ""

echo -e "${MAGENTA}╭─────────────────────────────────────────────────────────────╮"
echo -e "│ ${BOLD}PANES (splits)${RESET}${MAGENTA}                                              │"
echo -e "├─────────────────────────────────────────────────────────────┤${RESET}"
echo -e "${MAGENTA}│${RESET} ${YELLOW}%${RESET}       Split vertically (left/right)                    ${MAGENTA}${RESET}"
echo -e "${MAGENTA}│${RESET} ${YELLOW}\"${RESET}       Split horizontally (top/bottom)                 ${MAGENTA}${RESET}"
echo -e "${MAGENTA}│${RESET} ${YELLOW}arrows${RESET}  Navigate between panes                           ${MAGENTA}${RESET}"
echo -e "${MAGENTA}│${RESET} ${YELLOW}o${RESET}       Cycle through panes                              ${MAGENTA}${RESET}"
echo -e "${MAGENTA}│${RESET} ${YELLOW}z${RESET}       Zoom/unzoom pane (fullscreen toggle)             ${MAGENTA}${RESET}"
echo -e "${MAGENTA}│${RESET} ${YELLOW}x${RESET}       Kill current pane                                ${MAGENTA}${RESET}"
echo -e "${MAGENTA}│${RESET} ${YELLOW}{ / }${RESET}   Swap pane positions                              ${MAGENTA}${RESET}"
echo -e "${MAGENTA}╰─────────────────────────────────────────────────────────────╯${RESET}"
echo ""

echo -e "${CYAN}╭─────────────────────────────────────────────────────────────╮"
echo -e "│ ${BOLD}OTHER COMMANDS${RESET}${CYAN}                                              │"
echo -e "├─────────────────────────────────────────────────────────────┤${RESET}"
echo -e "${CYAN}│${RESET} ${YELLOW}?${RESET}       Show all keybindings                              ${CYAN}${RESET}"
echo -e "${CYAN}│${RESET} ${YELLOW}[${RESET}       Enter scroll/copy mode (q to quit)                ${CYAN}${RESET}"
echo -e "${CYAN}│${RESET} ${YELLOW}:${RESET}       Enter command mode                                ${CYAN}${RESET}"
echo -e "${CYAN}╰─────────────────────────────────────────────────────────────╯${RESET}"
echo ""

echo -e "${GREEN}${BOLD}Command Line (outside tmux):${RESET}"
echo -e "  ${YELLOW}tmux${RESET}                       Start new session"
echo -e "  ${YELLOW}tmux ls${RESET}                    List sessions"
echo -e "  ${YELLOW}tmux attach -t <name>${RESET}      Attach to session"
echo -e "  ${YELLOW}tmux kill-session -t <name>${RESET} Kill session"
echo ""
