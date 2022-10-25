def process_word(word):
    letras = "abcdefghijklmnopqrstuvwxyzñáéíóú"
    new_word = ""
    for c in word:
        if c in letras:
            new_word = new_word + c
        else:
            new_word = new_word + '.'
    return new_word.strip('.')
  
class DataRecovery():
      
    stop_list = []
    stemmer = SnowballStemmer('spanish')
    tokenizer = ToktokTokenizer()
    N = 0  # Cantidad de tweets
    n_terms = 0  # Cantidad de terminos

    map_score = {}
    list_keys = []
    map_tweets = {}
    max_score = 0
    
    def _init_(self):
        pass
  
    def get_stem(self, word):
        return self.stemmer.stem(word.lower())
    def __save_in_file_aux(self, local_map, path):
        local_map_keys = local_map.keys()
        local_map_keys = sorted(local_map_keys)
        with open(path, 'w', encoding="utf-8") as file_aux_out:
            for key in local_map_keys:
                file_aux_out.write(json.dumps(
                    {key: local_map[key]}, ensure_ascii=False))
                file_aux_out.write("\n")
            file_aux_out.close()
            
    def __save_in_file_norm(self, frecuency_map, id):
        with open(path_norm_doc, 'a', encoding="utf-8") as file_norm_out:
            id_sum = 0
            for key in frecuency_map:
                id_sum = id_sum + \
                    log10(frecuency_map[key]+1) * log10(frecuency_map[key]+1)
            id_sum = sqrt(id_sum)
            file_norm_out.write(json.dumps({id: id_sum}, ensure_ascii=False))
            file_norm_out.write("\n")
            file_norm_out.close()

  
    def load(self):
        open(path_file_data, 'w').close()
        open(path_norm_doc, 'w').close()
        local_map = {}
        size_of_local_map = 0
        id_file_aux = 1
        size = 0
        self.N = 0
        print("Generando archivos auxiliares")
        for f in listdir(path_data_in):
            file_in = join(path_data_in, f)
            if isfile(file_in):
                with open(file_in, 'r', encoding="utf-8") as file_to_load:
                    for tweet in file_to_load:
                        tweet = tweet.rstrip()
                        json_tweet = json.load(io.StringIO(tweet))
                        tweet_id = json_tweet.get("id")
                        tweet_text = json_tweet.get("text").lower() if json_tweet.get(
                            "RT_text") == None else json_tweet.get("RT_text").lower()
                        tweet_words = self.tokenizer.tokenize(tweet_text)
                        frecuency_map = {}
                        for tweet_word in tweet_words:
                            if tweet_word in self.stop_list:
                                continue
                            tweet_word = process_word(tweet_word)
                            if tweet_word == "":
                                continue
                            if '.' in tweet_word:
                                pos = tweet_word.find('.')
                                rest_word = tweet_word[pos+1:]
                                if rest_word != "":
                                    tweet_words.append(rest_word)
                                tweet_word = tweet_word[:pos]
                            if tweet_word == "":
                                continue
                            if tweet_word in self.stop_list:
                                continue
                            tweet_word_root = self.get_stem(tweet_word)
                            if tweet_word_root in local_map:
                                if tweet_id in local_map[tweet_word_root]:
                                    local_map[tweet_word_root][tweet_id] = local_map[tweet_word_root][tweet_id] + 1
                                else:
                                    size = size + 1
                                    local_map[tweet_word_root][tweet_id] = 1
                                    size_of_local_map = size_of_local_map + \
                                        len(str(tweet_id)) + 6
                            else:
                                size = size + 1
                                local_map[tweet_word_root] = {tweet_id: 1}
                                size_of_local_map = size_of_local_map + \
                                    len(str(tweet_id)) + 1 + \
                                    len(tweet_word_root) + 8
                            if size_of_local_map > MAX_TERMS_IN_MAP:
                                self.__save_in_file_aux(
                                    local_map, path_file_aux + str(id_file_aux) + path_file_aux_end)
                                local_map.clear()
                                size_of_local_map = 0
                                id_file_aux = id_file_aux + 1
                            if tweet_word_root in frecuency_map:
                                frecuency_map[tweet_word_root] = frecuency_map[tweet_word_root] + 1
                            else:
                                frecuency_map[tweet_word_root] = 1
                        self.__save_in_file_norm(frecuency_map, tweet_id)
                        self.N = self.N + 1
                    file_to_load.close()
        if len(local_map) > 0:
            self.__save_in_file_aux(local_map, path_file_aux +
                                    str(id_file_aux) + path_file_aux_end)
        print(str(id_file_aux) +
              " archivos auxiliares generados. Generando archivo único")
