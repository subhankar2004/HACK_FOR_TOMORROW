import sys
import logging
import time
import json
import os
import numpy as np

try:
    import qiskit
    from qiskit_aer.primitives import SamplerV2
    from qiskit.circuit.random import random_circuit
except ImportError as e:
    print(f"Error importing Qiskit: {e}")
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "qiskit", "qiskit-aer"])
    import qiskit
    from qiskit_aer.primitives import SamplerV2

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class QuantumKeyDistribution:
    def __init__(self):
        """Initialize QKD with modern Qiskit components"""
        try:
            self.sampler = SamplerV2()
            logging.info("Quantum sampler initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize sampler: {e}")
            raise

    def generate_bb84_key(self, key_length=32):
        """
        Implements BB84 protocol using modern Qiskit primitives
        """
        alice_bits = np.random.randint(2, size=key_length)
        alice_bases = np.random.randint(2, size=key_length)
        
        circuits = []
        for i in range(key_length):
            qc = qiskit.QuantumCircuit(1, 1)
            
            if alice_bits[i] == 1:
                qc.x(0)
            if alice_bases[i] == 0:
                qc.h(0)
                
            qc.measure(0, 0)
            circuits.append(qc)
        
        bob_bases = np.random.randint(2, size=key_length)
        
        try:
            job = self.sampler.run(circuits, shots=1)
            results = job.result()
            bob_results = []
            
            for i, res in enumerate(results):
                counts = res.data.get("counts", {})  # Fix: Extract counts safely
                if counts:
                    measured_bit = int(list(counts.keys())[0])
                    bob_results.append(measured_bit)
                else:
                    logging.warning(f"No measurement data for bit {i}")
                    bob_results.append(0)
            
            matching_bases = alice_bases == bob_bases
            final_key_bits = alice_bits[matching_bases]
            
            final_key = ''.join(map(str, final_key_bits))
            key_info = {
                "key": final_key,
                "length": len(final_key),
                "matching_bases_count": int(np.sum(matching_bases)),
                "total_bits_sent": key_length,
                "timestamp": time.time()
            }

            os.makedirs("quantum/keys", exist_ok=True)
            with open('quantum/keys/latest_key.json', 'w') as f:
                json.dump(key_info, f, indent=2)

            return key_info

        except Exception as e:
            logging.error(f"Error generating quantum key: {e}")
            raise

if __name__ == "__main__":
    try:
        qkd = QuantumKeyDistribution()
        logging.info("\U0001F680 Starting quantum key generation...")
        
        for i in range(5):
            key_info = qkd.generate_bb84_key()
            logging.info(f"\u2728 Generated key {i+1}/5: {key_info['key'][:8]}... "
                        f"({key_info['length']} bits)")
            time.sleep(0.5)
            
        logging.info("\u2705 Quantum module initialized successfully")
        sys.exit(0)
        
    except Exception as e:
        logging.error(f"\u274C Initialization failed: {e}")
        sys.exit(1)
