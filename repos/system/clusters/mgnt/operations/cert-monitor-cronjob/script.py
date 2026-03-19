import ssl
import socket
from datetime import datetime

from crossplane.function import request, response


def operate(req, rsp):
    # Get config from the operation input
    config = request.get_input(req)
    warning_days = config.get("warningThresholdDays", 30)

    # Get the watched Ingress resource
    ingress = request.get_required_resource(req, "ingress")
    if not ingress:
        response.set_output(rsp, {"error": "No ingress resource found"})
        return

    # Extract hostname from Ingress rules
    hostname = ingress["spec"]["rules"][0]["host"]
    port = 443

    # Fetch SSL certificate info
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    # Parse expiration date
    expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    days_until_expiry = (expiry_date - datetime.now()).days

    # Emit a warning if the certificate is expiring soon
    if days_until_expiry < warning_days:
        response.warning(
            rsp,
            f"Certificate for {hostname} expires in {days_until_expiry} days "
            f"(threshold: {warning_days})"
        )

    # Annotate the Ingress with expiry metadata
    rsp.desired.resources["ingress"].resource.update({
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": ingress["metadata"]["name"],
            "namespace": ingress["metadata"]["namespace"],
            "annotations": {
                "cert-monitor.crossplane.io/expires": cert["notAfter"],
                "cert-monitor.crossplane.io/days-until-expiry": str(days_until_expiry),
                "cert-monitor.crossplane.io/status": (
                    "warning" if days_until_expiry < warning_days else "ok"
                ),
            },
        },
    })

    response.set_output(rsp, {
        "hostname": hostname,
        "certificateExpires": cert["notAfter"],
        "daysUntilExpiry": days_until_expiry,
        "status": "warning" if days_until_expiry < warning_days else "ok",
    })
