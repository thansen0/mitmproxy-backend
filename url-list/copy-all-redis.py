import redis
import configparser

def store_lines_in_redis(input_file_path, prefix, redis_host='localhost', redis_port=6379):
    print("Adding " + input_file_path + " with prefix " + prefix)
    try:
        # Connect to the Redis instance
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_auth, db=redis_db)

        with open(input_file_path, 'r') as input_file:
            for line in input_file:
                # Remove leading and trailing whitespaces from the line
                line = line.strip().lower()
                
                # Use the line as the key, and set a dummy value (e.g., "1") in Redis
                r.set(prefix+":"+line, "1")

        r.connection_pool.disconnect()
        print("Lines stored in Redis successfully.")
    except FileNotFoundError:
        print(f"Input file '{input_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('../server-code/redis-config.ini')

    #redis_host = 'localhost'  # Replace with your Redis server's host
    #redis_port = 6379  # Replace with your Redis server's port
    redis_host = config['REDIS']['redis_host']
    redis_port = int(config['REDIS']['redis_port'])
    redis_auth = config['REDIS']['redis_auth']
    redis_db = int(config['REDIS']['redis_db'])

    store_lines_in_redis("nsfw-sites.txt", "nsfw", redis_host, redis_port)
    store_lines_in_redis("nsfw-subs.txt", "nsfw:subreddit", redis_host, redis_port)

    store_lines_in_redis("trans-sites.txt", "trans", redis_host, redis_port)
    store_lines_in_redis("trans-subs.txt", "trans:subreddit", redis_host, redis_port)

    store_lines_in_redis("lgbt-sites.txt", "lgbt", redis_host, redis_port)
    store_lines_in_redis("lgbt-subs.txt", "lgbt:subreddit", redis_host, redis_port)

    store_lines_in_redis("genai-sites.txt", "genai", redis_host, redis_port)

    store_lines_in_redis("atheism-sites.txt", "atheism", redis_host, redis_port)
    store_lines_in_redis("atheism-subs.txt", "atheism:subreddit", redis_host, redis_port)

    store_lines_in_redis("weed-sites.txt", "weed", redis_host, redis_port)
    store_lines_in_redis("weed-subs.txt", "weed:subreddit", redis_host, redis_port)

    store_lines_in_redis("alcohol-sites.txt", "alcohol", redis_host, redis_port)
    store_lines_in_redis("alcohol-subs.txt", "alcohol:subreddit", redis_host, redis_port)

    store_lines_in_redis("tobacco-sites.txt", "tobacco", redis_host, redis_port)
    store_lines_in_redis("tobacco-subs.txt", "tobacco:subreddit", redis_host, redis_port)

    store_lines_in_redis("drug-sites.txt", "drug", redis_host, redis_port)
    store_lines_in_redis("drug-subs.txt", "drug:subreddit", redis_host, redis_port)

    store_lines_in_redis("childfree-subs.txt", "childfree:subreddit", redis_host, redis_port)

    store_lines_in_redis("antiwork-subs.txt", "antiwork:subreddit", redis_host, redis_port)

    store_lines_in_redis("antiparent-subs.txt", "antiparent:subreddit", redis_host, redis_port)

    store_lines_in_redis("nonmonogomy-subs.txt", "nonmonogomy:subreddit", redis_host, redis_port)

    store_lines_in_redis("shortvideo-sites.txt", "shortvideo", redis_host, redis_port)
    store_lines_in_redis("shortvideo-subs.txt", "shortvideo:subreddit", redis_host, redis_port)

    store_lines_in_redis("suicide-subs.txt", "suicide:subreddit", redis_host, redis_port)

    store_lines_in_redis("gambling-sites.txt", "gambling", redis_host, redis_port)
    store_lines_in_redis("gambling-subs.txt", "gambling:subreddit", redis_host, redis_port)

    store_lines_in_redis("socialism-sites.txt", "socialism", redis_host, redis_port)
    store_lines_in_redis("socialism-subs.txt", "socialism:subreddit", redis_host, redis_port)

    store_lines_in_redis("communism-sites.txt", "communism", redis_host, redis_port)
    store_lines_in_redis("communism-subs.txt", "communism:subreddit", redis_host, redis_port)
