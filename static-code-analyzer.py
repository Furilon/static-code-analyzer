import sys
import utils
import analyzer


if __name__ == "__main__":
    # Check if correct number of arguments
    utils.is_correct_length(len(sys.argv))
    
    # Get path from stdin
    path = utils.get_path()

    # Check if path is file or directory
    analyzer.main(path)
