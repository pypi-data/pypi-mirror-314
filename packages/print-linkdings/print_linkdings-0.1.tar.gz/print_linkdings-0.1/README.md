# print-linkdings

This program sends API requests to the REST API of a Linkding instance on my Tailscale network, gathers the URLs from each unarchived bookmark, gathers URLs one hop away from each bookmark URL, and prints them to standard output.

The Linkding API key must be stored in a plaintext file at `/usr/local/etc/linkding_api_key.txt`.

## Installation

``` shell
pipx install print-linkdings
```

## Usage

``` shell
print-linkdings INSTANCE_URL
```

Example:

``` shell
print-linkdings "https://nas-local.tailnet.ts.net:7000"
```

