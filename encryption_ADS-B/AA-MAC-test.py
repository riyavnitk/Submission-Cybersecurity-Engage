def parse_adsb(msg):
    '''Function to parse an ADS-B message into its main components. The Function converts the hexadecimal message into to its binary string equivalent and processes it into the 5 ADS-B message components.
       The function takes 1 parameter: 
       @param msg: String value representing a legitimate 112-bit ADS-B data packet in hexadecimal format.
       @return: Returns a list of binary strings representing the ADS-B message
       components.
    '''
    msg = bin(int(msg,16))[2:]

    DF = ''
    CA = ''
    AA = ''
    Data = ''
    PI = ''
    for i in range(5):
        DF += msg[i]
    for i in range(5,8):
        CA += msg[i]
    for i in range(8,32):
        AA += msg[i]
    for i in range(32,88):
        Data += msg[i]
    for i in range(88,112):
        PI += msg[i]
    return [DF,CA,AA,Data,PI]


def create_block(hash, b_size=24): 
    '''Function to create a hash of the designated block size using bit-wise XOR.
    Note that this implementation is designed to be a simple demonstration and is not intended to be computationally efficient. There are certainly better data structures, such as mult-dimensional arrays, that would yield far more efficient algorithms than this iterative example.
    The function takes 1 required and 1 optional parameter:
    @param hash: String value representing a legitimate 112-bit ADS-B data
    packet in hexadecimal format.
    @param b_size: Integer value of the desired hash block size. The default
    value is 24.
    @return Returns binary string of length b_size.
    '''
    # convert the hexadecimal hash value into its binary string equivalent
    hash = bin(int(hash,16))[2:]
    # setup the values used to iterate over the binary hash string
    h_size = len(hash)
    idx = 0
    b_hash = 0
    # iterate over the binary hash in b_size increments and XOR the substrings
    if h_size%b_size != 0:
        n = h_size/b_size
    else:
        n = h_size/b_size - 1
    for i in range(n):
        idx += b_size
        if idx < h_size - b_size:
            b_hash = int(hash[idx:idx+b_size],2) ^ b_hash
        else:
            b_hash = int(hash[idx:],2) ^ b_hash
    return bin(b_hash)[2:]


def test_hash(msg, key, b_size=24, n=1000, xor=True): 
    '''Test function for detecting message authentication code failures, where the shortened hash is duplicated on distinctly different hash inputs. The message simulates a message error by randomly changing one of the 112 bits in the ADS-B message. The test compares the two hashes generated as the MAC to test for collisions due to the shortened hash. The function
    prints out the number of collisions detected as a percentage of the total number of iterations.
    The function takes 2 required and 3 optional parameters:
    @param msg: Hexadecimal string representing a legitimate 112-bit ADS-B data packet.
    @param key: String value of the secret authentication key.
    @param b_size: Integer value of the desired hash block size. The default value is 24.
    @param n: Integer value of the number of comparison iterations to perform. @param xor: Boolean value to determine if the create_block function is to
    be used to create the shortened MAC, or is a simple substring of the hash is to be used.
    '''
    import numpy as np
    from Crypto.Hash import MD5

    msg = parse_adsb(msg)[3]
    failure = 0
    for _ in range(n):
        # simulate error by modifying a random bit in msg
        i = np.random.randint(len(msg)) 
        if msg[i] == '0':
            msg_mod = msg[:i] + '1' + msg[i+1:]
        else:
            msg_mod = msg[:i] + '0' + msg[i+1:]
        h = MD5.new()
        h.update(msg+key)
        h_msg = h.hexdigest()
        h = MD5.new()
        h.update(msg_mod+key)
        h_msg_mod = h.hexdigest()
        
        if xor == True:
            test_msg = create_block(h_msg, b_size)
            test_msg_mod = create_block(h_msg_mod, b_size)
        else:
            test_msg = bin(int(h_msg,16))[2:b_size+2] 
            test_msg_mod = bin(int(h_msg_mod,16))[2:b_size+2]
        if test_msg == test_msg_mod:
            print(test_msg)
            print(test_msg_mod)
            print('\n')
            failure += 1
        if failure != 0:
            print('Failure percentage = {:.6f}%'.format(failure/float(n)))
        else:
            print('Test passed 100%')
