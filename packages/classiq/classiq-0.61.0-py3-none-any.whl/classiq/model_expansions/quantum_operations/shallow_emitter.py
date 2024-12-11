import ast
from typing import TYPE_CHECKING, Any, Optional, TypeVar

from classiq.interface.generator.arith.arithmetic import compute_arithmetic_result_type
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
    ArithmeticOperationKind,
)
from classiq.interface.model.quantum_statement import QuantumOperation, QuantumStatement

from classiq.model_expansions.closure import Closure
from classiq.model_expansions.evaluators.quantum_type_utils import copy_type_information
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import QuantumSymbol, Scope
from classiq.model_expansions.transformers.ast_renamer import rename_variables
from classiq.model_expansions.visitors.variable_references import VarRefCollector

if TYPE_CHECKING:
    from classiq.model_expansions.interpreter import Interpreter


QuantumOperationT = TypeVar("QuantumOperationT", bound=QuantumOperation)
_BLOCK_RENAMES = {
    "compute": "within",
    "action": "apply",
}
_REVERSE_BLOCK_RENAMES = {rename: name for name, rename in _BLOCK_RENAMES.items()}


class ShallowEmitter(Emitter[QuantumOperation]):
    def __init__(
        self,
        interpreter: "Interpreter",
        operation_name: str,
        *,
        components: Optional[list[str]] = None,
    ) -> None:
        super().__init__(interpreter)
        self._operation_name = operation_name
        self._components: list[str] = components or []

    def emit(self, op: QuantumOperation, /) -> None:
        expanded_components: dict[str, Any] = {}
        blocks, expressions, handles = self._split_components(op)

        if len(blocks) > 0:
            if op.is_generative():
                expanded_blocks = self.expand_generative_blocks(op)
            else:
                expanded_blocks = self.expand_blocks(op, blocks)
            expanded_components.update(expanded_blocks)

        for expression_name in expressions:
            expression = getattr(op, expression_name)
            expression = self._evaluate_expression(expression, preserve_bool_ops=True)
            self.capture_handles_in_expression(expression)
            expanded_components[expression_name] = expression

        for handle_name in handles:
            handle = getattr(op, handle_name)
            expanded_components[handle_name] = self._interpreter.evaluate(
                handle
            ).value.handle

        op = op.model_copy(update=expanded_components)
        if isinstance(op, ArithmeticOperation):
            self._post_process_assignment(op)
        self._builder.emit_statement(op)

    def _post_process_assignment(self, op: ArithmeticOperation) -> None:
        if op.operation_kind == ArithmeticOperationKind.Assignment:
            direction = PortDeclarationDirection.Output
            self._update_result_type(op)
        else:
            direction = PortDeclarationDirection.Inout
        self._capture_handle(op.result_var, direction)

    def _split_components(
        self, op: QuantumOperation
    ) -> tuple[list[str], list[str], list[str]]:
        blocks = self._filter_components(op, list)
        expressions = self._filter_components(op, Expression)
        handles = self._filter_components(op, HandleBinding)
        return blocks, expressions, handles

    def _filter_components(
        self, op: QuantumOperation, component_type: type
    ) -> list[str]:
        return [
            component
            for component in self._components
            if isinstance(getattr(op, component, None), component_type)
        ]

    def expand_blocks(
        self, op: QuantumOperation, block_names: list[str]
    ) -> dict[str, list[QuantumStatement]]:
        blocks = {
            _BLOCK_RENAMES.get(block, block): block_statements
            for block in block_names
            if (block_statements := getattr(op, block)) is not None
        }
        block_closure = Closure(
            name=self._operation_name,
            scope=Scope(parent=self._current_scope),
            blocks=blocks,
        )
        context = self._expand_operation(block_closure)
        return {
            block: context.statements(_BLOCK_RENAMES.get(block, block))
            for block in block_names
        }

    def expand_generative_blocks(
        self, op: QuantumOperation
    ) -> dict[str, list[QuantumStatement]]:
        blocks = [block for block in self._components if op.has_generative_block(block)]
        context = self._expand_generative_context(op, self._operation_name, blocks)
        return {
            _REVERSE_BLOCK_RENAMES.get(block, block): context.statements(block)
            for block in blocks
        }

    def _update_result_type(self, op: ArithmeticOperation) -> None:
        expr = str(self._evaluate_expression(op.expression))
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expr))
        symbols: list[QuantumSymbol] = [
            symbol
            for handle in vrc.var_handles
            if isinstance(
                symbol := self._interpreter.evaluate(handle).value, QuantumSymbol
            )
        ]
        expr = rename_variables(
            expr,
            {str(symbol.handle): symbol.handle.identifier for symbol in symbols}
            | {symbol.handle.qmod_expr: symbol.handle.identifier for symbol in symbols},
        )
        for symbol in symbols:
            expr = expr.replace(symbol.handle.qmod_expr, symbol.handle.identifier)
        result_type = compute_arithmetic_result_type(
            expr,
            {symbol.handle.identifier: symbol.quantum_type for symbol in symbols},
            self._machine_precision,
        )
        result_symbol = self._interpreter.evaluate(op.result_var).as_type(QuantumSymbol)
        copy_type_information(
            result_type, result_symbol.quantum_type, str(op.result_var)
        )
