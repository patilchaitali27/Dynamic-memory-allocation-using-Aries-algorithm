import tkinter as tk
import random

class MemoryAllocation:
    def __init__(self, m):
        self.m = m
        self.m.title("Aries Memory Allocation")
        self.m.geometry("650x650")

        font_style = ("Arial", 12)

        self.canvas = tk.Canvas(self.m, bg="white", width=600, height=300)
        self.canvas.pack()

        self.memory_size = 0
        self.memory_blocks = {}
        self.available_ids = []  # Track available IDs for reuse
        self.max_id = 0  # Track maximum ID assigned

        self.memory_size_label = tk.Label(self.m, text="Enter Total Memory Size:", font=font_style)
        self.memory_size_label.pack()

        self.memory_size_entry = tk.Entry(self.m, font=font_style)
        self.memory_size_entry.pack()

        self.enter_button = tk.Button(self.m, text="Enter", command=self.set_memory_size, font=font_style)
        self.enter_button.pack()

        self.allocate_label = tk.Label(self.m, text="Allocate Memory Block:", font=font_style)
        self.allocate_label.pack()

        self.allocate_entry = tk.Entry(self.m, font=font_style)
        self.allocate_entry.pack()

        self.allocate_button = tk.Button(self.m, text="Allocate", command=self.allocate_memory, font=font_style)
        self.allocate_button.pack()

        self.deallocate_button = tk.Button(self.m, text="Deallocate Memory", command=self.deallocate_memory, font=font_style)
        self.deallocate_button.pack()

        self.search_label = tk.Label(self.m, text="Search Memory by ID:", font=font_style)
        self.search_label.pack()

        self.search_entry = tk.Entry(self.m, font=font_style)
        self.search_entry.pack()

        self.search_button = tk.Button(self.m, text="Search", command=self.search_memory, font=font_style)
        self.search_button.pack()

        self.result_label = tk.Label(self.m, text="", font=font_style)
        self.result_label.pack()

        self.hover_info_label = tk.Label(self.m, text="", font=font_style)
        self.hover_info_label.pack()

        self.canvas.bind("<Leave>", self.clear_hover_info)

    def set_memory_size(self):
        self.memory_size = int(self.memory_size_entry.get())
        self.memory_size_label.config(text=f"Total Memory Size: {self.memory_size} units")

    def allocate_memory(self):
        block_size = int(self.allocate_entry.get())
        if self.memory_size >= block_size:
            if self.available_ids:
                block_id = self.available_ids.pop(0)  # Reuse available ID
            else:
                self.max_id += 1
                block_id = self.max_id  # Assign a new ID

            start_x = random.randint(10, 500)
            start_y = random.randint(10, 200)
            end_x = start_x + block_size * 5
            end_y = start_y + 30

            block_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            block = self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=block_color, outline="black")
            
            self.memory_blocks[block_id] = (block, block_size)  # Storing block and its size
            self.memory_size -= block_size
            self.update_memory_size_label()
            self.result_label.config(text="Memory block allocated successfully. ID: " + str(block_id))
            self.canvas.tag_bind(block, "<Enter>", lambda event, bid=block_id: self.show_hover_info(bid))
            self.canvas.tag_bind(block, "<Leave>", lambda event: self.clear_hover_info())
        else:
            self.result_label.config(text="Insufficient memory for allocation.")

    def deallocate_memory(self):
        if self.memory_blocks:
            block_id_to_deallocate = random.choice(list(self.memory_blocks.keys()))
            block_to_deallocate, freed_block_size = self.memory_blocks.pop(block_id_to_deallocate)
            self.available_ids.append(block_id_to_deallocate)  # Add freed ID to available list
            
            # Sort available IDs in ascending order
            self.available_ids.sort()

            self.canvas.delete(block_to_deallocate)
            self.memory_size += freed_block_size  # Increase memory size by freed block size
            self.update_memory_size_label()
            self.result_label.config(text="Memory block deallocated successfully. Freed ID: " + str(block_id_to_deallocate))
        else:
            self.result_label.config(text="No memory block to deallocate.")

    def search_memory(self):
        search_id = int(self.search_entry.get())
        if search_id in self.memory_blocks:
            block_info = self.memory_blocks[search_id]
            block_size = block_info[1]  # Extracting size from the stored block information
            self.result_label.config(text=f"Memory block ID {search_id} found. Size: {block_size} units")
        else:
            self.result_label.config(text=f"Memory block ID {search_id} not found.")

        

    def update_memory_size_label(self):
        self.memory_size_label.config(text=f"Total Memory Size: {self.memory_size} units")

    def show_hover_info(self, block_id):
        self.hover_info_label.config(text=f"ID: {block_id}")

    def clear_hover_info(self, event=None):
        self.hover_info_label.config(text="")

root = tk.Tk()
app = MemoryAllocation(root)
root.mainloop()
