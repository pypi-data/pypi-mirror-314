from poktroll_clients.ffi import ffi, libpoktroll_clients
from poktroll_clients.go_memory import go_ref, check_err, check_ref, GoManagedMem


def Supply(go_ref: go_ref) -> go_ref:
    """
    Supplies a Go-managed memory reference to a returned (Go-managed) depinject config.
    :param go_ref: The Go-managed memory reference to supply via depinject.
    :return: The Go-managed memory reference of the resulting depinject config.
    """

    err_ptr = ffi.new("char **")
    cfg_ref = libpoktroll_clients.Supply(go_ref, err_ptr)

    check_err(err_ptr)
    check_ref(cfg_ref)

    return cfg_ref


def SupplyMany(*go_objs: GoManagedMem) -> go_ref:
    """
    Supplies multiple Go-managed memory references to a returned (Go-managed) depinject config.
    :param go_objs: The Go-managed memory objects to supply via depinject.
    :return: The Go-managed memory reference of the resulting depinject config.
    """

    go_refs = [go_obj.go_ref for go_obj in go_objs]
    cgo_refs = ffi.new("go_ref[]", go_refs)
    err_ptr = ffi.new("char **")

    cfg_ref = libpoktroll_clients.SupplyMany(cgo_refs, len(go_objs), err_ptr)

    check_err(err_ptr)
    check_ref(cfg_ref)

    return cfg_ref
