from concurrent import futures
import grpc
import os
from proto import pdf_converter_pb2, pdf_converter_pb2_grpc
from queue import Queue
import tempfile

# tasks queue (pdf tmp files to convert)
tasks_queue = Queue()

class PDFConverterServicer(pdf_converter_pb2_grpc.PDFConverterServicer):
    def UploadPDF(self, request_iterator, context):
        try:
            # creating a new tmp .pdf file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                # collecting pdf data & wrighting in tmp
                for chunk in request_iterator:
                    if not chunk.data:
                        raise ValueError("Empty chunk received")
                    tmp.write(chunk.data)
                tmp_path = tmp.name

            #adding a file to a tasks queue
            tasks_queue.put(tmp_path)
            return pdf_converter_pb2.UploadResponce(success=True)
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return pdf_converter_pb2.UploadResponce(success=False)