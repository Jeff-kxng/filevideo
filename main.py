import hashlib


def calculate_h0(file_path):
    h0 = hashlib.sha256()

    with open(file_path, 'rb') as file:
        # Read the first block
        block = file.read(1024)
        h0.update(block)

        # Iterate through the rest of the blocks
        while len(block) == 1024:
            block = file.read(1024)
            h0.update(block)

    return h0.digest()


def verify_blocks(file_path, h0):
    with open(file_path, 'rb') as file:
        # Read the first block
        block = file.read(1024)
        current_hash = hashlib.sha256(block).digest()

        # Verify each block
        while len(block) == 1024:
            block = file.read(1024)
            expected_hash = hashlib.sha256(current_hash + block).digest()
            if expected_hash != h0:
                return False
            current_hash = hashlib.sha256(block).digest()

    return True


# Example usage
file_path = 'video.mp4'
h0 = calculate_h0(file_path)
print("h0:", h0.hex())

# Verify blocks
if verify_blocks(file_path, h0):
    print("All blocks verified successfully!")
else:
    print("Block verification failed!")
