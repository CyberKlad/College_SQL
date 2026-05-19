"""
Student: Korbin Gillette
Professor: Ben McCamish
Date: 7 March 2025
Description: indexing function that creates a bitmaps and compression function
that compresses the created bitmap index
"""
import sys
import os.path
import errno
import math

#############################_BITMAP_INDEX_#####################################

#function for opening the file and erroring if it cannot
def open_inout(input_file, output_path, sort_bool):
	#try opening the file
	try:
		infile = open(input_file, 'r')
	#if you cant write appropriate error the stderr
	except Exception as error:
	    sys.stderr.write(f"Error: {error}\n")
	    return -1, error.errno
	try:
		outfile = open(output_path, 'w')
	#if you cant write appropriate error the stderr
	except Exception as error:
	    sys.stderr.write(f"Error: {error}\n")
	    return -1, error.errno
	return infile, outfile

#input_file = given file in csv format that will be indexed
#output_path = destination directory for created file
#sorted = bool value specifying if the input should be sorted or int equivalant
def create_index(input_file, output_path, sort_bool):
	#we should expect the arguments of the types described above so I check for
	#them

	#this converts int of 0 or 1 to their bool equivalant
	if isinstance(sort_bool, int) and 0 <= sort_bool <= 1:
		sort_bool = bool(sort_bool)

	#input as a string path that leads to a file
	if not isinstance(input_file, str):
		sys.stderr.write("Error: argument 1 should be of type str")
		return -1

	#output file should be a path to a directory
	if not isinstance(output_path, str):
		sys.stderr.write("Error: argument 2 should be of type str")
		return -1
	if not os.path.isdir(output_path):
		sys.stderr.write("Error: argument 2 should be a directory")
		return -1

	#sort_bool should be a bool value of true or false
	if not isinstance(sort_bool, bool):
		sys.stderr.write("Error: argument 3 should be of type bool or int value 0-1")
		return -1

	#grab the file name of the input path for crafting filename of out
	true_infile = os.path.basename(input_file)

	#if the file is sorted add the _sorted tag to the end of the created file
	#these function return a FILE type and need to be closed
	if sort_bool:
		infile, outfile = open_inout(input_file, f"{output_path}/{true_infile}_sorted", sort_bool)
	else:
		infile, outfile = open_inout(input_file, f"{output_path}/{true_infile}", sort_bool)
	if infile == -1:
		return -1

	#make the file being sent in into a dictionary for easier mutation
	file_dict = {'animal':[], 'age':[], 'adopted':[]}
	#read the file line by line
	for line in infile:
		#remove leading and trailing characters such as '\n' or ' ' 
		line = line.strip()
		#ignore the line if after removing leading and trailing characters it does not
		#exist
		if line:
			#grab the 3 values seperated by 2 commas and place them into their respective
			#variables in the dictionary
			animal, age, adopted = line.split(',',2)
			file_dict['animal'].append(animal)
			file_dict['age'].append(age)
			file_dict['adopted'].append(adopted)

	#dictionary with all of the columns of the file are broken up into binary columns
	bitfile_dict = {'cat':[], 'dog':[], 'turtle':[], 'bird':[],
					'1-10':[], '11-20':[], '21-30':[], '31-40':[], '41-50':[],
					'51-60':[], '61-70':[], '71-80':[], '81-90':[], '91-100':[],
					'True':[], 'False':[]}
	#for loop going over every row
	for i in range(len(file_dict['age'])):
		#first append zeros to the new lists since python has dynamic lists
		for column in bitfile_dict:
			bitfile_dict[column].append(0)

		#this set of if elif and else check which bit should be turned on
		#based on the animal 
		if file_dict['animal'][i] == "cat":
			bitfile_dict['cat'][i] = 1
		elif file_dict['animal'][i] == "dog":
			bitfile_dict['dog'][i] = 1
		elif file_dict['animal'][i] == "turtle":
			bitfile_dict['turtle'][i] = 1
		else:
			bitfile_dict['bird'][i] = 1

		#this set of if elif and else check which age bucket the animal goes in
		if int(file_dict['age'][i])/10 > 9:
			bitfile_dict['91-100'][i] = 1
		elif int(file_dict['age'][i])/10 > 8:
			bitfile_dict['81-90'][i] = 1
		elif int(file_dict['age'][i])/10 > 7:
			bitfile_dict['71-80'][i] = 1
		elif int(file_dict['age'][i])/10 > 6:
			bitfile_dict['61-70'][i] = 1
		elif int(file_dict['age'][i])/10 > 5:
			bitfile_dict['51-60'][i] = 1
		elif int(file_dict['age'][i])/10 > 4:
			bitfile_dict['41-50'][i] = 1
		elif int(file_dict['age'][i])/10 > 3:
			bitfile_dict['31-40'][i] = 1
		elif int(file_dict['age'][i])/10 > 2:
			bitfile_dict['21-30'][i] = 1
		elif int(file_dict['age'][i])/10 > 1:
			bitfile_dict['11-20'][i] = 1
		else:
			bitfile_dict['1-10'][i] = 1

		#this if else segment will decide if the true or false bit is turned on
		if file_dict['adopted'][i].lower() == "true":
			bitfile_dict['True'][i] = 1
		else:
			bitfile_dict['False'][i] = 1


	#write the dictionary used internally to the right filename crafted above
	for i in range(len(bitfile_dict['cat'])):
		for column in bitfile_dict:
			outfile.write(f"{bitfile_dict[column][i]}")
		outfile.write("\n")
	#close the files being used
	infile.close()
	outfile.close()
	return 0

