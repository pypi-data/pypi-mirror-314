from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import TypeAlias, NamedTuple, Union, Optional
import re
import cedarscript_grammar
from tree_sitter import Parser


class ParseError(NamedTuple):
    ordinal: int
    message: str
    line: int
    column: int
    suggestion: str

    def __str__(self):
        line_msg = f'; LINE #{self.line}' if self.line else ''
        col_msg = f'; COLUMN #{self.column}' if self.column else ''
        cmd_or_block = 'BLOCK' if self.line else 'COMMAND'
        error_type = 'Source Parsing' if self.line else 'CST Parsing'
        suggestion_msg = f'{self.suggestion} ' if self.suggestion else ''
        return (
            f"<error-details><error-location>{cmd_or_block} #{self.ordinal}{line_msg}{col_msg}</error-location>"
            f"<type>{error_type} (no commands were applied at all)</type><description>{self.message}</description>"
            f"<suggestion>{suggestion_msg}"
            "(NEVER apologize; just take a deep breath, re-read grammar rules (enclosed by <grammar.js> tags) "
            "and fix you CEDARScript syntax)</suggestion></error-details>"
        )


# <location>


class BodyOrWhole(StrEnum):
    BODY = auto()
    WHOLE = auto()


MarkerType = StrEnum('MarkerType', 'LINE VARIABLE FUNCTION METHOD CLASS')
RelativePositionType = StrEnum('RelativePositionType', 'AT BEFORE AFTER INTO_TOP INTO_BOTTOM')


class MarkerCompatible:
    def as_marker(self) -> 'Marker':
        pass


@dataclass
class Marker(MarkerCompatible):
    """
    A marker can be one of:
    - LINE with string/number value
    - LINE REGEX with regex pattern
    - LINE PREFIX with prefix string
    - LINE SUFFIX with suffix string
    - VARIABLE with name
    - FUNCTION with name
    - CLASS with name
    See also: Marker.to_search_range
    """
    type: MarkerType
    value: str | int | None
    offset: int | None = None

    # See `line_base`
    marker_subtype: str | None = None

    @property
    def as_marker(self) -> 'Marker':
        return self

    def with_qualifier(self, qualifier: RelativePositionType):
        return RelativeMarker(
            qualifier=qualifier,
            type=self.type,
            value=self.value,
            offset=self.offset,
            marker_subtype = self.marker_subtype
        ) if qualifier else self

    def __str__(self):
        result = self.type.value
        match self.marker_subtype:
            case 'string' | None:
                pass
            case 'empty':
                result = 'empty line'
            case _:
                result += f' {self.marker_subtype}'

        if self.marker_subtype != 'empty':
            result += f" '{str(self.value).strip()}'"
        if self.offset is not None:
            result += f" ^{self.offset}"
        return result


