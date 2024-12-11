"""
Python bindings for the Mimir planning library.
"""
from __future__ import annotations
import pybind11_stubgen.typing_ext
import typing
__all__ = ['ACTION_COSTS', 'ADL', 'ASSIGN', 'AStarAlgorithm', 'AStarAlgorithmEventHandlerBase', 'AStarAlgorithmStatistics', 'Abstraction', 'Action', 'ActionGrounder', 'ActionList', 'AssignOperatorEnum', 'Axiom', 'AxiomGrounder', 'AxiomList', 'BinaryOperatorEnum', 'BlindHeuristic', 'BrFSAlgorithm', 'BrFSAlgorithmStatistics', 'CLOSED', 'CONDITIONAL_EFFECTS', 'CONSTRAINTS', 'Certificate2FWL', 'Certificate3FWL', 'Certificate4FWL', 'CertificateColorRefinement', 'ColorFunction', 'ColoredVertex', 'ConditionGrounder', 'DEAD_END', 'DECREASE', 'DERIVED_PREDICATES', 'DISJUNCTIVE_PRECONDITIONS', 'DIV', 'DURATIVE_ACTIONS', 'DebugAStarAlgorithmEventHandler', 'DebugBrFSAlgorithmEventHandler', 'DebugGroundedApplicableActionGeneratorEventHandler', 'DebugGroundedAxiomEvaluatorEventHandler', 'DebugLiftedApplicableActionGeneratorEventHandler', 'DebugLiftedAxiomEvaluatorEventHandler', 'DefaultAStarAlgorithmEventHandler', 'DefaultBrFSAlgorithmEventHandler', 'DefaultGroundedApplicableActionGeneratorEventHandler', 'DefaultGroundedAxiomEvaluatorEventHandler', 'DefaultIWAlgorithmEventHandler', 'DefaultLiftedApplicableActionGeneratorEventHandler', 'DefaultLiftedAxiomEvaluatorEventHandler', 'DefaultSIWAlgorithmEventHandler', 'DeleteRelaxedProblemExplorator', 'DerivedAssignmentSet', 'DerivedAtom', 'DerivedAtomList', 'DerivedGroundAtom', 'DerivedGroundAtomList', 'DerivedGroundLiteral', 'DerivedGroundLiteralList', 'DerivedLiteral', 'DerivedLiteralList', 'DerivedPredicate', 'DerivedPredicateList', 'Domain', 'DomainList', 'EQUALITY', 'EXHAUSTED', 'EXISTENTIAL_PRECONDITIONS', 'EffectConditional', 'EffectConditionalList', 'EffectStrips', 'EmptyEdge', 'EmptyVertex', 'FAILED', 'FLUENTS', 'FaithfulAbstractStateVertex', 'FaithfulAbstraction', 'FaithfulAbstractionOptions', 'FaithfulAbstractionsOptions', 'FluentAssignmentSet', 'FluentAtom', 'FluentAtomList', 'FluentGroundAtom', 'FluentGroundAtomList', 'FluentGroundLiteral', 'FluentGroundLiteralList', 'FluentLiteral', 'FluentLiteralList', 'FluentPredicate', 'FluentPredicateList', 'Function', 'FunctionExpression', 'FunctionExpressionBinaryOperator', 'FunctionExpressionFunction', 'FunctionExpressionList', 'FunctionExpressionMinus', 'FunctionExpressionMultiOperator', 'FunctionExpressionNumber', 'FunctionList', 'FunctionSkeleton', 'FunctionSkeletonList', 'GlobalFaithfulAbstractState', 'GlobalFaithfulAbstraction', 'GroundAction', 'GroundActionEdge', 'GroundActionList', 'GroundActionSpan', 'GroundActionsEdge', 'GroundAxiom', 'GroundAxiomList', 'GroundConditionStrips', 'GroundEffectConditional', 'GroundEffectConditionalList', 'GroundEffectDerivedLiteral', 'GroundEffectFluentLiteral', 'GroundEffectStrips', 'GroundFunction', 'GroundFunctionExpression', 'GroundFunctionExpressionBinaryOperator', 'GroundFunctionExpressionFunction', 'GroundFunctionExpressionList', 'GroundFunctionExpressionMinus', 'GroundFunctionExpressionMultiOperator', 'GroundFunctionExpressionNumber', 'GroundFunctionList', 'GroundedApplicableActionGenerator', 'GroundedAxiomEvaluator', 'IAStarAlgorithmEventHandler', 'IAlgorithm', 'IApplicableActionGenerator', 'IAxiomEvaluator', 'IBrFSAlgorithmEventHandler', 'IGroundedApplicableActionGeneratorEventHandler', 'IGroundedAxiomEvaluatorEventHandler', 'IHeuristic', 'IIWAlgorithmEventHandler', 'ILiftedApplicableActionGeneratorEventHandler', 'ILiftedAxiomEvaluatorEventHandler', 'INCREASE', 'IN_PROGRESS', 'ISIWAlgorithmEventHandler', 'IWAlgorithm', 'IWAlgorithmStatistics', 'IndexGroupedVector', 'IsomorphismTypeCompressionFunction', 'LiftedApplicableActionGenerator', 'LiftedAxiomEvaluator', 'MAXIMIZE', 'MINIMIZE', 'MINUS', 'MUL', 'MultiOperatorEnum', 'NEGATIVE_PRECONDITIONS', 'NEW', 'NUMERIC_FLUENTS', 'NautyCertificate', 'NautyDenseGraph', 'NautySparseGraph', 'None', 'NumericFluent', 'NumericFluentList', 'OBJECT_FLUENTS', 'OPEN', 'OUT_OF_MEMORY', 'OUT_OF_TIME', 'Object', 'ObjectGraphPruningStrategy', 'ObjectGraphPruningStrategyEnum', 'ObjectList', 'OptimizationMetric', 'OptimizationMetricEnum', 'PDDLParser', 'PDDLRepositories', 'PLUS', 'PREFERENCES', 'Plan', 'Problem', 'ProblemColorFunction', 'ProblemList', 'QUANTIFIED_PRECONDITIONS', 'RequirementEnum', 'Requirements', 'SCALE_DOWN', 'SCALE_UP', 'SIWAlgorithm', 'SIWAlgorithmStatistics', 'SOLVED', 'STRIPS', 'SearchNodeStatus', 'SearchResult', 'SearchStatus', 'State', 'StateList', 'StateRepository', 'StateSpace', 'StateSpaceOptions', 'StateSpacesOptions', 'StateSpan', 'StateVertex', 'StaticAssignmentSet', 'StaticAtom', 'StaticAtomList', 'StaticDigraph', 'StaticGroundAtom', 'StaticGroundAtomList', 'StaticGroundLiteral', 'StaticGroundLiteralList', 'StaticLiteral', 'StaticLiteralList', 'StaticPredicate', 'StaticPredicateList', 'StaticScc', 'StaticVertexColoredDigraph', 'StringToDerivedPredicateMap', 'StringToFluentPredicateMap', 'StringToStaticPredicateMap', 'TIMED_INITIAL_LITERALS', 'TYPING', 'Term', 'TermList', 'TupleGraph', 'TupleGraphFactory', 'TupleGraphVertex', 'TupleGraphVertexIndexGroupedVector', 'TupleGraphVertexSpan', 'TupleIndexMapper', 'UNIVERSAL_PRECONDITIONS', 'UNSOLVABLE', 'Variable', 'VariableList', 'compute_certificate_2fwl', 'compute_certificate_3fwl', 'compute_certificate_4fwl', 'compute_certificate_color_refinement', 'create_object_graph']
class AStarAlgorithm(IAlgorithm):
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, heuristic: IHeuristic) -> None:
        ...
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, heuristic: IHeuristic, event_handler: IAStarAlgorithmEventHandler) -> None:
        ...
class AStarAlgorithmEventHandlerBase(IAStarAlgorithmEventHandler):
    def __init__(self, quiet: bool = True) -> None:
        ...
class AStarAlgorithmStatistics:
    def get_num_deadends(self) -> int:
        ...
    def get_num_deadends_until_f_value(self) -> list[int]:
        ...
    def get_num_expanded(self) -> int:
        ...
    def get_num_expanded_until_f_value(self) -> list[int]:
        ...
    def get_num_generated(self) -> int:
        ...
    def get_num_generated_until_f_value(self) -> list[int]:
        ...
    def get_num_pruned(self) -> int:
        ...
    def get_num_pruned_until_f_value(self) -> list[int]:
        ...
