# STROBE

This is an implementation of STROBE in Python, using asyncio.

The algorithm allows a group of nodes to share a secret among themselves in a secure and distributed manner. Each node only knows a part of the secret, and the secret can only be reconstructed if enough nodes collaborate.

### Requirements
    - Python 3.7 or higher
    - asyncio, sympy, math, socket, json, tk Python libraries

You can install the required libraries using pip:
```bash
pip install asyncio sympy math socket json tk
```

### Usage

To run the simulation, run the following command:

```
python main.py
```

This will start the simulation with 8 nodes by default. You can change the number of nodes by modifying the `NUM_NODES` variable in `main.py`.

The GUI shows the current round and the message shared by each node in that round.

### Implementation details

Each node generates a random polynomial of degree n-1 with a secret x_0 as the constant term, and shares the polynomial coefficients with the other nodes. Each node then evaluates the polynomial at its own ID to get its own share of the secret.

In each round, each node sends its current share to a random subset of other nodes. Once a node has received shares from at least t+1 nodes, it can reconstruct the polynomial coefficients using Lagrange interpolation, and hence the secret. The nodes then increment the round counter and start a new round.

<strong>The algorithm is secure as long as the number of compromised nodes is less than t.</strong>