# Memory Storage

Memory Storage is a CST synchonization mechanism to synchonize memories across multiple CST instances, whether they are CST-Java or CST-Python instances.

Synchronization is performed using a Redis server. A server reachable by all instances must be running to use Memory Storage. Redis can be installed on Linux and Windows (using WSL) using [Redis documentation](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).

When using Memory Storage, each local CST instance is called a node. Memories with the same name in participating nodes are synchronized. Only memories that are used by more than one node are stored in the storage. Other memories are only indicated as existing in the storage, and can be transferred later if another node starts using them. 

The collection of synchonized nodes is a mind, and a single Redis instance can support multiple minds with unique names.

To use it, you just need to add a :class:`Memory Storage Codelet<cst_python.memory_storage.memory_storage>` to each mind participating in the network. Check the [Memory Storage Example](https://h-iaac.github.io/CST-Python/_build/html/_examples/Memory%20Storage.html) for how to use it.

## Protocol

This section presents the messages used for the operation of the Memory Storage. It is intended only for CST developers.

### Mind nodes

`<mind_name>:nodes` is a Redis set containing all the nodes names. When a node enters the network, it needs to add it's unique name to this set.

### Memory Lifecycle and Storage

Initially, no memory is stored in Memory Storage. In this case, memories are stored without data, only indicating which node it is stored in, called the owner. When another node creates a memory that already exists in Memory Storage, it checks its owner. If it is a node, it requests the transfer of the memory. Once transferred, the memory is stored in Memory Storage.

Each memory in the storage is stored in a Redis hash `<mind_name>:memories:<memory_name>` with the keys:

- `evaluation`: memory evaluation
- `I`: memory info
- `id`: memory id
- `owner`: current node owning the memory. If is in the storage, the value is set to "".
- `logical_time`: time when the memory was stored. 

When a local Memory Storage Codelet detects a new created memory, it checks if a corresponding hash `<mind_name>:memories:<memory_name>` exists. If so, it checks the owner. If it is a node, it requests the transfer of memory. After ensuring that the memory is in the storage, it performs the synchronization. If the created memory does not have a corresponding memory in the storage, the node sends an impostor containing only the owner set as its own name.

#### Memory Transfer

Each node subscribes to two Redis channels to perform memory transfers:

- `<mind_name>:nodes:<node_name>:transfer_memory`: receives transfer requests. Each request is a string containing a JSON. It must contain the "request" field, with subfields "memory_name" indicating which memory should be transferred, and "node" indicating which node requests the transfer. Optionally, it can contain a "logical_time" field with the time of the requesting node when making the request. After making the transfer, the node responds by sending a message on the requesting node's transfer done channel.
- `<mind_name>:nodes:<node_name>transfer_done:` Receives messages indicating that a requested memory transfer has been performed. The message is a string containing a JSON, with a "request" field and a "memory_name" subfield indicating which memory was transferred. Optionally, it can contain a "logical_time" field indicating the time when the transfer was performed.

A node waits for a transfer until a certain timeout. If it does not receive a response, it sends its own version of the memory to the Memory Storage.

Transferred memories are marked with `owner=""`, and are synchronized with each Memory Storage Codelet cycle on all nodes that have a version of this memory.

All nodes that have memory in the storage also subscribe to the memory update channel, `< mind_name>:memories:<memory_name>:update`.

#### Memory Update

When a node is synchronizing a memory, it checks each Memory Storage Codelet cycle to see if it has been updated locally, comparing the local memory timestamp with the last update. If it has been updated, it initiates an update.

In an update, the logical memory time in the storage is first obtained and compared with the logical memory time of the local memory. If the version in the storage is more recent, it retrieves the remote data. If the local version is more recent, it sends it to the storage and sends a message on the memory update channel.

Messages received on the memory update channel also initiate updates.

Memory Storage attempts to ensure that the most recent versions of memory are maintained, but overwrites can occur if a memory is updated concurrently on two nodes. Verification of which memory is more recent is done using logical clocks.