#function for transposing a animal file
def transpose_bit_animal(infile):
	bit_array = []
	bitfile_dict = {'cat':[], 'dog':[], 'turtle':[], 'bird':[],
					'1-10':[], '11-20':[], '21-30':[], '31-40':[], '41-50':[],
					'51-60':[], '61-70':[], '71-80':[], '81-90':[], '91-100':[],
					'True':[], 'False':[]}
	for line in infile:
		line = line.strip()
		if line:
			curs = 0
			for bit in line:
				(bitfile_dict[list(bitfile_dict)[curs]]).append(bit)
				curs += 1
	for column in bitfile_dict:
		bit_array += (bitfile_dict[column]+[2])
	return bit_array

#################################_BBC_##########################################

def bbc_string(run_count, dirty_count, dirty_loc, lit_count, literal_str, bit):
	#this is if the only lit is a dirty bit
	if dirty_count == 1:
		lit_count = 0
	#if there is more than 1 literal there shouldnt be any dirty count
	if lit_count > 1 and dirty_count > 0:
		sys.stderr.write("Error: something went wrong with dirty_count\n")
		dirty_count = 0
	output = ""
	if run_count <= 6:
		output += f"{(bin(run_count)[2:]).zfill(3)}"
	elif 7 <= run_count <= 32767:
		output += "111"
	else:
		sys.stderr.write("Error: there shouldnt be that large of a run count\n")
	if dirty_count == 1 and lit_count == 0:
		output += f"1{(bin(dirty_loc)[2:]).zfill(4)}"
	else:
		output += f"0{(bin(lit_count)[2:]).zfill(4)}"
	if 7 <= run_count <= 127:
		output += f"0{(bin(run_count)[2:]).zfill(7)}"
	if run_count > 127:
		output += f"1{(bin(run_count)[2:]).zfill(15)}"
	if lit_count > 0:
		output += literal_str
	if bit == 2:
		output += "\n"
	return output

def check_dirty(array):
	dirty_num = 0
	dirty_ind = 8
	for i,bit in enumerate(array):
		if bit != 0:
			dirty_num += 1
			dirty_ind = i
	if dirty_num > 1:
		dirty_ind = -1
	return dirty_ind

