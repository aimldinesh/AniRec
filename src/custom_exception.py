# Import required modules for error handling
import traceback
import sys


# Define a custom exception class to enhance error messages
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # Initialize the base Exception with the original error message
        super().__init__(error_message)

        # Create a detailed error message including file name and line number
        self.error_message = self.get_detailed_error_message(
            error_message, error_detail
        )

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        """
        Generates a detailed error message with traceback info.
        """
        # Get exception traceback object
        _, _, exc_tb = traceback.sys.exc_info()

        # Extract the file name and line number where the exception occurred
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        # Return a formatted string with error context
        return f"Error in {file_name} , line {line_number} : {error_message}"

    def __str__(self):
        # String representation of the custom exception
        return self.error_message
