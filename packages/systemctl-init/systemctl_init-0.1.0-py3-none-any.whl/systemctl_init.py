import os
import sys
from dataclasses import dataclass
import argparse

# 定义模板
TEMPLATE = """[Unit]
Description={description}
{unit_dependencies}

[Service]
ExecStart={exec_command}
Restart={restart_policy}
{working_directory}
{environment_vars}
{logging}
{chroot_dir}

[Install]
WantedBy=multi-user.target
"""

@dataclass
class ServiceConfig:
    exec_command: str
    description: str = None
    restart_policy: str = "no"
    working_dir: str = None
    environment: list = None
    require_network: bool = False
    dependencies: list = None
    log: str = "journal"
    chroot_dir: str = None
    output_path: str = ""

    def generate_unit_dependencies(self):
        dependencies = []
        if self.require_network:
            dependencies.append("Requires=network-online.target")
            dependencies.append("After=network-online.target")
        if self.dependencies:
            dependencies.extend([f"Requires={dep}" for dep in self.dependencies])
        return "\n".join(dependencies)

    def generate_environment_vars(self):
        if self.environment:
            return "\n".join([f"Environment={env}" for env in self.environment])
        return ""

    def generate_logging(self):
        if self.log == "journal":
            return "StandardOutput=journal\nStandardError=journal"
        elif self.log == "syslog":
            return "StandardOutput=syslog\nStandardError=syslog"
        else:
            return f"StandardOutput=file:{self.log}\nStandardError=file:{self.log}"

    def generate_template(self):
        return TEMPLATE.format(
            description=self.description or f"{self.exec_command.split(' ')[0].split('/')[-1].upper()} Service",
            exec_command=self.exec_command,
            restart_policy=self.restart_policy,
            working_directory=f"WorkingDirectory={self.working_dir}" if self.working_dir else "",
            environment_vars=self.generate_environment_vars(),
            logging=self.generate_logging(),
            chroot_dir=f"RootDirectory={self.chroot_dir}" if self.chroot_dir else "",
            unit_dependencies=self.generate_unit_dependencies(),
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate a systemd service file easily."
    )
    parser.add_argument("--exec", required=True, help="Command to execute for the service.")
    parser.add_argument("--description", help="Description of the service.")
    parser.add_argument("--restart", default="no", help="Restart policy (default: no).")
    parser.add_argument("--working-dir", help="Working directory for the service.")
    parser.add_argument("--env", nargs="+", help="Environment variables (e.g., KEY=VALUE).")
    parser.add_argument("--require-network", action="store_true", help="Add network-online.target dependencies.")
    parser.add_argument("--dependencies", nargs="+", help="Additional service dependencies.")
    parser.add_argument("--log", default="journal", help="Logging target (journal, syslog, or file path).")
    parser.add_argument("--chroot", help="Chroot directory for service isolation.")
    parser.add_argument("--output", default="", help="Path to save the service file.")
    return parser.parse_args()


def write_service_file(config: ServiceConfig):
    content = config.generate_template()
    if not config.output_path:
        config.output_path = f"{config.exec_command.split(' ')[0].split('/')[-1]}.service"
    with open(config.output_path, "w") as f:
        f.write(content)
    print(f"Service file created at {config.output_path}")
    print("To enable and start the service:")
    print(f"sudo mv {config.output_path} /etc/systemd/system/")
    print("sudo systemctl daemon-reload")
    print(f"sudo systemctl enable {os.path.basename(config.output_path)}")
    print(f"sudo systemctl start {os.path.basename(config.output_path)}")


def main():
    args = parse_arguments()
    config = ServiceConfig(
        exec_command=args.exec,
        description=args.description,
        restart_policy=args.restart,
        working_dir=args.working_dir,
        environment=args.env,
        require_network=args.require_network,
        dependencies=args.dependencies,
        log=args.log,
        chroot_dir=args.chroot,
        output_path=args.output,
    )
    write_service_file(config)


if __name__ == "__main__":
    main()