class Abstraction:
    @typing.overload
    def __init__(self, faithful_abstraction: FaithfulAbstraction) -> None:
        ...
    @typing.overload
    def __init__(self, global_faithful_abstraction: GlobalFaithfulAbstraction) -> None:
        ...
    def get_applicable_action_generator(self) -> IApplicableActionGenerator:
        ...
    def get_backward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_transitions(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_deadend_vertex_indices(self) -> set[int]:
        ...
    def get_edge_cost(self, edge_index: int) -> float:
        ...
    def get_forward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_goal_distance(self, state_index: int) -> float:
        ...
    def get_goal_distances(self) -> list[float]:
        ...
    def get_goal_vertex_indices(self) -> set[int]:
        ...
    def get_initial_vertex_index(self) -> int:
        ...
    def get_num_deadend_vertices(self) -> int:
        ...
    def get_num_edges(self) -> int:
        ...
    def get_num_goal_vertices(self) -> int:
        ...
    def get_num_vertices(self) -> int:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
    def get_state_repository(self) -> StateRepository:
        ...
    def get_vertex_index(self, arg0: State) -> int:
        ...
    def is_alive_vertex(self, vertex_index: int) -> bool:
        ...
    def is_deadend_vertex(self, vertex_index: int) -> bool:
        ...
    def is_goal_vertex(self, vertex_index: int) -> bool:
        ...
class Action:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_conditional_effects(self) -> EffectConditionalList:
        ...
    def get_derived_conditions(self) -> DerivedLiteralList:
        ...
    def get_fluent_conditions(self) -> FluentLiteralList:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_parameters(self) -> VariableList:
        ...
    def get_static_conditions(self) -> StaticLiteralList:
        ...
    def get_strips_effect(self) -> EffectStrips:
        ...
class ActionGrounder:
    def get_action_precondition_grounders(self) -> dict[Action, ConditionGrounder]:
        ...
    def get_ground_action(self, action_index: int) -> GroundAction:
        ...
    def get_ground_actions(self) -> GroundActionList:
        ...
    def get_num_ground_actions(self) -> int:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
    def ground_action(self, action: Action, binding: ObjectList) -> GroundAction:
        ...
class ActionList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Action) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: ActionList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> ActionList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Action:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ActionList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: ActionList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Action) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: ActionList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Action) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Action) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: ActionList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Action) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Action:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Action:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Action) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class AssignOperatorEnum:
    """
    Members:
    
      ASSIGN
    
      SCALE_UP
    
      SCALE_DOWN
    
      INCREASE
    
      DECREASE
    """
    ASSIGN: typing.ClassVar[AssignOperatorEnum]  # value = <AssignOperatorEnum.ASSIGN: 0>
    DECREASE: typing.ClassVar[AssignOperatorEnum]  # value = <AssignOperatorEnum.DECREASE: 4>
    INCREASE: typing.ClassVar[AssignOperatorEnum]  # value = <AssignOperatorEnum.INCREASE: 3>
    SCALE_DOWN: typing.ClassVar[AssignOperatorEnum]  # value = <AssignOperatorEnum.SCALE_DOWN: 2>
    SCALE_UP: typing.ClassVar[AssignOperatorEnum]  # value = <AssignOperatorEnum.SCALE_UP: 1>
    __members__: typing.ClassVar[dict[str, AssignOperatorEnum]]  # value = {'ASSIGN': <AssignOperatorEnum.ASSIGN: 0>, 'SCALE_UP': <AssignOperatorEnum.SCALE_UP: 1>, 'SCALE_DOWN': <AssignOperatorEnum.SCALE_DOWN: 2>, 'INCREASE': <AssignOperatorEnum.INCREASE: 3>, 'DECREASE': <AssignOperatorEnum.DECREASE: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Axiom:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_derived_conditions(self) -> DerivedLiteralList:
        ...
    def get_fluent_conditions(self) -> FluentLiteralList:
        ...
    def get_index(self) -> int:
        ...
    def get_literal(self) -> DerivedLiteral:
        ...
    def get_static_conditions(self) -> StaticLiteralList:
        ...
class AxiomGrounder:
    def get_axiom_precondition_grounders(self) -> dict[Axiom, ConditionGrounder]:
        ...
    def get_ground_axiom(self, axiom_index: int) -> GroundAxiom:
        ...
    def get_ground_axioms(self) -> GroundAxiomList:
        ...
    def get_num_ground_axioms(self) -> int:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
    def ground_axiom(self, axiom: Axiom, binding: ObjectList) -> GroundAxiom:
        ...
class AxiomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Axiom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: AxiomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> AxiomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Axiom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: AxiomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: AxiomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Axiom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: AxiomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Axiom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Axiom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: AxiomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Axiom) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Axiom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Axiom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Axiom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class BinaryOperatorEnum:
    """
    Members:
    
      MUL
    
      PLUS
    
      MINUS
    
      DIV
    """
    DIV: typing.ClassVar[BinaryOperatorEnum]  # value = <BinaryOperatorEnum.DIV: 3>
    MINUS: typing.ClassVar[BinaryOperatorEnum]  # value = <BinaryOperatorEnum.MINUS: 2>
    MUL: typing.ClassVar[BinaryOperatorEnum]  # value = <BinaryOperatorEnum.MUL: 0>
    PLUS: typing.ClassVar[BinaryOperatorEnum]  # value = <BinaryOperatorEnum.PLUS: 1>
    __members__: typing.ClassVar[dict[str, BinaryOperatorEnum]]  # value = {'MUL': <BinaryOperatorEnum.MUL: 0>, 'PLUS': <BinaryOperatorEnum.PLUS: 1>, 'MINUS': <BinaryOperatorEnum.MINUS: 2>, 'DIV': <BinaryOperatorEnum.DIV: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BlindHeuristic(IHeuristic):
    def __init__(self) -> None:
        ...
class BrFSAlgorithm(IAlgorithm):
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository) -> None:
        ...
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, event_handler: IBrFSAlgorithmEventHandler) -> None:
        ...
class BrFSAlgorithmStatistics:
    def get_num_deadends(self) -> int:
        ...
    def get_num_deadends_until_g_value(self) -> list[int]:
        ...
    def get_num_expanded(self) -> int:
        ...
    def get_num_expanded_until_g_value(self) -> list[int]:
        ...
    def get_num_generated(self) -> int:
        ...
    def get_num_generated_until_g_value(self) -> list[int]:
        ...
    def get_num_pruned(self) -> int:
        ...
    def get_num_pruned_until_g_value(self) -> list[int]:
        ...
class Certificate2FWL:
    def __eq__(self, arg0: Certificate2FWL) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def get_canonical_coloring(self) -> list[int]:
        ...
class Certificate3FWL:
    def __eq__(self, arg0: Certificate3FWL) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def get_canonical_coloring(self) -> list[int]:
        ...
class Certificate4FWL:
    def __eq__(self, arg0: Certificate4FWL) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def get_canonical_coloring(self) -> list[int]:
        ...
class CertificateColorRefinement:
    def __eq__(self, arg0: CertificateColorRefinement) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def get_canonical_coloring(self) -> list[int]:
        ...
class ColorFunction:
    def get_color_name(self, color: int) -> str:
        ...
class ColoredVertex:
    def __eq__(self, arg0: ColoredVertex) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_color(self) -> int:
        ...
    def get_index(self) -> int:
        ...
class ConditionGrounder:
    def __init__(self, problem: Problem, pddl_repositories: PDDLRepositories, parameters: VariableList, static_literals: StaticLiteralList, fluent_literals: FluentLiteralList, derived_literals: DerivedLiteralList, static_assignment_set: StaticAssignmentSet) -> None:
        ...
    def create_ground_conjunction_generator(self, arg0: State, arg1: int) -> list[tuple[ObjectList, tuple[StaticGroundLiteralList, FluentGroundLiteralList, DerivedGroundLiteralList]]]:
        ...
class DebugAStarAlgorithmEventHandler(IAStarAlgorithmEventHandler):
    def __init__(self, quiet: bool = True) -> None:
        ...
class DebugBrFSAlgorithmEventHandler(IBrFSAlgorithmEventHandler):
    def __init__(self) -> None:
        ...
class DebugGroundedApplicableActionGeneratorEventHandler(IGroundedApplicableActionGeneratorEventHandler):
    def __init__(self) -> None:
        ...
class DebugGroundedAxiomEvaluatorEventHandler(IGroundedAxiomEvaluatorEventHandler):
    def __init__(self) -> None:
        ...
class DebugLiftedApplicableActionGeneratorEventHandler(ILiftedApplicableActionGeneratorEventHandler):
    def __init__(self) -> None:
        ...
class DebugLiftedAxiomEvaluatorEventHandler(ILiftedAxiomEvaluatorEventHandler):
    def __init__(self) -> None:
        ...
class DefaultAStarAlgorithmEventHandler(IAStarAlgorithmEventHandler):
    def __init__(self, quiet: bool = True) -> None:
        ...
class DefaultBrFSAlgorithmEventHandler(IBrFSAlgorithmEventHandler):
    def __init__(self) -> None:
        ...
class DefaultGroundedApplicableActionGeneratorEventHandler(IGroundedApplicableActionGeneratorEventHandler):
    def __init__(self) -> None:
        ...
class DefaultGroundedAxiomEvaluatorEventHandler(IGroundedAxiomEvaluatorEventHandler):
    def __init__(self) -> None:
        ...
class DefaultIWAlgorithmEventHandler(IIWAlgorithmEventHandler):
    def __init__(self) -> None:
        ...
class DefaultLiftedApplicableActionGeneratorEventHandler(ILiftedApplicableActionGeneratorEventHandler):
    def __init__(self) -> None:
        ...
class DefaultLiftedAxiomEvaluatorEventHandler(ILiftedAxiomEvaluatorEventHandler):
    def __init__(self) -> None:
        ...
class DefaultSIWAlgorithmEventHandler(ISIWAlgorithmEventHandler):
    def __init__(self) -> None:
        ...
class DeleteRelaxedProblemExplorator:
    def __init__(self, problem: Problem, pddl_repositories: PDDLRepositories) -> None:
        ...
    def create_grounded_applicable_action_generator(self, axiom_evaluator_event_handler: IGroundedApplicableActionGeneratorEventHandler = ...) -> GroundedApplicableActionGenerator:
        ...
    def create_grounded_axiom_evaluator(self, axiom_evaluator_event_handler: IGroundedAxiomEvaluatorEventHandler = ...) -> GroundedAxiomEvaluator:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
class DerivedAssignmentSet:
    def __init__(self, problem: Problem, predicates: DerivedPredicateList, ground_atoms: DerivedGroundAtomList) -> None:
        ...
class DerivedAtom:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_predicate(self) -> DerivedPredicate:
        ...
    def get_terms(self) -> TermList:
        ...
    def get_variables(self) -> VariableList:
        ...
class DerivedAtomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: DerivedAtom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: DerivedAtomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> DerivedAtomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> DerivedAtom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: DerivedAtomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: DerivedAtomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: DerivedAtom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DerivedAtomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: DerivedAtom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: DerivedAtom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: DerivedAtomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: DerivedAtom) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> DerivedAtom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> DerivedAtom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: DerivedAtom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class DerivedGroundAtom:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_objects(self) -> ObjectList:
        ...
    def get_predicate(self) -> DerivedPredicate:
        ...
class DerivedGroundAtomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: DerivedGroundAtom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: DerivedGroundAtomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> DerivedGroundAtomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> DerivedGroundAtom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: DerivedGroundAtomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: DerivedGroundAtomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: DerivedGroundAtom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DerivedGroundAtomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: DerivedGroundAtom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: DerivedGroundAtom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: DerivedGroundAtomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: DerivedGroundAtom) -> None:
        """
        Insert an item at a given position.
        """
    def lift(self, pddl_repositories: ...) -> tuple[VariableList, DerivedAtomList]:
        ...
    @typing.overload
    def pop(self) -> DerivedGroundAtom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> DerivedGroundAtom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: DerivedGroundAtom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class DerivedGroundLiteral:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_atom(self) -> DerivedGroundAtom:
        ...
    def get_index(self) -> int:
        ...
    def is_negated(self) -> bool:
        ...
