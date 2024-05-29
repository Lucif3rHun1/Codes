import os
import concurrent.futures

def get_cpu_count():
    return os.cpu_count()

def suggest_thread_count():
    cpu_count = get_cpu_count()
    print(f"Your system has {cpu_count} CPU cores.")
    
    suggested_threads = max(1, min(cpu_count - 1, 4))  # Suggest using all cores but one, up to a maximum of 4 threads
    print(f"Suggested number of threads: {suggested_threads}")
    
    user_input = input("Enter the number of threads to use (or press Enter to use the suggested value): ")
    
    if user_input.strip():  # If the user provides input, use that value
        return int(user_input)
    else:
        return suggested_threads

def make_request(thread_id):
    # Implement your request logic here
    print(f"Thread {thread_id} is making a request.")

if __name__ == "__main__":
    num_threads = suggest_thread_count()

    # Use ThreadPoolExecutor for parallel requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(make_request, thread_id) for thread_id in range(num_threads)]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
