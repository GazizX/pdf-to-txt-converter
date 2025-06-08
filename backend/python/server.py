from concurrent import futures
import grpc
import os
from proto import pdf_converter_pb2, pdf_converter_pb2_grpc
from queue import Queue
import tempfile
import threading
import worker

# tasks queue (pdf tmp files to convert)
tasks_queue = Queue()

class PDFConverterServicer(pdf_converter_pb2_grpc.PDFConverterServicer):
    def Convert(self, request_iterator, context):
        try:
            # creating a new tmp .pdf file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                # collecting pdf data & wrighting in tmp
                for chunk in request_iterator:
                    if not chunk.data:
                        raise ValueError("Empty chunk received")
                    tmp.write(chunk.data)
                tmp_path = tmp.name

            # creating future for a result of conversion
            result_future = futures.Future()

            #adding a file to a tasks queue
            tasks_queue.put((tmp_path, result_future))

            # waiting for a result from a worker
            text = result_future.result()

            # deleting tmp pdf file
            os.unlink(tmp_path)

            return pdf_converter_pb2.ConvertResponse(text=text)
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return pdf_converter_pb2.ConvertResponse(text="")

def serve():
        # starting 5 workers
        for i in range(5):
            t = threading.Thread(target=worker.process_pdf_task, args=(tasks_queue,), daemon=True)
            t.start()

        # create a server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # connect a service to the server
        pdf_converter_pb2_grpc.add_PDFConverterServicer_to_server(PDFConverterServicer(), server)

        # set server port 50051 without TLS
        server.add_insecure_port('[::]:50051')

        server.start()
        server.wait_for_termination()

if __name__ == '__main__':
    serve()

