from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from classiq.interface.generator.expressions.qmod_struct_instance import (
    QmodStructInstance,
)
from classiq.interface.generator.functions.type_name import Struct
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    PositionalArg,
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumStatement

from classiq.model_expansions.closure import (
    FunctionClosure,
    GenerativeClosure,
)
from classiq.model_expansions.scope import Evaluated, QuantumSymbol
from classiq.qmod.generative import generative_mode_context, set_frontend_interpreter
from classiq.qmod.model_state_container import QMODULE
from classiq.qmod.qmod_parameter import CParamStruct
from classiq.qmod.qmod_variable import QNum, _create_qvar_for_qtype
from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.quantum_expandable import (
    QExpandable,
    QTerminalCallable,
)
from classiq.qmod.quantum_function import QFunc
from classiq.qmod.semantics.static_semantics_visitor import resolve_function_calls
from classiq.qmod.symbolic_expr import SymbolicExpr

if TYPE_CHECKING:
    from classiq.model_expansions.interpreter import Interpreter


class LenList(list):
    @property
    def len(self) -> int:
        return len(self)

    def __getitem__(self, item: Any) -> Any:
        if isinstance(item, QNum):
            return SymbolicExpr(f"{self}[{item}]", True)
        return super().__getitem__(item)

    @classmethod
    def wrap(cls, obj: Any) -> Any:
        if not isinstance(obj, list):
            return obj
        return LenList([cls.wrap(item) for item in obj])


def translate_ast_arg_to_python_qmod(param: PositionalArg, evaluated: Evaluated) -> Any:
    if isinstance(param, PortDeclaration):
        quantum_symbol = evaluated.as_type(QuantumSymbol)
        return _create_qvar_for_qtype(
            quantum_symbol.quantum_type, quantum_symbol.handle
        )
    if isinstance(param, QuantumOperandDeclaration):
        if param.is_list:
            func_list: list[FunctionClosure] = evaluated.as_type(list)
            return LenList(
                [
                    QTerminalCallable(
                        QuantumOperandDeclaration(
                            name=param.name,
                            positional_arg_declarations=param.positional_arg_declarations,
                        ),
                        index_=idx,
                    )
                    for idx in range(len(func_list))
                ]
            )
        else:
            func = evaluated.as_type(FunctionClosure)
            return QTerminalCallable(
                QuantumFunctionDeclaration(
                    name=param.name if func.is_lambda else func.name,
                    positional_arg_declarations=func.positional_arg_declarations,
                ),
            )
    classical_value = evaluated.value
    if isinstance(classical_value, QmodStructInstance):
        return CParamStruct(
            expr=param.name,
            struct_type=Struct(name=classical_value.struct_declaration.name),
            qmodule=QMODULE,
        )
    return LenList.wrap(classical_value)


class _InterpreterExpandable(QFunc):
    def __init__(self, interpreter: "Interpreter"):
        super().__init__(lambda: None)
        self._interpreter = interpreter

    def append_statement_to_body(self, stmt: QuantumStatement) -> None:
        current_operation = self._interpreter._builder._operations[-1]
        dummy_function = NativeFunctionDefinition(
            name=current_operation.name,
            positional_arg_declarations=current_operation.positional_arg_declarations,
            body=self._interpreter._builder._current_statements + [stmt],
        )
        resolve_function_calls(dummy_function, self._get_function_declarations())
        stmt = dummy_function.body[-1]
        with generative_mode_context(False):
            self._interpreter.emit_statement(stmt)

    def _get_function_declarations(self) -> Mapping[str, QuantumFunctionDeclaration]:
        return {
            name: QuantumFunctionDeclaration(
                name=name,
                positional_arg_declarations=evaluated.value.positional_arg_declarations,
            )
            for name, evaluated in self._interpreter._current_scope.items()
            if isinstance(evaluated, Evaluated)
            and isinstance(evaluated.value, FunctionClosure)
        } | nameables_to_dict(self._interpreter._get_function_declarations())


def emit_generative_statements(
    interpreter: "Interpreter",
    operation: GenerativeClosure,
    args: list[Evaluated],
) -> None:
    python_qmod_args = [
        translate_ast_arg_to_python_qmod(param, arg)
        for param, arg in zip(operation.positional_arg_declarations, args)
    ]
    interpreter_expandable = _InterpreterExpandable(interpreter)
    QExpandable.STACK.append(interpreter_expandable)
    QCallable.CURRENT_EXPANDABLE = interpreter_expandable
    set_frontend_interpreter(interpreter)
    for block_name, generative_function in operation.generative_blocks.items():
        with interpreter._builder.block_context(block_name), generative_mode_context(
            True
        ):
            generative_function._py_callable(*python_qmod_args)