class DerivedGroundLiteralList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: DerivedGroundLiteral) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: DerivedGroundLiteralList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> DerivedGroundLiteralList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> DerivedGroundLiteral:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: DerivedGroundLiteralList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: DerivedGroundLiteralList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: DerivedGroundLiteral) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DerivedGroundLiteralList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: DerivedGroundLiteral) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: DerivedGroundLiteral) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: DerivedGroundLiteralList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: DerivedGroundLiteral) -> None:
        """
        Insert an item at a given position.
        """
    def lift(self, pddl_repositories: ...) -> tuple[VariableList, ..., ...]:
        ...
    @typing.overload
    def pop(self) -> DerivedGroundLiteral:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> DerivedGroundLiteral:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: DerivedGroundLiteral) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class DerivedLiteral:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_atom(self) -> DerivedAtom:
        ...
    def get_index(self) -> int:
        ...
    def is_negated(self) -> bool:
        ...
class DerivedLiteralList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: DerivedLiteral) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: DerivedLiteralList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> DerivedLiteralList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> DerivedLiteral:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: DerivedLiteralList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: DerivedLiteralList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: DerivedLiteral) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DerivedLiteralList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: DerivedLiteral) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: DerivedLiteral) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: DerivedLiteralList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: DerivedLiteral) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> DerivedLiteral:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> DerivedLiteral:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: DerivedLiteral) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class DerivedPredicate:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_parameters(self) -> VariableList:
        ...
class DerivedPredicateList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: DerivedPredicate) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: DerivedPredicateList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> DerivedPredicateList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> DerivedPredicate:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: DerivedPredicateList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: DerivedPredicateList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: DerivedPredicate) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DerivedPredicateList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: DerivedPredicate) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: DerivedPredicate) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: DerivedPredicateList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: DerivedPredicate) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> DerivedPredicate:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> DerivedPredicate:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: DerivedPredicate) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class Domain:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_actions(self) -> ActionList:
        ...
    def get_constants(self) -> ObjectList:
        ...
    def get_derived_predicates(self) -> DerivedPredicateList:
        ...
    def get_filepath(self) -> str | None:
        ...
    def get_fluent_predicates(self) -> FluentPredicateList:
        ...
    def get_functions(self) -> FunctionSkeletonList:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_name_to_derived_predicate(self) -> StringToDerivedPredicateMap:
        ...
    def get_name_to_fluent_predicate(self) -> StringToFluentPredicateMap:
        ...
    def get_name_to_static_predicate(self) -> StringToStaticPredicateMap:
        ...
    def get_requirements(self) -> Requirements:
        ...
    def get_static_predicates(self) -> StaticPredicateList:
        ...
class DomainList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Domain) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: DomainList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> DomainList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Domain:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: DomainList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: DomainList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Domain) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DomainList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Domain) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Domain) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: DomainList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Domain) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Domain:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Domain:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Domain) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class EffectConditional:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_derived_conditions(self) -> DerivedLiteralList:
        ...
    def get_effects(self) -> FluentLiteralList:
        ...
    def get_fluent_conditions(self) -> FluentLiteralList:
        ...
    def get_index(self) -> int:
        ...
    def get_parameters(self) -> VariableList:
        ...
    def get_static_conditions(self) -> StaticLiteralList:
        ...
class EffectConditionalList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: EffectConditional) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: EffectConditionalList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> EffectConditionalList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> EffectConditional:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: EffectConditionalList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: EffectConditionalList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: EffectConditional) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: EffectConditionalList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: EffectConditional) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: EffectConditional) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: EffectConditionalList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: EffectConditional) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> EffectConditional:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> EffectConditional:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: EffectConditional) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class EffectStrips:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_effects(self) -> FluentLiteralList:
        ...
    def get_function_expression(self) -> ...:
        ...
    def get_index(self) -> int:
        ...
class EmptyEdge:
    def __eq__(self, arg0: EmptyEdge) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_source(self) -> int:
        ...
    def get_target(self) -> int:
        ...
class EmptyVertex:
    def __eq__(self, arg0: EmptyVertex) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_index(self) -> int:
        ...
class FaithfulAbstractStateVertex:
    def get_certificate(self) -> NautyCertificate:
        ...
    def get_index(self) -> int:
        ...
    def get_representative_state(self) -> State:
        ...
    def get_states(self) -> StateList:
        ...
class FaithfulAbstraction:
    @staticmethod
    @typing.overload
    def create(domain_filepath: str, problem_filepath: str, options: FaithfulAbstractionOptions = ...) -> FaithfulAbstraction | None:
        ...
    @staticmethod
    @typing.overload
    def create(problem: Problem, factories: PDDLRepositories, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, options: FaithfulAbstractionOptions = ...) -> FaithfulAbstraction | None:
        ...
    @staticmethod
    @typing.overload
    def create(domain_filepath: str, problem_filepaths: list[str], options: FaithfulAbstractionsOptions = ...) -> list[FaithfulAbstraction]:
        ...
    @staticmethod
    @typing.overload
    def create(memories: list[tuple[Problem, PDDLRepositories, IApplicableActionGenerator, StateRepository]], options: FaithfulAbstractionsOptions = ...) -> list[FaithfulAbstraction]:
        ...
    def __str__(self) -> str:
        ...
    def compute_pairwise_shortest_backward_state_distances(self) -> list[list[float]]:
        ...
    def compute_pairwise_shortest_forward_state_distances(self) -> list[list[float]]:
        ...
    def compute_shortest_backward_distances_from_states(self, vertex_indices: list[int]) -> list[float]:
        ...
    def compute_shortest_forward_distances_from_states(self, vertex_indices: list[int]) -> list[float]:
        ...
    def get_applicable_action_generator(self) -> IApplicableActionGenerator:
        ...
    def get_backward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_deadend_vertex_indices(self) -> set[int]:
        ...
    def get_edge(self, edge_index: int) -> GroundActionsEdge:
        ...
    def get_edge_cost(self, edge_index: int) -> float:
        ...
    def get_edges(self) -> list[GroundActionsEdge]:
        ...
    def get_forward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_goal_distance(self, state_index: int) -> float:
        ...
    def get_goal_distances(self) -> list[float]:
        ...
    def get_goal_vertex_indices(self) -> set[int]:
        ...
    def get_initial_vertex_index(self) -> int:
        ...
    def get_num_deadend_vertices(self) -> int:
        ...
    def get_num_edges(self) -> int:
        ...
    def get_num_goal_vertices(self) -> int:
        ...
    def get_num_vertices(self) -> int:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
    def get_state_repository(self) -> StateRepository:
        ...
    def get_state_to_vertex_index(self) -> dict[State, int]:
        ...
    def get_vertex_index(self, state: State) -> int:
        ...
    def get_vertices(self) -> list[FaithfulAbstractStateVertex]:
        ...
    def is_alive_vertex(self, vertex_index: int) -> bool:
        ...
    def is_deadend_vertex(self, vertex_index: int) -> bool:
        ...
    def is_goal_vertex(self, vertex_index: int) -> bool:
        ...
class FaithfulAbstractionOptions:
    compute_complete_abstraction_mapping: bool
    mark_true_goal_literals: bool
    max_num_abstract_states: int
    max_num_concrete_states: int
    pruning_strategy: ObjectGraphPruningStrategyEnum
    remove_if_unsolvable: bool
    timeout_ms: int
    use_unit_cost_one: bool
    def __init__(self, mark_true_goal_literals: bool = False, use_unit_cost_one: bool = True, remove_if_unsolvable: bool = True, compute_complete_abstraction_mapping: bool = False, max_num_concrete_states: int = 4294967295, max_num_abstract_states: int = 4294967295, timeout_ms: int = 4294967295, pruning_strategy: ObjectGraphPruningStrategyEnum = ...) -> None:
        ...
class FaithfulAbstractionsOptions:
    fa_options: FaithfulAbstractionOptions
    num_threads: int
    sort_ascending_by_num_states: bool
    def __init__(self, fa_options: FaithfulAbstractionOptions = ..., sort_ascending_by_num_states: bool = True, num_threads: int = 4) -> None:
        ...
class FluentAssignmentSet:
    def __init__(self, problem: Problem, predicates: FluentPredicateList, ground_atoms: FluentGroundAtomList) -> None:
        ...
class FluentAtom:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_predicate(self) -> FluentPredicate:
        ...
    def get_terms(self) -> TermList:
        ...
    def get_variables(self) -> VariableList:
        ...
class FluentAtomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FluentAtom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FluentAtomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FluentAtomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> FluentAtom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FluentAtomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FluentAtomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: FluentAtom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FluentAtomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FluentAtom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FluentAtom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FluentAtomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: FluentAtom) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> FluentAtom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> FluentAtom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FluentAtom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class FluentGroundAtom:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_objects(self) -> ObjectList:
        ...
    def get_predicate(self) -> FluentPredicate:
        ...
class FluentGroundAtomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FluentGroundAtom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FluentGroundAtomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FluentGroundAtomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> FluentGroundAtom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FluentGroundAtomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FluentGroundAtomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: FluentGroundAtom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FluentGroundAtomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FluentGroundAtom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FluentGroundAtom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FluentGroundAtomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: FluentGroundAtom) -> None:
        """
        Insert an item at a given position.
        """
    def lift(self, pddl_repositories: ...) -> tuple[VariableList, FluentAtomList]:
        ...
    @typing.overload
    def pop(self) -> FluentGroundAtom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> FluentGroundAtom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FluentGroundAtom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class FluentGroundLiteral:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_atom(self) -> FluentGroundAtom:
        ...
    def get_index(self) -> int:
        ...
    def is_negated(self) -> bool:
        ...
class FluentGroundLiteralList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FluentGroundLiteral) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FluentGroundLiteralList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FluentGroundLiteralList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> FluentGroundLiteral:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FluentGroundLiteralList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FluentGroundLiteralList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: FluentGroundLiteral) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FluentGroundLiteralList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FluentGroundLiteral) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FluentGroundLiteral) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FluentGroundLiteralList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: FluentGroundLiteral) -> None:
        """
        Insert an item at a given position.
        """
    def lift(self, pddl_repositories: ...) -> tuple[VariableList, ..., ...]:
        ...
    @typing.overload
    def pop(self) -> FluentGroundLiteral:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> FluentGroundLiteral:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FluentGroundLiteral) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class FluentLiteral:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_atom(self) -> FluentAtom:
        ...
    def get_index(self) -> int:
        ...
    def is_negated(self) -> bool:
        ...
