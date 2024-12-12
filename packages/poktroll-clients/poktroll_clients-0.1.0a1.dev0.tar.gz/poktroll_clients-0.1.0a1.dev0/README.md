# Poktroll-clients-py

Python bindings to the [`poktroll` client packages](https://pkg.go.dev/github.com/pokt-network/poktroll@v0.0.10/pkg/client).

## Start poktroll localnet
```bash
git clone https://github.com/pokt-network/poktroll
cd poktroll

# Start poktroll localnet
make localnet_up
```

## Build and install `libpoktroll_clients` shared library & headers
```bash
git clone https://github.com/byanchriswhite/libpoktroll_clients
cd libpoktroll_clients

# Build shared library - NOTE: this will take a while until some import optimizations are done.
mkdir build
cd build
cmake ..
make
sudo make install

#OR build and install os-specific package; see libpoktroll_clients/README.md.
```

## Poktroll-clients-py development environment setup
```bash
git clone https://github.com/bryanchriswhite/poktroll-clients-py
cd poktroll-clients-py

# Install dependencies
pip install pipenv
pipenv install
pipenv shell

# (optional) Update protobufs ("pull" from buf.build)
buf export buf.build/pokt-network/poktroll

# (optional) Re-generate protobufs & fix imports
buf generate && python ./scripts/fix_proto_imports.py

# Install the package in editable mode
pip install -e .

# Run tests
pytest
```