
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define bool int


struct node {
   bool end_of_word;
   struct node* children[256];
   int index;
};

struct trie {
   struct node *root;
   int number_of_words;
};


__declspec(dllexport)
struct trie* create_trie() {
   struct trie* t = (struct trie*)malloc(sizeof(struct trie));
   struct node* r = (struct node*)malloc(sizeof(struct node));
   memset(r, 0, sizeof(struct node));
   t->root = r;
   t->number_of_words = 0;
   return t;
}

__declspec(dllexport)
void delete_obj(void* p) {
   free(p);
}

__declspec(dllexport)
void delete_vector(const char** p, size_t size) {
	// deletes a vector of const char*
	for (int i = 0; i < size; ++i)
		free((void*)p[i]);
	free(p);
}





__declspec(dllexport)
struct node* insert(struct trie* t, const char* word, int index) {
	size_t len = strlen(word);
	if (!len)
		return NULL;
	struct node *n = t->root;
	for (int i = 0; i < len; ++i) {
		if (NULL != n->children[ (unsigned char)word[i] ]) {
			n = n->children[ (unsigned char)word[i] ];
		}else{
			struct node* tmp = (struct node*)malloc(sizeof(struct node));
			memset(tmp, 0, sizeof(struct node));
			n->children[ (unsigned char)word[i] ] = tmp;
			n = tmp;
		}
			
	}
	n->end_of_word = 1;
	n->index = index;
	return n;
}


__declspec(dllexport)
struct node* find(struct trie* t, const char* word) {
	struct node *n = t->root;
	for (int i = 0; i < strlen(word); ++i) {
		if (NULL != n->children[ (unsigned char)word[i] ]) {
			n = n->children[ (unsigned char)word[i] ];
		}else{
			n = NULL;
			break;
		}
	}
	if (n && !n->end_of_word)
		n = NULL;
	return n;
}

__declspec(dllexport)
struct node* find_longest_prefix(struct trie* t, const char* text, int text_len, int* index, int* depth) {
	struct node* n = t->root;
	struct node* prev = NULL;
	int prev_depth = 0;
	int curr_depth = 0;

	for (int i = 0; i < text_len; ++i) {
		if (NULL != n->children[ (unsigned char)text[i] ]) {
			n = n->children[ (unsigned char)text[i] ];
			curr_depth += 1;
			if (n->end_of_word) {
				prev = n;
				prev_depth = curr_depth;
			}
		}else{
			break;
		}
	}
	if (prev) {
		*index = prev->index;
		*depth = prev_depth;
	}
	return prev;
}


__declspec(dllexport)
int get_node_index(struct node* n) {
	return n->index;
}



const char** alloc_vector(const char** existing_vector, size_t size) {
	return (const char**)realloc((void*)existing_vector,
				size * sizeof(const char*)); 
}



__declspec(dllexport)
void tokenize(struct trie* t, const char* text, int text_len, const char*** tokens, int* length) {
	int current_capacity = 128;
	const char** vector = alloc_vector(NULL, current_capacity);
	int number_of_tokens = 0;

	int i = 0;
	int depth = 0;
	int index = 0;
	int current_length = text_len;
	const char* current_text = text;

	while (i < text_len) {
		current_text = text + i;
		current_length = text_len - i;

		struct node* n = find_longest_prefix(t, current_text, current_length, &index, &depth);
		if (n) {
			if (number_of_tokens == current_capacity) {
				current_capacity *= 2;
				vector = alloc_vector(vector, current_capacity);	
			}
			char* token = (char*)malloc(depth+1);
			memcpy(token, current_text, depth);
			token[depth] = 0;
			
			vector[number_of_tokens] = token;
			++number_of_tokens;

			i += depth;
		}else{
			++i;
		}
	}
	*tokens = vector;
	*length = number_of_tokens;
}


__declspec(dllexport)
void tokenize_indices(struct trie* t, const char* text, int text_len, const int** tokens, int *length) {
        int current_capacity = 256;
        int* vector = (int*)realloc(NULL, current_capacity*sizeof(int));
        int number_of_tokens = 0;

        int i = 0;
        int depth = 0;
        int index = 0;
        int current_length = text_len;
        const char* current_text = text;

        while (i < text_len) {
                current_text = text + i;
                current_length = text_len - i;

                struct node* n = find_longest_prefix(t, current_text, current_length, &index, &depth);
                if (n) {
                        if (number_of_tokens == current_capacity) {
                                current_capacity *= 2;
                                vector = (int*)realloc(vector, current_capacity*sizeof(int));
                        }

                        vector[number_of_tokens] = n->index;
                        ++number_of_tokens;

                        i += depth;
                }else{
                        ++i;
                }
        }
        *tokens = vector;
        *length = number_of_tokens;
}











