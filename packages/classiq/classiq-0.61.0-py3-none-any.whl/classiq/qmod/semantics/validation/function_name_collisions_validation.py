from typing import Optional

from classiq.interface.model.model import Model

from classiq.qmod.builtins.functions import CORE_LIB_DECLS


def _check_function_name_collisions(
    model: Model, error_type: Optional[type[Exception]]
) -> None:
    if error_type is None:
        return
    redefined_functions = [
        function.name
        for function in CORE_LIB_DECLS
        if function.name in model.function_dict
    ]
    if len(redefined_functions) == 1:
        raise error_type(
            f"Cannot redefine built-in function {redefined_functions[0]!r}"
        )
    elif len(redefined_functions) > 1:
        raise error_type(f"Cannot redefine built-in functions: {redefined_functions}")
