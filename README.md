Ansible Role: pve_ct_download
=========

This Ansible role is designed to manage and prepare environments for downloading container templates on Proxmox VE (PVE). It ensures the necessary dependencies are installed, variables are loaded, and the system is properly configured to execute related tasks.

```
    git clone https://github.com/lorephoenix/ansible-role-pve_ct_download pve_ct_download
```

Requirements
------------

- Ansible 2.11+.
- Proxmox VE with API access enabled.
- community.general collection for Proxmox integration.
- Python libraries for HTTP requests (requests) if not already installed.


Role Variables
--------------

The following variables can be customized to suit your environment. Default values are defined in `defaults/main.yml`

### Proxmox Connection Details

| Variable | Value | Data Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `pve_force`           | `false`               | Boolean  | Optional  | Force download if the template already exists.   |  
| `pve_host`            | `proxmox.example.com` | String   | Mandatory | Proxmox host address.                            |
| `pve_password `       | `*******`             | String   | Mandatory | Specify the password to authenticate with.       |
| `pve_port`            | `8006`                | Integer  | Optional  | Proxmox API port.                                |
| `pve_timeout`         | `500`                 | Integer  | Optional  | Timeout for template downloads.                  |
| `pve_tokenid`         | `root@pam!mytokenid`  | String   | Mandatory | API token ID for authentication.                 |
| `pve_token_secret `   | `*******`             | String   | Mandatory | API secret token                                 |
| `pve_validate_certs`  | `false`               | Boolean  | Optional  | Whether to validate SSL certificates.            |

If the variable `pve_password` is set, it takes precedence over the use of the `pve_token_secret` variable.

### Template items

| Variable        | Value                                        | Data Type     | Required  | Description                            |
| :---            | :---                                         | :---          | :---      | :---                                   |
| `pve_base_url`  | `http://download.proxmox.com/images/system/` | String        | Mandatory | Base URL to fetch container templates. |
| `pve_template`  | `debian`                                     | String or List| Mandatory | The OS package name to search for.     |


Dependencies
------------

This role makes use of the community.general collection, which is part of the Ansible package and includes many modules and plugins supported by Ansible community which are not part of more specialized community collections.

To install the collection:
```
    ansible-galaxy collection install -r requirements.yml
```


Example Playbook
----------------

Here’s an example of how to use this role:

```yaml
- name: (playbook) | Proxmox download latest CT image
  hosts: localhost
  vars_files:
    - vault.yml  # Load encrypted file with Proxmox token (pve_token_secret or pve_password)
  roles:
    - role: pve_ct_download
      vars:
        # Proxmox Connection Details
        pve_host: "pve1.example.com"
        pve_tokenid: "root@pam!Ansible"

        # Template items
        pve_template: 
          - "centos"
          - "ubuntu"
```

License
-------

MIT

Author Information
------------------

- Christophe Vermeren | [GitHub](https://github.com/lorephoenix) | [Facebook](https://www.facebook.com/cvermeren)
