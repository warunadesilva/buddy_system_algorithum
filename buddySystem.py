import math

class BuddyAllocator:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.free_blocks = {total_memory: [0]}  # Dictionary with block size as key and list of start addresses as value

    def allocate(self, request_size):
        # Round the request size up to the nearest power of 2
        block_size = 2 ** math.ceil(math.log2(request_size))

        if block_size > self.total_memory:
            print(f"Allocation failed: Requested size {request_size} exceeds total memory.")
            return -1

        # Find the smallest block size that can satisfy the request
        for size in sorted(self.free_blocks.keys()):
            if size >= block_size and self.free_blocks[size]:
                start_address = self.free_blocks[size].pop(0)  # Allocate the first block of this size

                # If no blocks of this size remain, remove the entry
                if not self.free_blocks[size]:
                    del self.free_blocks[size]

                # Split the block into smaller blocks if necessary
                while size > block_size:
                    size //= 2
                    if size not in self.free_blocks:
                        self.free_blocks[size] = []
                    self.free_blocks[size].append(start_address + size)

                print(f"Allocated {request_size} units at address {start_address}.")
                return start_address

        print(f"Allocation failed: No suitable block found for size {request_size}.")
        return -1

    def deallocate(self, start_address, block_size):
        size = 2 ** math.ceil(math.log2(block_size))
        if size > self.total_memory:
            print(f"Deallocation failed: Block size {block_size} exceeds total memory.")
            return

        # Add the block back to the free list
        if size not in self.free_blocks:
            self.free_blocks[size] = []
        self.free_blocks[size].append(start_address)
        self.free_blocks[size].sort()

        # Attempt to merge buddies
        while size < self.total_memory:
            buddy_address = start_address ^ size  # Calculate buddy's address
            if buddy_address in self.free_blocks[size]:
                # Remove buddy from the free list
                self.free_blocks[size].remove(buddy_address)
                if not self.free_blocks[size]:
                    del self.free_blocks[size]

                # Merge the blocks
                start_address = min(start_address, buddy_address)
                size *= 2
                if size not in self.free_blocks:
                    self.free_blocks[size] = []
                self.free_blocks[size].append(start_address)
                self.free_blocks[size].sort()
            else:
                break

        print(f"Deallocated block at address {start_address} with size {block_size}.")

    def display_memory(self):
        print("\nCurrent Free Blocks:")
        for size, addresses in sorted(self.free_blocks.items()):
            print(f"Size {size}: {addresses}")
        print()

# Main function
if __name__ == "__main__":
    allocator = BuddyAllocator(128)  # Initialize with 128 units of memory

    allocator.display_memory()

    # Allocate memory
    addr1 = allocator.allocate(20)
    addr2 = allocator.allocate(50)
    addr3 = allocator.allocate(10)
    
    allocator.display_memory()

    # Deallocate memory
    allocator.deallocate(addr1, 20)
    allocator.display_memory()

    # Allocate again
    addr4 = allocator.allocate(30)
    allocator.display_memory()