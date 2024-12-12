#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""SystemVerilog Expression Resolver."""

from collections.abc import Iterable, Iterator
from typing import ClassVar, Literal

import ucdp as u
from aligntext import Align
from matchor import matchs

DIRKEYWORDS = {
    u.IN: "input",
    u.OUT: "output",
    u.INOUT: "inout",
}
DIRCOMMENT = {
    u.IN: "I",
    u.OUT: "O",
    u.INOUT: "IO",
}

SvDecl = tuple[str, str]


def _is_param(ident: u.Ident) -> bool:
    return isinstance(ident, u.Param)


def _is_const(ident: u.Ident) -> bool:
    return isinstance(ident, u.Const)


class SvExprResolver(u.ExprResolver):
    """
    SystemVerilog Expression Resolver.

    >>> import ucdp as u
    >>> import ucdpsv as usv
    >>> resolver = usv.SvExprResolver()
    >>> resolver.resolve(u.ConstExpr(u.UintType(18, default=5)))
    "18'h00005"
    >>> resolver.resolve(u.ConstExpr(u.SintType(18, default=-5)))
    "18'sh3FFFB"
    """

    ff_dly: str = ""
    _opremap: ClassVar[dict[str, str]] = {"//": "/"}

    @staticmethod
    def _get_rail_value(value: int) -> str:
        return f"1'b{value}"

    @staticmethod
    def _get_bit_value(value: int) -> str:
        return f"1'b{value}"

    def _get_uint_value(self, value: int, width: int | u.Expr) -> str:
        if isinstance(width, int):
            hexstr = f"{value:X}".zfill((width + 3) // 4)
            return f"{width}'h{hexstr}"

        # parameterized width
        width = self.resolve(width)
        if value != 0:
            return f"'d{value}"

        return f"{{{width} {{1'b0}}}}"

    def _get_sint_value(self, value: int, width: int | u.Expr) -> str:
        if isinstance(width, int):
            wrap = 1 << width
            value = (value + wrap) % wrap
            hexstr = f"{value:X}".zfill((width + 3) // 4)
            return f"{width}'sh{hexstr}"

        # parameterized width
        width = self.resolve(width)

        # This is not the best, but all we can do - or?
        if value > 0:
            return f"'d{value}"
        if value < 0:
            return f"-('d{-value})"

        return f"{{{width} {{1'sb0}}}}"

    @staticmethod
    def _get_integer_value(value: int) -> str:
        return str(value)

    @staticmethod
    def _get_bool_value(value: bool) -> str:
        if value:
            return "true"
        return "false"

    @staticmethod
    def _get_string_value(value) -> str:
        return f'"{value}"'

    def _resolve_log2expr(self, expr: u.Log2Expr) -> str:
        return f"$clog2({self.resolve(expr.expr)})"

    def get_paramdecls(self, idents: u.Idents, is_last: bool = True, indent: int = 0) -> Align:
        """Return `Align` With Parameter Declarations."""
        return self._get_paramdecls(idents.iter(filter_=_is_param), "parameter", ",", is_last, indent)

    def get_localparamdecls(self, idents: u.Idents, indent: int = 0) -> Align:
        """Return `Align` With Local Parameter Declarations."""
        return self._get_paramdecls(idents.iter(filter_=_is_const), "localparam", ";", False, indent)

    def _get_paramdecls(self, iterator: Iterable[u.Ident], keyword: str, sep: str, is_last: bool, indent: int) -> Align:
        align = Align(rtrim=True, strip_empty_cols=True)
        pre = " " * indent
        align.set_separators(" ", first=pre)
        for ident, svdecl, svsep in self._iter_idents(align, pre, iterator, sep, is_last):
            name = ident.name
            svdims = self.get_dims(ident.type_)
            svdefault = self.get_default(ident.type_)
            svcomment = _get_comment(ident.doc.comment)
            svdefault = f"{svdefault}{svsep}"
            align.add_row((keyword, *svdecl, name, svdims, "=", svdefault, svcomment))
        return align

    def get_portdecls(
        self, ports: u.Idents, is_last: bool = True, indent: int = 0, wirenames: u.Names | None = None
    ) -> Align:
        """Return `Align` With Port Declarations."""
        return self._get_signaldecls(ports.iter(), ",", is_last=is_last, indent=indent, wirenames=wirenames, ports=True)

    def get_signaldecls(self, signals: u.Idents, indent: int = 0, wirenames: u.Names | None = None) -> Align:
        """Return `Align` With Signal Declarations."""

        def stop(signal):
            return isinstance(signal, u.Port)

        return self._get_signaldecls(signals.iter(stop=stop), ";", is_last=False, indent=indent, wirenames=wirenames)

    def _get_signaldecls(
        self,
        iterator: Iterable[u.Ident],
        sep: str,
        is_last: bool,
        indent: int,
        wirenames: u.Names | None = None,
        ports: bool = False,
    ) -> Align:
        align = Align(rtrim=True, strip_empty_cols=True)
        pre = " " * indent
        align.set_separators(" ", first=pre)
        wirenames = u.split(wirenames)
        for ident, svdecl, svsep in self._iter_idents(align, pre, iterator, sep, is_last):
            name = ident.name
            svdims = self.get_dims(ident.type_)
            if svdims:
                svdims = f"{svdims}{svsep}"
            else:
                name = f"{name}{svsep}"
            svcomment = _get_comment(ident.doc.comment)
            if ports:
                align.add_row((*_get_port_decl(ident, svdecl), name, svdims, svcomment))
            else:
                align.add_row((*svdecl, name, svdims, svcomment))
        return align

    def get_instparams(self, mod: u.BaseMod, is_last: bool = True, indent: int = 0) -> Align:
        """Return `Align` With Parameter Declarations."""
        align = Align(rtrim=True)
        pre = " " * indent
        align.set_separators("(", ")", "", first=pre)

        def filter_(ident):
            return isinstance(ident, u.Param) and ident.value is not None

        for ident, _, svsep in self._iter_idents(align, pre, mod.namespace.iter(filter_=filter_), ",", is_last):
            name = f".{ident.name}"
            expr = self.get_value(ident)
            svcomment = _get_comment(ident.doc.comment, pre=" ")
            align.add_row(name, expr, svsep, svcomment)
        return align

    def get_instcons(
        self, instcons: u.Assigns, skips: u.Names | None = None, is_last: bool = True, indent: int = 0
    ) -> Align:
        """Return `Align` With Parameter Declarations."""
        align = Align(rtrim=True)
        pre = " " * indent
        align.set_separators("(", ")", "", first=pre)
        skips = u.split(skips)
        if skips:
            instconstiter = instcons.iter(filter_=lambda ident: not matchs(ident.name, skips))
        else:
            instconstiter = instcons.iter()

        for assign, _, svsep in self._iter_idents(align, pre, instconstiter, ",", is_last):
            target = assign.target
            comments = []
            if target.suffix != target.direction.suffix:
                comments.append(DIRCOMMENT[target.direction])
            if isinstance(target.type_, u.RailType):
                comments.append("RAIL")

            source = assign.source
            if source is None:
                comments.append("TODO")
                if target.direction == u.IN:
                    source = self.get_default(target.type_)
            elif isinstance(source, u.Note):
                source = f"/* {source.note} */"
            else:
                source = self.resolve(source)
            comments.append(target.doc.comment)
            svcomment = _get_comment(u.join_names(*comments, concat=" - "), pre=" ")
            align.add_row(f".{assign.name}", source, svsep, svcomment)
        return align

    def get_defaults(self, assigns: Iterable[u.Assign], indent: int = 0, oper: str = "=") -> Align:
        """Get Assigns."""
        align = Align(rtrim=True, strip_empty_cols=True)
        pre = " " * indent
        align.set_separators(" ", first=pre)
        for ident, _, _ in self._iter_idents(align, pre, assigns):
            svvalue = self.get_value(ident)
            align.add_row((ident.name, f"{oper} {svvalue};"))
        return align

    def get_assigns(self, assigns: u.Assigns, indent: int, oper: str = "") -> Align:  # noqa: C901
        """Get Systemverilog Continuous Assigns."""
        align = Align(rtrim=True, strip_empty_cols=True)
        pre = " " * indent
        align.set_separators(" ", first=pre)
        if oper:
            for assign, _, _ in self._iter_idents(align, pre, assigns):
                name = assign.target.name
                source = assign.source
                if source is not None:
                    source = self.resolve(source)
                if source is None:
                    source = self.get_value(assign.target)
                direction = assign.target.direction
                if direction in (u.OUT, u.FWD):
                    align.add_row((name, oper, f"{source};"))
                elif direction in (u.IN, u.BWD):
                    align.add_row((source, oper, f"{name};"))
        else:
            for assign, _, _ in self._iter_idents(align, pre, assigns):
                name = assign.target.name
                source = assign.source
                if source is not None:
                    source = self.resolve(source)
                direction = assign.target.direction
                if direction in (u.OUT, u.FWD):
                    align.add_row(("assign", "", name, "=", f"{source};"))
                elif direction in (u.IN, u.BWD):
                    align.add_row(("assign", "", source, "=", f"{name};"))
                else:
                    align.add_row(("tran", f"u_tran_{name}", f"({name},", "", f"{source});"))
        return align

    def get_decl(self, type_: u.BaseType) -> SvDecl | None:  # noqa: PLR0911,C901
        """Get SV Declaration."""
        while isinstance(type_, u.ArrayType):
            type_ = type_.itemtype
        while isinstance(type_, u.BaseEnumType):
            type_ = type_.keytype

        if isinstance(type_, (u.BitType, u.RailType)):
            keyword = "logic" if type_.logic else "bit"
            return keyword, ""
        if isinstance(type_, u.UintType):
            keyword = "logic" if type_.logic else "bit"
            return keyword, self._resolve_slice(type_.slice_).replace(" ", "")

        if isinstance(type_, u.SintType):
            keyword = "logic signed" if type_.logic else "bit signed"
            return keyword, self._resolve_slice(type_.slice_).replace(" ", "")

        if isinstance(type_, u.BaseStructType):
            return None

        if isinstance(type_, u.IntegerType):
            keyword = "integer" if type_.logic else "int"
            return keyword, ""

        if isinstance(type_, u.BoolType):
            return "bool", ""

        if isinstance(type_, u.StringType):
            return "string", ""

        if isinstance(type_, u.FloatType):
            return "real", ""

        if isinstance(type_, u.DoubleType):
            return "real", ""

        raise ValueError(type_)  # pragma: no cover

    def get_dims(self, type_: u.BaseType) -> str:
        """Get SV Dimensions."""
        dims = []
        while isinstance(type_, u.ArrayType):
            dims.append(self._resolve_slice(type_.slice_).replace(" ", ""))
            type_ = type_.itemtype
        return "".join(dims)

    def get_default(self, type_: u.BaseType) -> str:
        """Get SV Default."""
        return self._resolve_value(type_)

    def get_value(self, ident: u.Ident) -> str:
        """Get SV Value."""
        return self._resolve_value(ident.type_, value=getattr(ident, "value", None))

    def _iter_idents(
        self, align: Align, pre: str, idents: Iterable[u.Ident | u.Assign], sep: str = ";", is_last: bool = False
    ) -> Iterator[tuple[u.Ident, SvDecl, str]]:
        decls = [(ident, self.get_decl(ident.type_)) for ident in idents]
        nosepmap = _get_nosepmap(decls) if is_last else {}
        pendlevel = None
        ifdef = None
        ended = False
        # Iterate over all identifier and their declarations
        for ident, svdecl in decls:
            # emit ifdef, even if empty
            ifdef = _add_ifdef(pre, align, ifdef, ident.ifdef)
            if svdecl is not None:
                if ended:
                    align.add_spacer(f"{pre}{sep}")
                    ended = False
                pendlevel = _add_declcomment(align, ident, pendlevel, svdecl, pre)
                if is_last and nosepmap.get(ident.ifdef, None) == ident.name:
                    yield ident, svdecl, ""
                    ended = True
                else:
                    yield ident, svdecl, sep
            else:
                pendlevel = _add_declcomment(align, ident, pendlevel, svdecl, pre)
        _add_ifdef(pre, align, ifdef)

    def get_ident_expr(self, type_: u.BaseScalarType, name: str, op: Literal[None, 0, 1, "", "~"]) -> str | None:
        """Get Ident Expression."""
        if op is None:
            return None
        if op == 0:
            return self._resolve_value(type_, value=0)
        if op == 1:
            return self._resolve_value(type_, value=type_.max_)
        return f"{op}{name}"

    def _get_array_value(self, itemvalue: str, slice_: u.Slice) -> str:
        width = slice_.width
        if not isinstance(width, int):
            width = self._resolve(width)
        return f"'{{{width}{{{itemvalue}}}}}"

    def split_mux_conds(self, sel, conds):
        """Split Multiplexer Conditions."""
        cases, defaultcase = [], None
        default = sel.type_.default

        for cond, assigns in conds.items():
            condstr = self._resolve(cond)
            is_range = isinstance(cond, u.RangeExpr)
            try:
                is_default = default in cond.range_ if is_range else default == sel.type_.encode(cond)
            except ValueError:
                is_default = False
            if is_default:
                defaultcase = condstr, assigns
            elif is_range:
                cases.append((condstr, assigns))
            else:
                cases.append((condstr, assigns))

        return cases, defaultcase


def _get_comment(comment, level=0, pre="") -> str:
    """Return Systemverilog Comment."""
    if comment:
        comment = comment.split("\n", maxsplit=1)[0]
        fill = "  " * level
        return f"{pre}// {fill}{comment}"
    return ""


def _get_nosepmap(decls: Iterable[tuple[u.Ident, SvDecl | None]]) -> dict[str, str]:
    """Create Auxiliary Structure To Determine Proper Commas."""
    nosepmap: dict[str, str] = {}
    for ident, svdecl in decls:
        if svdecl is not None:
            if not ident.ifdef:
                nosepmap.clear()
            nosepmap[ident.ifdef] = ident.name
    return nosepmap


def _add_ifdef(pre: str, align: Align, act: str | None, ifdef: str | None = None):
    """Add IFDEF/ENDIFs."""
    if ifdef != act:
        if act:
            align.add_spacer(f"{pre}`endif // {act}")
        if ifdef:
            align.add_spacer(f"{pre}`ifdef {ifdef}")
    return ifdef


def _add_declcomment(align: Align, ident: u.Ident | u.Assign, pendlevel, svdecl, pre):
    """Add Struct Declaration Comments ."""
    if svdecl is None:
        name = ident.name
        comment = ident.doc.comment or ""
        if name and comment:
            comment = f"{name}: {comment}"
        else:
            comment = f"{name}{comment}"
        align.add_spacer(_get_comment(comment, pre=pre))
        return 0
    return None


def _get_port_decl(ident: u.Ident, svdecl: SvDecl) -> tuple[str, str, str]:
    dirkeyword = DIRKEYWORDS[ident.direction]
    svdecl0 = svdecl[0].replace("logic", "wire") if ident.direction != u.OUT else svdecl[0]
    return dirkeyword, svdecl0, svdecl[1]


def get_resolver(mod: u.BaseMod, inst: u.BaseMod | None = None) -> SvExprResolver:
    """Get SvExprResolver for `mod`."""
    if inst is not None:
        return SvExprResolver(namespace=mod.namespace, remap=inst.params)
    return SvExprResolver(namespace=mod.namespace)
