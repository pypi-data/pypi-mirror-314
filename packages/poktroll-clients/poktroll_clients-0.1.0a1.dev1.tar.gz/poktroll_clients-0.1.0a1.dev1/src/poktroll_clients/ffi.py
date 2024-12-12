import platform
from os import path
from pathlib import Path
from typing import Callable, Tuple

from cffi import FFI

# Initialize CFFI
ffi = FFI()

# TODO_IN_THIS_COMMIT: comment
callback_type = Callable[[ffi.CData, ffi.CData], None]

# Load and read the header file contents
thisDirPath = path.dirname(path.abspath(__file__))

# TODO_IMPROVE: Extract docstring to an appropriately named file.
# DEV_NOTE: ffi.cdef MUST NOT depend on any pre-processing (e.g. macros, defs, etc.).

# Add complete struct definitions for CFFI
ffi.cdef("""
    typedef struct {
        unsigned char __size[40];
        long int __align;
    } pthread_mutex_t;

    typedef struct {
        unsigned char __size[48];
        long long int __align;
    } pthread_cond_t;

    typedef struct AsyncContext {
        pthread_mutex_t mutex;
        pthread_cond_t cond;
        bool completed;
        bool success;
        void* data;
        size_t data_len;
        int error_code;
        char error_msg[256];
    } AsyncContext;

    typedef void (*success_callback)(AsyncContext* ctx, const void* result);
    typedef void (*error_callback)(AsyncContext* ctx, const char* error);
    typedef void (*cleanup_callback)(AsyncContext* ctx);

    typedef struct AsyncOperation {
        AsyncContext* ctx;
        success_callback on_success;
        error_callback on_error;
        cleanup_callback cleanup;
    } AsyncOperation;

    void init_context(AsyncContext* ctx);
    void cleanup_context(AsyncContext* ctx);
    void handle_error(AsyncContext* ctx, const char* error);
    void handle_success(AsyncContext* ctx, const void* result);
    bool wait_for_completion(AsyncContext* ctx, int timeout_ms);

    typedef void (callback_fn)(void *data, char **err);

    typedef int64_t go_ref;

    void FreeGoMem(go_ref go_ref);

    go_ref Supply(go_ref go_ref, char **err);
    go_ref SupplyMany(go_ref *go_refs, int num_go_refs, char **err);

    typedef struct {
        uint8_t* type_url;
        size_t type_url_length;
        uint8_t* data;
        size_t data_length;
    } serialized_proto;

    typedef struct {
        serialized_proto* messages;
        size_t num_messages;
    } proto_message_array;

    go_ref NewEventsQueryClient(const char* comet_websocket_url);
    go_ref EventsQueryClientEventsBytes(go_ref selfRef, const char* query);

    go_ref NewBlockQueryClient(char *comet_websocket_url, char **err);

    go_ref NewTxContext(char *tcp_url, char **err);

    go_ref NewBlockClient(go_ref cfg_ref, char **err);

    go_ref NewTxClient(go_ref cfg_ref, char *signing_key_name, char **err);
    go_ref TxClient_SignAndBroadcast(AsyncOperation* op, go_ref self_ref, serialized_proto *msg);
    go_ref TxClient_SignAndBroadcastMany(AsyncOperation* op, go_ref self_ref, proto_message_array *msgs);
""")


def get_platform_info() -> Tuple[str, str]:
    """
    Get exact OS and architecture information.

    Returns:
        Tuple of (os_name, machine) exactly as reported by platform module
    """
    system = platform.system()
    machine = platform.machine()

    # Validate system
    if system not in ("Linux", "Darwin", "Windows"):
        raise OSError(f"Unsupported operating system: {system}")

    # Validate machine architecture
    valid_machines = {
        "Linux": {"x86_64", "aarch64"},
        "Darwin": {"x86_64", "arm64"},
        "Windows": {"AMD64", "x86"}
    }

    if machine not in valid_machines[system]:
        raise OSError(
            f"Unsupported architecture {machine} for {system}. "
            f"Supported architectures: {valid_machines[system]}"
        )

    return system, machine


def machine_to_go_arch(machine: str) -> str:
    """
    TODO_IN_THIS_COMMIT: move and comment...
    """

    arch_map = {
        "x86_64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
    }

    return arch_map[machine]

def get_library_name(system: str, machine: str) -> str:
    """
    Get the exact platform-specific library name.

    Args:
        system: Value from platform.system()
        machine: Value from platform.machine()

    Returns:
        The platform-specific library filename
    """

    go_arch = machine_to_go_arch(machine)

    if system == "Linux":
        return f"libpoktroll_clients-{go_arch}.so"
    elif system == "Darwin":
        return f"libpoktroll_clients-{go_arch}.dylib"
    elif system == "Windows":
        return f"poktroll_clients-{go_arch}.dll"
    else:
        raise OSError(f"Unsupported platform combination: {system} {machine}")


def get_library_path() -> Path:
    """
    Get the full path to the appropriate native library for the current platform.

    Returns:
        Path to the native library

    Raises:
        OSError: If the platform is unsupported or the library is not found
    """
    system, machine = get_platform_info()
    lib_name = get_library_name(system, machine)

    package_dir = Path(__file__).parent.absolute()
    lib_path = package_dir / 'lib' / lib_name

    if not lib_path.exists():
        raise OSError(
            f"Native library not found for {system} {machine}\n"
            f"Expected path: {lib_path}\n"
            f"Expected filename: {lib_name}"
        )

    return lib_path


# Load the shared library.
# TODO_IN_THIS_COMMIT: select shared library based on OS/Arch.
# libpoktroll_clients = ffi.dlopen(path.join(thisDirPath, "..", "..", "native_libs", "libpoktroll_clients.so"))
libpoktroll_clients = ffi.dlopen(str(get_library_path()))
# TODO_IN_THIS_COMMIT: add env var to override packaged shared library with OS installed version.
# TODO_CONSIDERATION: look for an OS installed shared library if there's no packaged one for the current OS/Arch.
# libpoktroll_clients = ffi.dlopen("poktroll_clients")
