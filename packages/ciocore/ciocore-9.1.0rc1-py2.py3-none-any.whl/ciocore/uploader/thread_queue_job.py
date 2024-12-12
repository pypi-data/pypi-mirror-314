import logging
from ciocore import loggeria

logger = logging.getLogger("{}.uploader".format(loggeria.CONDUCTOR_LOGGER_NAME))

class ThreadQueueJob():
    pass

class UploadThreadQueueJob(ThreadQueueJob):
    
    def __init__(self, path, file_size, presigned_url, file_md5=None, upload_id=None, part_size=None, total_parts=1, part_index=1, kms_key_name=None):

        super().__init__()

        self.path = path
        self.file_size = file_size 
        self.upload_id = upload_id
        self.presigned_url = presigned_url
        self.file_md5 = file_md5
        self.part_size = part_size
        self.part_index = part_index
        self.total_parts = total_parts
        self.kms_key_name = kms_key_name

        logger.info("Creating %s (%s): %s", str(self.__class__), str(self), str(self.__dict__))

    def is_multipart(self):
        return self.total_parts != 1

    def is_vendor_aws(self):
        return "amazonaws" in self.presigned_url
    
    def is_vendor_cw(self):
        return "coreweave" in self.presigned_url    

    @classmethod
    def create_from_response(cls, response):

        new_thread_queue_jobs = []

        for part_type, file_request_list in response.items():

            for file_request in file_request_list:
                if part_type == "multiPartURLs":
                        
                        for part in file_request["parts"]:
                            new_tqj = cls( path=file_request['filePath'],
                                           file_size = file_request['filePath'],
                                           presigned_url = file_request['preSignedURL'],
                                           file_md5  = file_request['preSignedURL'],
                                           upload_id = file_request['preSignedURL'],
                                           part_size = file_request['preSignedURL'],
                                           part_index = file_request['preSignedURL'])
                            

                else:
                    new_tqj = cls( path=file_request['filePath'],
                                   file_size = file_request['filePath'],
                                   presigned_url = file_request['preSignedURL'])
                    
        new_thread_queue_jobs.append(new_tqj)



class MultiPartThreadQueueJob(ThreadQueueJob):
    
    def __init__(self, path, md5, total_parts=1, part_index=1):

        super().__init__()

        self.upload_id = None
        self.md5 = md5
        self.project = None
        self.path = path
        self.part_index = part_index
        self.etag = None
        self.total_parts = total_parts

        logger.info("Creating %s (%s): %s", str(self.__class__), str(self), str(self.__dict__))

    def is_multipart(self):
        return self.total_parts != 1
    
    # def __str__(self):
    #     return

    @staticmethod
    def aggregate_parts(parts):
        """
        Helper function to take all the parts of a multipart upload and put 
        them into a format that's expected for the HTTP call.
        """

        completed_parts_payload = []
        
        for part in parts:
            completed_parts_payload.append({'partNumber': part.part,
                                                       'etag': part.etag}
                                                      )
            
        return completed_parts_payload