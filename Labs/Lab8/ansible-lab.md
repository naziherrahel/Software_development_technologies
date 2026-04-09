# Lab: Automating Multiple Servers with Ansible

## Objective

In this lab, you will use Ansible to configure:

- two web servers: `web-1` and `web-2`
- one load balancer: `lb-1`

At the end of the lab, `lb-1` will distribute HTTP requests between the two web servers.

## What You Will Learn

- how to prepare a control node for Ansible
- how to connect to multiple servers over SSH
- how to write a simple Ansible inventory
- how to automate web server configuration with Ansible
- how to configure Nginx as a load balancer

## Topology

```text
Client Browser
      |
      v
    lb-1
   /    \
  v      v
web-1  web-2
```

## Before You Start

- Read each step in order.
- Do not skip steps.
- If something fails, fix it before moving on.
- Replace all placeholders such as `<web-1-ip>` with your real values.

You will need:

- access to Yandex Cloud
- one SSH key pair
- three Ubuntu 24 virtual machines
- a control node with Ansible installed

Important:

- If you are on Windows, only the WSL installation commands are run in PowerShell.
- After Ubuntu opens successfully, all remaining Linux commands in this lab must be run inside Ubuntu.

---

## Step 0. Prepare Your Environment

### Option A. Windows + WSL2 + Ubuntu 24.04

Before installing WSL, make sure:

1. You are using Windows 10 21H2 or newer, or Windows 11.
2. Virtualization is enabled in BIOS/UEFI.
3. Drive `C:` has at least `10 GB` free space. `15 GB` is recommended.

Open **PowerShell as Administrator** and run:

```powershell
wsl --update
wsl --install -d Ubuntu-24.04
```

If Windows asks you to restart, restart your computer.

After restart:

1. Open `Ubuntu 24.04 LTS`.
2. Create your Linux username and password when prompted.

Before installing Ansible, verify that Ubuntu created a normal Linux user correctly:

```bash
whoami
cd ~
pwd
sudo -v
```

Expected result:

- `whoami` shows your Linux username, not `root`
- `pwd` shows a home directory like `/home/<your-user>`
- `sudo -v` asks for your password once and then returns without an error

Important:

- When you type your Linux password, nothing appears on screen. This is normal.
- Use the password you created during Ubuntu's first start, not your Windows password.

Then, inside the Ubuntu terminal, install Ansible:

```bash
sudo apt update
sudo apt install ansible -y
ansible --version
```

Notes:

- If WSL opens in a path like `/mnt/c/Users/...`, that is usually normal.
- Run `cd ~` to go to your Linux home directory.
- Do not assume `/mnt/c/...` means WSL is broken.

If Ubuntu opens as `root`, or `sudo` keeps rejecting the password:

1. Close Ubuntu.
2. In PowerShell, run:

```powershell
wsl --shutdown
```

3. Open Ubuntu again and check whether it asks you to create a username and password.

If it still opens as `root`, create a user manually from PowerShell:

```powershell
wsl -d Ubuntu-24.04 -u root -- adduser student
wsl -d Ubuntu-24.04 -u root -- usermod -aG sudo student
wsl --manage Ubuntu-24.04 --set-default-user student
```

Then open Ubuntu again and verify:

```bash
whoami
sudo -v
```

If WSL installation fails:

1. Free space on drive `C:` until at least `10 GB` is available.
2. Run:

```powershell
wsl --shutdown
wsl --list --online
wsl -l -v
```

3. Install Ubuntu again:

```powershell
wsl --install --web-download -d Ubuntu-24.04
```

4. Only if you see a broken partial Ubuntu entry, remove that exact distro name and install again:

```powershell
wsl --unregister Ubuntu-24.04
wsl --install --web-download -d Ubuntu-24.04
```

Important:

- `wsl --unregister` permanently deletes that distro's data.
- Use it only for a broken install that you are ready to recreate.

### Option B. Linux

Run:

```bash
sudo apt update
sudo apt install ansible -y
ansible --version
```

### Option C. WSL Does Not Work

Create one extra Ubuntu VM in Yandex Cloud and use it as your Ansible control node.

Then run:

```bash
sudo apt update
sudo apt install ansible -y
ansible --version
```

---

## Step 1. Create Virtual Machines

Create three Ubuntu 24 virtual machines in Yandex Cloud:

- `web-1`
- `web-2`
- `lb-1`

When creating the VMs:

- attach the same SSH public key to all three VMs
- make sure each VM has a public IP address
- place them in a network where they can reach each other