class FluentLiteralList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FluentLiteral) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FluentLiteralList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FluentLiteralList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> FluentLiteral:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FluentLiteralList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FluentLiteralList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: FluentLiteral) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FluentLiteralList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FluentLiteral) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FluentLiteral) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FluentLiteralList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: FluentLiteral) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> FluentLiteral:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> FluentLiteral:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FluentLiteral) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class FluentPredicate:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_parameters(self) -> VariableList:
        ...
class FluentPredicateList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FluentPredicate) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FluentPredicateList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FluentPredicateList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> FluentPredicate:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FluentPredicateList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FluentPredicateList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: FluentPredicate) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FluentPredicateList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FluentPredicate) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FluentPredicate) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FluentPredicateList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: FluentPredicate) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> FluentPredicate:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> FluentPredicate:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FluentPredicate) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class Function:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function_skeleton(self) -> FunctionSkeleton:
        ...
    def get_index(self) -> int:
        ...
    def get_terms(self) -> TermList:
        ...
class FunctionExpression:
    def get(self) -> typing.Any:
        ...
class FunctionExpressionBinaryOperator:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_binary_operator(self) -> BinaryOperatorEnum:
        ...
    def get_index(self) -> int:
        ...
    def get_left_function_expression(self) -> FunctionExpression:
        ...
    def get_right_function_expression(self) -> FunctionExpression:
        ...
class FunctionExpressionFunction:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function(self) -> Function:
        ...
    def get_index(self) -> int:
        ...
class FunctionExpressionList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FunctionExpression) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FunctionExpressionList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FunctionExpressionList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> FunctionExpression:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FunctionExpressionList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FunctionExpressionList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: FunctionExpression) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FunctionExpressionList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FunctionExpression) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FunctionExpression) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FunctionExpressionList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: FunctionExpression) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> FunctionExpression:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> FunctionExpression:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FunctionExpression) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class FunctionExpressionMinus:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function_expression(self) -> FunctionExpression:
        ...
    def get_index(self) -> int:
        ...
class FunctionExpressionMultiOperator:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function_expressions(self) -> FunctionExpressionList:
        ...
    def get_index(self) -> int:
        ...
    def get_multi_operator(self) -> MultiOperatorEnum:
        ...
class FunctionExpressionNumber:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_number(self) -> float:
        ...
class FunctionList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Function) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FunctionList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FunctionList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Function:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FunctionList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FunctionList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Function) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FunctionList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Function) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Function) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FunctionList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Function) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Function:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Function:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Function) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class FunctionSkeleton:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_parameters(self) -> VariableList:
        ...
class FunctionSkeletonList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FunctionSkeleton) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FunctionSkeletonList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FunctionSkeletonList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> FunctionSkeleton:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FunctionSkeletonList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FunctionSkeletonList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: FunctionSkeleton) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FunctionSkeletonList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FunctionSkeleton) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FunctionSkeleton) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FunctionSkeletonList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: FunctionSkeleton) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> FunctionSkeleton:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> FunctionSkeleton:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FunctionSkeleton) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class GlobalFaithfulAbstractState:
    def __eq__(self, arg0: GlobalFaithfulAbstractState) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_faithful_abstraction_index(self) -> int:
        ...
    def get_faithful_abstraction_vertex_index(self) -> int:
        ...
    def get_global_index(self) -> int:
        ...
    def get_vertex_index(self) -> int:
        ...
class GlobalFaithfulAbstraction:
    @staticmethod
    @typing.overload
    def create(domain_filepath: str, problem_filepaths: list[str], options: FaithfulAbstractionsOptions = ...) -> list[GlobalFaithfulAbstraction]:
        ...
    @staticmethod
    @typing.overload
    def create(memories: list[tuple[Problem, PDDLRepositories, IApplicableActionGenerator, StateRepository]], options: FaithfulAbstractionsOptions = ...) -> list[GlobalFaithfulAbstraction]:
        ...
    def __str__(self) -> str:
        ...
    def compute_pairwise_shortest_backward_state_distances(self) -> list[list[float]]:
        ...
    def compute_pairwise_shortest_forward_state_distances(self) -> list[list[float]]:
        ...
    def compute_shortest_backward_distances_from_states(self, vertex_indices: list[int]) -> list[float]:
        ...
    def compute_shortest_forward_distances_from_states(self, vertex_indices: list[int]) -> list[float]:
        ...
    def get_abstractions(self) -> list[FaithfulAbstraction]:
        ...
    def get_applicable_action_generator(self) -> IApplicableActionGenerator:
        ...
    def get_backward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_deadend_vertex_indices(self) -> set[int]:
        ...
    def get_edge(self, edge_index: int) -> GroundActionsEdge:
        ...
    def get_edge_cost(self, edge_index: int) -> float:
        ...
    def get_edges(self) -> list[GroundActionsEdge]:
        ...
    def get_forward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_global_vertex_index_to_vertex_index(self) -> dict[int, int]:
        ...
    def get_goal_distance(self, state_index: int) -> float:
        ...
    def get_goal_distances(self) -> list[float]:
        ...
    def get_goal_vertex_indices(self) -> set[int]:
        ...
    def get_index(self) -> int:
        ...
    def get_initial_vertex_index(self) -> int:
        ...
    def get_num_deadend_vertices(self) -> int:
        ...
    def get_num_edges(self) -> int:
        ...
    def get_num_goal_vertices(self) -> int:
        ...
    def get_num_isomorphic_states(self) -> int:
        ...
    def get_num_non_isomorphic_states(self) -> int:
        ...
    def get_num_vertices(self) -> int:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
    def get_state_repository(self) -> StateRepository:
        ...
    def get_state_to_vertex_index(self) -> dict[State, int]:
        ...
    @typing.overload
    def get_vertex_index(self, state: State) -> int:
        ...
    @typing.overload
    def get_vertex_index(self, global_state_index: int) -> int:
        ...
    def get_vertices(self) -> list[GlobalFaithfulAbstractState]:
        ...
    def is_alive_vertex(self, vertex_index: int) -> bool:
        ...
    def is_deadend_vertex(self, vertex_index: int) -> bool:
        ...
    def is_goal_vertex(self, vertex_index: int) -> bool:
        ...
class GroundAction:
    def __eq__(self, arg0: GroundAction) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_action_index(self) -> int:
        ...
    def get_conditional_effects(self) -> GroundEffectConditionalList:
        ...
    def get_index(self) -> int:
        ...
    def get_object_indices(self) -> FlatIndexList:
        ...
    def get_strips_effect(self) -> GroundEffectStrips:
        ...
    def get_strips_precondition(self) -> GroundConditionStrips:
        ...
    def to_string(self, arg0: PDDLRepositories) -> str:
        ...
    def to_string_for_plan(self, arg0: PDDLRepositories) -> str:
        ...
class GroundActionEdge:
    def __eq__(self, arg0: GroundActionEdge) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_cost(self) -> float:
        ...
    def get_creating_action(self) -> GroundAction:
        ...
    def get_index(self) -> int:
        ...
    def get_source(self) -> int:
        ...
    def get_target(self) -> int:
        ...
class GroundActionList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: GroundAction) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: GroundActionList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> GroundActionList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> GroundAction:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: GroundActionList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: GroundActionList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: GroundAction) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: GroundActionList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: GroundAction) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: GroundAction) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: GroundActionList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: GroundAction) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> GroundAction:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> GroundAction:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: GroundAction) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class GroundActionSpan:
    def __getitem__(self, arg0: int) -> GroundAction:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
class GroundActionsEdge:
    def __eq__(self, arg0: GroundActionsEdge) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_actions(self) -> GroundActionList:
        ...
    def get_cost(self) -> float:
        ...
    def get_index(self) -> int:
        ...
    def get_representative_action(self) -> GroundAction:
        ...
    def get_source(self) -> int:
        ...
    def get_target(self) -> int:
        ...
class GroundAxiom:
    def __eq__(self, arg0: GroundAxiom) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_axiom_index(self) -> int:
        ...
    def get_derived_effect(self) -> GroundEffectDerivedLiteral:
        ...
    def get_index(self) -> int:
        ...
    def get_object_indices(self) -> FlatIndexList:
        ...
    def get_strips_precondition(self) -> GroundConditionStrips:
        ...
    def to_string(self, arg0: PDDLRepositories) -> str:
        ...
class GroundAxiomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: GroundAxiom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: GroundAxiomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> GroundAxiomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> GroundAxiom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: GroundAxiomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: GroundAxiomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: GroundAxiom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: GroundAxiomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: GroundAxiom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: GroundAxiom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: GroundAxiomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: GroundAxiom) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> GroundAxiom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> GroundAxiom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: GroundAxiom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class GroundConditionStrips:
    def get_derived_negative_condition(self) -> FlatBitset:
        ...
    def get_derived_positive_condition(self) -> FlatBitset:
        ...
    def get_fluent_negative_condition(self) -> FlatBitset:
        ...
    def get_fluent_positive_condition(self) -> FlatBitset:
        ...
    def get_static_negative_condition(self) -> FlatBitset:
        ...
    def get_static_positive_condition(self) -> FlatBitset:
        ...
    def is_applicable(self, problem: Problem, state: State) -> bool:
        ...
    def is_dynamically_applicable(self, state: State) -> bool:
        ...
class GroundEffectConditional:
    def get_derived_negative_condition(self) -> FlatIndexList:
        ...
    def get_derived_positive_condition(self) -> FlatIndexList:
        ...
    def get_fluent_effect_literals(self) -> ...:
        ...
    def get_fluent_negative_condition(self) -> FlatIndexList:
        ...
    def get_fluent_positive_condition(self) -> FlatIndexList:
        ...
    def get_static_negative_condition(self) -> FlatIndexList:
        ...
    def get_static_positive_condition(self) -> FlatIndexList:
        ...
class GroundEffectConditionalList:
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, s: slice) -> GroundEffectConditionalList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> GroundEffectConditional:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: GroundEffectConditionalList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: GroundEffectConditional) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: GroundEffectConditionalList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: GroundEffectConditional) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: GroundEffectConditionalList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: GroundEffectConditional) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> GroundEffectConditional:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> GroundEffectConditional:
        """
        Remove and return the item at index ``i``
        """
class GroundEffectDerivedLiteral:
    @property
    def atom_index(self) -> int:
        ...
    @property
    def is_negated(self) -> bool:
        ...
class GroundEffectFluentLiteral:
    @property
    def atom_index(self) -> int:
        ...
    @property
    def is_negated(self) -> bool:
        ...
class GroundEffectStrips:
    def get_cost(self) -> float:
        ...
    def get_negative_effects(self) -> FlatBitset:
        ...
    def get_positive_effects(self) -> FlatBitset:
        ...
