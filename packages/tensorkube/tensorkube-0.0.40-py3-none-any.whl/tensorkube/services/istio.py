import platform
import subprocess
import os
import click
from kubernetes import config, client

from tensorkube.configurations.configuration_urls import DOMAIN_SERVER_URL, KNATIVE_ISTIO_CONTROLLER_URL
from tensorkube.services.eks_service import get_pods_using_namespace, apply_yaml_from_url, delete_resources_from_url
from tensorkube.services.k8s_service import get_tensorkube_cluster_context_name


def check_and_install_istioctl():
    """Check if istioctl is installed and install it if it's not."""
    try:
        subprocess.run(["istioctl", "version"], check=True)
        print("istioctl is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("istioctl is not installed. Proceeding with installation.")
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "istioctl"], check=True)
            except subprocess.CalledProcessError as e:
                print("Unable to install istioctl using Homebrew. Please install istioctl manually.")
                raise e
        elif platform.system() == "Linux":
            try:
                install_command = "curl -sL https://istio.io/downloadIstioctl | sh -"
                # Download and install istioctl
                subprocess.run(install_command, shell=True,
                               check=True)

                # Add istioctl to PATH
                istioctl_path = os.path.expanduser("~/.istioctl/bin")
                if istioctl_path not in os.environ["PATH"]:
                    os.environ["PATH"] += os.pathsep + istioctl_path
                    # Optionally, you can add this path to .bashrc or .bash_profile to make it permanent
                    with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
                        bashrc.write(f'\nexport PATH="$HOME/.istioctl/bin:$PATH"\n')

                print("istioctl installed successfully and PATH updated.")
            except subprocess.CalledProcessError as e:
                print("Unable to install istioctl using curl. Please install istioctl manually.")
                raise e
        else:
            print("Unsupported operating system. Please install istioctl manually.")
            raise Exception('Unsupported operating system.')

        # Verify istioctl installation
        try:
            subprocess.run(["istioctl", "version"], check=True)
            print("istioctl installed successfully.")
        except subprocess.CalledProcessError as e:
            print("istioctl installation failed. Please install istioctl manually.")
            raise e


def install_istio_on_cluster():
    """Install Istio with the default profile."""
    try:
        subprocess.run(["istioctl", "install", "--set", "profile=default", "-y"])
        print("Istio installed successfully.")
    except Exception as e:
        print(f"Error installing Istio: {e}")
        raise e
    # finally using the kubeconfi
    pods = get_pods_using_namespace("istio-system")
    for pod in pods.items:
        click.echo(f"Pod name: {pod.metadata.name}, Pod status: {pod.status.phase}")


def remove_domain_server():
    delete_resources_from_url(DOMAIN_SERVER_URL, "removing Knative Default Domain")


def uninstall_istio_from_cluster():
    """Uninstall Istio from the cluster."""
    # remove knative istion controller
    delete_resources_from_url(KNATIVE_ISTIO_CONTROLLER_URL, "uninstalling Knative Net Istio")
    # remove istio
    try:
        subprocess.run(["istioctl", "x", "uninstall", "--purge", "-y"])
        click.echo("Istio uninstalled successfully.")
    except Exception as e:
        click.echo(f"Error uninstalling Istio: {e}")


def install_net_istio():
    apply_yaml_from_url(KNATIVE_ISTIO_CONTROLLER_URL, "installing Knative Net Istio")


def install_default_domain():
    apply_yaml_from_url(DOMAIN_SERVER_URL, "installing Knative Default Domain")


def configure_ssl_for_ingress_gateway(certificate_arn: str, ssl_ports: str = "443") -> bool:
    """
    Configure SSL certificate for istio-ingressgateway service
    Args:
        certificate_arn: ACM certificate ARN
        ssl_ports: Comma-separated list of SSL ports (default: "443")
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load kubernetes config
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return False
        api_client = config.new_client_from_config(context=context_name)
        v1 = client.CoreV1Api(api_client)

        # Get existing service
        service = v1.read_namespaced_service(
            name='istio-ingressgateway',
            namespace='istio-system'
        )

        # Prepare annotations
        if not service.metadata.annotations:
            service.metadata.annotations = {}

        service.metadata.annotations.update({
            'service.beta.kubernetes.io/aws-load-balancer-ssl-cert': certificate_arn,
            'service.beta.kubernetes.io/aws-load-balancer-ssl-ports': ssl_ports,
            'service.beta.kubernetes.io/aws-load-balancer-backend-protocol': "http"
        })

        # Update service
        v1.patch_namespaced_service(
            name='istio-ingressgateway',
            namespace='istio-system',
            body=service
        )

        return True

    except client.exceptions.ApiException as e:
        click.echo(f"Failed to configure SSL: {str(e)}")
        return False
    except Exception as e:
        click.echo(f"Unexpected error configuring SSL: {str(e)}")
        return False

def configure_443_port_for_gateway() -> bool:
    """
    Add port 443 support to knative-ingress-gateway
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load kubernetes config
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return False
        api_client = config.new_client_from_config(context=context_name)
        custom_api = client.CustomObjectsApi(api_client)

        # Get existing gateway
        gateway = custom_api.get_namespaced_custom_object(
            group="networking.istio.io",
            version="v1",
            namespace="knative-serving",
            plural="gateways",
            name="knative-ingress-gateway"
        )

        # Check if 443 port is already configured
        for server in gateway['spec']['servers']:
            if server.get('port', {}).get('number') == 443:
                click.echo("Port 443 already configured in gateway")
                return True

        # Add new server for port 443
        gateway['spec']['servers'].append({
            'hosts': ['*'],
            'port': {
                'name': 'http-443',
                'number': 443,
                'protocol': 'HTTP'
            }
        })

        # Patch gateway
        custom_api.patch_namespaced_custom_object(
            group="networking.istio.io",
            version="v1",
            namespace="knative-serving",
            plural="gateways",
            name="knative-ingress-gateway",
            body=gateway
        )

        click.echo("Successfully added port 443 to gateway")
        return True

    except client.exceptions.ApiException as e:
        click.echo(f"Failed to configure gateway: {str(e)}")
        return False
    except Exception as e:
        click.echo(f"Unexpected error configuring gateway: {str(e)}")
        return False
