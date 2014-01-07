import ctypes
from pathes import PATHES

dll = ctypes.cdll.LoadLibrary(PATHES['BASE'] + r'\cpp\trie.dll')


class Trie():
    def __init__(self):
        self._create_trie = dll.create_trie
        self._delete_obj = dll.delete_obj
        self._insert = dll.insert
        self._find = dll.find
        self._find_longest_prefix = dll.find_longest_prefix
        self._tokenize = dll.tokenize
        self._tokenize_indices = dll.tokenize_indices

        self.trie = self._create_trie()

    def close(self):
        self._delete_obj(self.trie)
        self.trie = None

    def insert(self, word, index):
        return self._insert(self.trie, word, index)

    def find(self, word):
        return self._find(self.trie, word)


    def get_index(self, node):
        return dll.get_node_index(node)

    def load_file(self, fname, word_col=1, index_col=0):
        with open(fname, "r") as fin:
            for line in fin:
                line = line.strip()
                if line and not line.startswith('#'):
                    tokens = line.split(' ')    # word index number
                    self._insert(self.trie, tokens[word_col], int(tokens[index_col]))

    def tokenize_old(self, s="", return_indices = True):
        i = 0
        a = []
        s_len = len(s)
        while i < s_len:
            d = ctypes.c_int(-1)
            index = ctypes.c_int(-1)
##            if "Is this the case? Has no treatment since 1920 done anything to increase the chance" in s[i:]:
##                print s[i:]
            text = s[i:]
            text_len = len(text)
            n = self._find_longest_prefix(self.trie, text, text_len, ctypes.pointer(index), ctypes.pointer(d))
            if n:
                if not return_indices:
                    a.extend([s[i:i+d.value]])
                else:
                    a.extend([index.value])
                i += d.value
            else:
                i += 1

        return a

    def tokenize(self, s="", return_indices = True):
        s_len = len(s)
        result = []
        tokens = ctypes.c_void_p(0)
        tokens_len = ctypes.c_int(0)
        if not return_indices:
            self._tokenize(self.trie, s, s_len, ctypes.addressof(tokens), ctypes.addressof(tokens_len))
            array_of_strings = ctypes.cast(tokens, ctypes.POINTER(ctypes.c_char_p*tokens_len.value))

            for i in range(tokens_len.value):
                result.append(array_of_strings.contents[i])
            # free memory
            dll.delete_vector(tokens, tokens_len)
        else:
            self._tokenize_indices(self.trie, s, s_len, ctypes.addressof(tokens), ctypes.addressof(tokens_len))
            array_of_int = ctypes.cast(tokens, ctypes.POINTER(ctypes.c_int*tokens_len.value))

            for i in range(tokens_len.value):
                result.append(array_of_int.contents[i])
            self._delete_obj(tokens)

        return result


def main():
    d=Trie()
    d.insert("", -1)
    d.insert("max", 0)
    d.insert("home", 1)
    d.insert("homeless", 2)
    d.insert("less", 3)
    d.insert("at", 4)
    d.insert("c++", 5)
    d.insert("c#", 6)
    n = d.insert("too", 7)


    assert(not d.find(""))
    assert(d.find("max"))
    assert(not d.find("maxim"))
    assert(d.find("home"))
    assert(d.find("less"))
    assert(d.find("homeless"))
    d.close()



    dic = Trie()
    dic.insert("have", 0)
    dic.insert("submitting", 1)
    dic.insert('via', 2)
    dic.insert('http', 3)
    dic.insert('ajax',4)
    s = "<p>so i -have  form that I amsubmitting++ *via* <a href=\"http://jquery.malsup.com/form/#ajaxSubmit\" rel=\"nofollow\">jQuery form's ajaxSubmit</a> it was working fine until I tried to put in text that is over 5100 characters long any idea why  this would be a problem ?</p> <p>this is what shows up in the error console</p> <p>Error: no element found Source File: <a href=\"https://myebsite/\" rel=\"nofollow\">https://myebsite/</a> Line: 1</p> <p>and this is that line </p> <p>ok I found the problem but I don't understand why the name of the field was \"summary\" if I change it to anything else the problem goes away</p> <p><strong>New Edit</strong></p> <p>well this gets stranger changing the name only works until I save my js file then it breaks again. also I Can't post this</p> <pre><code>  newteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststory </code></pre> <p><strong>BUT</strong> i can post this</p> <pre><code> &lt;p&gt; newteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststorynewteststory&lt;/p&gt; </code></pre> <p>which is just wrapping it in a paragraph tag wtf ?</p>"
    print len(s)
    print "old: ", dic.tokenize_old(s)
    print "new: ", dic.tokenize(s)
    d.close()

    dic = Trie()
    s = "MaximAlekseykin c++ or c#"
    dic.insert("Maxim", 0)
    dic.insert("Aleks", 1)
    dic.insert('Max', 2)
    dic.insert('Aleksey', 3)
    dic.insert('Alekseykin',4)
    dic.insert('c#', 5)
    print dic.tokenize(s, return_indices=False)
    d.close()

    d=Trie()
    d.load_file(r'C:\Kaggle\FB3\dicts\Word_stem.txt')
    s='''@ changing to inverted question mark after urlencode
<p>In my sms sending script, I found out that when
an @ symbol is typed it gets changed to an inverted
question mark in the recipient's phone.</p>

<p>The message has to be urlencoded before
sending.</p>'''
    print "old: ", d.tokenize_old(s, return_indices=False)
    print "new: ", d.tokenize(s, return_indices=False)

if __name__ == '__main__':
    main()
