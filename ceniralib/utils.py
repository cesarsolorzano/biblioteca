

def text_pieces(string):
	pieces = []
	for word in string.split():
		cursor = 1
		while True:
			# this method produces pieces of 'TEXT' as 'T,TE,TEX,TEXT'
			pieces.append(word[:cursor])
			if cursor == len(word):
				break
			cursor += 1

	return ','.join(pieces)