class GroundFunction:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function_skeleton(self) -> FunctionSkeleton:
        ...
    def get_index(self) -> int:
        ...
    def get_objects(self) -> ObjectList:
        ...
class GroundFunctionExpression:
    def get(self) -> typing.Any:
        ...
class GroundFunctionExpressionBinaryOperator:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_binary_operator(self) -> BinaryOperatorEnum:
        ...
    def get_index(self) -> int:
        ...
    def get_left_function_expression(self) -> GroundFunctionExpression:
        ...
    def get_right_function_expression(self) -> GroundFunctionExpression:
        ...
class GroundFunctionExpressionFunction:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function(self) -> GroundFunction:
        ...
    def get_index(self) -> int:
        ...
class GroundFunctionExpressionList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: GroundFunctionExpression) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: GroundFunctionExpressionList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> GroundFunctionExpressionList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> GroundFunctionExpression:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: GroundFunctionExpressionList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: GroundFunctionExpressionList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: GroundFunctionExpression) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: GroundFunctionExpressionList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: GroundFunctionExpression) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: GroundFunctionExpression) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: GroundFunctionExpressionList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: GroundFunctionExpression) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> GroundFunctionExpression:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> GroundFunctionExpression:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: GroundFunctionExpression) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class GroundFunctionExpressionMinus:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function_expression(self) -> GroundFunctionExpression:
        ...
    def get_index(self) -> int:
        ...
class GroundFunctionExpressionMultiOperator:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function_expressions(self) -> GroundFunctionExpressionList:
        ...
    def get_index(self) -> int:
        ...
    def get_multi_operator(self) -> MultiOperatorEnum:
        ...
class GroundFunctionExpressionNumber:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_number(self) -> float:
        ...
class GroundFunctionList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self: list[GroundFunction]) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self: list[GroundFunction], x: GroundFunction) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self: list[GroundFunction], arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self: list[GroundFunction], arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self: list[GroundFunction], arg0: list[GroundFunction]) -> bool:
        ...
    @typing.overload
    def __getitem__(self: list[GroundFunction], s: slice) -> list[GroundFunction]:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self: list[GroundFunction], arg0: int) -> GroundFunction:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: list[GroundFunction]) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self: list[GroundFunction]) -> typing.Iterator:
        ...
    def __len__(self: list[GroundFunction]) -> int:
        ...
    def __ne__(self: list[GroundFunction], arg0: list[GroundFunction]) -> bool:
        ...
    def __repr__(self: list[GroundFunction]) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self: list[GroundFunction], arg0: int, arg1: GroundFunction) -> None:
        ...
    @typing.overload
    def __setitem__(self: list[GroundFunction], arg0: slice, arg1: list[GroundFunction]) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self: list[GroundFunction], x: GroundFunction) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self: list[GroundFunction]) -> None:
        """
        Clear the contents
        """
    def count(self: list[GroundFunction], x: GroundFunction) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self: list[GroundFunction], L: list[GroundFunction]) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self: list[GroundFunction], L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self: list[GroundFunction], i: int, x: GroundFunction) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self: list[GroundFunction]) -> GroundFunction:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self: list[GroundFunction], i: int) -> GroundFunction:
        """
        Remove and return the item at index ``i``
        """
    def remove(self: list[GroundFunction], x: GroundFunction) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class GroundedApplicableActionGenerator(IApplicableActionGenerator):
    pass
class GroundedAxiomEvaluator(IAxiomEvaluator):
    pass
class IAStarAlgorithmEventHandler:
    def get_statistics(self) -> AStarAlgorithmStatistics:
        ...
class IAlgorithm:
    @typing.overload
    def find_solution(self) -> SearchResult:
        ...
    @typing.overload
    def find_solution(self, start_state: State) -> SearchResult:
        ...
class IApplicableActionGenerator:
    def create_applicable_action_generator(self, state: State) -> GroundActionList:
        ...
    def get_action_grounder(self) -> ActionGrounder:
        ...
class IAxiomEvaluator:
    def get_axiom_grounder(self) -> AxiomGrounder:
        ...
class IBrFSAlgorithmEventHandler:
    def get_statistics(self) -> BrFSAlgorithmStatistics:
        ...
class IGroundedApplicableActionGeneratorEventHandler:
    pass
class IGroundedAxiomEvaluatorEventHandler:
    pass
class IHeuristic:
    def __init__(self) -> None:
        ...
class IIWAlgorithmEventHandler:
    def get_statistics(self) -> IWAlgorithmStatistics:
        ...
class ILiftedApplicableActionGeneratorEventHandler:
    pass
class ILiftedAxiomEvaluatorEventHandler:
    pass
class ISIWAlgorithmEventHandler:
    def get_statistics(self) -> SIWAlgorithmStatistics:
        ...
class IWAlgorithm(IAlgorithm):
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, max_arity: int) -> None:
        ...
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, max_arity: int, brfs_event_handler: IBrFSAlgorithmEventHandler, iw_event_handler: IIWAlgorithmEventHandler) -> None:
        ...
class IWAlgorithmStatistics:
    def get_brfs_statistics_by_arity(self) -> list[BrFSAlgorithmStatistics]:
        ...
    def get_effective_width(self) -> int:
        ...
class IndexGroupedVector:
    def __getitem__(self, arg0: int) -> StateSpan:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
class IsomorphismTypeCompressionFunction:
    def __init__(self) -> None:
        ...
class LiftedApplicableActionGenerator(IApplicableActionGenerator):
    @typing.overload
    def __init__(self, problem: Problem, pddl_repositories: PDDLRepositories) -> None:
        ...
    @typing.overload
    def __init__(self, problem: Problem, pddl_repositories: PDDLRepositories, event_handler: ILiftedApplicableActionGeneratorEventHandler) -> None:
        ...
class LiftedAxiomEvaluator(IAxiomEvaluator):
    @typing.overload
    def __init__(self, problem: Problem, pddl_repositories: PDDLRepositories) -> None:
        ...
    @typing.overload
    def __init__(self, problem: Problem, pddl_repositories: PDDLRepositories, event_handler: ILiftedAxiomEvaluatorEventHandler) -> None:
        ...
class MultiOperatorEnum:
    """
    Members:
    
      MUL
    
      PLUS
    """
    MUL: typing.ClassVar[MultiOperatorEnum]  # value = <MultiOperatorEnum.MUL: 0>
    PLUS: typing.ClassVar[MultiOperatorEnum]  # value = <MultiOperatorEnum.PLUS: 1>
    __members__: typing.ClassVar[dict[str, MultiOperatorEnum]]  # value = {'MUL': <MultiOperatorEnum.MUL: 0>, 'PLUS': <MultiOperatorEnum.PLUS: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class NautyCertificate:
    def __eq__(self, arg0: NautyCertificate) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_canonical_coloring(self) -> list[int]:
        ...
    def get_canonical_graph(self) -> str:
        ...
class NautyDenseGraph:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, num_vertices: int) -> None:
        ...
    @typing.overload
    def __init__(self, digraph: ..., mimir: ...) -> None:
        ...
    def add_edge(self, source: int, target: int) -> None:
        ...
    def clear(self, num_vertices: int) -> None:
        ...
    def compute_certificate(self) -> NautyCertificate:
        ...
class NautySparseGraph:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, num_vertices: int) -> None:
        ...
    @typing.overload
    def __init__(self, digraph: ..., mimir: ...) -> None:
        ...
    def add_edge(self, source: int, target: int) -> None:
        ...
    def clear(self, num_vertices: int) -> None:
        ...
    def compute_certificate(self) -> NautyCertificate:
        ...
class NumericFluent:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function(self) -> GroundFunction:
        ...
    def get_index(self) -> int:
        ...
    def get_number(self) -> float:
        ...
class NumericFluentList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: NumericFluent) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: NumericFluentList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> NumericFluentList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> NumericFluent:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: NumericFluentList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: NumericFluentList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: NumericFluent) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: NumericFluentList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: NumericFluent) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: NumericFluent) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: NumericFluentList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: NumericFluent) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> NumericFluent:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> NumericFluent:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: NumericFluent) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class Object:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
class ObjectGraphPruningStrategy:
    pass
class ObjectGraphPruningStrategyEnum:
    """
    Members:
    
      None
    
      StaticScc
    """
    None: typing.ClassVar[ObjectGraphPruningStrategyEnum]  # value = <ObjectGraphPruningStrategyEnum.None: 0>
    StaticScc: typing.ClassVar[ObjectGraphPruningStrategyEnum]  # value = <ObjectGraphPruningStrategyEnum.StaticScc: 1>
    __members__: typing.ClassVar[dict[str, ObjectGraphPruningStrategyEnum]]  # value = {'None': <ObjectGraphPruningStrategyEnum.None: 0>, 'StaticScc': <ObjectGraphPruningStrategyEnum.StaticScc: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ObjectList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Object) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: ObjectList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> ObjectList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Object:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ObjectList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: ObjectList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Object) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: ObjectList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Object) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Object) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: ObjectList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Object) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Object:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Object:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Object) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class OptimizationMetric:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_function_expression(self) -> GroundFunctionExpression:
        ...
    def get_index(self) -> int:
        ...
    def get_optimization_metric(self) -> OptimizationMetricEnum:
        ...
class OptimizationMetricEnum:
    """
    Members:
    
      MINIMIZE
    
      MAXIMIZE
    """
    MAXIMIZE: typing.ClassVar[OptimizationMetricEnum]  # value = <OptimizationMetricEnum.MAXIMIZE: 1>
    MINIMIZE: typing.ClassVar[OptimizationMetricEnum]  # value = <OptimizationMetricEnum.MINIMIZE: 0>
    __members__: typing.ClassVar[dict[str, OptimizationMetricEnum]]  # value = {'MINIMIZE': <OptimizationMetricEnum.MINIMIZE: 0>, 'MAXIMIZE': <OptimizationMetricEnum.MAXIMIZE: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class PDDLParser:
    def __init__(self, domain_path: str, problem_path: str) -> None:
        ...
    def get_domain(self) -> Domain:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
