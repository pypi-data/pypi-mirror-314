#   ***  *******************************************************
#   ***  REVERSION : JANE ESSADI                            ****
#   ***  *******************************************************

# Constants for py_visual_cobol project
# This file holds the static values that are used across the project.


# Each record in a variable structure file is preceded by a two- or four-byte record header. 
# The first four bits of this indicate the status of the record, for example, a value of 0100 means
# that this record is a normal user data record.
NORMAL_USER_DATA_RECORD_PREFIX = "0100"
# System record
SYSTEM_RECORD_PREFIX = "0011"


# Length of the file header. The first 4 bits are always set to 3 (0011 in binary) 
# indicating that this is a system record. The remaining bits contain the length of 
# the file header record, unless the file is an indexed file type that does not include a 
# separate index file (such as IDXFORMAT8); for those types of file, see Index File - File Header.
#  If the maximum record length is less than 4095 bytes, the length is 126 and is held in the next 12 bits;
#  otherwise it is 124 and is held in the next 28 bits. Hence, in a file where the maximum record length is less than 4095 bytes,
#  this field contains x"30 7E 00 00". Otherwise, this field contains x"30 00 00 7C".
MAX_RECORD_LENGTH = 0xFFF  # -> int(0xFFF) = 4095


#  If the maximum record length is less than 4095 bytes, the length is 126 and is held in the next 12 bits;
#  otherwise it is 124 and is held in the next 28 bits.
FILE_HEADER_LENGTH = 126