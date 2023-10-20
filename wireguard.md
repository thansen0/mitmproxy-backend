# Set up WireGuard

Wireguard should allow for better battery health and easier implementation, as it exists as a network device all traffic is routed through.

## Linux server setup

To generate the private key in the current directory (has to be done on both client and server)

```
sudo apt instal wireguard
wg genkey | tee privatekey | wg pubkey > publickey
```

Then we have to create a config file `/etc/wireguard/wg0.conf` which will name our interface wg0, and write our configuration info

Note: address range must be unique or we'll get routing issues

```
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = (server_private_key)

# Add client configurations below
SaveConfig=true
PostUp=iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o enp1s0 -j MASQUERADE
PostUp=iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o enp1s0 -j MASQUERADE
```

We can start it with systemctl using the commands

```
# sudo systemctl enable wg-quick@wg0 # unsure if we want to use this??
# sudo systemctl start wg-quick@wg0
wg-quick up wg0
```

And we can view wg and see the interface by running 

```
sudo wg
ip link
```

### Housekeeping for server

We can add users to the server while running with the command

```
sudo wg set wg0 peer <public key> allow-ip
```


# Windows Client

I'm not sure how to generate this on windows, so I just created it on the server and copied it over

```
wg genkey | tee privatekey | wg pubkey > publickey
```

Here's the conf file to add it to

```
[Interface]
Address = 10.0.0.2/24
ListenPort = 51820
PrivateKey = (client_private_key)

[Peer]
PublicKey = (server_public_key)
Endpoint = (server IP addr):51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 30
```
NOTE: I found I can have DNS issues if I don't allow 8.8.8.8 on the client (or another DNS server).

Then I add the client to the server by running this on the server

```
sudo wg set wg0 peer <client public key> allowed-ips 10.0.0.2/24
```

Where allowed-ips is the mask for the client I think, although I'm not certain it's required.

From there I click "Add Tunnel", "Add empty tunnel", and then copy in the conf file. It generates the public key automatically from the private key which is nifty.


TODO currently having issues where it's not forwarding out (or recieving) data from public IP addresses other than the server it's connecting to. But I know it's connecting to my server because when I ping it from the client, I can see the ping messages on the server by running `sudo tcpdump -envi wg0 host 45.76.232.143`





# Trouble shooting

The following value should always be one, enabling forwarding. 

cat /proc/sys/net/ipv4/ip_forward

If it's not, we can set it to one using the command

sudo sysctl -w net.ipv4.ip_forward=1




# Setup stuff I did 

After having trouble accessing public IP's, I tried a few things.

 - I went in /etc/sysctl.conf and uncommented the net.ipv4.ip_forward=1 line
   - Apply change by running "sudo sysctl -p"
 - Good site https://linuxiac.com/how-to-set-up-wireguard-vpn-server-on-ubuntu/hhKbdToNQ7LQbuJ249d/rN9S5rrsB+4cLz223Lxk2G8=
