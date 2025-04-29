import cv2
import numpy as np
import random
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def BinaryToDecimal(binary):
    return int(binary, 2)


def strToBinary(string):
    bin_conv = []
    for char in string:
        ascii_val = ord(char)
        if ascii_val < 64:
            bin_conv.append('0')
        binary_val = bin(ascii_val)
        bin_conv.append(binary_val[2:])
    return ''.join(bin_conv)


def encrypt(image_path, message, extension, output_image_name):
    signature = "11111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000011111111111111111111111111111111110"
    img = cv2.imread(image_path, 1)
    b, g, r = cv2.split(img)
    bin_message = strToBinary(message)
    full_data = signature + bin_message + signature
    height, width, _ = img.shape
    rand_row = random.randrange(0, height - 12, 1)

    for i in range(rand_row, height):
        for j in range(width):
            if len(full_data) != 0:
                if (full_data[0] == '1' and b[i][j] % 2 == 0) or (full_data[0] == '0' and b[i][j] % 2 == 1):
                    if b[i][j] == 255:
                        b[i][j] -= 1
                    else:
                        b[i][j] += 1
                full_data = full_data[1:]
    encrypted_img = cv2.merge((b, g, r))
    filename = f"{output_image_name}.{extension}"
    cv2.imwrite(filename, encrypted_img)
    return len(full_data) == 0


def decrypt(image_path):
    signature = "11111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000011111111111111111111111111111111110"
    img = cv2.imread(image_path, 1)
    b, _, _ = cv2.split(img)
    height, width, _ = img.shape
    bitstream = ""
    for i in range(height):
        for j in range(width):
            bitstream += str(b[i][j] % 2)
    start = bitstream.find(signature)
    if start == -1:
        return "ERROR: No hidden message found!"
    start += 128
    bitstream = bitstream[start:]
    end = bitstream.find(signature)
    bitstream = bitstream[:end]
    decrypted_msg = ""
    for i in range(0, len(bitstream), 7):
        temp = bitstream[i:i + 7]
        decrypted_msg += chr(BinaryToDecimal(temp))
    return decrypted_msg


class StegoApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Steganography Tool")
        master.geometry("600x450")
        master.configure(bg="#f4f4f4")

        Label(master, text="Image Steganography Tool", font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#333").pack(pady=15)

        self.image_path = None

        Button(master, text="Select Image", command=self.load_image, bg="#007bff", fg="white", font=("Helvetica", 12), width=20).pack(pady=5)

        self.message_entry = Text(master, height=5, width=50, font=("Helvetica", 10))
        self.message_entry.pack(pady=5)
        self.message_entry.insert(END, "Enter your message here...")

        self.output_name = Entry(master, font=("Helvetica", 10), width=50)
        self.output_name.pack(pady=5)
        self.output_name.insert(0, "Enter output image name (without extension)")

        Button(master, text="Encrypt Message", command=self.encrypt_image, bg="#28a745", fg="white", font=("Helvetica", 12), width=20).pack(pady=10)
        Button(master, text="Decrypt Message", command=self.decrypt_image, bg="#dc3545", fg="white", font=("Helvetica", 12), width=20).pack(pady=10)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *")])
        if self.image_path:
            messagebox.showinfo("Selected Image", f"Selected: {self.image_path}")

    def encrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        message = self.message_entry.get("1.0", END).strip()
        output_name = self.output_name.get().strip()
        extension = self.image_path.split('.')[-1]

        if not message or not output_name:
            messagebox.showerror("Error", "Please enter both message and output image name.")
            return

        success = encrypt(self.image_path, message, extension, output_name)
        if success:
            messagebox.showinfo("Success", f"Message encrypted and saved as {output_name}.{extension}")
        else:
            messagebox.showerror("Error", "Message encryption failed.")

    def decrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        message = decrypt(self.image_path)
        messagebox.showinfo("Decrypted Message", message)


if __name__ == "__main__":
    root = Tk()
    app = StegoApp(root)
    root.mainloop()
