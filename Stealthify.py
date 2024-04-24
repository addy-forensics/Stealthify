import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stealthify")

        self.label = tk.Label(master, text="Enter Message to Hide:")
        self.label.pack()

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack()

        self.encode_button = tk.Button(master, text="Encode", command=self.encode_message)
        self.encode_button.pack()

        self.decode_button = tk.Button(master, text="Decode", command=self.decode_message)
        self.decode_button.pack()

    def encode_message(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to encode.")
            return

        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not image_path:
            return

        try:
            self.encode_image(image_path, message)
            messagebox.showinfo("Success", "Message encoded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode_message(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not image_path:
            return

        decoded_message = self.decode_image(image_path)
        messagebox.showinfo("Decoded Message", f"The decoded message is:\n\n{decoded_message}")

    def encode_image(self, image_path, message):
        img = Image.open(image_path)
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        if len(binary_message) > img.width * img.height * 3:
            raise ValueError("Message too long to encode in the image")

        index = 0
        for y in range(img.height):
            for x in range(img.width):
                pixel = list(img.getpixel((x, y)))
                for i in range(3):
                    if index < len(binary_message):
                        pixel[i] = pixel[i] & ~1 | int(binary_message[index])
                        index += 1
                img.putpixel((x, y), tuple(pixel))

        img.save("encoded_image.png")

    def decode_image(self, image_path):
        img = Image.open(image_path)
        binary_message = ''

        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                for i in range(3):
                    binary_message += str(pixel[i] & 1)

        message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        return message

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
