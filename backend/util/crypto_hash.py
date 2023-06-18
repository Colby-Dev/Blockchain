import hashlib
import json

def crypto_hash(*args):
    '''
    :param data: Blockchain data
    :return: sha-256 hash of the input parameters
    '''
    # string_data = json.dumps(data)
    # return hashlib.sha256(string_data.encode('utf-8'))

    stringed_data = sorted(map(lambda data: json.dumps(data), args))
    joined_string_data = ''.join(stringed_data)

    # print(joined_string_data)

    return hashlib.sha256(joined_string_data.encode('utf-8')).hexdigest()



def main():
    print(f'hashing test: {crypto_hash("one", {"a key":2}, 3)}')
    print(f'hashing test 2: {crypto_hash(3, {"a key":2}, "one")}')


if __name__ == '__main__':
    main()