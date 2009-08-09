# encoding: utf-8

from optparse import OptionParser
import sys

class Cheshire(object):
    """Cheshire, a class for simple Caesar-cipher-like encryption.
    
    Cheshire, depending on use, is a very complex form of Caesar-cipher.
    It has superb security if used with a properly random passphrase and
    completely random alphabet.  The encrypted result usualy has a
    uniform character distribution.
    
    Cheshire was chosen as the name due to the polymorphing ability of
    the cipher.  For example, with an ordered alphabet and a passphrase
    length of one, Cheshire is a simple Caesar cipher.  Using a
    passphrase the same length as the message to encode, Cheshire is an
    unbreakable one-time-pad.  Cheshire supports passphrase repitition
    and autokeying, too.
    
    The entire Cheshire cipher is implementable as one fixed, and two
    free-spinning alphabetic wheels.
    
    B{Note:} All characters in the passphrase and message body B{must}
    be present in the alphabet.
    
    >>> alphabet = "QWERTYUIOPASDFGH JKLZXCVBNM,."
    >>> cat = Cheshire("MY KEYPHRASE", alphabet)
    >>> cat.encode("HELLO WORLD.")
    'KMRWUSXCQPWM'
    >>> cat.decode(" Y F.MATFDXQPGQDU,AMN")
    'FAREWELL CREUL WORLD.'
    
    Using Cheshire as an overkill ROT-13:
    
    >>> alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    >>> cat = Cheshire("N", alphabet)
    >>> cat.encode("HELLO WORLD.")
    'URYYB JBEYQ.'
    >>> cat.decode("SNERJRYY PERHY JBEYQ.")
    'FAREWELL CREUL WORLD.'
    """
    
    def __init__(self, keys, alphabet, autokey = False):
        """Initialize the Cheshire cipher.
        
        All characters in the keyphrase B{must} be present in the
        alphabet.
        
        @param keys: The keyphrase.  This can be a string, or a list or
                     tuple of individual characters.
        
        @param alphabet: The alphabet.
        @type alphabet: string
        
        @param autokey: Enable or disable autokeying.
        @type autokey: bool
        """
        
        self.keys = keys
        self.alphabet = alphabet
        self.autokey = autokey
    
    def rotate(self, offset):
        """Rotate the alphabet by a given offset.
        
        @param offset: The offset by which to rotate the alphabet.
        @type offset: int
        
        @return: Returns the untrimmed, rotated alphabet.
        @rtype: string
        """
        
        return self.alphabet[offset:] + self.alphabet[:offset]
    
    def encode(self, text):
        """Encode a block of plaintext using the passphrase and alphabet.
        
        @param text: The plaintext block to encode.
        @type text: string
        
        @return: Returns the cyphertext representation of the plaintext.
        @rtype: string
        """
        
        cyphertext = list()
        
        for i in xrange(len(text)):
            if not self.autokey or i < len(self.keys):
                alphabet = self.rotate(self.alphabet.index(self.keys[i%len(self.keys)]))
            else:
                alphabet = self.rotate(self.alphabet.index(text[i-len(self.keys)]))
            
            if self.alphabet.find(text[i]) < 0:
                cyphertext.append(text[i])
                continue
            
            cyphertext.append(self.alphabet[alphabet.index(text[i])])
        
        return "".join(cyphertext)
    
    def decode(self, text):
        """Decode a block of ciphertext using the passphrase and alphabet.
        
        @param text: The ciphertext block to decode.
        @type text: string
        
        @return: Returns the plaintext representation of the ciphertext.
        @rtype: string
        """

        cleartext = list()
        
        for i in xrange(len(text)):
            if not self.autokey or i < len(self.keys):
                alphabet = self.rotate(self.alphabet.index(self.keys[i%len(self.keys)]))
            else:
                alphabet = self.rotate(self.alphabet.index(cleartext[i-len(self.keys)]))
            
            if self.alphabet.find(text[i]) < 0:
                cleartext.append(text[i])
                continue
            
            cleartext.append(alphabet[self.alphabet.index(text[i])])
        
        return "".join(cleartext)


if __name__ == "__main__":
    base_alphabet = '''T&#LAt=~M$:c- hD]ZB|S+rfk7_}1J[,\0HW
obj(3Y"m?C'2e{vFaK5GE/^z<Xs.Rix wdp>8PlV4!u*n;9Og)6UQyqN@I%'''
    
    # Step 1: Decode command-line arguments.
    parser = OptionParser(usage="%prog [-Adev] [--help] [-a alphabet] [--] <keyphrase> [filename]", version="%prog 1.0")
    parser.add_option("-a", "--alphabet", dest="alphabet", default=base_alphabet,
            help="use a custom ALPHABET", metavar="ALPHABET")
    parser.add_option("-A", "--auto-key", action="store_true", dest="autokey", default=False,
            help="use plaintext to continue the keyphrase")
    parser.add_option("-e", "--encode", action="store_true", dest="encode", default=True,
            help="encode the given input or file (default)")
    parser.add_option("-d", "--decode", action="store_false", dest="encode",
            help="decode the given input or file")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
            help="display process analysis")
    parser.add_option("-i", "--ignore-errors", action="store_true", dest="ignore", default=False,
            help="ignore invalid characters in keyphrase and text")
    
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("You must supply a keyphrase.")
    
    if len(args) > 2:
        parser.error("Supply at most one input file.")
    
    keyphrase = args[0]
    keys = list()
    
    for i in xrange(len(options.alphabet)):
        if base_alphabet.count(options.alphabet[i]) != 1:
            parser.error("More than one occurance of the character '%s' in alphabet." % options.alphabet[i])
    
    for i in xrange(len(keyphrase)):
        if base_alphabet.find(keyphrase[i]) < 0:
            if not options.ignore:
                parser.error("Invalid character '%s' in keyphrase." % keyphrase[i])
        else: keys.append(keyphrase[i])
    
    if len(keys) == 0:
        parser.error("No valid characters in keyphrase.")
    
    # Load the plaintext/ciphertext from the selected file, or stdin.
    if len(args) == 2: file = open(args[1])
    else: file = sys.stdin
    
    text = file.read()
    cheshire = Cheshire(keys, options.alphabet, options.autokey)
    
    if options.encode:
        result = cheshire.encode(text)
        print result
    
    else:
        result = cheshire.decode(text)
        print result
    
    if options.verbose:
        print >> sys.stderr, "Character frequency analysis:"
        
        characters = dict()
        for char in options.alphabet:
            characters[char] = [0.0, 0.0]
        
        for char in text:
            if char in characters: characters[char][0] += 1
        
        for char in result:
            if char in characters: characters[char][1] += 1
        
        source_len = len(text)
        result_len = len(result)
        
        items = [(v, k) for k, v in characters.items()]
        items.sort()
        items.reverse()
        items = [(k, v) for v, k in items]
        
        for char, counts in items:
            print >> sys.stderr, "Character: %s\tSource: %d (%0.2f)\tDestination: %d (%0.2f)" % ( char, counts[0], counts[0]/source_len*100, counts[1], counts[1]/source_len*100 )
    
    sys.exit()