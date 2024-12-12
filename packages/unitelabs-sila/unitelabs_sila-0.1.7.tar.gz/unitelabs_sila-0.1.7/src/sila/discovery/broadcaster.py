from __future__ import annotations

import asyncio
import ipaddress
import logging
import socket
import typing

import zeroconf

if typing.TYPE_CHECKING:
    from sila.server import Server


class Broadcaster:
    """
    Promotes the provided server on the network.

    In order to provide a true zero-configuration experience, this implements multicast DNS (mDNS) and DNS-based Service
    Discovery (DNS-SD). It broadcasts the socket address on which the grpc server is available, some metadata about the
    server and optionally the server certificate.

    Parameters:
        server: The server to promote on the network.
    """

    def __init__(self, server: Server):
        properties = {
            "version": server.version.encode("utf-8")[:247],
            "server_name": server.name.encode("utf-8")[:243],
            "description": server.description.encode("utf-8")[:243],
        }

        if server.certificate:
            certificate = server.certificate[1]
            properties.update({f"ca{i}": line for i, line in enumerate(certificate.splitlines(keepends=False))})

        self.mdns = zeroconf.Zeroconf()
        self.service = zeroconf.ServiceInfo(
            type_="_sila._tcp.local.",
            name=f"{server.uuid}._sila._tcp.local.",
            parsed_addresses=[find_ip_address(server.host)],
            port=int(server.port),
            properties=properties,
        )

    async def start(self):
        """Starts the broadcasting."""
        self.logger.info("Starting broadcaster...")

        try:
            await self.mdns.async_register_service(self.service)
            while True:
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            await self.stop()

    async def stop(self):
        """Stops this broadcasting."""
        self.logger.info("Stopping broadcaster...")
        await self.mdns.async_unregister_all_services()
        self.mdns.close()

    @property
    def logger(self) -> logging.Logger:
        """A standard Python :class:`~logging.Logger` for the app."""
        return logging.getLogger(__package__)


def find_ip_address(address: str) -> str:
    """
    Returns a valid ip address for a given hostname or address.

    Parameters:
        address: A hostname or address, e.g. `localhost` or `0.0.0.0`.

    Returns:
        A valid ip address that represents the given address.
    """
    if address == "0.0.0.0":
        ip_address = "127.0.0.1"
        try:
            ip_address = socket.gethostbyname(socket.gethostname())
        except OSError:
            pass

        if ip_address == "127.0.0.1":
            connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            connection.settimeout(0)
            try:
                connection.connect(("8.8.8.8", 80))
            except OSError:
                pass
            ip_address = next(iter(connection.getsockname()), ip_address)

        return ip_address

    try:
        return ipaddress.ip_address(address).exploded
    except ValueError:
        try:
            return socket.gethostbyname(address)
        except OSError:
            return "127.0.0.1"
