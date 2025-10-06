Example of Destructor code:
---------------------------
free the memory in Destructor.

struct Node {
    Node* links[26];
    int cntEndWith = 0;
    int cntPrefix = 0; 

    bool containsKey(char ch) {
        return (links[ch - 'a'] != NULL); 
    }

    Node* get(char ch) {
        return links[ch - 'a']; 
    }

    void put(char ch, Node* node) {
        links[ch - 'a'] = node;
    }
    
    ~Node() {
        for (int i=0; i<26; ++i) {
            delete links[i];
        }
    }
};

class Trie {
    private:
        Node* root; 

    public:
        Trie() {
            root = new Node();
        }
        
        ~Trie() { delete root; }
        
        int computeValue(string& word) {
            int exist = 0;
            for (int i = 0; i < word.size(); i++) {
                Node* node = root;
                for (int j = i; j < word.size(); j++) {
                    if (!node->containsKey(word[j])) {
                        node->put(word[j], new Node());
                        exist++;
                    }
                    node = node->get(word[j]);
                }
				// delete node; it is wrong. we should not delete memory from active Instance. 
            }
            return exist+1;
        }
};


int countDistinctSubstring(string s) {
    Trie* trie = new Trie();
    int ans = trie->computeValue(s);
    delete trie;   // ✅ proper cleanup
    return ans;
}


Most important:
--------------
1. You must NOT delete node inside the loop
	delete node;
	This line is wrong.
	node points to part of your active trie. When you delete it, you are corrupting the trie structure. The next substring insertion tries to access freed memory → runtime error or memory corruption.
	👉 The memory should only be freed when you’re done with the entire trie, not while still building it.