class PDDLRepositories:
    def get_derived_ground_atom(self, arg0: int) -> DerivedGroundAtom:
        ...
    def get_derived_ground_atoms_from_indices(self, arg0: list[int]) -> DerivedGroundAtomList:
        ...
    def get_fluent_ground_atom(self, arg0: int) -> FluentGroundAtom:
        ...
    def get_fluent_ground_atoms_from_indices(self, arg0: list[int]) -> FluentGroundAtomList:
        ...
    def get_object(self, arg0: int) -> Object:
        ...
    def get_static_ground_atom(self, arg0: int) -> StaticGroundAtom:
        ...
    @typing.overload
    def get_static_ground_atoms(self) -> StaticGroundAtomList:
        ...
    @typing.overload
    def get_static_ground_atoms(self) -> FluentGroundAtomList:
        ...
    @typing.overload
    def get_static_ground_atoms(self) -> DerivedGroundAtomList:
        ...
    def get_static_ground_atoms_from_indices(self, arg0: list[int]) -> StaticGroundAtomList:
        ...
class Plan:
    def __len__(self) -> int:
        ...
    def get_actions(self) -> GroundActionList:
        ...
    def get_cost(self) -> float:
        ...
class Problem:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_derived_goal_condition(self) -> DerivedGroundLiteralList:
        ...
    def get_domain(self) -> Domain:
        ...
    def get_filepath(self) -> str | None:
        ...
    def get_fluent_goal_condition(self) -> FluentGroundLiteralList:
        ...
    def get_fluent_initial_literals(self) -> FluentGroundLiteralList:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_numeric_fluents(self) -> NumericFluentList:
        ...
    def get_objects(self) -> ObjectList:
        ...
    def get_optimization_metric(self) -> OptimizationMetric | None:
        ...
    def get_requirements(self) -> Requirements:
        ...
    def get_static_goal_condition(self) -> StaticGroundLiteralList:
        ...
    def get_static_initial_literals(self) -> StaticGroundLiteralList:
        ...
class ProblemColorFunction(ColorFunction):
    def __init__(self, problem: Problem) -> None:
        ...
    @typing.overload
    def get_color(self, object: Object) -> int:
        ...
    @typing.overload
    def get_color(self, atom: StaticGroundAtom, position: int) -> int:
        ...
    @typing.overload
    def get_color(self, atom: FluentGroundAtom, position: int) -> int:
        ...
    @typing.overload
    def get_color(self, atom: DerivedGroundAtom, position: int) -> int:
        ...
    @typing.overload
    def get_color(self, state: State, literal: StaticGroundLiteral, position: int, mark_true_goal_literal: bool) -> int:
        ...
    @typing.overload
    def get_color(self, state: State, literal: FluentGroundLiteral, position: int, mark_true_goal_literal: bool) -> int:
        ...
    @typing.overload
    def get_color(self, state: State, literal: DerivedGroundLiteral, position: int, mark_true_goal_literal: bool) -> int:
        ...
    def get_color_to_name(self) -> dict[int, str]:
        ...
    def get_name_to_color(self) -> dict[str, int]:
        ...
    def get_problem(self) -> Problem:
        ...
class ProblemList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Problem) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: ProblemList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> ProblemList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Problem:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ProblemList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: ProblemList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Problem) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: ProblemList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Problem) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Problem) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: ProblemList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Problem) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Problem:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Problem:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Problem) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class RequirementEnum:
    """
    Members:
    
      STRIPS
    
      TYPING
    
      NEGATIVE_PRECONDITIONS
    
      DISJUNCTIVE_PRECONDITIONS
    
      EQUALITY
    
      EXISTENTIAL_PRECONDITIONS
    
      UNIVERSAL_PRECONDITIONS
    
      QUANTIFIED_PRECONDITIONS
    
      CONDITIONAL_EFFECTS
    
      FLUENTS
    
      OBJECT_FLUENTS
    
      NUMERIC_FLUENTS
    
      ADL
    
      DURATIVE_ACTIONS
    
      DERIVED_PREDICATES
    
      TIMED_INITIAL_LITERALS
    
      PREFERENCES
    
      CONSTRAINTS
    
      ACTION_COSTS
    """
    ACTION_COSTS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.ACTION_COSTS: 18>
    ADL: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.ADL: 12>
    CONDITIONAL_EFFECTS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.CONDITIONAL_EFFECTS: 8>
    CONSTRAINTS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.CONSTRAINTS: 17>
    DERIVED_PREDICATES: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.DERIVED_PREDICATES: 14>
    DISJUNCTIVE_PRECONDITIONS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.DISJUNCTIVE_PRECONDITIONS: 3>
    DURATIVE_ACTIONS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.DURATIVE_ACTIONS: 13>
    EQUALITY: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.EQUALITY: 4>
    EXISTENTIAL_PRECONDITIONS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.EXISTENTIAL_PRECONDITIONS: 5>
    FLUENTS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.FLUENTS: 9>
    NEGATIVE_PRECONDITIONS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.NEGATIVE_PRECONDITIONS: 2>
    NUMERIC_FLUENTS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.NUMERIC_FLUENTS: 11>
    OBJECT_FLUENTS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.OBJECT_FLUENTS: 10>
    PREFERENCES: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.PREFERENCES: 16>
    QUANTIFIED_PRECONDITIONS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.QUANTIFIED_PRECONDITIONS: 7>
    STRIPS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.STRIPS: 0>
    TIMED_INITIAL_LITERALS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.TIMED_INITIAL_LITERALS: 15>
    TYPING: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.TYPING: 1>
    UNIVERSAL_PRECONDITIONS: typing.ClassVar[RequirementEnum]  # value = <RequirementEnum.UNIVERSAL_PRECONDITIONS: 6>
    __members__: typing.ClassVar[dict[str, RequirementEnum]]  # value = {'STRIPS': <RequirementEnum.STRIPS: 0>, 'TYPING': <RequirementEnum.TYPING: 1>, 'NEGATIVE_PRECONDITIONS': <RequirementEnum.NEGATIVE_PRECONDITIONS: 2>, 'DISJUNCTIVE_PRECONDITIONS': <RequirementEnum.DISJUNCTIVE_PRECONDITIONS: 3>, 'EQUALITY': <RequirementEnum.EQUALITY: 4>, 'EXISTENTIAL_PRECONDITIONS': <RequirementEnum.EXISTENTIAL_PRECONDITIONS: 5>, 'UNIVERSAL_PRECONDITIONS': <RequirementEnum.UNIVERSAL_PRECONDITIONS: 6>, 'QUANTIFIED_PRECONDITIONS': <RequirementEnum.QUANTIFIED_PRECONDITIONS: 7>, 'CONDITIONAL_EFFECTS': <RequirementEnum.CONDITIONAL_EFFECTS: 8>, 'FLUENTS': <RequirementEnum.FLUENTS: 9>, 'OBJECT_FLUENTS': <RequirementEnum.OBJECT_FLUENTS: 10>, 'NUMERIC_FLUENTS': <RequirementEnum.NUMERIC_FLUENTS: 11>, 'ADL': <RequirementEnum.ADL: 12>, 'DURATIVE_ACTIONS': <RequirementEnum.DURATIVE_ACTIONS: 13>, 'DERIVED_PREDICATES': <RequirementEnum.DERIVED_PREDICATES: 14>, 'TIMED_INITIAL_LITERALS': <RequirementEnum.TIMED_INITIAL_LITERALS: 15>, 'PREFERENCES': <RequirementEnum.PREFERENCES: 16>, 'CONSTRAINTS': <RequirementEnum.CONSTRAINTS: 17>, 'ACTION_COSTS': <RequirementEnum.ACTION_COSTS: 18>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Requirements:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_requirements(self) -> set[RequirementEnum]:
        ...
class SIWAlgorithm(IAlgorithm):
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, max_arity: int) -> None:
        ...
    @typing.overload
    def __init__(self, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, max_arity: int, brfs_event_handler: IBrFSAlgorithmEventHandler, iw_event_handler: IIWAlgorithmEventHandler, siw_event_handler: ISIWAlgorithmEventHandler) -> None:
        ...
class SIWAlgorithmStatistics:
    def get_average_effective_width(self) -> float:
        ...
    def get_iw_statistics_by_subproblem(self) -> list[IWAlgorithmStatistics]:
        ...
    def get_maximum_effective_width(self) -> int:
        ...
class SearchNodeStatus:
    """
    Members:
    
      NEW
    
      OPEN
    
      CLOSED
    
      DEAD_END
    """
    CLOSED: typing.ClassVar[SearchNodeStatus]  # value = <SearchNodeStatus.CLOSED: 2>
    DEAD_END: typing.ClassVar[SearchNodeStatus]  # value = <SearchNodeStatus.DEAD_END: 3>
    NEW: typing.ClassVar[SearchNodeStatus]  # value = <SearchNodeStatus.NEW: 0>
    OPEN: typing.ClassVar[SearchNodeStatus]  # value = <SearchNodeStatus.OPEN: 1>
    __members__: typing.ClassVar[dict[str, SearchNodeStatus]]  # value = {'NEW': <SearchNodeStatus.NEW: 0>, 'OPEN': <SearchNodeStatus.OPEN: 1>, 'CLOSED': <SearchNodeStatus.CLOSED: 2>, 'DEAD_END': <SearchNodeStatus.DEAD_END: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SearchResult:
    goal_state: State | None
    plan: Plan | None
    status: SearchStatus
    def __init__(self) -> None:
        ...
