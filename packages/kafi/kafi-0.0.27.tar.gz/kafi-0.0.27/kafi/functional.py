# Constants

ALL_MESSAGES = -1

#

class Functional:
    def foldl(self, topic, foldl_function, initial_acc, n=ALL_MESSAGES, **kwargs):
        verbose_int = self.verbose()
        #
        progress_num_messages_int = self.progress_num_messages()
        #
        consumer = self.consumer(topic, **kwargs)
        #
        def foldl_function1(acc_consume_message_counter_int_tuple, message_dict):
            (acc, consume_message_counter_int) = acc_consume_message_counter_int_tuple
            #
            acc = foldl_function(acc, message_dict)
            #
            consume_message_counter_int += 1
            if verbose_int > 0 and consume_message_counter_int % progress_num_messages_int == 0:
                print(f"Read: {consume_message_counter_int}")
            #
            return (acc, consume_message_counter_int)
        #
        acc_consume_message_counter_int_tuple = consumer.foldl(foldl_function1, (initial_acc, 0), n, **kwargs)
        #
        consumer.close()
        #
        return acc_consume_message_counter_int_tuple

    #

    def flatmap(self, topic, flatmap_function, n=ALL_MESSAGES, **kwargs):
        def foldl_function(list, message_dict):
            list += flatmap_function(message_dict)
            #
            return list
        #
        return self.foldl(topic, foldl_function, [], n, **kwargs)

    def map(self, topic, map_function, n=ALL_MESSAGES, **kwargs):
        def flatmap_function(message_dict):
            return [map_function(message_dict)]
        #
        return self.flatmap(topic, flatmap_function, n, **kwargs)

    def filter(self, topic, filter_function, n=ALL_MESSAGES, **kwargs):
        def flatmap_function(message_dict):
            return [message_dict] if filter_function(message_dict) else []
        #
        return self.flatmap(topic, flatmap_function, n, **kwargs)

    def foreach(self, topic, foreach_function, n=ALL_MESSAGES, **kwargs):
        def foldl_function(_, message_dict):
            foreach_function(message_dict)
        #
        self.foldl(topic, foldl_function, None, n, **kwargs)

    #

    def foldl_to(self, topic, target_storage, target_topic, foldl_to_function, initial_acc, n=ALL_MESSAGES, **kwargs):
        verbose_int = self.verbose()
        #
        progress_num_messages_int = self.progress_num_messages()
        #

        def foldl_to_function1(acc_consume_message_counter_int_produce_batch_size_int_produce_batch_message_dict_list_produce_message_counter_int_tuple, message_dict):
            (acc, consume_message_counter_int, produce_batch_size_int, produce_batch_message_dict_list, produce_message_counter_int) = acc_consume_message_counter_int_produce_batch_size_int_produce_batch_message_dict_list_produce_message_counter_int_tuple
            #
            (acc, message_dict_list) = foldl_to_function(acc, message_dict)
            #
            consume_message_counter_int += 1
            if verbose_int > 0 and consume_message_counter_int % progress_num_messages_int == 0:
                print(f"Read: {consume_message_counter_int}")
            #
            produce_batch_message_dict_list += message_dict_list
            #
            if len(produce_batch_message_dict_list) == produce_batch_size_int:
                target_producer.produce_list(produce_batch_message_dict_list, **target_kwargs)
                #
                produce_message_counter_int += len(produce_batch_message_dict_list)
                if verbose_int > 0 and produce_message_counter_int % progress_num_messages_int == 0:
                    print(f"Written: {produce_message_counter_int}")
                #
                return (acc, consume_message_counter_int, produce_batch_size_int, [], produce_message_counter_int)
            else:
                return (acc, consume_message_counter_int, produce_batch_size_int, produce_batch_message_dict_list, produce_message_counter_int)

        #
        source_kwargs = self.get_source_kwargs(**kwargs)
        #
        target_kwargs = self.get_target_kwargs(**kwargs)
        #
        produce_batch_size_int = kwargs["produce_batch_size"] if "produce_batch_size" in kwargs else target_storage.produce_batch_size()
        #
        consumer = self.consumer(topic, **source_kwargs)
        #
        target_producer = target_storage.producer(target_topic, **target_kwargs)
        #
        (acc, consume_message_counter_int, _, produce_batch_message_dict_list, produce_message_counter_int) = consumer.foldl(foldl_to_function1, (initial_acc, 0, produce_batch_size_int, [], 0), n, **kwargs)
        #
        consumer.close()
        #
        if len(produce_batch_message_dict_list) > 0:
            target_producer.produce_list(produce_batch_message_dict_list, **target_kwargs)
            produce_message_counter_int += len(produce_batch_message_dict_list)
        #
        target_producer.close()
        #
        return (acc, consume_message_counter_int, produce_message_counter_int)

    def flatmap_to(self, topic, target_storage, target_topic, flatmap_function, n=ALL_MESSAGES, **kwargs):
        def foldl_to_function(_, message_dict):
            return (None, flatmap_function(message_dict))
        #
        (_, consume_message_counter_int, produce_message_counter_int) = self.foldl_to(topic, target_storage, target_topic, foldl_to_function, None, n, **kwargs)
        return (consume_message_counter_int, produce_message_counter_int)

    def map_to(self, topic, target_storage, target_topic, map_function, n=ALL_MESSAGES, **kwargs):
        def flatmap_function(message_dict):
            return [map_function(message_dict)]
        #
        return self.flatmap_to(topic, target_storage, target_topic, flatmap_function, n, **kwargs)

    def filter_to(self, topic, target_storage, target_topic, filter_function, n=ALL_MESSAGES, **kwargs):
        def flatmap_function(message_dict):
            return [message_dict] if filter_function(message_dict) else []
        #
        return self.flatmap_to(topic, target_storage, target_topic, flatmap_function, n, **kwargs)

    #

    def zip_foldl(self, topic1, storage2, topic2, zip_foldl_function, initial_acc, n=ALL_MESSAGES, **kwargs):
        n_int = n
        #
        verbose_int = self.verbose()
        progress_num_messages_int = self.progress_num_messages()
        #
        consume_batch_size_int = kwargs["consume_batch_size"] if "consume_batch_size" in kwargs else self.consume_batch_size()
        if consume_batch_size_int > n_int:
            consume_batch_size_int = n_int
        #
        break_function = kwargs["break_function"] if "break_function" in kwargs else lambda _, _1: False
        #
        kwargs1 = kwargs.copy()
        kwargs1["group"] = kwargs1["group1"] if "group1" in kwargs1 else None
        kwargs1["offsets"] = kwargs1["offsets1"] if "offsets1" in kwargs1 else None
        kwargs1["key_type"] = kwargs1["key_type1"] if "key_type1" in kwargs1 else "bytes"
        kwargs1["value_type"] = kwargs1["value_type1"] if "value_type1" in kwargs1 else "bytes"
        kwargs1["type"] = kwargs1["type1"] if "type1" in kwargs1 else "bytes"
        #
        kwargs2 = kwargs.copy()
        kwargs2["group"] = kwargs2["group2"] if "group2" in kwargs2 else None
        kwargs2["offsets"] = kwargs2["offsets2"] if "offsets2" in kwargs2 else None
        kwargs2["key_type"] = kwargs2["key_type2"] if "key_type2" in kwargs2 else "bytes"
        kwargs2["value_type"] = kwargs2["value_type2"] if "value_type2" in kwargs2 else "bytes"
        kwargs2["type"] = kwargs2["type2"] if "type2" in kwargs2 else "bytes"
        #
        consumer1 = self.consumer(topic1, **kwargs1)
        consumer2 = storage2.consumer(topic2, **kwargs2)
        #
        message_counter_int1 = 0
        message_counter_int2 = 0
        acc = initial_acc
        break_bool = False
        while True:
            message_dict_list1 = []
            while True:
                message_dict_list1 += consumer1.consume(n=consume_batch_size_int)
                if not message_dict_list1 or consume_batch_size_int == ALL_MESSAGES or len(message_dict_list1) == consume_batch_size_int:
                    break
            if not message_dict_list1:
                break
            num_messages_int1 = len(message_dict_list1)
            message_counter_int1 += num_messages_int1
            if verbose_int > 0 and message_counter_int1 % progress_num_messages_int == 0:
                print(f"Read (storage 1): {message_counter_int1}")
            #
            consume_batch_size_int2 = num_messages_int1 if num_messages_int1 < consume_batch_size_int else consume_batch_size_int
            message_dict_list2 = []
            while True:
                message_dict_list2 += consumer2.consume(n=consume_batch_size_int2)
                if not message_dict_list2 or consume_batch_size_int2 == ALL_MESSAGES or len(message_dict_list2) == consume_batch_size_int2:
                    break
            if not message_dict_list2:
                break
            num_messages_int2 = len(message_dict_list2)
            message_counter_int2 += num_messages_int2
            if verbose_int > 0 and message_counter_int2 % progress_num_messages_int == 0:
                print(f"Read (storage 2): {message_counter_int2}")
            #
            if num_messages_int1 != num_messages_int2:
                break
            #
            for message_dict1, message_dict2 in zip(message_dict_list1, message_dict_list2):
                if break_function(message_dict1, message_dict2):
                    break_bool = True
                    break
                acc = zip_foldl_function(acc, message_dict1, message_dict2)
            #
            if break_bool:
                break
            #
            if n_int != ALL_MESSAGES:
                if message_counter_int1 >= n_int:
                    break
        #
        consumer1.close()
        consumer2.close()
        #
        return acc, message_counter_int1, message_counter_int2

    #

    def zip_foldl_to(self, topic1, storage2, topic2, target_storage, target_topic, zip_foldl_to_function, initial_acc, n=ALL_MESSAGES, **kwargs):
        n_int = n
        #
        verbose_int = self.verbose()
        progress_num_messages_int = self.progress_num_messages()
        #
        consume_batch_size_int = kwargs["consume_batch_size"] if "consume_batch_size" in kwargs else self.consume_batch_size()
        if consume_batch_size_int > n_int:
            consume_batch_size_int = n_int
        #
        break_function = kwargs["break_function"] if "break_function" in kwargs else lambda _, _1: False
        #
        kwargs1 = kwargs.copy()
        kwargs1["group"] = kwargs1["group1"] if "group1" in kwargs1 else None
        kwargs1["offsets"] = kwargs1["offsets1"] if "offsets1" in kwargs1 else None
        kwargs1["key_type"] = kwargs1["key_type1"] if "key_type1" in kwargs1 else "bytes"
        kwargs1["value_type"] = kwargs1["value_type1"] if "value_type1" in kwargs1 else "bytes"
        kwargs1["type"] = kwargs1["type1"] if "type1" in kwargs1 else "bytes"
        #
        kwargs2 = kwargs.copy()
        kwargs2["group"] = kwargs2["group2"] if "group2" in kwargs2 else None
        kwargs2["offsets"] = kwargs2["offsets2"] if "offsets2" in kwargs2 else None
        kwargs2["key_type"] = kwargs2["key_type2"] if "key_type2" in kwargs2 else "bytes"
        kwargs2["value_type"] = kwargs2["value_type2"] if "value_type2" in kwargs2 else "bytes"
        kwargs2["type"] = kwargs2["type2"] if "type2" in kwargs2 else "bytes"
        #
        target_kwargs = self.get_target_kwargs(**kwargs)
        #
        produce_batch_size_int = kwargs["produce_batch_size"] if "produce_batch_size" in kwargs else target_storage.produce_batch_size()
        #
        consumer1 = self.consumer(topic1, **kwargs1)
        consumer2 = storage2.consumer(topic2, **kwargs2)
        #
        target_producer = target_storage.producer(target_topic, **target_kwargs)
        #
        message_counter_int1 = 0
        message_counter_int2 = 0
        acc = initial_acc
        break_bool = False
        batch_message_dict_list = []
        progress_message_counter_int = 0
        while True:
            message_dict_list1 = []
            while True:
                message_dict_list1 += consumer1.consume(n=consume_batch_size_int)
                if not message_dict_list1 or consume_batch_size_int == ALL_MESSAGES or len(message_dict_list1) == consume_batch_size_int:
                    break
            if not message_dict_list1:
                break
            num_messages_int1 = len(message_dict_list1)
            message_counter_int1 += num_messages_int1
            if verbose_int > 0 and message_counter_int1 % progress_num_messages_int == 0:
                print(f"Read (storage 1): {message_counter_int1}")
            #
            consume_batch_size_int2 = num_messages_int1 if num_messages_int1 < consume_batch_size_int else consume_batch_size_int
            message_dict_list2 = []
            while True:
                message_dict_list2 += consumer2.consume(n=consume_batch_size_int2)
                if not message_dict_list2 or consume_batch_size_int2 == ALL_MESSAGES or len(message_dict_list2) == consume_batch_size_int2:
                    break
            if not message_dict_list2:
                break
            num_messages_int2 = len(message_dict_list2)
            message_counter_int2 += num_messages_int2
            if verbose_int > 0 and message_counter_int2 % progress_num_messages_int == 0:
                print(f"Read (storage 2): {message_counter_int2}")
            #
            if num_messages_int1 != num_messages_int2:
                break
            #
            for message_dict1, message_dict2 in zip(message_dict_list1, message_dict_list2):
                if break_function(message_dict1, message_dict2):
                    break_bool = True
                    break
                (acc, message_dict_list) = zip_foldl_to_function(acc, message_dict1, message_dict2)
            #
            if break_bool:
                break
            #!
            batch_message_dict_list += message_dict_list
            #
            if len(batch_message_dict_list) == produce_batch_size_int:
                target_producer.produce_list(batch_message_dict_list, **target_kwargs)
                #
                progress_message_counter_int += len(batch_message_dict_list)
                if verbose_int > 0 and progress_message_counter_int % progress_num_messages_int == 0:
                    print(f"Written: {progress_message_counter_int}")
                #
                batch_message_dict_list = []
            #
            if n_int != ALL_MESSAGES:
                if message_counter_int1 >= n_int:
                    break
        #
        consumer1.close()
        consumer2.close()
        #
        target_producer.close()
        #
        return acc, message_counter_int1, message_counter_int2

    #

    def get_source_kwargs(self, **kwargs):
        source_kwargs = kwargs.copy()
        if "source_key_type" in kwargs:
            source_kwargs["key_type"] = kwargs["source_key_type"]
        if "source_value_type" in kwargs:
            source_kwargs["value_type"] = kwargs["source_value_type"]
        if "source_type" in kwargs:
            source_kwargs["type"] = kwargs["source_type"]
        if "source_key_schema" in kwargs:
            source_kwargs["key_schema"] = kwargs["source_key_schema"]
        if "source_value_schema" in kwargs:
            source_kwargs["value_schema"] = kwargs["source_value_schema"]
        if "source_key_schema_id" in kwargs:
            source_kwargs["key_schema_id"] = kwargs["source_key_schema_id"]
        if "source_value_schema_id" in kwargs:
            source_kwargs["value_schema_id"] = kwargs["source_value_schema_id"]
        #
        return source_kwargs

    def get_target_kwargs(self, **kwargs):
        target_kwargs = kwargs.copy()
        if "target_key_type" in kwargs:
            target_kwargs["key_type"] = kwargs["target_key_type"]
        if "target_value_type" in kwargs:
            target_kwargs["value_type"] = kwargs["target_value_type"]
        if "target_type" in kwargs:
            target_kwargs["type"] = kwargs["target_type"]
        if "target_key_schema" in kwargs:
            target_kwargs["key_schema"] = kwargs["target_key_schema"]
        if "target_value_schema" in kwargs:
            target_kwargs["value_schema"] = kwargs["target_value_schema"]
        if "target_key_schema_id" in kwargs:
            target_kwargs["key_schema_id"] = kwargs["target_key_schema_id"]
        if "target_value_schema_id" in kwargs:
            target_kwargs["value_schema_id"] = kwargs["target_value_schema_id"]
        #
        return target_kwargs
