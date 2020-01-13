# Configure Access to Muaddib

## Configure SSH access at Sicara

- Ask Antoine or Laurent to add your public RSA `{YOUR_RSA_KEY.pub}` key to Muaddib
- Ask Antoine or Laurent the Muaddib password
- On your machine, add muaddib in your `/etc/hosts` configuration:
  ```
  10.20.200.125 muaddib
  ```
- On your machine, edit the `~/.ssh/config` file to add the Muaddib configuration:
  ```
  Host muaddib
      hostname muaddib
      port 22
      IdentityFile ~/.ssh/{YOUR_RSA_KEY}
      User muaddib
  ```
- Connect to Muaddib using `ssh muaddib`.
- Load Polyaxon dashboard in your browser at `muaddib:32116`
  

## Access to Muaddib from outside Sicara

- Get the public IP from where you want to connect, by loading [Whatismyip](https://www.whatismyip.com/) on your chosen
network
- Andon AntoineT or RaphaelM to add it to the authorized IPs
- On your machine, add muaddib in your `/etc/hosts` configuration:
  ```
  88.190.212.196 muaddib-home
  ```
- Add the following config to your `~/.ssh/config`:
    ```
    Host muaddib-home
        hostname muaddib-home
        port 20022
        User muaddib
    ```
- Connect to Muaddib using `ssh muaddib-home`.
- Load Polyaxon dashboard at `muaddib-home:32116`
