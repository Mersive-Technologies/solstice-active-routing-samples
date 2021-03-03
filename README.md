# Introduction

These are some examples of using the Solstice Active Routing API using Python and SimplSharp.

# Pre-requisites

* Python 3
* Requests Library
* Solstice Pod 4.5 or greater

# Getting Started

Clone this repository.

Change into the repo's directory

Execute `pip install -r requirements.txt`

Update the `config.py` file with the IP addresses of your Active Routing pods.

Run an example script: `python script_name.py`

# Examples in `/samples` directory

`auth.py`: Demonstrates how to get a token to be used in subsequent steps

`patch_active_learning.py`: Demonstrates authentication and routing displays to multiple Pods (aka sinks)

`delete_active_learning.py`: Demonstrates authentication and deleting the connections to the Pods (aka sinks)

# Example in `/csharp-samples` directory

`active-routing-simplsharp.cs`: Demonstrates how to interact with the Active Routing API. NB: There is a limitation in SimplSharp using the HTTP verb Patch. See the note in the code for more details. Also, the console logging does not use the SimplSharp facility. You'll need to update the code to use the built-in SimplSharp logging mechanism.
