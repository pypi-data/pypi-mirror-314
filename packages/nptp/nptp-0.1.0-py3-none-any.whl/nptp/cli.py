import argparse
import os
import sys
import logging

# logging for developer specific errors.
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', filename='app_error.log')

# func: process_file
# args: file_path, output_file (def: None)
# returns: Boolean value (True if the file readable)
def process_file(file_path, output_file=None):
    # Ensure the file exists and handle FileNotFoundError
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return False
    
    # Checking if the file is readable
    if not os.access(file_path, os.R_OK):
        print(f"Error: Cannot read the file {file_path}. Permission denied.")
        return False
    
    try:
        # opens and closes a file when done
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
            # Check if file is empty or improperly formatted (index testing)
            if len(lines) == 0 or all(line.strip() == "" for line in lines):
                print(f"Error: The file {file_path} is empty or improperly formatted.")
                return False
            
            # Process each line of content of a file
            for index, line in enumerate(lines):
                if index < len(lines):
                    print(f"Processing line {index}: {line.strip()}")
                else:
                    print(f"Error: Out-of-bounds index access at line {index}.")
                    return False
                
            # Write to output file if specified
            if output_file:
                try:
                    with open(output_file, 'w') as out_f:
                        out_f.writelines(lines)
                except PermissionError:
                    print(f"Error: Cannot write to the output file {output_file}. Permission denied.")
                    return False
                except Exception as e:
                    print(f"Error: An error occurred while writing to the output file.")
                    logging.error(f"Error writing to output file: {e}")
                    return False

    except Exception as e:
        print(f"Error: An unexpected error occurred while processing the file.")
        logging.error(f"Unexpected error while processing file {file_path}: {e}")
        return False

    return True  # Return True if everything works fine

# Type testing: Check for non-existing files, incorrect argument types (jpg, png, gif), and corrupted files
def type_testing(file_path):
    if not isinstance(file_path, str):
        print("Error: Invalid argument type. The file path must be a string.")
        return False
    if not os.path.isfile(file_path):
        print(f"Error: The specified file {file_path} does not exist.")
        return False
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if content is None:
                print(f"Error: The file {file_path} seems corrupted or empty.")
                return False
    except Exception as e:
        print(f"Error: An error occurred while handling the file.")
        logging.error(f"Error handling file {file_path}: {e}")
        return False

    return True

# Input/Output Testing: Checking for read/write permissions 
def input_output_testing(file_path, output_path):
    # Test file read permission
    if not os.access(file_path, os.R_OK):
        print(f"Error: No read permission for file {file_path}.")
        return False

    # Test write permission for the output file
    if not os.access(os.path.dirname(output_path), os.W_OK):
        print(f"Error: No write permission for directory of output file {output_path}.")
        return False
    
    # Attempt to write output file
    try:
        with open(output_path, 'w') as out_f:
            out_f.write("Test write permissions and file handling.")
            print(f"Data written successfully to {output_path}")
    except PermissionError:
        print(f"Error: Permission denied while trying to write to {output_path}.")
        return False
    except Exception as e:
        print(f"Error: An error occurred while writing to the output file.")
        logging.error(f"Error writing to output file {output_path}: {e}")
        return False

    return True

# func: get_stats()
# arg: file_loc (file path)
# return: count of lines, words & characters
#         Else
#         FileNotFound or RuntimeErrorExceptions
def get_stats(file_loc):
    """Calculate lines, words, and characters in a file."""
    try:
        with open(file_loc, 'r') as file:
            content = file.readlines()

        # If file is empty
        if not content:
            raise RuntimeError(f"The file '{file_loc}' is empty.")

        # count the no. of lines
        lines = len(content)
        
        # break each line and count no. of words (handling multiple spaces)
        words = sum(len(line.split()) for line in content)
        
        # break each word in a line and count no. of characters
        characters = sum(len(line) for line in content)
        
        # return count of lines, words & characters
        return lines, words, characters
    
    except Exception as e:
        print(f"Error: An unexpected error occurred while processing the file.")
        logging.error(f"Unexpected error while processing file {file_loc}: {e}")
        return None, None, None

def main():
    """Main function for command-line interface (CLI)."""
    if len(sys.argv) < 2:
        print("Usage: python __main__.py <file_path> [output_path]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Performing type testing
    if not type_testing(input_file_path):
        return

    # Run the file processing with I/O and indexing checks
    if not process_file(input_file_path, output_file_path):
        return

    # Input/Output testing for file read/write operations
    if output_file_path and not input_output_testing(input_file_path, output_file_path):
        return

    # Calculate and display file statistics (lines, words, characters)
    lines, words, characters = get_stats(input_file_path)
    if lines is not None and words is not None and characters is not None:
        print(f"{lines} lines, {words} words, {characters} characters")

if __name__ == "__main__":
    main()