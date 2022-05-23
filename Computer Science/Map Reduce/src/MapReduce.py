import os
import json
from multiprocessing import Process
import re
import logging as logger

log_file = "logs/log_file.log"
if not os.path.exists(log_file):
    temp_fil = open(log_file,'x')
    temp_fil.close()
logger.basicConfig(filename = log_file, filemode= 'a',format="Process: %(process)d Time: %(asctime)s Message: %(message)s",level=logger.INFO)

class mapreduce(object):

    def __init__(self,default_n_mappers,default_n_reducers):
        logger.info("System Ready to run Map Reduce")
        self.num_mappers = default_n_mappers
        self.num_reducers = default_n_reducers
    
    def split_file(self,input_location):
        logger.info("Splitting input file to feed to Mappers")
        if not os.path.isdir("Data/temp_"+str(input_location)):
            os.mkdir("Data/temp_"+str(input_location))
        size = os.path.getsize("Data/"+input_location)
        unit = size/self.num_mappers + 1
        ip_file = open("Data/"+input_location,'r')
        cont = ip_file.read()
        cont = (re.sub('[^A-Za-z]+',' ', cont))
        ip_file.close()
        (ind,split) = (1,1)
        curr_split_unit = open("Data/temp_"+str(input_location)+"/chunk_"+str(split-1),"w+")
        for char in cont:
            curr_split_unit.write(char)
            if (ind>unit*split+1) and (char.isspace()):
                curr_split_unit.close()
                split += 1
                curr_split_unit = open("Data/temp_"+str(input_location)+"/chunk_"+str(split-1),"w+")
            ind += 1
        curr_split_unit.close()
        logger.info("Finished Splitting the file")

    def merge_files(self,input_location):
        consolidated_data = []
        for map_in in range(0,self.num_mappers):
            for red_in in range(0,self.num_reducers):
                temp_file = open("Data/temp_"+str(input_location)+"/map_file_" + str(map_in)+"-" + str(red_in),'r')
                consolidated_data.append(json.load(temp_file))
                temp_file.close()
                os.unlink("Data/temp_"+str(input_location)+"/map_file_" + str(map_in)+"-" + str(red_in))
        con_file = open("Data/temp_"+str(input_location)+"/ConsolidatedFile","w")
        json.dump(consolidated_data,con_file)

    def get_keys(self,input_location):
        temp = open("Data/temp_"+str(input_location)+"/ConsolidatedFile",'r')
        map_res = json.load(temp)
        all_keys = set()
        for temp_list in map_res:
            for key in temp_list.keys():
                if len(key) > 2:
                    all_keys.add(key)
        all_keys = list(all_keys)
        all_keys.sort()
        return all_keys
    
    def join_files(self,input_location,output_location):
        temp_list = []
        for ind in range(0,self.num_reducers):
            file = open("Data/temp_"+str(input_location)+"/reduced_file_"+str(ind),'r')
            temp_list.append(json.load(file))
            file.close()
            os.unlink("Data/temp_"+str(input_location)+"/reduced_file_"+str(ind))
        op_file = open(output_location,'w+')
        op_dict = {}
        for dict in temp_list:
            op_dict.update(dict)
        json.dump(op_dict,op_file)
        op_file.close()

    def word_count_mapper(self,val):
        result = {}
        words = val.split()
        for word in words:
            word = word.lower()
            if word in result.keys():
                result[word] += 1
            else:
                result[word] = 1
        return result

    def inv_index_mapper(self,value,index):
        result = {}
        words = value.split()
        for word in words:
            temp_list = [index,1]
            word = word.lower()
            if word in result.keys():
                result[word][1] += 1
            else:
                result[word] = temp_list
        return result

    def run_map(self,ind,input_location,map_func):
        split_file = open("Data/temp_"+str(input_location)+"/chunk_"+ str(ind),'r')
        value = split_file.read()
        split_file.close()
        os.unlink("Data/temp_"+str(input_location)+"/chunk_"+ str(ind))
        if map_func == "word count":
            map_res = self.word_count_mapper(value)
        elif map_func == "inverted index":
            map_res = self.inv_index_mapper(value,ind)
        else:
            map_res = map_func(value)
        for red in range(self.num_reducers):
            temp = open("Data/temp_"+str(input_location)+"/map_file_" + str(ind)+"-" + str(red),'w+')
            json.dump(map_res,temp)
            temp.close()
    
    def reducer_word_count(self,key,input_location):
        temp = open("Data/temp_"+str(input_location)+"/ConsolidatedFile",'r')
        map_res = json.load(temp)
        temp.close()
        count = 0
        for lis in map_res:
            if key in lis.keys():
                count+= lis[key]
        return count

    def inv_index_reducer(self,key,input_location):
        temp = open("Data/temp_"+str(input_location)+"/ConsolidatedFile",'r')
        map_res = json.load(temp)
        temp.close()
        temp = []
        for lis in map_res:
            if key in lis.keys():
                temp.append(lis[key])
        result = []
        for i in range(self.num_mappers):
            count = 0
            for ele in temp:
                if ele[0] == i:
                    count += ele[1]
            if count == 0:
                pass
            else:
                result.append([i,count])
        return result

    def run_reduce(self,ind,reduce_func,input_location):
        all_keys = self.get_keys(input_location)
        chunk_size = (len(all_keys))/self.num_reducers +1
        start_in = int(chunk_size*(int(ind)))
        end_in = int(chunk_size*(int(ind)+1))
        temp = all_keys[start_in:end_in]
        result = {}
        for element in temp:
            if reduce_func == "word count":
                data = self.reducer_word_count(element,input_location)
            elif reduce_func == "inverted index":
                data = self.inv_index_reducer(element,input_location)
            else:
                data = reduce_func(element)
            result[element] = data
        temp_file = open("Data/temp_"+str(input_location)+"/reduced_file_"+str(ind),'w+')
        json.dump(result,temp_file)
        temp_file.close

    def runMapReduce(self,input_location,map_func,reduce_func,output_location):
        logger.info("Client has started Map Reduce Operation.")
        self.split_file(input_location)
        map_worker = []
        red_worker = []
        # Implementing Fault Tolerance for map: If it fails at any step, restart the mappers
        logger.info("Starting Map operations for "+str(map_func))
        restart_map = True
        while restart_map:
            try:
                for process_id in range(self.num_mappers):
                    pro = Process(target=self.run_map,args=(process_id,input_location,map_func))
                    pro.start()
                    map_worker.append(pro)
                [temp.join() for temp in map_worker]
                restart_map = False
                logger.info("Finished Running all mappers")
            except:
                logger.error("Map failure, Restarting Map operation....")
                pass
        # Implementing Fault Tolerance: Creating a temporary file storage in case any task of reducer fails to be able to provide correct input to reducers
        logger.info("Merging file to feed to reducers")
        self.merge_files(input_location)
        logger.info("Merge files finished")
        # Implementing Fault Tolerance for reduce: If it fails at any step, restart the reducers
        logger.info("Starting reduce operations for "+str(reduce_func))
        restart_red = True
        while restart_red:
            try:
                for thread_id in range(self.num_reducers):
                    pro = Process(target=self.run_reduce,args=(thread_id,reduce_func,input_location))
                    pro.start()
                    red_worker.append(pro)
                [temp.join() for temp in red_worker]
                restart_red = False
                logger.info("Finished running all reducers")
            except:
                logger.error("Reduce failure, Restarting Reduce operation....")
                pass
        logger.info("Combining results for all Reducers")
        self.join_files(input_location,output_location)
        logger.info("Finished combining results. Final result file created.")
        os.unlink("Data/temp_"+str(input_location)+"/ConsolidatedFile")
        os.rmdir("Data/temp_"+str(input_location))
        logger.info("Deleted all temporary files. Ending map reduce instance.")
        return "Completed"