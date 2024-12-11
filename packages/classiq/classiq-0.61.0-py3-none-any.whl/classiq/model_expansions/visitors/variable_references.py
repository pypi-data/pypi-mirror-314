import ast
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Optional, Union

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.arith.arithmetic_expression_validator import (
    DEFAULT_SUPPORTED_FUNC_NAMES,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.sympy_supported_expressions import (
    SYMPY_SUPPORTED_EXPRESSIONS,
)
from classiq.interface.model.handle_binding import (
    FieldHandleBinding,
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)


class VarRefCollector(ast.NodeVisitor):
    def __init__(
        self, ignore_duplicated_handles: bool = False, unevaluated: bool = False
    ) -> None:
        self._var_handles: dict[HandleBinding, bool] = {}
        self._ignore_duplicated_handles = ignore_duplicated_handles
        self._unevaluated = unevaluated
        self._is_nested = False

    @property
    def var_handles(self) -> list[HandleBinding]:
        return list(self._var_handles)

    def visit(self, node: ast.AST) -> Union[
        SubscriptHandleBinding,
        SlicedHandleBinding,
        FieldHandleBinding,
        HandleBinding,
        None,
    ]:
        res = super().visit(node)
        if not self._ignore_duplicated_handles and len(self._var_handles) != len(
            {handle.name for handle in self._var_handles}
        ):
            raise ClassiqExpansionError(
                "Multiple non-identical variable references in an expression are not supported."
            )
        return res

    def visit_Subscript(
        self, node: ast.Subscript
    ) -> Union[SubscriptHandleBinding, SlicedHandleBinding, None]:
        with self.set_nested():
            base_handle = self.visit(node.value)
        if base_handle is None:
            return None

        handle: Union[SubscriptHandleBinding, SlicedHandleBinding]
        if isinstance(node.slice, ast.Slice):
            if not self._unevaluated and (
                not isinstance(node.slice.lower, ast.Num)
                or not isinstance(node.slice.upper, ast.Num)
            ):
                raise ClassiqInternalExpansionError("Unevaluated slice bounds.")
            if node.slice.lower is None or node.slice.upper is None:
                raise ClassiqExpansionError(
                    f"{str(base_handle)!r} slice must specify both lower and upper bounds"
                )
            handle = SlicedHandleBinding(
                base_handle=base_handle,
                start=Expression(expr=ast.unparse(node.slice.lower)),
                end=Expression(expr=ast.unparse(node.slice.upper)),
            )
        elif not self._unevaluated and not isinstance(node.slice, ast.Num):
            raise ClassiqInternalExpansionError("Unevaluated slice.")
        else:
            handle = SubscriptHandleBinding(
                base_handle=base_handle,
                index=Expression(expr=ast.unparse(node.slice)),
            )

        if not self._is_nested:
            self._var_handles[handle] = True
        return handle

    def visit_Attribute(self, node: ast.Attribute) -> Optional[FieldHandleBinding]:
        return self._get_field_handle(node.value, node.attr)

    def visit_Call(self, node: ast.Call) -> Optional[FieldHandleBinding]:
        if (
            not isinstance(node.func, ast.Name)
            or node.func.id != "get_field"
            or len(node.args) != 2
            or not isinstance(node.args[1], ast.Constant)
            or not isinstance(node.args[1].value, str)
        ):
            return self.generic_visit(node)
        return self._get_field_handle(node.args[0], node.args[1].value)

    def _get_field_handle(
        self, subject: ast.expr, field: str
    ) -> Optional[FieldHandleBinding]:
        with self.set_nested():
            base_handle = self.visit(subject)
        if base_handle is None:
            return None
        handle = FieldHandleBinding(
            base_handle=base_handle,
            field=field,
        )
        if not self._is_nested:
            self._var_handles[handle] = True
        return handle

    def visit_Name(self, node: ast.Name) -> Optional[HandleBinding]:
        if node.id in set(SYMPY_SUPPORTED_EXPRESSIONS) | set(
            DEFAULT_SUPPORTED_FUNC_NAMES
        ):
            return None
        handle = HandleBinding(name=node.id)
        if not self._is_nested:
            self._var_handles[handle] = True
        return handle

    @contextmanager
    def set_nested(self) -> Iterator[None]:
        previous_is_nested = self._is_nested
        self._is_nested = True
        yield
        self._is_nested = previous_is_nested


class VarRefTransformer(ast.NodeTransformer):
    def __init__(self, var_mapping: dict[str, str]) -> None:
        self.var_mapping = var_mapping

    def visit_Name(self, node: ast.Name) -> ast.Name:
        if node.id in self.var_mapping:
            node.id = self.var_mapping[node.id]
        return node