class SearchStatus:
    """
    Members:
    
      IN_PROGRESS
    
      OUT_OF_TIME
    
      OUT_OF_MEMORY
    
      FAILED
    
      EXHAUSTED
    
      SOLVED
    
      UNSOLVABLE
    """
    EXHAUSTED: typing.ClassVar[SearchStatus]  # value = <SearchStatus.EXHAUSTED: 4>
    FAILED: typing.ClassVar[SearchStatus]  # value = <SearchStatus.FAILED: 3>
    IN_PROGRESS: typing.ClassVar[SearchStatus]  # value = <SearchStatus.IN_PROGRESS: 0>
    OUT_OF_MEMORY: typing.ClassVar[SearchStatus]  # value = <SearchStatus.OUT_OF_MEMORY: 2>
    OUT_OF_TIME: typing.ClassVar[SearchStatus]  # value = <SearchStatus.OUT_OF_TIME: 1>
    SOLVED: typing.ClassVar[SearchStatus]  # value = <SearchStatus.SOLVED: 5>
    UNSOLVABLE: typing.ClassVar[SearchStatus]  # value = <SearchStatus.UNSOLVABLE: 6>
    __members__: typing.ClassVar[dict[str, SearchStatus]]  # value = {'IN_PROGRESS': <SearchStatus.IN_PROGRESS: 0>, 'OUT_OF_TIME': <SearchStatus.OUT_OF_TIME: 1>, 'OUT_OF_MEMORY': <SearchStatus.OUT_OF_MEMORY: 2>, 'FAILED': <SearchStatus.FAILED: 3>, 'EXHAUSTED': <SearchStatus.EXHAUSTED: 4>, 'SOLVED': <SearchStatus.SOLVED: 5>, 'UNSOLVABLE': <SearchStatus.UNSOLVABLE: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class State:
    def __eq__(self, arg0: State) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    @typing.overload
    def contains(self, atom: FluentGroundAtom) -> bool:
        ...
    @typing.overload
    def contains(self, atom: DerivedGroundAtom) -> bool:
        ...
    def get_derived_atoms(self) -> FlatBitset:
        ...
    def get_fluent_atoms(self) -> FlatBitset:
        ...
    def get_index(self) -> int:
        ...
    @typing.overload
    def literal_holds(self, literal: FluentGroundLiteral) -> bool:
        ...
    @typing.overload
    def literal_holds(self, literal: DerivedGroundLiteral) -> bool:
        ...
    @typing.overload
    def literals_hold(self, literals: FluentGroundLiteralList) -> bool:
        ...
    @typing.overload
    def literals_hold(self, literals: DerivedGroundLiteralList) -> bool:
        ...
    @typing.overload
    def superset_of(self, atoms: FluentGroundAtomList) -> bool:
        ...
    @typing.overload
    def superset_of(self, atoms: DerivedGroundAtomList) -> bool:
        ...
    def to_string(self, problem: Problem, pddl_repositories: PDDLRepositories) -> str:
        ...
class StateList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: State) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StateList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StateList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> State:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StateList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StateList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: State) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StateList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: State) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: State) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StateList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: State) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> State:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> State:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: State) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class StateRepository:
    def __init__(self, axiom_evaluator: IAxiomEvaluator) -> None:
        ...
    def get_or_create_initial_state(self) -> State:
        ...
    def get_or_create_state(self, atoms: FluentGroundAtomList) -> State:
        ...
    def get_or_create_successor_state(self, state: State, action: GroundAction) -> tuple[State, float]:
        ...
    def get_reached_derived_ground_atoms_bitset(self) -> FlatBitset:
        ...
    def get_reached_fluent_ground_atoms_bitset(self) -> FlatBitset:
        ...
    def get_state_count(self) -> int:
        ...
class StateSpace:
    @staticmethod
    @typing.overload
    def create(domain_filepath: str, problem_filepaths: str, options: StateSpaceOptions = ...) -> StateSpace | None:
        ...
    @staticmethod
    @typing.overload
    def create(problem: Problem, factories: PDDLRepositories, applicable_action_generator: IApplicableActionGenerator, state_repository: StateRepository, options: StateSpaceOptions = ...) -> StateSpace | None:
        ...
    @staticmethod
    @typing.overload
    def create(domain_filepath: str, problem_filepaths: list[str], options: StateSpacesOptions = ...) -> list[StateSpace]:
        ...
    @staticmethod
    @typing.overload
    def create(memories: list[tuple[Problem, PDDLRepositories, IApplicableActionGenerator, StateRepository]], options: StateSpacesOptions = ...) -> list[StateSpace]:
        ...
    def __str__(self) -> str:
        ...
    def compute_pairwise_shortest_backward_state_distances(self) -> list[list[float]]:
        ...
    def compute_pairwise_shortest_forward_state_distances(self) -> list[list[float]]:
        ...
    def compute_shortest_backward_distances_from_states(self, state_indices: list[int]) -> list[float]:
        ...
    def compute_shortest_forward_distances_from_states(self, state_indices: list[int]) -> list[float]:
        ...
    def get_applicable_action_generator(self) -> IApplicableActionGenerator:
        ...
    def get_backward_adjacent_state_indices(self, state_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_states(self, state_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_transition_indices(self, state_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_transitions(self, state_index: int) -> typing.Iterator:
        ...
    def get_deadend_vertex_indices(self) -> set[int]:
        ...
    def get_edge(self, edge_index: int) -> GroundActionEdge:
        ...
    def get_edge_cost(self, edge_index: int) -> float:
        ...
    def get_edges(self) -> list[GroundActionEdge]:
        ...
    def get_forward_adjacent_state_indices(self, state_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_states(self, state_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_transition_indices(self, state_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_transitions(self, state_index: int) -> typing.Iterator:
        ...
    def get_goal_distance(self, state_index: int) -> float:
        ...
    def get_goal_distances(self) -> list[float]:
        ...
    def get_goal_vertex_indices(self) -> set[int]:
        ...
    def get_initial_vertex_index(self) -> int:
        ...
    def get_max_goal_distance(self) -> float:
        ...
    def get_num_deadend_vertices(self) -> int:
        ...
    def get_num_edges(self) -> int:
        ...
    def get_num_goal_vertices(self) -> int:
        ...
    def get_num_vertices(self) -> int:
        ...
    def get_pddl_repositories(self) -> PDDLRepositories:
        ...
    def get_problem(self) -> Problem:
        ...
    def get_state_repository(self) -> StateRepository:
        ...
    def get_vertex(self, state_index: int) -> StateVertex:
        ...
    def get_vertex_index(self, state: State) -> int:
        ...
    def get_vertices(self) -> list[StateVertex]:
        ...
    def is_alive_vertex(self, state_index: int) -> bool:
        ...
    def is_deadend_vertex(self, state_index: int) -> bool:
        ...
    def is_goal_vertex(self, state_index: int) -> bool:
        ...
    def sample_vertex_index_with_goal_distance(self, goal_distance: float) -> int:
        ...
class StateSpaceOptions:
    max_num_states: int
    remove_if_unsolvable: bool
    timeout_ms: int
    use_unit_cost_one: bool
    def __init__(self, use_unit_cost_one: bool = True, remove_if_unsolvable: bool = True, max_num_states: int = 4294967295, timeout_ms: int = 4294967295) -> None:
        ...
class StateSpacesOptions:
    num_threads: int
    sort_ascending_by_num_states: bool
    state_space_options: StateSpaceOptions
    def __init__(self, state_space_options: StateSpaceOptions = ..., sort_ascending_by_num_states: bool = True, num_threads: int = 4) -> None:
        ...
class StateSpan:
    def __getitem__(self, arg0: int) -> State:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
class StateVertex:
    def __eq__(self, arg0: StateVertex) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_state(self) -> State:
        ...
class StaticAssignmentSet:
    def __init__(self, problem: Problem, predicates: StaticPredicateList, ground_atoms: StaticGroundAtomList) -> None:
        ...
class StaticAtom:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_predicate(self) -> StaticPredicate:
        ...
    def get_terms(self) -> TermList:
        ...
    def get_variables(self) -> VariableList:
        ...
class StaticAtomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: StaticAtom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StaticAtomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StaticAtomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> StaticAtom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StaticAtomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StaticAtomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: StaticAtom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StaticAtomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: StaticAtom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: StaticAtom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StaticAtomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: StaticAtom) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> StaticAtom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> StaticAtom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: StaticAtom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class StaticDigraph:
    def __init__(self) -> None:
        ...
    def __str__(self) -> str:
        ...
    def add_directed_edge(self, arg0: int, arg1: int) -> int:
        ...
    def add_undirected_edge(self, arg0: int, arg1: int) -> tuple[int, int]:
        ...
    def add_vertex(self) -> int:
        ...
    def clear(self) -> None:
        ...
    def get_backward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_edges(self) -> list[EmptyEdge]:
        ...
    def get_forward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_num_edges(self) -> int:
        ...
    def get_num_vertices(self) -> int:
        ...
    def get_vertices(self) -> list[EmptyVertex]:
        ...
class StaticGroundAtom:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_objects(self) -> ObjectList:
        ...
    def get_predicate(self) -> StaticPredicate:
        ...
class StaticGroundAtomList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: StaticGroundAtom) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StaticGroundAtomList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StaticGroundAtomList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> StaticGroundAtom:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StaticGroundAtomList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StaticGroundAtomList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: StaticGroundAtom) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StaticGroundAtomList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: StaticGroundAtom) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: StaticGroundAtom) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StaticGroundAtomList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: StaticGroundAtom) -> None:
        """
        Insert an item at a given position.
        """
    def lift(self, pddl_repositories: ...) -> tuple[VariableList, StaticAtomList]:
        ...
    @typing.overload
    def pop(self) -> StaticGroundAtom:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> StaticGroundAtom:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: StaticGroundAtom) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class StaticGroundLiteral:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_atom(self) -> StaticGroundAtom:
        ...
    def get_index(self) -> int:
        ...
    def is_negated(self) -> bool:
        ...
class StaticGroundLiteralList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: StaticGroundLiteral) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StaticGroundLiteralList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StaticGroundLiteralList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> StaticGroundLiteral:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StaticGroundLiteralList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StaticGroundLiteralList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: StaticGroundLiteral) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StaticGroundLiteralList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: StaticGroundLiteral) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: StaticGroundLiteral) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StaticGroundLiteralList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: StaticGroundLiteral) -> None:
        """
        Insert an item at a given position.
        """
    def lift(self, pddl_repositories: ...) -> tuple[VariableList, ..., ...]:
        ...
    @typing.overload
    def pop(self) -> StaticGroundLiteral:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> StaticGroundLiteral:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: StaticGroundLiteral) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class StaticLiteral:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_atom(self) -> StaticAtom:
        ...
    def get_index(self) -> int:
        ...
    def is_negated(self) -> bool:
        ...
class StaticLiteralList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: StaticLiteral) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StaticLiteralList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StaticLiteralList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> StaticLiteral:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StaticLiteralList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StaticLiteralList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: StaticLiteral) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StaticLiteralList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: StaticLiteral) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: StaticLiteral) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StaticLiteralList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: StaticLiteral) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> StaticLiteral:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> StaticLiteral:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: StaticLiteral) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class StaticPredicate:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_arity(self) -> int:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_parameters(self) -> VariableList:
        ...
