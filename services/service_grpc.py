from concurrent import futures
import grpc
import sales_records_pb2_grpc, sales_records_pb2
import asyncio

class SalesRecordServicer(sales_records_pb2_grpc.SalesRecordServicer):
    def PingSalesRecords(self, request, context):
        response = sales_records_pb2.PingSalesRecordsResponse(ack='1')
        #response.ack = "Pong"
        return response

async def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sales_records_pb2_grpc.add_SalesRecordServicer_to_server(
        SalesRecordServicer(), server)
    server.add_insecure_port('[::]:50051')
    await asyncio.to_thread(server.start)
    await asyncio.to_thread(server.wait_for_termination)