def bbc_compression(bit_array):
	#max run can be hard coded because 15 bits is the most that can be used for bbc runs
	max_run = 32767
	#max lit can be hard coded because you only have 4 bits to count them
	max_lit = 15
	#BBC always has a word size of 8
	word_size = 8
	#set up some variables for building as I read the bit_array in
	compress_output = ""
	literal_str = ""
	#this is because dirty bits are considered literals if they have literals that follow
	word_save = ""
	dirty_save = 0
	#array of 8 for reading in one word at a time
	word_chunk = [0] * word_size
	#counter used for checking how much of the word ive read in
	tick = 0
	#various variable needed 
	run_count = 0
	dirty_count = 0
	dirty_loc = 0
	lit_count = 0


	#read each bit in
	for bit in bit_array:
		#convert the bit to an int
		bit = int(bit)


		#check if the bit is the end of a string denoted internally by 2
		if bit == 2:
			#fill the current read if its partway filled with trailing 0's
			if tick > 0:
				#if there was a partial word fill the right side with 0's and check
				#if its a run or a literal
				word_chunk[tick-(word_size):] = [0] * (word_size-tick)
				tick = 8
			else:
				#check that we wont be adding some random word with no info
				if run_count == 0 and lit_count == 0 and dirty_count == 0:
					compress_output += "\n"
					continue
				#if nothing was read in at this time then ignore the word just print 
				#what is currently gathered
				compress_output += bbc_string(run_count, dirty_count, dirty_save,
				lit_count, literal_str, bit)
				#reset the variables
				lit_count = 0
				run_count = 0
				dirty_count = 0
				literal_str = ""
				word_save = ""
				tick = 0
				continue

		else:
			#place the bit in the word chuck
			word_chunk[tick] = bit
			tick += 1


		#only move on to the dificult checks after I have read in an entire word
		#for BBC this would be 8
		if tick == word_size:
			#call function that return -1 if the word is a literal, 9 if the word is a run
			#and a number 0-7 if its a dirty bit with 0-7 being the index
			dirty_loc = check_dirty(word_chunk)

			#code for if the word is a literal
			if dirty_loc == -1:
				#if the dirty bit needs to be stored as a literal do that now
				if dirty_count == 1:
					dirty_count = 0
					literal_str += f"{word_save}"
					word_save = ""
				#up the literal count
				lit_count += 1
				#store the word in the literal_str
				for j in word_chunk:
					literal_str += f"{j}"

				#check if max literals has already been met if so add the composed words
				#before dealing with this literal
				if lit_count == max_lit:
					#if the lits have been maxed out dump the stored info and start reading
					#more write all runs being stored up till now
					compress_output += bbc_string(run_count, dirty_count, dirty_loc,
					lit_count, literal_str, bit)
					#reset the variables and start fresh
					lit_count = 0
					run_count = 0
					literal_str = ""

				#reset tick for new word
				tick = 0
				continue

			#code for if the word is a run of 0's
			if dirty_loc == 8:
				#if there is already literals or a dirty bit dump current word
				if (lit_count > 0 or dirty_count == 1):
					compress_output += bbc_string(run_count, dirty_count, dirty_save,
					lit_count, literal_str, bit)
					#reset the variables
					run_count = 0
					lit_count = 0
					dirty_count = 0
					literal_str = ""

				run_count += 1
				#check if this run would go over max_run
				if run_count == max_run:
					compress_output += bbc_string(run_count, dirty_count, dirty_save,
					lit_count, literal_str, bit)
					#reset the variables
					lit_count = 0
					run_count = 0
					dirty_count = 0
					literal_str = ""

				#reset tick for new word
				tick = 0
				continue

			#code for if the word is a dirty bit
			if 0 <= dirty_loc <= 7:
				#if there is already literals the dirty bit doesnt matter
				if lit_count > 0:
					#if the literal was because of a dirty bit put the dirty
					#bit into the literal_str
					if dirty_count == 1:
						dirty_count = 0
						literal_str += f"{word_save}"
						word_save = ""
					lit_count += 1
					for j in word_chunk:
						literal_str += f"{j}"
				#this is our first dirty bit and no literals or other dirty bits
				else:
					#up lit count because this dirty bit could change
					lit_count = 1
					dirty_count = 1
					#if dirty bit is found save the location
					dirty_save = dirty_loc
					word_save = ""
					for j in word_chunk:
						word_save += f"{j}"	
				#check if max literals has already been met if so add the composed words
				#before dealing with this dirty bit
				if lit_count == max_lit:
					#if the lits have been maxed out dump the stored info and start reading
					#more write all runs being stored up till now
					compress_output += bbc_string(run_count, dirty_count, dirty_loc,
					lit_count, literal_str, bit)
					#reset the variables and start fresh
					lit_count = 0
					run_count = 0
					literal_str = ""

				#reset tick for new word
				tick = 0
				continue
	return compress_output

#################################_WAH_##########################################

def wah_string(run_count, run_num, word_size):
	output = ""
	output += "1"
	output += f"{run_num}"
	output += f"{(bin(run_count)[2:]).zfill(word_size-2)}"
	return output

def wah_lit_string(word_chunk):
	output = ""
	output += "0"
	for j in word_chunk:
		output += f"{j}"
	return output

def check_run(array):
	run_type = array[0]
	for bit in array:
		if bit != run_type:
			return -1
	return run_type	