Record the public IP addresses in a table like this:

```text
web-1  -> <web-1-ip>
web-2  -> <web-2-ip>
lb-1   -> <lb-1-ip>
```

---

## Step 2. Test SSH Access

From your control node, test SSH access to each server:

```bash
ssh ubuntu@<web-1-ip>
ssh ubuntu@<web-2-ip>
ssh ubuntu@<lb-1-ip>
```

If SSH asks whether you trust the host, type `yes`.

If SSH does not work, stop here and fix it before continuing.

Check the following:

- the VM is running
- the public IP address is correct
- the security group is attached
- you are using the same private key that matches the public key added to the VMs

Rule to remember:

If you can SSH to a server from the control node, Ansible can usually connect to it too.

---

## Step 3. Create the Project Folder

Run:

```bash
mkdir -p ~/ansible-lab
cd ~/ansible-lab
touch inventory.ini web.yml lb.yml
```

---

## Step 4. Create the Inventory File

Open `inventory.ini` and add:

```ini
[web]
web-1 ansible_host=<web-1-ip>
web-2 ansible_host=<web-2-ip>

[lb]
lb-1 ansible_host=<lb-1-ip>

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
```

Important:

- If your private key file is not `~/.ssh/id_rsa`, replace it with the correct path.
- For example, many students use `~/.ssh/id_ed25519`.

---

## Step 5. Test the Ansible Connection

Run:

```bash
ansible -i inventory.ini all -m ping
```

Expected result:

- all three hosts should return `SUCCESS`

If this fails:

- check SSH again
- check the private key path in `inventory.ini`
- check the IP addresses

---

## Step 6. Configure the Web Servers

Open `web.yml` and add:

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Create custom page
      copy:
        content: "<h1>Hello from {{ inventory_hostname }}</h1>"
        dest: /var/www/html/index.html
        mode: "0644"

    - name: Ensure nginx is running
      service:
        name: nginx
        state: restarted
        enabled: true
```

---

## Step 7. Run the Web Server Playbook

Run:

```bash
ansible-playbook -i inventory.ini web.yml
```

When the playbook finishes, both web servers should have:

- Nginx installed
- a custom HTML page
- the Nginx service running

You can verify manually:

```bash
curl http://<web-1-ip>
curl http://<web-2-ip>
```

Expected output:

- `Hello from web-1`
- `Hello from web-2`

---

## Step 8. Configure the Load Balancer

Open `lb.yml` and add:

```yaml
---
- name: Configure load balancer
  hosts: lb
  become: true

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Configure nginx as load balancer
      copy:
        dest: /etc/nginx/sites-available/default
        mode: "0644"
        content: |
          upstream backend {
              server <web-1-ip>;
              server <web-2-ip>;
          }

          server {
              listen 80;
              server_name _;

              location / {
                  proxy_pass http://backend;
                  proxy_set_header Host $host;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                  proxy_set_header X-Forwarded-Proto $scheme;
              }
          }

    - name: Validate nginx configuration
      command: nginx -t
      changed_when: false

    - name: Ensure nginx is running
      service:
        name: nginx
        state: restarted
        enabled: true
```

Important:

- Replace `<web-1-ip>` and `<web-2-ip>` with the real IP addresses of your web servers before saving the file.

---

## Step 9. Run the Load Balancer Playbook

Run:

```bash
ansible-playbook -i inventory.ini lb.yml
```

If `nginx -t` fails, read the error carefully and fix the configuration before running the playbook again.

---

## Step 10. Verify the Result

Open the load balancer in your browser:

```text
http://<lb-1-ip>
```

Refresh the page several times.

You should see responses from both servers over time.

Expected result:

- some responses should say `Hello from web-1`
- some responses should say `Hello from web-2`

---

## Troubleshooting Checklist

If something does not work, check the following in this order:

1. SSH works from the control node to every target server.
2. IP addresses in `inventory.ini` are correct.
3. The private key path in `inventory.ini` is correct.
4. The security group is attached to all VMs.
5. The playbook YAML indentation is correct.
6. The load balancer config contains the correct web server IP addresses.

Useful commands:

```bash
ansible -i inventory.ini all -m ping
ansible -i inventory.ini all -a "hostname"
ansible -i inventory.ini web -a "curl -s http://localhost"
ansible -i inventory.ini lb -b -a "nginx -t"
```

---

## Final Rule to Remember

If you can SSH to the servers without problems, Ansible will usually work too.
