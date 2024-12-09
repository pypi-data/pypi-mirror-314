from pathlib import Path


SERVICES = {x.stem: x.resolve().as_posix() for x in Path('./ressources').glob("**/*.wsdl")}

def wsdl(service_name: str) -> str:
    """Return path to WSDL file for `service_name`."""
    try:
        return SERVICES[service_name]
    except KeyError:
        raise KeyError(
            "Unknown service name {!r}, available services are {}".format(
                service_name,
                ", ".join(sorted(SERVICES)),
            ),
        ) from None


