Bitmap indexing and compression module
	-The purpose of this code is to reduce the size of a large csv through bitmap
	compression

Description
	-This code takes a csv formated txt file with columns Animal,Age,Adopted
	in that order and convert it to a bitmap index and then compress that
	index for storing a large data set with limited storage. 

Dependencies (python 3.12.2)
	-standard library sys
	-standard library os.path
	-standard library errno
	-standard library math

How to execute
	1. import Bitmap (or current file name) as a module in your code 
	2. call create_index(input_file, output_path, sort_bool)
		i. input_file needs to be a path to a file in csv format with
		columns Animal,Age,Adopted in that order. The path in String format
		ii. output_path needs to be a path to a directory in String format
		iii. sort_bool needs to be True/1 or False/0 and indicate if input_file is sorted
	3. call compress_index(bitmap_index, output_path, compression_method, word_size)
		i. bitmap_index is a path in String format to one of the files created 
		by create_index()
		ii. output_path needs to be a path to a directory in String format
		iii. compression_method current will only be able to equal "WAH" or "BBC"
		iv. word_size is any number greater than 2 since the first 2 bits in a word are
		reserved for if its a run and what type of run word size doesnt matter for BBC 
		it will always be 8
	example code
		Bitmap.create_index("animals.txt", "bitmaps", True)
			this would create a bitmap index in file bitmaps/animals.txt_sorted
		Bitmap.compress_index("bitmaps/animals.txt_sorted", "compressed", "WAH", 16)
			this would create a compressed file compressed/animals.txt_sorted_WAH_16

Error handling
	-both functions will return 0 if theyre successful and -1 if theyre not successful

Creator
	-Korbin Gillette
