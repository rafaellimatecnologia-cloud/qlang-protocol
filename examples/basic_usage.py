#!/usr/bin/env python3
"""
Q-Lang Protocol: Basic Usage Example

This example demonstrates how to create and serialize Q-Lang instructions.
"""

import json
import sys

# For demonstration purposes, we'll create a simple Q-Lang instruction class
# In production, this would use the compiled Protobuf classes

class QLangInstruction:
    """Simple Q-Lang instruction representation"""
    
    def __init__(self, command_id, context_flag, data_payload=b""):
        self.command_id = command_id
        self.context_flag = context_flag
        self.data_payload = data_payload
    
    def to_binary(self):
        """Convert instruction to binary format (simplified)"""
        # In production, use Protobuf serialization
        binary = bytearray()
        binary.extend(self.command_id.to_bytes(4, 'little'))
        binary.append(self.context_flag)
        binary.extend(self.data_payload)
        return bytes(binary)
    
    def __repr__(self):
        return f"QLangInstruction(cmd=0x{self.command_id:02X}, ctx={self.context_flag}, payload_len={len(self.data_payload)})"


def main():
    print("=" * 60)
    print("Q-Lang Protocol: Basic Usage Example")
    print("=" * 60)
    
    # Example 1: Create a simple instruction
    print("\n1. Creating a Q-Lang Instruction:")
    instruction = QLangInstruction(
        command_id=0x01,
        context_flag=1,  # Context B (High Resource)
        data_payload=b"model_weights_v2"
    )
    print(f"   {instruction}")
    
    # Example 2: Serialize to binary
    print("\n2. Serializing to Binary:")
    binary = instruction.to_binary()
    print(f"   Binary size: {len(binary)} bytes")
    print(f"   Hex: {binary.hex()}")
    
    # Example 3: Compare with JSON
    print("\n3. Comparison with JSON:")
    json_equivalent = {
        "command_id": 0x01,
        "context_flag": 1,
        "data_payload": "model_weights_v2"
    }
    json_bytes = json.dumps(json_equivalent).encode('utf-8')
    print(f"   JSON size: {len(json_bytes)} bytes")
    print(f"   Q-Lang size: {len(binary)} bytes")
    print(f"   Compression ratio: {len(json_bytes) / len(binary):.2f}x")
    
    # Example 4: Batch multiple instructions
    print("\n4. Batch Processing:")
    instructions = [
        QLangInstruction(0x01, 1, b"weights_v2"),
        QLangInstruction(0x02, 0, b"cache_data"),
        QLangInstruction(0x03, 1, b"retrain"),
        QLangInstruction(0x04, 0, b"incremental"),
    ]
    
    total_size = sum(len(instr.to_binary()) for instr in instructions)
    print(f"   Instructions: {len(instructions)}")
    print(f"   Total size: {total_size} bytes")
    print(f"   Average per instruction: {total_size / len(instructions):.1f} bytes")
    
    # Example 5: Context-aware behavior
    print("\n5. Superposition of Commands (SoC):")
    print("   Command 0x01 resolves to different operations based on context:")
    print("   - Context A (Low Resource): LOCAL_WEIGHT_UPDATE (0x1A)")
    print("   - Context B (High Resource): FULL_SYNC_REQUEST (0x1B)")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
