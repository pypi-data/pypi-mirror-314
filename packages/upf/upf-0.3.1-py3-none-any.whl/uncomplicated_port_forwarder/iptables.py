# Copyright (C) 2024-2025 Bruno Bernard
# SPDX-License-Identifier: Apache-2.0

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models.port_forward import PortForward
    
def add_rule(port_forward: "PortForward") -> None:
    commands = [
        [
            "iptables", "-t", "nat", "-A", "PREROUTING",
            "-p", port_forward.protocol,
            "--dport", str(port_forward.host_port),
            "-j", "DNAT",
            "--to-destination", f"{port_forward.dest_ip}:{port_forward.dest_port}",
            "-m", "comment",
            "--comment", port_forward.rule_id,
        ],
        [
            "iptables", "-A", "FORWARD",
            "-p", port_forward.protocol,
            "-d", port_forward.dest_ip,
            "--dport", str(port_forward.dest_port),
            "-m", "state", "--state", "NEW,ESTABLISHED,RELATED",
            "-j", "ACCEPT",
            "-m", "comment",
            "--comment", port_forward.rule_id,
        ]
    ]
    
    for cmd in commands:
        subprocess.run(cmd, check=True)

def delete_rule(port_forward: "PortForward") -> None:
    commands = [
        [
            "iptables", "-t", "nat", "-D", "PREROUTING",
            "-p", port_forward.protocol,
            "--dport", str(port_forward.host_port),
            "-j", "DNAT",
            "--to-destination", f"{port_forward.dest_ip}:{port_forward.dest_port}",
            "-m", "comment",
            "--comment", port_forward.rule_id,
        ],
        [
            "iptables", "-D", "FORWARD",
            "-p", port_forward.protocol,
            "-d", port_forward.dest_ip,
            "--dport", str(port_forward.dest_port),
            "-m", "state", "--state", "NEW,ESTABLISHED,RELATED",
            "-j", "ACCEPT",
            "-m", "comment",
            "--comment", port_forward.rule_id,
        ]
    ]
    
    for cmd in commands:
        subprocess.run(cmd, check=True)
    commands = [
        [
            "iptables", "-t", "nat", "-D", "PREROUTING",
            "-p", port_forward.protocol,
            "--dport", str(port_forward.host_port),
            "-j", "DNAT",
            "--to-destination", f"{port_forward.dest_ip}:{port_forward.dest_port}",
            "-m", "comment",
            "--comment", port_forward.rule_id,
        ],
        [
            "iptables", "-t", "nat", "-D", "POSTROUTING",
            "-p", port_forward.protocol,
            "-d", port_forward.dest_ip,
            "--dport", str(port_forward.dest_port),
            "-j", "MASQUERADE",
            "-m", "comment",
            "--comment", port_forward.rule_id,
        ],
    ]
    for cmd in commands:
        subprocess.run(cmd, check=True)