class StaticPredicateList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: StaticPredicate) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StaticPredicateList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StaticPredicateList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> StaticPredicate:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StaticPredicateList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StaticPredicateList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: StaticPredicate) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StaticPredicateList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: StaticPredicate) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: StaticPredicate) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StaticPredicateList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: StaticPredicate) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> StaticPredicate:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> StaticPredicate:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: StaticPredicate) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class StaticVertexColoredDigraph:
    def __init__(self) -> None:
        ...
    def add_directed_edge(self, source: int, target: int) -> int:
        ...
    def add_undirected_edge(self, source: int, target: int) -> tuple[int, int]:
        ...
    def add_vertex(self, color: int) -> int:
        ...
    def clear(self) -> None:
        ...
    def get_backward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_backward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_edges(self) -> list[EmptyEdge]:
        ...
    def get_forward_adjacent_edge_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_edges(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertex_indices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_forward_adjacent_vertices(self, vertex_index: int) -> typing.Iterator:
        ...
    def get_num_edges(self) -> int:
        ...
    def get_num_vertices(self) -> int:
        ...
    def get_vertices(self) -> list[ColoredVertex]:
        ...
    def to_string(self, color_function: ColorFunction) -> str:
        ...
class StringToDerivedPredicateMap:
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> DerivedPredicate:
        ...
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: str, arg1: DerivedPredicate) -> None:
        ...
    def items(self) -> typing.ItemsView[str, ...]:
        ...
    def keys(self) -> typing.KeysView[str]:
        ...
    def values(self) -> typing.ValuesView[...]:
        ...
class StringToFluentPredicateMap:
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> FluentPredicate:
        ...
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: str, arg1: FluentPredicate) -> None:
        ...
    def items(self) -> typing.ItemsView[str, ...]:
        ...
    def keys(self) -> typing.KeysView[str]:
        ...
    def values(self) -> typing.ValuesView[...]:
        ...
class StringToStaticPredicateMap:
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> StaticPredicate:
        ...
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: str, arg1: StaticPredicate) -> None:
        ...
    def items(self) -> typing.ItemsView[str, ...]:
        ...
    def keys(self) -> typing.KeysView[str]:
        ...
    def values(self) -> typing.ValuesView[...]:
        ...
class Term:
    def get(self) -> typing.Any:
        ...
class TermList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Term) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: TermList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> TermList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Term:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: TermList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: TermList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Term) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: TermList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Term) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Term) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: TermList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Term) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Term:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Term:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Term) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class TupleGraph:
    def __str__(self) -> str:
        ...
    @typing.overload
    def compute_admissible_chain(self, arg0: FluentGroundAtomList) -> list[int] | None:
        ...
    @typing.overload
    def compute_admissible_chain(self, arg0: StateList) -> list[int] | None:
        ...
    def get_digraph(self) -> ...:
        ...
    def get_root_state(self) -> State:
        ...
    def get_state_space(self) -> StateSpace:
        ...
    def get_states_grouped_by_distance(self) -> IndexGroupedVector:
        ...
    def get_tuple_index_mapper(self) -> TupleIndexMapper:
        ...
    def get_vertices_grouped_by_distance(self) -> TupleGraphVertexIndexGroupedVector:
        ...
class TupleGraphFactory:
    def __init__(self, state_space: StateSpace, arity: int, prune_dominated_tuples: bool = False) -> None:
        ...
    def create(self, arg0: State) -> TupleGraph:
        ...
    def get_state_space(self) -> StateSpace:
        ...
    def get_tuple_index_mapper(self) -> TupleIndexMapper:
        ...
class TupleGraphVertex:
    def get_index(self) -> int:
        ...
    def get_states(self) -> StateList:
        ...
    def get_tuple_index(self) -> int:
        ...
class TupleGraphVertexIndexGroupedVector:
    def __getitem__(self, arg0: int) -> TupleGraphVertexSpan:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
class TupleGraphVertexSpan:
    def __getitem__(self, arg0: int) -> TupleGraphVertex:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
class TupleIndexMapper:
    def get_arity(self) -> int:
        ...
    def get_empty_tuple_index(self) -> int:
        ...
    def get_factors(self) -> typing.Annotated[list[int], pybind11_stubgen.typing_ext.FixedSize(6)]:
        ...
    def get_max_tuple_index(self) -> int:
        ...
    def get_num_atoms(self) -> int:
        ...
    def to_atom_indices(self, tuple_index: int) -> list[int]:
        ...
    def to_tuple_index(self, atom_indices: list[int]) -> int:
        ...
    def tuple_index_to_string(self, tuple_index: int) -> str:
        ...
class Variable:
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_index(self) -> int:
        ...
    def get_name(self) -> str:
        ...
class VariableList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Variable) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: VariableList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> VariableList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Variable:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: VariableList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: VariableList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Variable) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: VariableList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Variable) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Variable) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: VariableList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Variable) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Variable:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Variable:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Variable) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
def compute_certificate_2fwl(static_vertex_colored_digraph: StaticVertexColoredDigraph, isomorphism_type_compression_function: dict[NautyCertificate, int]) -> Certificate2FWL:
    ...
def compute_certificate_3fwl(static_vertex_colored_digraph: StaticVertexColoredDigraph, isomorphism_type_compression_function: dict[NautyCertificate, int]) -> Certificate3FWL:
    ...
def compute_certificate_4fwl(static_vertex_colored_digraph: StaticVertexColoredDigraph, isomorphism_type_compression_function: dict[NautyCertificate, int]) -> Certificate4FWL:
    ...
def compute_certificate_color_refinement(graph: StaticVertexColoredDigraph) -> CertificateColorRefinement:
    """
    Creates color refinement certificate
    """
def create_object_graph(color_function: ProblemColorFunction, pddl_repositories: PDDLRepositories, problem: Problem, state: State, state_index: int = 0, mark_true_goal_literals: bool = False, pruning_strategy: ObjectGraphPruningStrategy = ...) -> StaticVertexColoredDigraph:
    """
    Creates an object graph based on the provided parameters
    """
ACTION_COSTS: RequirementEnum  # value = <RequirementEnum.ACTION_COSTS: 18>
ADL: RequirementEnum  # value = <RequirementEnum.ADL: 12>
ASSIGN: AssignOperatorEnum  # value = <AssignOperatorEnum.ASSIGN: 0>
CLOSED: SearchNodeStatus  # value = <SearchNodeStatus.CLOSED: 2>
CONDITIONAL_EFFECTS: RequirementEnum  # value = <RequirementEnum.CONDITIONAL_EFFECTS: 8>
CONSTRAINTS: RequirementEnum  # value = <RequirementEnum.CONSTRAINTS: 17>
DEAD_END: SearchNodeStatus  # value = <SearchNodeStatus.DEAD_END: 3>
DECREASE: AssignOperatorEnum  # value = <AssignOperatorEnum.DECREASE: 4>
DERIVED_PREDICATES: RequirementEnum  # value = <RequirementEnum.DERIVED_PREDICATES: 14>
DISJUNCTIVE_PRECONDITIONS: RequirementEnum  # value = <RequirementEnum.DISJUNCTIVE_PRECONDITIONS: 3>
DIV: BinaryOperatorEnum  # value = <BinaryOperatorEnum.DIV: 3>
DURATIVE_ACTIONS: RequirementEnum  # value = <RequirementEnum.DURATIVE_ACTIONS: 13>
EQUALITY: RequirementEnum  # value = <RequirementEnum.EQUALITY: 4>
EXHAUSTED: SearchStatus  # value = <SearchStatus.EXHAUSTED: 4>
EXISTENTIAL_PRECONDITIONS: RequirementEnum  # value = <RequirementEnum.EXISTENTIAL_PRECONDITIONS: 5>
FAILED: SearchStatus  # value = <SearchStatus.FAILED: 3>
FLUENTS: RequirementEnum  # value = <RequirementEnum.FLUENTS: 9>
INCREASE: AssignOperatorEnum  # value = <AssignOperatorEnum.INCREASE: 3>
IN_PROGRESS: SearchStatus  # value = <SearchStatus.IN_PROGRESS: 0>
MAXIMIZE: OptimizationMetricEnum  # value = <OptimizationMetricEnum.MAXIMIZE: 1>
MINIMIZE: OptimizationMetricEnum  # value = <OptimizationMetricEnum.MINIMIZE: 0>
MINUS: BinaryOperatorEnum  # value = <BinaryOperatorEnum.MINUS: 2>
MUL: MultiOperatorEnum  # value = <MultiOperatorEnum.MUL: 0>
NEGATIVE_PRECONDITIONS: RequirementEnum  # value = <RequirementEnum.NEGATIVE_PRECONDITIONS: 2>
NEW: SearchNodeStatus  # value = <SearchNodeStatus.NEW: 0>
NUMERIC_FLUENTS: RequirementEnum  # value = <RequirementEnum.NUMERIC_FLUENTS: 11>
None: ObjectGraphPruningStrategyEnum  # value = <ObjectGraphPruningStrategyEnum.None: 0>
OBJECT_FLUENTS: RequirementEnum  # value = <RequirementEnum.OBJECT_FLUENTS: 10>
OPEN: SearchNodeStatus  # value = <SearchNodeStatus.OPEN: 1>
OUT_OF_MEMORY: SearchStatus  # value = <SearchStatus.OUT_OF_MEMORY: 2>
OUT_OF_TIME: SearchStatus  # value = <SearchStatus.OUT_OF_TIME: 1>
PLUS: MultiOperatorEnum  # value = <MultiOperatorEnum.PLUS: 1>
PREFERENCES: RequirementEnum  # value = <RequirementEnum.PREFERENCES: 16>
QUANTIFIED_PRECONDITIONS: RequirementEnum  # value = <RequirementEnum.QUANTIFIED_PRECONDITIONS: 7>
SCALE_DOWN: AssignOperatorEnum  # value = <AssignOperatorEnum.SCALE_DOWN: 2>
SCALE_UP: AssignOperatorEnum  # value = <AssignOperatorEnum.SCALE_UP: 1>
SOLVED: SearchStatus  # value = <SearchStatus.SOLVED: 5>
STRIPS: RequirementEnum  # value = <RequirementEnum.STRIPS: 0>
StaticScc: ObjectGraphPruningStrategyEnum  # value = <ObjectGraphPruningStrategyEnum.StaticScc: 1>
TIMED_INITIAL_LITERALS: RequirementEnum  # value = <RequirementEnum.TIMED_INITIAL_LITERALS: 15>
TYPING: RequirementEnum  # value = <RequirementEnum.TYPING: 1>
UNIVERSAL_PRECONDITIONS: RequirementEnum  # value = <RequirementEnum.UNIVERSAL_PRECONDITIONS: 6>
UNSOLVABLE: SearchStatus  # value = <SearchStatus.UNSOLVABLE: 6>
__version__: str = 'dev'
