import time

def prevent_user_input(seconds):
    end_time = time.time() + seconds
    while time.time() < end_time:
        pass

# Execute the sleep command
prevent_user_input(5)

# Allow user input again
input("User input is allowed now.")