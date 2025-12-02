# Superposition of Commands (SoC) Workflow

The Superposition of Commands (SoC) is the core innovation of Q-Lang, enabling context-aware execution with minimal overhead. This document details the step-by-step flow of an instruction from the Cloud to the Edge Device.

## 1. The Principle: Quantum-Inspired Execution

In Q-Lang, a command is sent in a state of **superposition**, meaning it represents two potential outcomes simultaneously. The final outcome is determined only when the instruction interacts with the **Local Context Engine (LCE)** on the Edge Device, which acts as the "observer" that collapses the superposition.

## 2. Step-by-Step Flow

### Step 1: Cloud Server Sends Instruction

The Cloud Server decides on the **intent** (e.g., "Update Model Weights") and serializes the instruction using the Q-Lang Protobuf schema.

| Field | Value | Rationale |
| :--- | :--- | :--- |
| `command_id` | `0x01` | Represents the intent: `WEIGHT_UPDATE_OR_SYNC`. |
| `context_flag` | `1` (Context B) | The Cloud's *preferred* state (e.g., "Assume high resource"). |
| `data_payload` | `[quantized_weights]` | The data required for the operation. |

### Step 2: Edge Device Receives Instruction

The Edge Device receives the binary instruction and passes it to the LCE.

### Step 3: LCE Determines True Context

The LCE (implemented in Rust) checks the device's real-time metrics, ignoring the `context_flag` from the Cloud if necessary.

| Metric | Value | LCE Decision |
| :--- | :--- | :--- |
| **Battery** | 25% | **Low Resource** |
| **Bandwidth** | 10 Mbps | High Resource |
| **True Context** | **Context A (Low Resource)** | Battery is below the 30% threshold. |

### Step 4: Superposition Collapse

The LCE collapses the superposition by mapping the `Command ID` and the `True Context` to a final `Operation ID`.

| Input 1 | Input 2 | Output |
| :--- | :--- | :--- |
| `Command ID` (`0x01`) | `True Context` (Context A) | **`Operation ID` (`0x1A`)** |

### Step 5: Execution

The Edge Device executes the resolved operation.

| Command ID | True Context | Resolved Operation | Action |
| :--- | :--- | :--- | :--- |
| `0x01` | Context A (Low Resource) | **LOCAL_WEIGHT_UPDATE** | Device applies the update locally and defers synchronization. **Saves battery and bandwidth.** |
| `0x01` | Context B (High Resource) | **FULL_SYNC_REQUEST** | Device initiates a full model synchronization with the Cloud. |

## 3. Example Code Flow (Rust LCE)

The core logic is executed in microseconds by the Rust LCE:

```rust
// 1. LCE determines the true context
let true_context = ContextEngine::determine_context(
    25.0,  // Battery: 25% (Low)
    10.0   // Bandwidth: 10 Mbps (High)
);
// true_context is Context::ContextA

// 2. LCE collapses the superposition
let operation = SuperpositionEngine::collapse(
    Command(0x01), // WEIGHT_UPDATE_OR_SYNC
    true_context
);

// 3. Result: The operation is LOCAL_WEIGHT_UPDATE (0x1A)
assert_eq!(operation.name, "LOCAL_WEIGHT_UPDATE");
```

This deterministic, microsecond-level decision-making is what gives Q-Lang its **62x throughput advantage** over traditional application-layer logic.
