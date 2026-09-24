#/bin/bash

replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

cp /etc/sysctl.conf backups/sysctl.conf.bak

replace_command "net.ipv4.conf.all.rp_filter" "net.ipv4.conf.all.rp_filter = 1" /etc/sysctl.conf
replace_command "net.ipv4.conf.default.rp_filter" "net.ipv4.conf.default.rp_filter = 1" /etc/sysctl.conf
replace_command "net.ipv4.icmp_echo_ignore_broadcasts" "net.ipv4.icmp_echo_ignore_broadcasts = 1" /etc/sysctl.conf

replace_command "net.ipv4.conf.all.accept_source_route" "net.ipv4.conf.all.accept_source_route = 0" /etc/sysctl.conf
replace_command "net.ipv6.conf.all.accept_source_route" "net.ipv6.conf.all.accept_source_route = 0" /etc/sysctl.conf
replace_command "net.ipv4.conf.default.accept_source_route" "net.ipv4.conf.default.accept_source_route = 0" /etc/sysctl.conf
replace_command "net.ipv6.conf.default.accept_source_route" "net.ipv6.conf.default.accept_source_route = 0" /etc/sysctl.conf

replace_command "net.ipv4.conf.all.send_redirects" "net.ipv4.conf.all.send_redirects = 0" /etc/sysctl.conf
replace_command "net.ipv4.conf.default.send_redirects" "net.ipv4.conf.default.send_redirects = 0" /etc/sysctl.conf

replace_command "net.ipv4.tcp_syncookies" "net.ipv4.tcp_syncookies = 1" /etc/sysctl.conf
replace_command "net.ipv4.tcp_max_syn_backlog" "net.ipv4.tcp_max_syn_backlog = 2048" /etc/sysctl.conf
replace_command "net.ipv4.tcp_synack_retries" "net.ipv4.tcp_synack_retries = 2" /etc/sysctl.conf
replace_command "net.ipv4.tcp_syn_retries" "net.ipv4.tcp_syn_retries = 5" /etc/sysctl.conf

replace_command "net.ipv4.ip_forward" "net.ipv4.ip_forward = 0" /etc/sysctl.conf

replace_command "net.ipv4.conf.all.log_martians" "net.ipv4.conf.all.log_martians = 1" /etc/sysctl.conf
replace_command "net.ipv4.icmp_ignore_bogus_error_responses" "net.ipv4.icmp_ignore_bogus_error_responses = 1" /etc/sysctl.conf

replace_command "net.ipv4.conf.all.accept_redirects" "net.ipv4.conf.all.accept_redirects = 0" /etc/sysctl.conf
replace_command "net.ipv6.conf.all.accept_redirects" "net.ipv6.conf.all.accept_redirects = 0" /etc/sysctl.conf
replace_command "net.ipv4.conf.default.accept_redirects" "net.ipv4.conf.default.accept_redirects = 0" /etc/sysctl.conf
replace_command "net.ipv6.conf.default.accept_redirects" "net.ipv6.conf.default.accept_redirects = 0" /etc/sysctl.conf

replace_command "net.ipv4.icmp_echo_ignore_all" "net.ipv4.icmp_echo_ignore_all = 1" /etc/sysctl.conf

sysctl --system