def wah_compression(bit_array, word_size):
	#set up some variables for building as I read the bit_array in
	compress_output = ""
	#only for counting fills and literals
	fillcount = 0
	litcount = 0
	word_chunk = [0] * (word_size-1)
	tick = 0
	run_count = 0
	run_num = 0
	max_run = (math.pow(2, word_size-2))-1
	#read each bit in
	for bit in bit_array:
		#convert the bit to an int
		bit = int(bit)
		#check if the bit is the end of a string denoted internally by 2
		if bit == 2:
			#if this would result in adding a useless word dont add it
			if run_count > 0:
				#write all runs being stored up till now
				compress_output += wah_string(run_count, run_num, word_size)
				fillcount += 1
			#if a partial word is read in
			if tick > 0:
				#fill the current read in bits with trailing 0's
				word_chunk[tick-(word_size-1):] = [0] * ((word_size-1)-tick)
				#write the remaining bits as a literal
				compress_output += wah_lit_string(word_chunk)
				litcount += 1	
			#start a new stream with a '\n'
			compress_output += '\n'
			#reset the variables and start fresh
			tick = 0
			run_count = 0
			continue
		#place the bit in the word chuck
		word_chunk[tick] = bit
		tick += 1
		#only move on to the dificult checks after I have read in an entire word
		#for WAH this is wordsize-1
		if tick == word_size-1:
			if run_count == max_run:
				compress_output += wah_string(run_count, run_num, word_size)
				fillcount += 1
				run_count = 0
			runcheck = check_run(word_chunk)
			if runcheck == -1:
				#this is for literals
				if run_count > 0:
					compress_output += wah_string(run_count, run_num, word_size)
					fillcount += 1
					run_count = 0
				compress_output += wah_lit_string(word_chunk)
				litcount += 1
				tick = 0
				continue
			if runcheck and not run_count:
				#this is for the first run of 1's
				run_num = 1
				run_count = 1
				tick = 0
				continue
			if not runcheck and not run_count:
				#this is for the first run of 0's
				run_num = 0
				run_count = 1
				tick = 0
				continue	
			if runcheck and run_num:
				#this is for multiple 1's
				run_count += 1
				tick = 0
				continue
			if not runcheck and not run_num:
				#this is for multiple 0's
				run_count += 1
				tick = 0
				continue
			if runcheck and not run_num:
				#this is for a run of 1's after a run of 0's
				compress_output += wah_string(run_count, run_num, word_size)
				fillcount += 1
				run_count = 1
				run_num = 1
				tick = 0
				continue
			if not runcheck and run_num:
				#this is for a run of 0's after a run of 1's
				compress_output += wah_string(run_count, run_num, word_size)
				fillcount += 1
				run_count = 1
				run_num = 0
				tick = 0
				continue
	#only for printing the fills and literals counted
	#print(str(word_size)+"fills words: "+str(fillcount), "literal words: "+str(litcount))
	return compress_output

############################_BITMAP_COMPRESS_###################################

def compress_index(bitmap_index, output_path, compression_method, word_size):
	#we should expect the arguments of the types described above so I check for them

	#input as a string 
	if not isinstance(bitmap_index, str):
		sys.stderr.write("Error: argument 1 should be of type str")
		return -1

	#output file should be a str path to a directory
	if not isinstance(output_path, str):
		sys.stderr.write("Error: argument 2 should be of type str")
		return -1
	if not os.path.isdir(output_path):
		sys.stderr.write("Error: argument 2 should be a directory")
		return -1

	#compression_method for now should just equal "WAH" will implement BBC later
	#for extra credit
	if not isinstance(compression_method, str):
		sys.stderr.write("Error: argument 3 should be of type str")
		return -1
	if not (compression_method == "WAH" or compression_method == "BBC"):
		sys.stderr.write("Error: argument 3 can only be \"WAH\" or \"BBC\" right now")
		return -1

	#word_size just needs to be an int thats greater than 2 since WAH uses 1-2 bit
	#for headers
	if not isinstance(word_size, int):
		sys.stderr.write("Error: argument 4 should be of type int")
		return -1
	if not word_size > 2:
		sys.stderr.write("Error: argument 4 should be > 2")
		return -1

	#grab the file name of the input path for crafting filename of out
	true_infile = os.path.basename(bitmap_index)
	if compression_method == "BBC":
		#open files this returns a FILE type so it needs to be closed
		infile, outfile = open_inout(bitmap_index,
							output_path+f"/{true_infile}_{compression_method}_8",
							0)
	else:
		#open files this returns a FILE type so it needs to be closed
		infile, outfile = open_inout(bitmap_index,
							output_path+f"/{true_infile}_{compression_method}_{word_size}",
							0)
	if infile == -1:
		return -1

	#convert the bitmap file into a transposed array of bits with 2's denoting \n
	bit_array = transpose_bit_animal(infile)

	if compression_method == "WAH":
		outfile.write(wah_compression(bit_array, word_size))
	elif compression_method == "BBC":
		outfile.write(bbc_compression(bit_array))
	else:
		sys.stderr.write(f"Error: compression method {compression_method} is not supported")
		#close the files being used
		infile.close()
		outfile.close()
		return -1

	#close the files being used
	infile.close()
	outfile.close()
	return 0
