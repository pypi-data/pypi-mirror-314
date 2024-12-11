import logging
from dataclasses import dataclass
from functools import cached_property
from typing import Sequence, Iterable

from cedarscript_ast_parser import Marker, MarkerType, Segment, RelativeMarker
from grep_ast import filename_to_lang
from text_manipulation.indentation_kit import get_line_indent_count
from text_manipulation.range_spec import IdentifierBoundaries, RangeSpec, ParentInfo, ParentRestriction
from text_manipulation import IdentifierFinder
from tree_sitter_languages import get_language, get_parser

from .tree_sitter_identifier_queries import LANG_TO_TREE_SITTER_QUERY

"""
Parser for extracting identifier information from source code using tree-sitter.
Supports multiple languages and provides functionality to find and analyze identifiers
like functions and classes along with their hierarchical relationships.
"""

_log = logging.getLogger(__name__)


class TreeSitterIdentifierFinder(IdentifierFinder):
    """Finds identifiers in source code based on markers and parent restrictions.

    Attributes:
        lines: List of source code lines
        file_path: Path to the source file
        source: Complete source code as a single string
        language: Tree-sitter language instance
        tree: Parsed tree-sitter tree
        query_info: Language-specific query information
    """

    def __init__(self, fname: str, source: str | Sequence[str], parent_restriction: ParentRestriction = None):
        super().__init__()
        self.parent_restriction = parent_restriction
        match source:
            case str() as s:
                self.lines = s.splitlines()
            case _ as lines:
                self.lines = lines
                source = '\n'.join(lines)
        langstr = filename_to_lang(fname)
        if langstr is None:
            self.language = None
            self.query_info = None
            _log.info(f"[TreeSitterIdentifierFinder] NO LANGUAGE for `{fname}`")
            return
        self.query_info: dict[str, dict[str, str]] = LANG_TO_TREE_SITTER_QUERY[langstr]
        self.language = get_language(langstr)
        _log.info(f"[TreeSitterIdentifierFinder] Selected {self.language}")
        self.tree = get_parser(langstr).parse(bytes(source, "utf-8"))

    def __call__(
            self, mos: Marker | Segment, parent_restriction: ParentRestriction = None
    ) -> IdentifierBoundaries | RangeSpec | None:
        parent_restriction = parent_restriction or self.parent_restriction
        match mos:
            case Marker(MarkerType.LINE) | Segment():
                # TODO pass IdentifierFinder to enable identifiers as start and/or end of a segment
                return mos.to_search_range(self.lines, parent_restriction).set_line_count(1)  # returns RangeSpec

            case Marker() as marker:
                # Returns IdentifierBoundaries
                return self._find_identifier(marker, parent_restriction)


    def _find_identifier(self,
        marker: Marker,
        parent_restriction: ParentRestriction
    ) -> IdentifierBoundaries | RangeSpec | None:
        """Finds an identifier in the source code using tree-sitter queries.

        Args:
            language: Tree-sitter language
            source: List of source code lines
            tree: Parsed tree-sitter tree
            query_scm: Dictionary of queries for different identifier types
            marker: Type, name and offset of the identifier to find

        Returns:
            IdentifierBoundaries with identifier IdentifierBoundaries with identifier start, body start, and end lines of the identifier
        or None if not found
        """
        query_info_key = marker.type
        identifier_name = marker.value
        try:
            all_restrictions: list[ParentRestriction] = [parent_restriction]
            # Extract parent name if using dot notation
            if '.' in identifier_name:
                *parent_parts, identifier_name = identifier_name.split('.')
                all_restrictions.append("." + '.'.join(reversed(parent_parts)))

            identifier_type = marker.type
            # Get all node candidates first
            candidates = self.find_identifiers(query_info_key, identifier_name, all_restrictions)
        except Exception as e:
            raise ValueError(f"Unable to capture nodes for {marker}: {e}") from e

        candidate_count = len(candidates)
        if not candidate_count:
            return None
        if candidate_count > 1 and marker.offset is None:
            raise ValueError(
                f"The {marker.type} identifier named `{identifier_name}` is ambiguous (found {candidate_count} matches). "
                f"Choose an `OFFSET` between 0 and {candidate_count - 1} to determine how many to skip. "
                f"Example to reference the *last* `{identifier_name}`: `OFFSET {candidate_count - 1}`"
            )
        if marker.offset and marker.offset >= candidate_count:
            raise ValueError(
                f"There are only {candidate_count} {marker.type} identifiers named `{identifier_name}`, "
                f"but 'OFFSET' was set to {marker.offset} (you can skip at most {candidate_count - 1} of those)"
            )
        candidates.sort(key=lambda x: x.whole.start)
        result: IdentifierBoundaries = _get_by_offset(candidates, marker.offset or 0)
        match marker:
            case RelativeMarker(qualifier=relative_position_type):
                return result.location_to_search_range(relative_position_type)
        return result

    def find_identifiers(
        self, identifier_type: str, name: str, all_restrictions: list[ParentRestriction] = []
    ) -> list[IdentifierBoundaries]:
        if not self.language:
            return []
        match identifier_type:
            case 'method':
                identifier_type = 'function'
        _query = self.query_info[identifier_type].format(name=name)
        candidate_nodes = self.language.query(_query).captures(self.tree.root_node)
        if not candidate_nodes:
            return []
        # Convert captures to boundaries and filter by parent
        candidates: list[IdentifierBoundaries] = []
        for ib in capture2identifier_boundaries(candidate_nodes, self.lines):
            # For methods, verify the immediate parent is a class
            if identifier_type == 'method':
                if not ib.parents or not ib.parents[0].parent_type.startswith('class'):
                    continue
            # Check parent restriction (e.g., specific class name)
            candidate_matched_all_restrictions = True
            for pr in all_restrictions:
                if not ib.match_parent(pr):
                    candidate_matched_all_restrictions = False
                    break
            if candidate_matched_all_restrictions:
                candidates.append(ib)
        return candidates


