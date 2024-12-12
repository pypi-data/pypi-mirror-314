import asyncio
from typing import Dict, Tuple

from atomics import INTEGRAL, atomic, INT
from google.protobuf.message import Message

from cffi import FFIError

from poktroll_clients.ffi import ffi, libpoktroll_clients
from poktroll_clients.go_memory import GoManagedMem, go_ref, check_err, check_ref
from poktroll_clients.protobuf import SerializedProto, ProtoMessageArray


class TxClient(GoManagedMem):
    """
    TODO_IN_THIS_COMMIT: comment
    """

    go_ref: go_ref
    err_ptr: ffi.CData
    _callback_idx: INTEGRAL = atomic(width=8, atype=INT)
    _callback_fns: Dict[int, Tuple[ffi.CData, ffi.CData, ffi.CData]] = {}

    def __init__(self, cfg_ref: go_ref, signing_key_name: str):
        """
        Constructor for TxClient.
        :param cfg_ref: A Go-managed memory reference to a depinject config.
        """
        go_ref = libpoktroll_clients.NewTxClient(cfg_ref, signing_key_name.encode('utf-8'), self.err_ptr)
        super().__init__(go_ref)

        check_err(self.err_ptr)
        check_ref(go_ref)

    async def sign_and_broadcast(self, *msgs: Message) -> asyncio.Future:
        """
        Signs and broadcasts a transaction.
        :param msgs: The protobuf Message(s) to sign and broadcast.
        :return: Future that completes when the transaction is processed.
        """

        op, future = self._new_async_operation()

        serialized_msgs = ProtoMessageArray(messages=[
            SerializedProto(
                type_url=msg.DESCRIPTOR.full_name,
                data=msg.SerializeToString()
            ) for msg in msgs
        ])

        err_ch_ref = libpoktroll_clients.TxClient_SignAndBroadcastMany(  # <-- line 71
            op,
            self.go_ref,
            serialized_msgs.to_c_struct(),
        )

        if err_ch_ref == -1:
            error_msg = ffi.string(op.ctx.error_msg).decode('utf-8')
            future.set_exception(FFIError(error_msg))

        return await future

    def _new_async_operation(self) -> Tuple[ffi.CData, asyncio.Future]:
        """
        Creates a new AsyncOperation with callbacks and associated Future.
        The callbacks are protected from garbage collection by storing in self._callback_fns.
        """

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        future = loop.create_future()

        # Create AsyncContext
        ctx = ffi.new("AsyncContext *")
        next_callback_idx = self._callback_idx.fetch_inc()

        # Define callbacks
        @ffi.callback("void(AsyncContext*, const void*)")
        def success_cb(ctx, result):
            try:
                loop.call_soon_threadsafe(future.set_result, None)
            finally:
                self._free_callback(next_callback_idx)

        @ffi.callback("void(AsyncContext*, const char*)")
        def error_cb(ctx, error):
            try:
                error_str = ffi.string(error).decode('utf-8')
                loop.call_soon_threadsafe(future.set_exception, Exception(error_str))
            except Exception as e:
                future.set_exception(e)
            finally:
                self._free_callback(next_callback_idx)

        @ffi.callback("void(AsyncContext*)")
        def cleanup_cb(ctx):
            self._free_callback(next_callback_idx)

        # Create AsyncOperation
        op = ffi.new("AsyncOperation *")
        op.ctx = ctx
        op.on_success = success_cb
        op.on_error = error_cb
        op.cleanup = cleanup_cb

        # Store callbacks to protect from garbage collection
        self._callback_fns[next_callback_idx] = (success_cb, error_cb, cleanup_cb)

        return op, future

    def _free_callback(self, callback_idx: int):
        """
        Clean up stored callbacks.
        """
        self._callback_fns.pop(callback_idx)


class TxContext(GoManagedMem):
    """
    TODO_IN_THIS_COMMIT: comment
    """

    go_ref: go_ref
    err_ptr: ffi.CData

    def __init__(self, tcp_url: str):
        """
        Constructor for TxContext.
        :param tcp_url: The gRPC URL for the client to use (e.g. tcp://127.0.0.1:26657).
        """

        go_ref = libpoktroll_clients.NewTxContext(tcp_url.encode('utf-8'), self.err_ptr)
        super().__init__(go_ref)
