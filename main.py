import hashlib
import requests

# Function to calculate SHA256 hash for a block
def sha256_hash(block):
    return hashlib.sha256(block).digest()

# Function to calculate the value h0 of a file
def calculate_h0(file_url):
    h0 = None
    response = requests.get(file_url, stream=True)
    block_size = 1024  # Size of each block is 1KB
    for block in response.iter_content(block_size):
        h = hashlib.sha256()  # Initialize a SHA256 object
        h.update(block)       # Update hash value with the content of the block
        h.update(h0 or b'')   # Add the previous hash value (or empty if it's the first block)
        h0 = h.digest()       # Save the new hash value
    return h0

# Function to validate the authenticity of each block as it is received
def validate_blocks(file_url, h0):
    response = requests.get(file_url, stream=True)
    block_size = 1024
    block_number = 0
    for block in response.iter_content(block_size):
        h = hashlib.sha256()
        h.update(block)
        h.update(h0 if block_number == 0 else blocks_hashes[block_number - 1])  # Add the previous hash value
        block_hash = h.digest()
        if block_number >= len(blocks_hashes):
            blocks_hashes.append(block_hash)
        if block_hash != blocks_hashes[block_number]:
            print(f"Block {block_number} is not valid!")  # Print if the block is invalid
        else:
            print(f"Block {block_number} is valid!")      # Print if the block is valid
        block_number += 1

# Dropbox link to the video file needing authentication
file_url = 'https://www.dropbox.com/s/a9lr8g1cj3o4dcn/birthday.mp4?dl=1'

# Calculate the value h0 of the file
h0 = calculate_h0(file_url)
print("h0:", h0.hex())

# Store the hash values of each block
blocks_hashes = [h0]

# Validate each block as it is received
validate_blocks(file_url, h0)
