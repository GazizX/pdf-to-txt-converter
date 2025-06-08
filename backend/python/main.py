from server import serve, tasks_queue
from worker import process_pdf_task

def main():
    serve()

if __name__ == '__main__':
    main()
