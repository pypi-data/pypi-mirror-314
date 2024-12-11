
## Install Require

netbox version >= 4.0

## Known Issues

- WARNING: This plugin is only tested with a single NetBox version at this time.

## Installation Guide

### In mono service:

To install the plugin, first using pip and install netbox-k8s-cluster-info:

   ```
   cd /opt/netbox
   source venv/bin/activate
   pip install netbox-k8s-cluster-info
   ```

Next, enable the plugin in /opt/netbox/netbox/netbox/configuration.py, or if you have a /configuration/plugins.py file, the plugins.py file will take precedence.

   ```
   PLUGINS = [
      'netbox_k8s_cluster_info'
   ]
   ```
Then you may need to perform the final step of restarting the service to ensure that the changes take effect correctly:

   ```
   python netbox/manage.py migrate netbox_k8s_cluster_info
   sudo systemctl restart netbox
   ```
