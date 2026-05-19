import Bitmap

class main:
	# Bitmap.create_index("animals.txt", "bitmaps", False)
	# Bitmap.create_index("animals_sorted.txt", "bitmaps", True)
	Bitmap.compress_index("bitmaps/animals.txt", "compressed", "BBC", 200)
	Bitmap.compress_index("bitmaps/animals_sorted.txt_sorted", "compressed", "BBC", 200)
	Bitmap.compress_index("bitmaps/animals.txt", "compressed", "WAH", 4)
	Bitmap.compress_index("bitmaps/animals_sorted.txt_sorted", "compressed", "WAH", 4)
	Bitmap.compress_index("bitmaps/animals.txt", "compressed", "WAH", 8)
	Bitmap.compress_index("bitmaps/animals_sorted.txt_sorted", "compressed", "WAH", 8)
	Bitmap.compress_index("bitmaps/animals.txt", "compressed", "WAH", 16)
	Bitmap.compress_index("bitmaps/animals_sorted.txt_sorted", "compressed", "WAH", 16)
	Bitmap.compress_index("bitmaps/animals.txt", "compressed", "WAH", 32)
	Bitmap.compress_index("bitmaps/animals_sorted.txt_sorted", "compressed", "WAH", 32)
	Bitmap.compress_index("bitmaps/animals.txt", "compressed", "WAH", 64)
	Bitmap.compress_index("bitmaps/animals_sorted.txt_sorted", "compressed", "WAH", 64)

if __name__ == '__main__':
	main()
