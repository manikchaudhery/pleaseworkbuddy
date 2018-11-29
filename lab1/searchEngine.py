        words = WORD_SEPARATORS.split(elem.string.lower())
        for word in words:
            word = word.strip()
            if word in self._ignored_words:
                continue
            self._curr_words.append((self.word_id(word), self._font_size))

	    #Map word_id to the current documentID
        word_id = self.word_id(word)
        if word_id in self._inverted_index:
            self._inverted_index[word_id].add(self._curr_doc_id)
        else:
            self._inverted_index[word_id] = {self._curr_doc_id}

	    #Map each word to the current url
        if word in self._resolved_inverted_index:
            self._resolved_inverted_index[str(word)].add(self._curr_url)
        else:
            self._resolved_inverted_index[str(word)] = {self._curr_url}
