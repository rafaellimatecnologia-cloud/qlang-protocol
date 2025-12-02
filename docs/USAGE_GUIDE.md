# Q-Lang Protocol: Practical Usage Guide

This guide provides practical examples for integrating and using the Q-Lang Protocol in both Cloud (Python) and Edge (Rust) environments.

## 1. Cloud-Side Implementation (Python)

The Cloud Server is responsible for creating and sending the Q-Lang instructions. We use the generated Protobuf classes for serialization.

### 1.1. Creating a Q-Lang Instruction

```python
# Assuming Protobuf classes are generated and imported
from qlang.v1.q_lang_pb2 import QLangInstruction, QLangMetadata

# 1. Define the metadata
metadata = QLangMetadata(
    timestamp_ms=int(time.time() * 1000),
    device_id="device-uuid-12345",
    priority=10
)

# 2. Create the instruction
instruction = QLangInstruction(
    command_id=0x02,  # Data Offload or Cache
    context_flag=1,   # Cloud prefers Context B (Offload)
    data_payload=b"sensor_data_batch_1",
    metadata=metadata
)

# 3. Serialize and send
binary_message = instruction.SerializeToString()

print(f"Binary message size: {len(binary_message)} bytes")
# Send binary_message over the network (e.g., MQTT, TCP)
```

### 1.2. Processing a Q-Lang Response

The Cloud Server receives a binary response and deserializes it to confirm the executed operation.

```python
from qlang.v1.q_lang_pb2 import QLangResponse

# Assume 'binary_response' is received from the Edge Device
response = QLangResponse()
response.ParseFromString(binary_response)

print(f"Operation Executed: {response.operation_name}")
print(f"Execution Time: {response.execution_time_us} µs")

if response.operation_name == "CLOUD_OFFLOAD_DATA":
    # Success: Data was offloaded to the cloud
    process_offloaded_data(response.response_data)
else:
    # Failure/Adaptation: Data was cached locally
    log_local_caching_event()
```

## 2. Edge-Side Implementation (Rust)

The Edge Device is responsible for receiving the instruction, collapsing the SoC using the LCE, and executing the resolved operation.

### 2.1. Integrating the LCE

The LCE is integrated as a dependency in `Cargo.toml`:

```toml
[dependencies]
qlang-core = "0.1.0"
protobuf = "3.0" # For deserializing the instruction
```

### 2.2. Processing the Instruction and Collapsing SoC

```rust
use qlang_core::{Command, SuperpositionEngine};
use protobuf::Message; // Assuming Protobuf is used for deserialization
// use qlang::v1::q_lang_pb2::QLangInstruction; // Actual Protobuf struct

// Simplified deserialization for example purposes
fn process_qlang_instruction(binary_message: &[u8], battery: f32, bandwidth: f32) {
    // 1. Deserialize the instruction (Simplified)
    // let instruction = QLangInstruction::parse_from_bytes(binary_message).unwrap();
    
    // Simplified extraction of Command ID (0x02)
    let command_id = 0x02; 
    
    // 2. Collapse the Superposition using the LCE
    let operation = SuperpositionEngine::process_instruction(
        Command(command_id),
        battery,
        bandwidth,
    );

    // 3. Execute the resolved operation
    match operation.name {
        "CACHE_DATA_LOCALLY" => {
            println!("LCE collapsed to: CACHE_DATA_LOCALLY. Saving data locally.");
            // execute_local_caching(instruction.data_payload);
        }
        "CLOUD_OFFLOAD_DATA" => {
            println!("LCE collapsed to: CLOUD_OFFLOAD_DATA. Initiating cloud offload.");
            // execute_cloud_offload(instruction.data_payload);
        }
        _ => {
            println!("Unknown operation: {}", operation.name);
        }
    }
}

// Example usage: Low resource scenario
process_qlang_instruction(&[0u8; 10], 20.0, 1.5); 
// Output: LCE collapsed to: CACHE_DATA_LOCALLY. Saving data locally.

// Example usage: High resource scenario
process_qlang_instruction(&[0u8; 10], 80.0, 10.0); 
// Output: LCE collapsed to: CLOUD_OFFLOAD_DATA. Initiating cloud offload.
```
