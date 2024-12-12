# mach-client-py

A (mostly) strongly typed Python client for the Mach exchange, including multichain abstractions for interacting with each network.

## Getting Started

Create a copy of the `template.config.yaml` file:

```bash
cp template.config.yaml config.yaml
```

Edit the config to add the credentials for the account you wish to run the example with:

```yaml
accounts:
  ethereum: "YOUR PRIVATE KEY"
  solana: "..."
  tron: "..."
# ...
```

Then look at the notebook in the `examples/` directory.
