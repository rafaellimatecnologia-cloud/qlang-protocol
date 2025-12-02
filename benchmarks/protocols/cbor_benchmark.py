"""
CBOR Benchmark Module

Benchmarks CBOR (Concise Binary Object Representation) performance.
"""

import cbor2
import time
import io


class CBORBenchmark:
    """Benchmark suite for CBOR protocol"""
    
    def __init__(self):
        self.results = {
            "protocol": "CBOR",
            "message_size": 0,
            "serialization_time_us": 0.0,
            "deserialization_time_us": 0.0,
            "throughput_msg_sec": 0.0,
            "memory_usage_mb": 0.0,
        }
    
    def serialize_instruction(self, command_id, context_flag, payload):
        """Serialize instruction to CBOR"""
        data = {
            "command_id": command_id,
            "context_flag": context_flag,
            "payload": payload
        }
        fp = io.BytesIO()
        cbor2.dump(data, fp)
        return fp.getvalue()
    
    def deserialize_instruction(self, cbor_data):
        """Deserialize instruction from CBOR"""
        fp = io.BytesIO(cbor_data)
        return cbor2.load(fp)
    
    def benchmark_serialization(self, iterations=100000):
        """Benchmark serialization performance"""
        payload = b"model_weights_v2_data_payload_test"
        
        start = time.perf_counter()
        for _ in range(iterations):
            self.serialize_instruction(0x01, 1, payload)
        end = time.perf_counter()
        
        total_time = (end - start) * 1_000_000
        avg_time = total_time / iterations
        
        return avg_time
    
    def benchmark_deserialization(self, iterations=100000):
        """Benchmark deserialization performance"""
        payload = b"model_weights_v2_data_payload_test"
        cbor_data = self.serialize_instruction(0x01, 1, payload)
        
        start = time.perf_counter()
        for _ in range(iterations):
            self.deserialize_instruction(cbor_data)
        end = time.perf_counter()
        
        total_time = (end - start) * 1_000_000
        avg_time = total_time / iterations
        
        return avg_time
    
    def benchmark_throughput(self, duration_seconds=1.0):
        """Benchmark throughput"""
        payload = b"model_weights_v2_data_payload_test"
        count = 0
        
        start = time.perf_counter()
        while time.perf_counter() - start < duration_seconds:
            self.serialize_instruction(0x01, 1, payload)
            count += 1
        
        throughput = count / duration_seconds
        return throughput
    
    def benchmark_message_size(self):
        """Benchmark message size"""
        payload = b"model_weights_v2_data_payload_test"
        cbor_data = self.serialize_instruction(0x01, 1, payload)
        return len(cbor_data)
    
    def run_all_benchmarks(self):
        """Run all benchmarks"""
        print("Running CBOR Benchmarks...")
        
        msg_size = self.benchmark_message_size()
        self.results["message_size"] = msg_size
        print(f"  Message Size: {msg_size} bytes")
        
        ser_time = self.benchmark_serialization()
        self.results["serialization_time_us"] = ser_time
        print(f"  Serialization: {ser_time:.4f} µs")
        
        deser_time = self.benchmark_deserialization()
        self.results["deserialization_time_us"] = deser_time
        print(f"  Deserialization: {deser_time:.4f} µs")
        
        throughput = self.benchmark_throughput()
        self.results["throughput_msg_sec"] = throughput
        print(f"  Throughput: {throughput:,.0f} msg/sec")
        
        return self.results


if __name__ == "__main__":
    benchmark = CBORBenchmark()
    results = benchmark.run_all_benchmarks()
    print(f"\nResults: {results}")
