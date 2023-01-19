import gzip
import json
import base64
import pyperclip
import tkinter as tk

# Compress using gzip, and convert to base64.
def gzip_zip(s):
	return base64.b64encode(gzip.compress(s.encode()))

# Convert from base64 to bytestream, then decompress using gzip.
def gzip_unzip(s):
	return gzip.decompress(base64.b64decode(s)).decode()

# Decode the input string and display in JSON format.
def decode():
	# Get the contents of the input box, strip Skytils' header.
	encoded = txt_input.get("1.0", "end-1c").replace("<Skytils-Waypoint-Data>(V1):", "")
	
	# Ensure input is present and decode.
	if not encoded: return
	decoded = gzip_unzip(encoded)
	
	# Skytils includes info of all categories for some reason? Not just the ones you selected?
	# Prune away the unselected (empty) categories.
	decoded_json = json.loads(decoded)
	pruned_categories = [c for c in decoded_json["categories"] if c["waypoints"]]
	pruned_dict = {}
	pruned_dict["categories"] = pruned_categories
	
	# Format the resulting JSON and update the output box.
	formatted = json.dumps(pruned_dict, indent=2)
	txt_output.delete("1.0", "end")
	txt_output.insert("1.0", formatted)

# Encode the JSON into an importable Skytils string, and copy to clipboard.
def encode():	
	# Get the contents of the output box, return if empty.
	decoded = txt_output.get("1.0", "end-1c")
	if not decoded: return
	
	# Check for valid JSON formatting.
	try:
		decoded_json = json.loads(decoded)
	except json.decoder.JSONDecodeError as e:
		# Display a popup indicating invalid formatting.
		popup = tk.Toplevel(window)
		popup.title("Invalid!")
		tk.Label(popup, text="Text is not a valid JSOn!").pack()
		tk.Label(popup, text=str(e)).pack()
		return
	
	# Calculate the number of waypoints to be converted.
	length = 0
	for c in decoded_json["categories"]:
		length += len(c["waypoints"])
		
	# Encode the JSON data and apply Skytils' header. Copy the resulting string to clipboard.
	encoded = gzip_zip(decoded)
	copied = "<Skytils-Waypoint-Data>(V1):" + encoded.decode()
	pyperclip.copy(copied)
	
	# Display a popup of how many waypoints were copied.
	popup = tk.Toplevel(window)
	popup.geometry("300x50")
	popup.title("Waypoints Copied!")
	tk.Label(popup, text="Copied " + str(length) + " waypoints to clipboard!").place(x=10, y=12)

# Main
if __name__ == "__main__":
	# Main window.
	window = tk.Tk()
	window.title("Skytils Waypoint Import/Export Editor")

	# Widgets frame. Used for window resizability.
	frame = tk.Frame(window)
	frame.pack(expand=True)

	# Input instruction text.
	lbl_input = tk.Label(frame, text="Paste the export from Skytils, then press Decode:")
	lbl_input.grid(row=0, column=0, columnspan=2)

	# Input text box.
	txt_input = tk.Text(frame, height=4)
	txt_input.grid(row=1, column=0, columnspan=2)

	# Decode button.
	btn_decode = tk.Button(frame, text="Decode", command=decode)
	btn_decode.grid(row=2, column=0, pady=10)

	# Encode button.
	btn_encode = tk.Button(frame, text="Encode", command=encode)
	btn_encode.grid(row=2, column=1, pady=10)

	# Output text box.
	txt_output = tk.Text(frame, height=18)
	txt_output.grid(row=3, column=0, columnspan=2)

	# Output instruction text.
	lbl_output = tk.Label(frame, text="Make your modifications, then press Encode.")
	lbl_output.grid(row=4, column=0, columnspan=2)

	# Start the GUI.
	window.mainloop()