class RelativeMarker(Marker):
    qualifier: RelativePositionType

    def __init__(self, qualifier: RelativePositionType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qualifier = qualifier

    def __str__(self):
        result = super().__str__()
        match self.qualifier:
            case RelativePositionType.AT:
                pass
            case _:
                result = f'{result} ({str(self.qualifier).replace("_", " ")})'
        return result


@dataclass
class Segment:
    start: RelativeMarker
    end: RelativeMarker

    def __str__(self):
        return f"segment from [{self.start}] to [{self.end}]"


MarkerOrSegment: TypeAlias = Marker | Segment
Region: TypeAlias = BodyOrWhole | Marker | Segment
RegionOrRelativeMarker: BodyOrWhole | Marker | Segment | RelativeMarker
# <file-or-identifier>


@dataclass
class WhereClause:
    field: str
    operator: str
    value: str


@dataclass
class SingleFileClause:
    file_path: str


@dataclass
class IdentifierFromFile(SingleFileClause, MarkerCompatible):
    identifier_type: MarkerType  # VARIABLE, FUNCTION, CLASS (but not LINE)
    name: str
    where_clause: WhereClause
    offset: int | None = None

    @property
    def as_marker(self) -> Marker:
        # TODO Handle different values for field and operator in where_clause
        return Marker(self.identifier_type, self.name or self.where_clause.value, self.offset)

    def __str__(self):
        wc = self.where_clause or ''
        if wc:
            wc = f' ({wc})'
        result = f"{str(self.identifier_type).lower()} {self.name}{wc}"
        if self.offset is not None:
            result += f" at offset {self.offset}"
        return f"{result} [{str(self.file_path).split('/')[-1]}]"


FileOrIdentifierWithin: TypeAlias = SingleFileClause | IdentifierFromFile

# </file-or-identifier>

# </location>


# <editing-clause>

@dataclass
class RegionClause:
    region: Region


@dataclass
class ReplaceClause(RegionClause):
    pass


@dataclass
class DeleteClause(RegionClause):
    pass


@dataclass
class InsertClause(MarkerCompatible):
    insert_position: RelativeMarker

    @property
    def as_marker(self) -> RelativeMarker:
        return self.insert_position


@dataclass
class MoveClause(DeleteClause, InsertClause):
    to_other_file: SingleFileClause | None = None
    relative_indentation: int | None = None


EditingAction: TypeAlias = ReplaceClause | DeleteClause | InsertClause | MoveClause

# </editing-clause>

# <command>

@dataclass
class Command:
    type: str

    @property
    def files_to_change(self) -> tuple[str, ...]:
        return ()

# <file-command>


@dataclass
class FileCommand(Command):
    file_path: str

    @property
    def files_to_change(self) -> tuple[str, ...]:
        return (self.file_path,)


@dataclass
class CreateCommand(FileCommand):
    content: str


@dataclass
class RmFileCommand(FileCommand):
    pass


@dataclass
class MvFileCommand(FileCommand):
    target_path: str

    @property
    def files_to_change(self) -> tuple[str, ...]:
        return super().files_to_change + (self.target_path,)

# </file-command>


@dataclass
class LoopControl(StrEnum):
    BREAK = 'BREAK'
    CONTINUE = 'CONTINUE'


@dataclass
class CaseWhen:
    """Represents a WHEN condition in a CASE statement"""
    empty: bool = False
    indent_level: int | None = None
    line_number: int | None = None
    line_matcher: str | None = None
    regex: str | None = None
    prefix: str | None = None
    suffix: str | None = None


@dataclass
class CaseAction:
    """Represents a THEN action in a CASE statement"""
    loop_control: LoopControl | None = None
    remove: bool = False
    sub_pattern: str | None = None  # For SUB command pattern
    sub_repl: str | None = None    # For SUB command replacement
    indent: int | None = None
    content: Optional[str | tuple[Region, int | None]] = None

class LineFilter:
    pass

@dataclass
class CaseStatement(LineFilter):
    """Represents a CASE statement with when-then pairs and optional else"""
    cases: list[tuple[CaseWhen, CaseAction]]
    else_action: Optional[CaseAction] = None


@dataclass
class EdScript(LineFilter):
    """Represents an ED script content"""
    script: str


@dataclass
class UpdateCommand(Command):
    target: FileOrIdentifierWithin
    action: EditingAction
    content: str | tuple[Region, int | None] | EdScript | CaseStatement | None = None

    @property
    def files_to_change(self) -> tuple[str, ...]:
        result = (self.target.file_path,)
        match self.action:
            case MoveClause(to_other_file=target_file):
                if target_file:
                    result += (target_file,)
        return result


@dataclass
# TODO
class SelectCommand(Command):
    target: Union['FileNamesPathsTarget', 'OtherTarget']
    source: Union['SingleFileClause', 'MultiFileClause']
    where_clause: WhereClause | None = None
    limit: int | None = None


# </command>

def _generate_suggestion(error_node, code_text) -> str:
    """
    Generates a suggestion based on the context of the error.
    """
    # Analyze the parent node to provide context
    parent = error_node.parent
    if not parent:
        return "Please check the syntax near the error."

    parent_type = parent.type
    if parent_type == 'content_literal':
        return "Ensure the content block is properly enclosed with matching quotes (''' or \"\")."
    if parent_type == 'update_command':
        return "An action clause ('REPLACE', 'INSERT', 'DELETE') is expected in the 'UPDATE' command."
    if parent_type == 'create_command':
        return "The 'CREATE' command may be missing 'WITH CONTENT' or has a syntax issue."
    # Default suggestion
    return f"Please check the syntax near the error (parent node: {parent_type})"


class _CEDARScriptASTParserBase:
    def __init__(self):
        """Load the CEDARScript language, and initialize the parser.
        """
        from importlib.metadata import version
        from packaging import version as v

        package_version = version('tree_sitter')
        parsed_version = v.parse(package_version)

        match parsed_version:
            case x if x <= v.parse('0.21.3'):
                self.parser = Parser()
                self.parser.set_language(cedarscript_grammar.language())
            case _:
                self.parser = Parser(cedarscript_grammar.language())


class CEDARScriptASTParser(_CEDARScriptASTParserBase):
    def parse_script(self, code_text: str) -> tuple[Sequence[Command], Sequence[ParseError]]:
        """
        Parses the CEDARScript code and returns a tuple containing:
        - A list of Command objects if parsing is successful.
        - A list of ParseError objects if there are parsing errors.
        """
        command_ordinal = 1
        try:
            root_node = self.parser.parse(bytes(code_text, 'utf8')).root_node

            errors = self._collect_parse_errors(root_node, code_text, command_ordinal)
            if errors:
                # If there are errors, return them without commands
                return [], errors

            # Extract commands from the parse tree
            commands = []
            for child in root_node.children:
                node_type = child.type.casefold()
                if node_type == 'comment':
                    print("(COMMENT) " + self.parse_string(child).removeprefix("--").removeprefix("/*").strip())
                if not node_type.endswith('_command'):
                    continue
                commands.append(self.parse_command(child))
                command_ordinal += 1

            return commands, []
        except Exception as e:
            # Handle any unexpected exceptions during parsing
            error_message = str(e)
            error = ParseError(
                ordinal=command_ordinal,
                message=error_message,
                line=0,
                column=0,
                suggestion="Revise your CEDARScript syntax."
            )
            return [], [error]

    def _collect_parse_errors(self, node, code_text, command_ordinal: int) -> list[ParseError]:
        """
        Recursively traverses the syntax tree to collect parse errors.
        """
        errors = []
        if node.has_error:
            if node.type == 'ERROR':
                # Get the line and column numbers
                start_point = node.start_point  # (row, column)
                line = start_point[0] + 1       # Line numbers start at 1
                column = start_point[1] + 1     # Columns start at 1

                # Extract the erroneous text
                error_text = code_text[node.start_byte:node.end_byte].strip()

                # Create a helpful error message
                message = f"Syntax error near '{error_text}' at line {line}, column {column}."
                suggestion = _generate_suggestion(node, code_text)

                error = ParseError(
                    ordinal=command_ordinal,
                    message=message,
                    line=line,
                    column=column,
                    suggestion=suggestion
                )
                errors.append(error)

            # Recurse into children to find all errors
            for child in node.children:
                errors.extend(self._collect_parse_errors(child, code_text, command_ordinal))
        return errors

    def _get_expected_tokens(self, error_node) -> tuple[str]:
        """
        Provides expected tokens based on the error_node's context.
        """
        # Since Tree-sitter doesn't provide expected tokens directly,
        # you might need to implement this based on the grammar and error context.
        # For now, we'll return an empty list to simplify.
        return tuple()

    def parse_command(self, node):
        match node.type:
            case 'create_command':
                return self.parse_create_command(node)
            case 'rm_file_command':
                return self.parse_rm_file_command(node)
            case 'mv_file_command':
                return self.parse_mv_file_command(node)
            case 'update_command':
                return self.parse_update_command(node)
            # case 'select_command':
            #     return self.parse_select_command(node)
            case _:
                raise ValueError(f"Unexpected command type: {node.type}")

    def parse_create_command(self, node):
        file_path = self.parse_singlefile_clause(self.find_first_by_type(node.children, 'singlefile_clause')).file_path
        content = self.parse_content(node)
        return CreateCommand(type='create', file_path=file_path, content=content)

    def parse_rm_file_command(self, node):
        file_path = self.parse_singlefile_clause(self.find_first_by_type(node.children, 'singlefile_clause')).file_path
        return RmFileCommand(type='rm_file', file_path=file_path)

    def parse_mv_file_command(self, node):
        file_path = self.parse_singlefile_clause(self.find_first_by_type(node.children, 'singlefile_clause')).file_path
        target_path = self.parse_to_value_clause(self.find_first_by_type(node.children, 'to_value_clause'))
        return MvFileCommand(type='mv_file', file_path=file_path, target_path=target_path)

    def parse_update_command(self, node):
        target = self.parse_update_target(node)
        action = self.parse_update_action(node)
        content = self.parse_content(node)
        return UpdateCommand(type='update', target=target, action=action, content=content)

    def parse_update_target(self, node):
        types = [
            'singlefile_clause',
            'identifier_from_file'
        ]
        target_node = self.find_first_by_type(node.named_children, types)
        if target_node is None:
            raise ValueError("No valid target found in update command")

        match target_node.type.casefold():
            case 'singlefile_clause':
                return self.parse_singlefile_clause(target_node)
            case 'identifier_from_file':
                return self.parse_identifier_from_file(target_node)
            case _ as invalid:
                raise ValueError(f"[parse_update_target] Invalid target: {invalid}")

    def parse_identifier_from_file(self, node):
        identifier_matcher = self.find_first_by_type(node.named_children, 'identifier_matcher')
        identifier_type = MarkerType(identifier_matcher.children[0].type.casefold())
        name = self.parse_string(identifier_matcher.named_children[0])
        offset_clause = self.find_first_by_type(identifier_matcher.named_children, 'offset_clause')
        file_clause = self.find_first_by_type(node.named_children, 'singlefile_clause')
        where_clause = self.find_first_by_type(node.named_children, 'where_clause')

        if not file_clause or not name:
            raise ValueError("Invalid identifier_from_file clause")

        file_path = self.parse_singlefile_clause(file_clause).file_path
        offset = self.find_primitive(offset_clause) if offset_clause else None
        where = self.parse_where_clause(where_clause)

        return IdentifierFromFile(file_path=file_path,
                                  identifier_type=identifier_type,  name=name, offset=offset,
                                  where_clause=where
                                  )

    def parse_where_clause(self, node):
        if not node:
            return None
        condition = self.find_first_by_type(node.children, 'condition')
        if not condition:
            raise ValueError("No condition found in where clause")

        field = self.parse_string(self.find_first_by_type(condition.children, 'conditions_left'))
        operator = self.parse_string(self.find_first_by_type(condition.children, 'operator'))
        value = self.parse_string(self.find_first_by_type(condition.children, 'string'))

        return WhereClause(field=field, operator=operator, value=value)

    def parse_update_action(self, node):
        child_types = [
            'update_delete_region_clause', 'update_delete_mos_clause', 'update_move_region_clause',
            'update_move_mos_clause', 'insert_clause', 'replace_mos_clause', 'replace_region_clause'
        ]
        action_node = self.find_first_by_type(node.named_children, child_types)
        if action_node is None:
            raise ValueError("No valid action found in update command")

        match action_node.type:
            case 'update_delete_mos_clause' | 'update_delete_region_clause':
                return self.parse_delete_clause(action_node)
            case 'update_move_mos_clause' | 'update_move_region_clause':
                return self.parse_move_clause(action_node)
            case 'insert_clause':
                return self.parse_insert_clause(action_node)
            case 'replace_mos_clause' | 'replace_region_clause':
                return self.parse_replace_clause(action_node)
            case _ as invalid:
                raise ValueError(f'[parse_update_action] Invalid: {invalid}')

    def parse_delete_clause(self, node):
        region = self.parse_region(self.find_first_by_type(node.named_children, ['marker_or_segment', 'region_field']))
        return DeleteClause(region=region)

    def parse_move_clause(self, node):
        source = self.parse_region(self.find_first_by_type(node.named_children, ['marker_or_segment', 'region_field']))
        destination = self.find_first_by_type(node.named_children, 'update_move_clause_destination')
        insert_clause = self.find_first_by_type(destination.named_children, 'insert_clause')
        insert_clause = self.parse_insert_clause(insert_clause)
        rel_indent = self.parse_relative_indentation(destination)
        # TODO to_other_file
        return MoveClause(
            region=source,
            insert_position=insert_clause.insert_position,
            relative_indentation=rel_indent
        )

    def parse_insert_clause(self, node) -> InsertClause:
        relative_marker = self.find_first_by_type(node.children, 'relpos_bai')
        relative_marker: RelativeMarker = self.parse_region(relative_marker)
        # TODO check relative_marker type
        return InsertClause(insert_position=relative_marker)

    def parse_replace_clause(self, node):
        region = self.parse_region(self.find_first_by_type(node.named_children, ['marker_or_segment', 'region_field']))
        return ReplaceClause(region=region)

    def parse_region(self, node) -> Region:
        qualifier = None
        match node.type.casefold():
            case 'marker_or_segment':
                node = node.named_children[0]
            case 'region_field':
                node = node.children[0]
                if node.type.casefold() == 'marker_or_segment':
                    node = node.named_children[0]
            case 'relpos_bai':
                node = node.named_children[0]
                main_type = node.child(0).type.casefold()
                match main_type:
                    case 'into':
                        # INTO_TOP, INTO_BOTTOM
                        main_type += '_' + node.child(2).type.casefold()
                qualifier = RelativePositionType(main_type)
                node = node.named_children[0]
            case 'relpos_beforeafter':
                qualifier = RelativePositionType(node.child(0).type.casefold())
                node = node.named_children[0]
            case 'relpos_at':
                node = node.named_children[0]

        match node.type.casefold():
            case 'marker' | 'line_matcher' | 'identifier_matcher':
                result = self.parse_marker(node)
            case 'segment':
                result = self.parse_segment(node)
            case BodyOrWhole.BODY | BodyOrWhole.WHOLE as bow:
                result = BodyOrWhole(bow.lower())
            case _:
                raise ValueError(f"Unexpected node type: {node.type}")
        return result.with_qualifier(qualifier) if qualifier else result

    def parse_marker(self, node) -> Marker:
        # Handle marker inside marker_or_segment
        if node.type.casefold() == 'marker':
            node = node.named_children[0]
        
        marker_type = node.named_children[0].type
        # LINE, VARIABLE, FUNCTION, METHOD or CLASS
        marker_subtype = None
        value = None

        # Handle the different marker types
        if marker_type == 'line_base':
            marker_type = 'line'
            # subtype: None, number, EMPTY, REGEX, PREFIX, SUFFIX, INDENT-LEVEL
            line_base_node = node.named_children[0] # line_base
            marker_subtype = [n.type.casefold() for n in line_base_node.children if n.type.casefold() != 'line'][0]
            value = self.find_primitive(line_base_node)

        else:  # identifier_matcher
            marker_type = node.children[0].type.casefold()
            value = self.find_primitive(node)

        offset = self.find_first_by_type(node.named_children, 'offset_clause')
        offset = self.find_primitive(offset)
        return Marker(
            type=MarkerType(marker_type.casefold()),
            marker_subtype=marker_subtype,
            value=value,
            offset=offset
        )

    def parse_segment(self, node) -> Segment:
        relpos_start = self.find_first_by_type(node.named_children, 'relpos_segment_start').children[1]
        relpos_end = self.find_first_by_type(node.named_children, 'relpos_segment_end').children[1]
        start: RelativeMarker = self.parse_region(relpos_start)
        end: RelativeMarker = self.parse_region(relpos_end)
        return Segment(start=start, end=end)

    def parse_relative_indentation(self, node) -> int | None:
        node = self.find_first_by_type(node.named_children, 'relative_indentation')
        return self.find_primitive(node)

    def parse_content(self, node) -> str | tuple[Region, int | None] | None:
        content = self.find_first_by_type(node.named_children, [
            'content_literal', 'content_from_segment', 'line_filter'
        ])
        if not content:
            return None
        match content.type:
            case 'content_literal':
                return self.parse_content_literal(content)  # str
            case 'content_from_segment':
                return self.parse_content_from_segment_clause(content)  # tuple[Region, int]
            case 'line_filter':
                return self.parse_line_filter(content)
            case _:
                raise ValueError(f"Invalid content type: {content.type}")

    def parse_line_filter(self, node) -> LineFilter:
        node = node.named_children[0]
        match node.type:
            case 'ed_stmt':
                return self.parse_ed_stmt(node)  # EdScript
            case 'case_stmt':
                return self.parse_case_stmt(node)  # CaseStatement


    def parse_ed_stmt(self, node) -> EdScript:
        """Parse an ED script statement"""
        ed_script = self.find_first_by_type(node.children, 'string')
        if ed_script is None:
            raise ValueError("No ED script found in ed_stmt")
        return EdScript(script=self.parse_string(ed_script))

    def parse_case_stmt(self, node) -> CaseStatement:
        """Parse a CASE statement"""
        cases = []
        
        # Parse all WHEN-THEN pairs
        current_when = None
        for child in node.children:
            match child.type:
                case 'line_base':
                    current_when = self.parse_case_when(child)
                case 'case_action' if current_when is not None:
                    action = self.parse_case_action(child)
                    cases.append((current_when, action))
                    current_when = None

        # Parse optional ELSE clause
        else_action = None
        else_node = self.find_first_by_field_name(node, 'else')
        if else_node:
            else_action = self.parse_case_action(else_node)

        return CaseStatement(cases=cases, else_action=else_action)

    def parse_case_when(self, node) -> CaseWhen:
        """Parse a WHEN clause in a CASE statement"""
        when = CaseWhen()

        if self.find_first_by_field_name(node, 'empty'):
            when.empty = True

        elif indent := self.find_first_by_field_name(node, 'indent_level'):
            when.indent_level = int(indent.text.decode('utf8'))

        elif line_num := self.find_first_by_field_name(node, 'line_number'):
            when.line_number = int(line_num.text.decode('utf8'))

        elif line_str := self.find_first_by_field_name(node, 'line_matcher'):
            when.line_matcher = self.parse_string(line_str)

        elif regex := self.find_first_by_field_name(node, 'regex'):
            when.regex = re.compile(self.parse_string(regex))

        elif prefix := self.find_first_by_field_name(node, 'prefix'):
            when.prefix = self.parse_string(prefix)

        elif suffix := self.find_first_by_field_name(node, 'suffix'):
            when.suffix = self.parse_string(suffix)

        return when

    def parse_case_action(self, node) -> CaseAction:
        """Parse a THEN clause in a CASE statement"""
        action = CaseAction()
        
        # Parse loop control if present
        loop_control = self.find_first_by_type(node.children, 'loop_control')
        if loop_control:
            if self.find_first_by_type(loop_control.children, 'loop_break'):
                action.loop_control = LoopControl.BREAK
            elif self.find_first_by_type(loop_control.children, 'loop_continue'):
                action.loop_control = LoopControl.CONTINUE

        # Parse other action types
        if self.find_first_by_field_name(node, 'remove'):
            action.remove = True
        elif pattern := self.find_first_by_field_name(node, 'pattern'):
            action.sub_pattern = re.compile(self.parse_string(pattern))
            if repl := self.find_first_by_field_name(node, 'repl'):
                action.sub_repl = self.parse_string(repl)
        elif indent := self.find_first_by_field_name(node, 'indent'):
            action.indent = int(indent.text)
        else:
            # Check for content replacement
            content = self.find_first_by_type(node.children, ['content_literal', 'content_from_segment'])
            if content:
                action.content = self.parse_content(content)

        return action

    def parse_singlefile_clause(self, node):
        if node is None or node.type != 'singlefile_clause':
            raise ValueError("Expected singlefile_clause node")
        path_node = self.find_first_by_type(node.children, 'string')
        if path_node is None:
            raise ValueError("No file_path found in singlefile_clause")
        return SingleFileClause(file_path=self.parse_string(path_node))

    def parse_content_literal(self, node) -> str:
        child_type = ['string', 'relative_indent_block', 'multiline_string']
        content_node = self.find_first_by_type(node.children, child_type)
        if content_node is None:
            raise ValueError("No content found in content_literal")
        if content_node.type == 'string':
            return self.parse_string(content_node)
        elif content_node.type == 'relative_indent_block':
            return self.parse_relative_indent_block(content_node)
        elif content_node.type == 'multiline_string':
            return self.parse_multiline_string(content_node)

    def parse_content_from_segment_clause(self, node) -> tuple[Region, int | None]:
        child_type = ['marker_or_segment']
        content_node = self.find_first_by_type(node.children, child_type)
        # TODO parse relative indentation
        if content_node is None:
            raise ValueError("No content found in content_from_segment")
        rel_indent = self.parse_relative_indentation(node)
        return self.parse_region(content_node), rel_indent

    def parse_to_value_clause(self, node):
        if node is None or node.type != 'to_value_clause':
            raise ValueError("Expected to_value_clause node")
        value_node = self.find_first_by_type(node.children, 'string')
        if value_node is None:
            raise ValueError("No value found in to_value_clause")
        return self.parse_string(value_node)

    def find_primitive(self, node):
        if node is None:
            return None
        node = self.find_first_by_type(node.named_children, ['string', 'number'])
        if node is None:
            return None
        match node.type.casefold():
            case 'string':
                return self.parse_string(node)
            case 'number':
                return int(node.text)
            case _:
                raise ValueError(f"[find_primitive] Invalid primitive: {node.type} ({node.text})")

    @staticmethod
    def parse_string(node):
        match node.type.casefold():
            case 'string':
                node = node.named_children[0]
        text = node.text.decode('utf8')
        match node.type.casefold():
            case 'raw_string':
                match text:
                    case x if x.startswith("r'''") or x.startswith('r"""'):
                        text = text[4:-3]
                    case x if x.startswith("r'") or x.startswith('r"'):
                        text = text[2:-1]
                    case _:
                        raise ValueError(f"Invalid raw string: `{text}`")
            case 'single_quoted_string':
                text = text[1:-1]  # Remove surrounding quotes
                text = text.replace(r"\'", "'").replace(r'\"', '"').replace(r"\t", '\t').replace("\\\\", "\\")
            case 'multi_line_string':
                text = text[3:-3]

        return text

    @staticmethod
    def parse_multiline_string(node):
        return node.text.decode('utf8').strip("'''").strip('"""')

    def parse_relative_indent_block(self, node) -> str:
        lines = []
        for line_node in node.children:
            if line_node.type == 'relative_indent_line':
                indent_prefix = self.find_first_by_type(line_node.children, 'relative_indent_prefix')
                content = self.find_first_by_type(line_node.children, 'match_any_char')
                if indent_prefix and content:
                    indent = int(indent_prefix.text.strip('@:'))
                    lines.append(f"{' ' * (4 * indent)}{content.text}")
        return '\n'.join(lines)

    @staticmethod
    def find_first_by_type(nodes: Sequence[any], child_type):
        if isinstance(child_type, list):
            for child in nodes:
                if child.type in child_type:
                    return child
        else:
            for child in nodes:
                if child.type == child_type:
                    return child
        return None

    @staticmethod
    def find_first_by_field_name(node: any, field_names):
        if not isinstance(field_names, list):
            return node.child_by_field_name(field_names)

        for field_name in field_names:
            result = node.child_by_field_name(field_name)
            if result:
                return result

        return None
