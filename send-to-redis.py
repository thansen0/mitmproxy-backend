from nsfw_detector import predict
import redis

def store_lines_in_redis(input_file_path, redis_host='localhost', redis_port=6379):
    try:
        # Connect to the Redis instance
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_auth, db=redis_db)

        with open(input_file_path, 'r') as input_file:
            for line in input_file:
                # Remove leading and trailing whitespaces from the line
                line = line.strip().lower()
                
                # Use the line as the key, and set a dummy value (e.g., "1") in Redis
                r.set(line, "1")

        print("Lines stored in Redis successfully.")
    except FileNotFoundError:
        print(f"Input file '{input_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('redis-config.ini')

    #redis_host = 'localhost'  # Replace with your Redis server's host
    #redis_port = 6379  # Replace with your Redis server's port
    redis_host = config['REDIS']['redis_host']
    redis_port = int(config['REDIS']['redis_port'])
    redis_auth = config['REDIS']['redis_auth']
    redis_db = int(config['REDIS']['redis_db'])

    input_file_path = "nsfw-subs.txt"  # Replace with your output file path
    store_lines_in_redis(input_file_path, redis_host, redis_port)