def _get_by_offset(obj: Sequence, offset: int):
    if 0 <= offset < len(obj):
        return obj[offset]
    return None


@dataclass(frozen=True)
class CaptureInfo:
    """Container for information about a captured node from tree-sitter parsing.

    Attributes:
        capture_type: Type of the captured node (e.g., 'function.definition')
        node: The tree-sitter node that was captured

    Properties:
        node_type: Type of the underlying node
        range: Tuple of (start_line, end_line)
        identifier: Name of the identifier if this is a name capture
        parents: List of (node_type, node_name) tuples representing the hierarchy
    """
    capture_type: str
    node: any

    def to_range_spec(self, lines: Sequence[str]) -> RangeSpec:
        start, end = self.range
        return RangeSpec(start, end + 1, get_line_indent_count(lines[start]))

    @property
    def node_type(self):
        return self.node.type

    @property
    def range(self):
        return self.node.range.start_point[0], self.node.range.end_point[0]

    @property
    def identifier(self):
        if not self.capture_type.endswith('.name'):
            return None
        return self.node.text.decode("utf-8")

    @cached_property
    def parents(self) -> list[ParentInfo]:
        """Returns a list of (node_type, node_name) tuples representing the hierarchy.
        The list is ordered from immediate parent to root."""
        parents: list[ParentInfo] = []
        current = self.node.parent

        while current:
            # Check if current node is a container type we care about - TODO exact field depends on language
            if current.type.endswith('_definition') and current.type != 'decorated_definition':
                # Try to find the name node - TODO exact field depends on language
                name = None
                for child in current.children:
                    if child.type == 'identifier' or child.type == 'name':
                        name = child.text.decode('utf-8')
                        break
                parents.append(ParentInfo(name, current.type))
            current = current.parent

        return parents


def associate_identifier_parts(captures: Iterable[CaptureInfo], lines: Sequence[str]) -> list[IdentifierBoundaries]:
    """Associates related identifier parts (definition, body, docstring, etc) into IdentifierBoundaries.

    Args:
        captures: Iterable of CaptureInfo objects representing related parts
        lines: Sequence of source code lines

    Returns:
        List of IdentifierBoundaries with all parts associated
    """
    identifier_map: dict[int, IdentifierBoundaries] = {}

    for capture in captures:
        capture_type = capture.capture_type.split('.')[-1]
        range_spec = capture.to_range_spec(lines)
        if capture_type == 'definition':
            identifier_map[range_spec.start] = IdentifierBoundaries(
                whole=range_spec,
                parents=capture.parents
            )

        else:
            parent = find_parent_definition(capture.node)
            if parent:
                parent_key = parent.start_point[0]
                parent = identifier_map.get(parent_key)
            if parent is None:
                raise ValueError(f'Parent node not found for [{capture.capture_type} - {capture.node_type}] ({capture.node.text.decode("utf-8").strip()})')
            match capture_type:
                case 'body':
                    parent.body=range_spec
                case 'docstring':
                    parent.docstring=range_spec
                case 'decorator':
                    parent.append_decorator(range_spec)
                case _ as invalid:
                    raise ValueError(f'Invalid capture type: {invalid}')

    return sorted(identifier_map.values(), key=lambda x: x.whole.start)


def find_parent_definition(node):
    """Returns the first parent node that ends with '_definition'"""
    # TODO How to deal with 'decorated_definition' ?
    while node.parent:
        node = node.parent
        if node.type.endswith('_definition'):
            if node.type == 'decorated_definition':
                node = node.named_children[0].next_named_sibling
            return node
    return None


def capture2identifier_boundaries(captures, lines: Sequence[str]) -> list[IdentifierBoundaries]:
    """Converts raw tree-sitter captures to IdentifierBoundaries objects.

    Args:
        captures: Raw captures from tree-sitter query
        lines: Sequence of source code lines

    Returns:
        List of IdentifierBoundaries representing the captured identifiers
    """
    captures = [CaptureInfo(c[1], c[0]) for c in captures if not c[1].startswith('_')]
    unique_captures = {}
    for capture in captures:
        unique_captures[f'{capture.range[0]}:{capture.capture_type}'] = capture
    # unique_captures={
    # '157:function.decorator': CaptureInfo(capture_type='function.decorator', node=<Node type=decorator, start_point=(157, 4), end_point=(157, 17)>),
    # '158:function.definition': CaptureInfo(capture_type='function.definition', node=<Node type=function_definition, start_point=(158, 4), end_point=(207, 19)>),
    # '159:function.body': CaptureInfo(capture_type='function.body', node=<Node type=block, start_point=(159, 8), end_point=(207, 19)>)
    # }
    return associate_identifier_parts(sort_captures(unique_captures), lines)

def parse_capture_key(key):
    """
    Parses the dictionary key into line number and capture type.
    Args:
        key (str): The key in the format 'line_number:capture_type'.
    Returns:
        tuple: (line_number as int, capture_type as str)
    """
    line_number, capture_type = key.split(':')
    return int(line_number), capture_type.split('.')[-1]

def get_sort_priority():
    """
    Returns a dictionary mapping capture types to their sort priority.
    Returns:
        dict: Capture type priorities.
    """
    return {'definition': 1, 'decorator': 2, 'body': 3, 'docstring': 4}

def sort_captures(captures):
    """
    Sorts the values of the captures dictionary by capture type and line number.
    Args:
        captures (dict): The dictionary to sort.
    Returns:
        list: Sorted list of values.
    """
    priority = get_sort_priority()
    sorted_items = sorted(
        captures.items(),
        key=lambda item: (
            priority[parse_capture_key(item[0])[1]],  # Sort by capture type priority
            parse_capture_key(item[0])[0]  # Then by line number
        )
    )
    return [value for _, value in sorted_items]
