from enum import IntEnum, auto
from typing import Dict, List, Tuple
class AssignOp(IntEnum):
    AssignOp_Eq = auto()
    AssignOp_PlusEq = auto()
    AssignOp_MinusEq = auto()
    AssignOp_ShlEq = auto()
    AssignOp_ShrEq = auto()
    AssignOp_OrEq = auto()
    AssignOp_AndEq = auto()
    
class ExecKind(IntEnum):
    ExecKind_Body = auto()
    ExecKind_Header = auto()
    ExecKind_Declaration = auto()
    ExecKind_RunStart = auto()
    ExecKind_RunEnd = auto()
    ExecKind_InitDown = auto()
    ExecKind_InitUp = auto()
    ExecKind_PreSolve = auto()
    ExecKind_PostSolve = auto()
    
class StructKind(IntEnum):
    Buffer = auto()
    Struct = auto()
    Resource = auto()
    Stream = auto()
    State = auto()
    
class SymbolRefPathElemKind(IntEnum):
    ElemKind_ChildIdx = auto()
    ElemKind_ArgIdx = auto()
    ElemKind_Inline = auto()
    ElemKind_ParamIdx = auto()
    ElemKind_Super = auto()
    ElemKind_TypeSpec = auto()
    
class ExprBinOp(IntEnum):
    BinOp_LogOr = auto()
    BinOp_LogAnd = auto()
    BinOp_BitOr = auto()
    BinOp_BitXor = auto()
    BinOp_BitAnd = auto()
    BinOp_Lt = auto()
    BinOp_Le = auto()
    BinOp_Gt = auto()
    BinOp_Ge = auto()
    BinOp_Exp = auto()
    BinOp_Mul = auto()
    BinOp_Div = auto()
    BinOp_Mod = auto()
    BinOp_Add = auto()
    BinOp_Sub = auto()
    BinOp_Shl = auto()
    BinOp_Shr = auto()
    BinOp_Eq = auto()
    BinOp_Ne = auto()
    
class ExprUnaryOp(IntEnum):
    UnaryOp_Plus = auto()
    UnaryOp_Minus = auto()
    UnaryOp_LogNot = auto()
    UnaryOp_BitNeg = auto()
    UnaryOp_BitAnd = auto()
    UnaryOp_BitOr = auto()
    UnaryOp_BitXor = auto()
    
class ExtendTargetE(IntEnum):
    Action = auto()
    Buffer = auto()
    Component = auto()
    Enum = auto()
    Resource = auto()
    State = auto()
    Stream = auto()
    Struct = auto()
    
class TypeCategory(IntEnum):
    Action = auto()
    Component = auto()
    Buffer = auto()
    Resource = auto()
    State = auto()
    Stream = auto()
    Struct = auto()
    
class ParamDir(IntEnum):
    ParamDir_Default = auto()
    ParamDir_In = auto()
    ParamDir_Out = auto()
    ParamDir_InOut = auto()
    
class PlatQual(IntEnum):
    PlatQual_None = auto()
    PlatQual_Target = auto()
    PlatQual_Solve = auto()
    
class FunctionParamDeclKind(IntEnum):
    ParamKind_DataType = auto()
    ParamKind_Type = auto()
    ParamKind_RefAction = auto()
    ParamKind_RefComponent = auto()
    ParamKind_RefBuffer = auto()
    ParamKind_RefResource = auto()
    ParamKind_RefState = auto()
    ParamKind_RefStream = auto()
    ParamKind_RefStruct = auto()
    ParamKind_Struct = auto()
    
class FieldAttr(IntEnum):
    Action = auto()
    Builtin = auto()
    Rand = auto()
    Const = auto()
    Static = auto()
    Private = auto()
    Protected = auto()
    
class Factory(object):
    def mkExecTargetTemplateParam(self,
        expr : Expr,
        start : int,
        end : int) -> 'ExecTargetTemplateParam': ...
    def mkSymbolImportSpec(self) -> 'SymbolImportSpec': ...
    def mkActivitySelectBranch(self,
        guard : Expr,
        weight : Expr,
        body : ScopeChild) -> 'ActivitySelectBranch': ...
    def mkSymbolRefPath(self) -> 'SymbolRefPath': ...
    def mkActivityMatchChoice(self,
        is_default : bool,
        cond : ExprOpenRangeList,
        body : ScopeChild) -> 'ActivityMatchChoice': ...
    def mkRefExpr(self) -> 'RefExpr': ...
    def mkTemplateParamDeclList(self) -> 'TemplateParamDeclList': ...
    def mkTemplateParamValueList(self) -> 'TemplateParamValueList': ...
    def mkTemplateParamValue(self) -> 'TemplateParamValue': ...
    def mkExpr(self) -> 'Expr': ...
    def mkExprAggrMapElem(self,
        lhs : Expr,
        rhs : Expr) -> 'ExprAggrMapElem': ...
    def mkActivityJoinSpec(self) -> 'ActivityJoinSpec': ...
    def mkExprAggrStructElem(self,
        name : ExprId,
        value : Expr) -> 'ExprAggrStructElem': ...
    def mkAssocData(self) -> 'AssocData': ...
    def mkScopeChild(self) -> 'ScopeChild': ...
    def mkExecStmt(self) -> 'ExecStmt': ...
    def mkExecTargetTemplateBlock(self,
        kind : ExecKind,
        data : str) -> 'ExecTargetTemplateBlock': ...
    def mkExtendEnum(self,
        target : TypeIdentifier) -> 'ExtendEnum': ...
    def mkProceduralStmtIfClause(self,
        cond : Expr,
        body : ScopeChild) -> 'ProceduralStmtIfClause': ...
    def mkTemplateParamDecl(self,
        name : ExprId) -> 'TemplateParamDecl': ...
    def mkTemplateParamTypeValue(self,
        value : DataType) -> 'TemplateParamTypeValue': ...
    def mkTemplateParamExprValue(self,
        value : Expr) -> 'TemplateParamExprValue': ...
    def mkFunctionDefinition(self,
        proto : FunctionPrototype,
        body : ExecScope,
        plat : PlatQual) -> 'FunctionDefinition': ...
    def mkFunctionParamDecl(self,
        kind : FunctionParamDeclKind,
        name : ExprId,
        type : DataType,
        dir : ParamDir,
        dflt : Expr) -> 'FunctionParamDecl': ...
    def mkFunctionImport(self,
        plat : PlatQual,
        lang : str) -> 'FunctionImport': ...
    def mkSymbolChild(self) -> 'SymbolChild': ...
    def mkScope(self) -> 'Scope': ...
    def mkSymbolScopeRef(self,
        name : str) -> 'SymbolScopeRef': ...
    def mkScopeChildRef(self,
        target : ScopeChild) -> 'ScopeChildRef': ...
    def mkNamedScopeChild(self,
        name : ExprId) -> 'NamedScopeChild': ...
    def mkPackageImportStmt(self,
        wildcard : bool,
        alias : ExprId) -> 'PackageImportStmt': ...
    def mkPyImportStmt(self) -> 'PyImportStmt': ...
    def mkPyImportFromStmt(self) -> 'PyImportFromStmt': ...
    def mkConstraintStmt(self) -> 'ConstraintStmt': ...
    def mkExprAggrLiteral(self) -> 'ExprAggrLiteral': ...
    def mkExprBin(self,
        lhs : Expr,
        op : ExprBinOp,
        rhs : Expr) -> 'ExprBin': ...
    def mkExprBitSlice(self,
        lhs : Expr,
        rhs : Expr) -> 'ExprBitSlice': ...
    def mkExprBool(self,
        value : bool) -> 'ExprBool': ...
    def mkExprCast(self,
        casting_type : DataType,
        expr : Expr) -> 'ExprCast': ...
    def mkExprCompileHas(self,
        ref : ExprRefPathStatic) -> 'ExprCompileHas': ...
    def mkExprCond(self,
        cond_e : Expr,
        true_e : Expr,
        false_e : Expr) -> 'ExprCond': ...
    def mkExprDomainOpenRangeList(self) -> 'ExprDomainOpenRangeList': ...
    def mkExprDomainOpenRangeValue(self,
        single : bool,
        lhs : Expr,
        rhs : Expr) -> 'ExprDomainOpenRangeValue': ...
    def mkExprHierarchicalId(self) -> 'ExprHierarchicalId': ...
    def mkExprId(self,
        id : str,
        is_escaped : bool) -> 'ExprId': ...
    def mkExprIn(self,
        lhs : Expr,
        rhs : ExprOpenRangeList) -> 'ExprIn': ...
    def mkExprListLiteral(self) -> 'ExprListLiteral': ...
    def mkExprStructLiteral(self) -> 'ExprStructLiteral': ...
    def mkExprStructLiteralItem(self,
        id : ExprId,
        value : Expr) -> 'ExprStructLiteralItem': ...
    def mkExprMemberPathElem(self,
        id : ExprId,
        params : MethodParameterList) -> 'ExprMemberPathElem': ...
    def mkExprNull(self) -> 'ExprNull': ...
    def mkExprNumber(self) -> 'ExprNumber': ...
    def mkExprOpenRangeList(self) -> 'ExprOpenRangeList': ...
    def mkExprOpenRangeValue(self,
        lhs : Expr,
        rhs : Expr) -> 'ExprOpenRangeValue': ...
    def mkExprRefPath(self) -> 'ExprRefPath': ...
    def mkExprRefPathElem(self) -> 'ExprRefPathElem': ...
    def mkExprStaticRefPath(self,
        is_global : bool,
        leaf : ExprMemberPathElem) -> 'ExprStaticRefPath': ...
    def mkExprString(self,
        value : str,
        is_raw : bool) -> 'ExprString': ...
    def mkExprSubscript(self,
        expr : Expr,
        subscript : Expr) -> 'ExprSubscript': ...
    def mkExprUnary(self,
        op : ExprUnaryOp,
        rhs : Expr) -> 'ExprUnary': ...
    def mkMethodParameterList(self) -> 'MethodParameterList': ...
    def mkTypeIdentifier(self) -> 'TypeIdentifier': ...
    def mkTypeIdentifierElem(self,
        id : ExprId,
        params : TemplateParamValueList) -> 'TypeIdentifierElem': ...
    def mkDataType(self) -> 'DataType': ...
    def mkRefExprTypeScopeGlobal(self,
        fileid : int) -> 'RefExprTypeScopeGlobal': ...
    def mkRefExprTypeScopeContext(self,
        base : RefExpr,
        offset : int) -> 'RefExprTypeScopeContext': ...
    def mkRefExprScopeIndex(self,
        base : RefExpr,
        offset : int) -> 'RefExprScopeIndex': ...
    def mkActivityStmt(self) -> 'ActivityStmt': ...
    def mkActivitySchedulingConstraint(self,
        is_parallel : bool) -> 'ActivitySchedulingConstraint': ...
    def mkActivityJoinSpecBranch(self) -> 'ActivityJoinSpecBranch': ...
    def mkActivityJoinSpecSelect(self,
        count : Expr) -> 'ActivityJoinSpecSelect': ...
    def mkActivityJoinSpecNone(self) -> 'ActivityJoinSpecNone': ...
    def mkActivityJoinSpecFirst(self,
        count : Expr) -> 'ActivityJoinSpecFirst': ...
    def mkProceduralStmtAssignment(self,
        lhs : Expr,
        op : AssignOp,
        rhs : Expr) -> 'ProceduralStmtAssignment': ...
    def mkProceduralStmtExpr(self,
        expr : Expr) -> 'ProceduralStmtExpr': ...
    def mkProceduralStmtFunctionCall(self,
        prefix : ExprRefPathStaticRooted) -> 'ProceduralStmtFunctionCall': ...
    def mkProceduralStmtReturn(self,
        expr : Expr) -> 'ProceduralStmtReturn': ...
    def mkProceduralStmtBody(self,
        body : ScopeChild) -> 'ProceduralStmtBody': ...
    def mkExtendType(self,
        kind : ExtendTargetE,
        target : TypeIdentifier) -> 'ExtendType': ...
    def mkProceduralStmtIfElse(self) -> 'ProceduralStmtIfElse': ...
    def mkProceduralStmtMatch(self,
        expr : Expr) -> 'ProceduralStmtMatch': ...
    def mkProceduralStmtMatchChoice(self,
        is_default : bool,
        cond : ExprOpenRangeList,
        body : ScopeChild) -> 'ProceduralStmtMatchChoice': ...
    def mkProceduralStmtBreak(self) -> 'ProceduralStmtBreak': ...
    def mkProceduralStmtContinue(self) -> 'ProceduralStmtContinue': ...
    def mkProceduralStmtDataDeclaration(self,
        name : ExprId,
        datatype : DataType,
        init : Expr) -> 'ProceduralStmtDataDeclaration': ...
    def mkProceduralStmtYield(self) -> 'ProceduralStmtYield': ...
    def mkTemplateGenericTypeParamDecl(self,
        name : ExprId,
        dflt : DataType) -> 'TemplateGenericTypeParamDecl': ...
    def mkField(self,
        name : ExprId,
        type : DataType,
        attr : FieldAttr,
        init : Expr) -> 'Field': ...
    def mkFieldCompRef(self,
        name : ExprId,
        type : DataTypeUserDefined) -> 'FieldCompRef': ...
    def mkFieldRef(self,
        name : ExprId,
        type : DataTypeUserDefined,
        is_input : bool) -> 'FieldRef': ...
    def mkFieldClaim(self,
        name : ExprId,
        type : DataTypeUserDefined,
        is_lock : bool) -> 'FieldClaim': ...
    def mkFunctionPrototype(self,
        name : ExprId,
        rtype : DataType,
        is_target : bool,
        is_solve : bool) -> 'FunctionPrototype': ...
    def mkFunctionImportType(self,
        plat : PlatQual,
        lang : str,
        type : TypeIdentifier) -> 'FunctionImportType': ...
    def mkFunctionImportProto(self,
        plat : PlatQual,
        lang : str,
        proto : FunctionPrototype) -> 'FunctionImportProto': ...
    def mkSymbolChildrenScope(self,
        name : str) -> 'SymbolChildrenScope': ...
    def mkGlobalScope(self,
        fileid : int) -> 'GlobalScope': ...
    def mkNamedScope(self,
        name : ExprId) -> 'NamedScope': ...
    def mkPackageScope(self) -> 'PackageScope': ...
    def mkConstraintScope(self) -> 'ConstraintScope': ...
    def mkConstraintStmtExpr(self,
        expr : Expr) -> 'ConstraintStmtExpr': ...
    def mkConstraintStmtField(self,
        name : ExprId,
        type : DataType) -> 'ConstraintStmtField': ...
    def mkConstraintStmtIf(self,
        cond : Expr,
        true_c : ConstraintScope,
        false_c : ConstraintScope) -> 'ConstraintStmtIf': ...
    def mkConstraintStmtUnique(self) -> 'ConstraintStmtUnique': ...
    def mkConstraintStmtDefault(self,
        hid : ExprHierarchicalId,
        expr : Expr) -> 'ConstraintStmtDefault': ...
    def mkConstraintStmtDefaultDisable(self,
        hid : ExprHierarchicalId) -> 'ConstraintStmtDefaultDisable': ...
    def mkExprAggrEmpty(self) -> 'ExprAggrEmpty': ...
    def mkExprAggrList(self) -> 'ExprAggrList': ...
    def mkExprAggrMap(self) -> 'ExprAggrMap': ...
    def mkExprAggrStruct(self) -> 'ExprAggrStruct': ...
    def mkExprRefPathId(self,
        id : ExprId) -> 'ExprRefPathId': ...
    def mkExprRefPathContext(self,
        hier_id : ExprHierarchicalId) -> 'ExprRefPathContext': ...
    def mkExprRefPathStatic(self,
        is_global : bool) -> 'ExprRefPathStatic': ...
    def mkTemplateCategoryTypeParamDecl(self,
        name : ExprId,
        category : TypeCategory,
        restriction : TypeIdentifier,
        dflt : DataType) -> 'TemplateCategoryTypeParamDecl': ...
    def mkExprRefPathStaticRooted(self,
        root : ExprRefPathStatic,
        leaf : ExprHierarchicalId) -> 'ExprRefPathStaticRooted': ...
    def mkExprSignedNumber(self,
        image : str,
        width : int,
        value : int) -> 'ExprSignedNumber': ...
    def mkTemplateValueParamDecl(self,
        name : ExprId,
        type : DataType,
        dflt : Expr) -> 'TemplateValueParamDecl': ...
    def mkExprUnsignedNumber(self,
        image : str,
        width : int,
        value : int) -> 'ExprUnsignedNumber': ...
    def mkDataTypeBool(self) -> 'DataTypeBool': ...
    def mkDataTypeChandle(self) -> 'DataTypeChandle': ...
    def mkDataTypeEnum(self,
        tid : DataTypeUserDefined,
        in_rangelist : ExprOpenRangeList) -> 'DataTypeEnum': ...
    def mkEnumItem(self,
        name : ExprId,
        value : Expr) -> 'EnumItem': ...
    def mkEnumDecl(self,
        name : ExprId) -> 'EnumDecl': ...
    def mkDataTypeInt(self,
        is_signed : bool,
        width : Expr,
        in_range : ExprDomainOpenRangeList) -> 'DataTypeInt': ...
    def mkDataTypePyObj(self) -> 'DataTypePyObj': ...
    def mkDataTypeRef(self,
        type : DataTypeUserDefined) -> 'DataTypeRef': ...
    def mkDataTypeString(self,
        has_range : bool) -> 'DataTypeString': ...
    def mkDataTypeUserDefined(self,
        is_global : bool,
        type_id : TypeIdentifier) -> 'DataTypeUserDefined': ...
    def mkActivityBindStmt(self,
        lhs : ExprHierarchicalId) -> 'ActivityBindStmt': ...
    def mkActivityConstraint(self,
        constraint : ConstraintStmt) -> 'ActivityConstraint': ...
    def mkActivityLabeledStmt(self) -> 'ActivityLabeledStmt': ...
    def mkActivityRepeatCount(self,
        loop_var : ExprId,
        count : Expr,
        body : ScopeChild) -> 'ActivityRepeatCount': ...
    def mkActivityRepeatWhile(self,
        cond : Expr,
        body : ScopeChild) -> 'ActivityRepeatWhile': ...
    def mkActivityForeach(self,
        it_id : ExprId,
        idx_id : ExprId,
        target : ExprRefPathContext,
        body : ScopeChild) -> 'ActivityForeach': ...
    def mkActivitySelect(self) -> 'ActivitySelect': ...
    def mkActivityIfElse(self,
        cond : Expr,
        true_s : ActivityStmt,
        false_s : ActivityStmt) -> 'ActivityIfElse': ...
    def mkActivityMatch(self,
        cond : Expr) -> 'ActivityMatch': ...
    def mkActivityReplicate(self,
        idx_id : ExprId,
        it_label : ExprId,
        body : ScopeChild) -> 'ActivityReplicate': ...
    def mkActivitySuper(self) -> 'ActivitySuper': ...
    def mkProceduralStmtRepeatWhile(self,
        body : ScopeChild,
        expr : Expr) -> 'ProceduralStmtRepeatWhile': ...
    def mkProceduralStmtWhile(self,
        body : ScopeChild,
        expr : Expr) -> 'ProceduralStmtWhile': ...
    def mkTypeScope(self,
        name : ExprId,
        super_t : TypeIdentifier) -> 'TypeScope': ...
    def mkSymbolScope(self,
        name : str) -> 'SymbolScope': ...
    def mkConstraintBlock(self,
        name : str,
        is_dynamic : bool) -> 'ConstraintBlock': ...
    def mkConstraintStmtForeach(self,
        expr : Expr) -> 'ConstraintStmtForeach': ...
    def mkConstraintStmtForall(self,
        iterator_id : ExprId,
        type_id : DataTypeUserDefined,
        ref_path : ExprRefPath) -> 'ConstraintStmtForall': ...
    def mkConstraintStmtImplication(self,
        cond : Expr) -> 'ConstraintStmtImplication': ...
    def mkExprRefPathStaticFunc(self,
        is_global : bool,
        params : MethodParameterList) -> 'ExprRefPathStaticFunc': ...
    def mkExprRefPathSuper(self,
        hier_id : ExprHierarchicalId) -> 'ExprRefPathSuper': ...
    def mkActivityActionHandleTraversal(self,
        target : ExprRefPathContext,
        with_c : ConstraintStmt) -> 'ActivityActionHandleTraversal': ...
    def mkActivityActionTypeTraversal(self,
        target : DataTypeUserDefined,
        with_c : ConstraintStmt) -> 'ActivityActionTypeTraversal': ...
    def mkExecScope(self,
        name : str) -> 'ExecScope': ...
    def mkSymbolEnumScope(self,
        name : str) -> 'SymbolEnumScope': ...
    def mkRootSymbolScope(self,
        name : str) -> 'RootSymbolScope': ...
    def mkSymbolExtendScope(self,
        name : str) -> 'SymbolExtendScope': ...
    def mkSymbolTypeScope(self,
        name : str,
        plist : SymbolScope) -> 'SymbolTypeScope': ...
    def mkSymbolFunctionScope(self,
        name : str) -> 'SymbolFunctionScope': ...
    def mkAction(self,
        name : ExprId,
        super_t : TypeIdentifier,
        is_abstract : bool) -> 'Action': ...
    def mkComponent(self,
        name : ExprId,
        super_t : TypeIdentifier) -> 'Component': ...
    def mkConstraintSymbolScope(self,
        name : str) -> 'ConstraintSymbolScope': ...
    def mkActivityDecl(self,
        name : str) -> 'ActivityDecl': ...
    def mkProceduralStmtSymbolBodyScope(self,
        name : str,
        body : ScopeChild) -> 'ProceduralStmtSymbolBodyScope': ...
    def mkActivityLabeledScope(self,
        name : str) -> 'ActivityLabeledScope': ...
    def mkStruct(self,
        name : ExprId,
        super_t : TypeIdentifier,
        kind : StructKind) -> 'Struct': ...
    def mkActivitySchedule(self,
        name : str,
        join_spec : ActivityJoinSpec) -> 'ActivitySchedule': ...
    def mkExecBlock(self,
        name : str,
        kind : ExecKind) -> 'ExecBlock': ...
    def mkProceduralStmtRepeat(self,
        name : str,
        body : ScopeChild,
        it_id : ExprId,
        count : Expr) -> 'ProceduralStmtRepeat': ...
    def mkProceduralStmtForeach(self,
        name : str,
        body : ScopeChild,
        path : ExprRefPath,
        it_id : ExprId,
        idx_id : ExprId) -> 'ProceduralStmtForeach': ...
    def mkActivitySequence(self,
        name : str) -> 'ActivitySequence': ...
    def mkActivityParallel(self,
        name : str,
        join_spec : ActivityJoinSpec) -> 'ActivityParallel': ...
    @staticmethod
    def inst() -> 'Factory': ...
    
class ExecTargetTemplateParam(object):
    pass
    
    def getExpr(self) -> Expr: ...
    
class SymbolImportSpec(object):
    pass
    
    def imports(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getImports(self) -> List[PackageImportStmt]: ...
    
class ActivitySelectBranch(object):
    pass
    
    def getGuard(self) -> Expr: ...
    
    def getWeight(self) -> Expr: ...
    
    def getBody(self) -> ScopeChild: ...
    
class SymbolRefPath(object):
    pass
    
    def path(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getPath(self) -> List[SymbolRefPathElem]: ...
    
class ActivityMatchChoice(object):
    pass
    
    def getCond(self) -> ExprOpenRangeList: ...
    
    def getBody(self) -> ScopeChild: ...
    
class RefExpr(object):
    pass
    
class TemplateParamDeclList(object):
    pass
    
    def params(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getParams(self) -> List[TemplateParamDecl]: ...
    
class TemplateParamValueList(object):
    pass
    
    def values(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getValues(self) -> List[TemplateParamValue]: ...
    
class TemplateParamValue(object):
    pass
    
class Expr(object):
    pass
    
class ExprAggrMapElem(object):
    pass
    
    def getLhs(self) -> Expr: ...
    
    def getRhs(self) -> Expr: ...
    
class ActivityJoinSpec(object):
    pass
    
class ExprAggrStructElem(object):
    pass
    
    def getName(self) -> ExprId: ...
    
    def getValue(self) -> Expr: ...
    
class AssocData(object):
    pass
    
class ScopeChild(object):
    pass
    
    def getDocstring(self) -> str: ...
    
    def setDocstring(self, v : str): ...
    
    def getParent(self) -> Scope: ...
    
    def getAssocData(self) -> AssocData: ...
    
class ExecStmt(ScopeChild):
    pass
    
    def getUpper(self) -> SymbolScope: ...
    
class ExecTargetTemplateBlock(ScopeChild):
    pass
    
    def setKind(self, v : ExecKind): ...
    
    def getData(self) -> str: ...
    
    def setData(self, v : str): ...
    
    def parameters(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getParameters(self) -> List[ExecTargetTemplateParam]: ...
    
class ExtendEnum(ScopeChild):
    pass
    
    def getTarget(self) -> TypeIdentifier: ...
    
    def items(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getItems(self) -> List[EnumItem]: ...
    
class ProceduralStmtIfClause(ScopeChild):
    pass
    
    def getCond(self) -> Expr: ...
    
    def getBody(self) -> ScopeChild: ...
    
class TemplateParamDecl(ScopeChild):
    pass
    
    def getName(self) -> ExprId: ...
    
class TemplateParamTypeValue(TemplateParamValue):
    pass
    
    def getValue(self) -> DataType: ...
    
class TemplateParamExprValue(TemplateParamValue):
    pass
    
    def getValue(self) -> Expr: ...
    
class FunctionDefinition(ScopeChild):
    pass
    
    def getProto(self) -> FunctionPrototype: ...
    
    def getBody(self) -> ExecScope: ...
    
    def setPlat(self, v : PlatQual): ...
    
class FunctionParamDecl(ScopeChild):
    pass
    
    def setKind(self, v : FunctionParamDeclKind): ...
    
    def getName(self) -> ExprId: ...
    
    def getType(self) -> DataType: ...
    
    def setDir(self, v : ParamDir): ...
    
    def getDflt(self) -> Expr: ...
    
class FunctionImport(ScopeChild):
    pass
    
    def setPlat(self, v : PlatQual): ...
    
    def getLang(self) -> str: ...
    
    def setLang(self, v : str): ...
    
class SymbolChild(ScopeChild):
    pass
    
    def getUpper(self) -> SymbolScope: ...
    
class Scope(ScopeChild):
    pass
    
    def children(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getChildren(self) -> List[ScopeChild]: ...
    
class SymbolScopeRef(ScopeChild):
    pass
    
    def getName(self) -> str: ...
    
    def setName(self, v : str): ...
    
class ScopeChildRef(ScopeChild):
    pass
    
    def getTarget(self) -> ScopeChild: ...
    
class NamedScopeChild(ScopeChild):
    pass
    
    def getName(self) -> ExprId: ...
    
class PackageImportStmt(ScopeChild):
    pass
    
    def getAlias(self) -> ExprId: ...
    
    def getPath(self) -> TypeIdentifier: ...
    
class PyImportStmt(ScopeChild):
    pass
    
    def path(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getPath(self) -> List[ExprId]: ...
    
    def getAlias(self) -> ExprId: ...
    
class PyImportFromStmt(ScopeChild):
    pass
    
    def path(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getPath(self) -> List[ExprId]: ...
    
    def targets(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getTargets(self) -> List[ExprId]: ...
    
class ConstraintStmt(ScopeChild):
    pass
    
class ExprAggrLiteral(Expr):
    pass
    
class ExprBin(Expr):
    pass
    
    def getLhs(self) -> Expr: ...
    
    def setOp(self, v : ExprBinOp): ...
    
    def getRhs(self) -> Expr: ...
    
class ExprBitSlice(Expr):
    pass
    
    def getLhs(self) -> Expr: ...
    
    def getRhs(self) -> Expr: ...
    
class ExprBool(Expr):
    pass
    
class ExprCast(Expr):
    pass
    
    def getCasting_type(self) -> DataType: ...
    
    def getExpr(self) -> Expr: ...
    
class ExprCompileHas(Expr):
    pass
    
    def getRef(self) -> ExprRefPathStatic: ...
    
class ExprCond(Expr):
    pass
    
    def getCond_e(self) -> Expr: ...
    
    def getTrue_e(self) -> Expr: ...
    
    def getFalse_e(self) -> Expr: ...
    
class ExprDomainOpenRangeList(Expr):
    pass
    
    def values(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getValues(self) -> List[ExprDomainOpenRangeValue]: ...
    
class ExprDomainOpenRangeValue(Expr):
    pass
    
    def getLhs(self) -> Expr: ...
    
    def getRhs(self) -> Expr: ...
    
class ExprHierarchicalId(Expr):
    pass
    
    def elems(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getElems(self) -> List[ExprMemberPathElem]: ...
    
class ExprId(Expr):
    pass
    
    def getId(self) -> str: ...
    
    def setId(self, v : str): ...
    
class ExprIn(Expr):
    pass
    
    def getLhs(self) -> Expr: ...
    
    def getRhs(self) -> ExprOpenRangeList: ...
    
class ExprListLiteral(Expr):
    pass
    
    def value(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getValue(self) -> List[Expr]: ...
    
class ExprStructLiteral(Expr):
    pass
    
    def values(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getValues(self) -> List[ExprStructLiteralItem]: ...
    
class ExprStructLiteralItem(Expr):
    pass
    
    def getId(self) -> ExprId: ...
    
    def getValue(self) -> Expr: ...
    
class ExprMemberPathElem(Expr):
    pass
    
    def getId(self) -> ExprId: ...
    
    def getParams(self) -> MethodParameterList: ...
    
    def subscript(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getSubscript(self) -> List[Expr]: ...
    
class ExprNull(Expr):
    pass
    
class ExprNumber(Expr):
    pass
    
class ExprOpenRangeList(Expr):
    pass
    
    def values(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getValues(self) -> List[ExprOpenRangeValue]: ...
    
class ExprOpenRangeValue(Expr):
    pass
    
    def getLhs(self) -> Expr: ...
    
    def getRhs(self) -> Expr: ...
    
class ExprRefPath(Expr):
    pass
    
    def getTarget(self) -> SymbolRefPath: ...
    
class ExprRefPathElem(Expr):
    pass
    
class ExprStaticRefPath(Expr):
    pass
    
    def base(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getBase(self) -> List[TypeIdentifierElem]: ...
    
    def getLeaf(self) -> ExprMemberPathElem: ...
    
class ExprString(Expr):
    pass
    
    def getValue(self) -> str: ...
    
    def setValue(self, v : str): ...
    
class ExprSubscript(Expr):
    pass
    
    def getExpr(self) -> Expr: ...
    
    def getSubscript(self) -> Expr: ...
    
class ExprUnary(Expr):
    pass
    
    def setOp(self, v : ExprUnaryOp): ...
    
    def getRhs(self) -> Expr: ...
    
class MethodParameterList(Expr):
    pass
    
    def parameters(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getParameters(self) -> List[Expr]: ...
    
class TypeIdentifier(Expr):
    pass
    
    def elems(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getElems(self) -> List[TypeIdentifierElem]: ...
    
    def getTarget(self) -> SymbolRefPath: ...
    
class TypeIdentifierElem(Expr):
    pass
    
    def getId(self) -> ExprId: ...
    
    def getParams(self) -> TemplateParamValueList: ...
    
class DataType(ScopeChild):
    pass
    
class RefExprTypeScopeGlobal(RefExpr):
    pass
    
class RefExprTypeScopeContext(RefExpr):
    pass
    
    def getBase(self) -> RefExpr: ...
    
class RefExprScopeIndex(RefExpr):
    pass
    
    def getBase(self) -> RefExpr: ...
    
class ActivityStmt(ScopeChild):
    pass
    
class ActivitySchedulingConstraint(ScopeChild):
    pass
    
    def targets(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getTargets(self) -> List[ExprHierarchicalId]: ...
    
class ActivityJoinSpecBranch(ActivityJoinSpec):
    pass
    
    def branches(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getBranches(self) -> List[ExprRefPathContext]: ...
    
class ActivityJoinSpecSelect(ActivityJoinSpec):
    pass
    
    def getCount(self) -> Expr: ...
    
class ActivityJoinSpecNone(ActivityJoinSpec):
    pass
    
class ActivityJoinSpecFirst(ActivityJoinSpec):
    pass
    
    def getCount(self) -> Expr: ...
    
class ProceduralStmtAssignment(ExecStmt):
    pass
    
    def getLhs(self) -> Expr: ...
    
    def setOp(self, v : AssignOp): ...
    
    def getRhs(self) -> Expr: ...
    
class ProceduralStmtExpr(ExecStmt):
    pass
    
    def getExpr(self) -> Expr: ...
    
class ProceduralStmtFunctionCall(ExecStmt):
    pass
    
    def getPrefix(self) -> ExprRefPathStaticRooted: ...
    
    def params(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getParams(self) -> List[Expr]: ...
    
class ProceduralStmtReturn(ExecStmt):
    pass
    
    def getExpr(self) -> Expr: ...
    
class ProceduralStmtBody(ExecStmt):
    pass
    
    def getBody(self) -> ScopeChild: ...
    
class ExtendType(Scope):
    """
    Maps between local item identifier and item child index
    
    """
    pass
    
    def setKind(self, v : ExtendTargetE): ...
    
    def getTarget(self) -> TypeIdentifier: ...
    
    def getImports(self) -> SymbolImportSpec: ...
    
class ProceduralStmtIfElse(ExecStmt):
    pass
    
    def if_then(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getIf_then(self) -> List[ProceduralStmtIfClause]: ...
    
    def getElse_then(self) -> ScopeChild: ...
    
class ProceduralStmtMatch(ExecStmt):
    pass
    
    def getExpr(self) -> Expr: ...
    
    def choices(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getChoices(self) -> List[ProceduralStmtMatchChoice]: ...
    
class ProceduralStmtMatchChoice(ExecStmt):
    pass
    
    def getCond(self) -> ExprOpenRangeList: ...
    
    def getBody(self) -> ScopeChild: ...
    
class ProceduralStmtBreak(ExecStmt):
    pass
    
class ProceduralStmtContinue(ExecStmt):
    pass
    
class ProceduralStmtDataDeclaration(ExecStmt):
    pass
    
    def getName(self) -> ExprId: ...
    
    def getDatatype(self) -> DataType: ...
    
    def getInit(self) -> Expr: ...
    
class ProceduralStmtYield(ExecStmt):
    pass
    
class TemplateGenericTypeParamDecl(TemplateParamDecl):
    pass
    
    def getDflt(self) -> DataType: ...
    
class Field(NamedScopeChild):
    pass
    
    def getType(self) -> DataType: ...
    
    def setAttr(self, v : FieldAttr): ...
    
    def getInit(self) -> Expr: ...
    
class FieldCompRef(NamedScopeChild):
    pass
    
    def getType(self) -> DataTypeUserDefined: ...
    
class FieldRef(NamedScopeChild):
    pass
    
    def getType(self) -> DataTypeUserDefined: ...
    
class FieldClaim(NamedScopeChild):
    pass
    
    def getType(self) -> DataTypeUserDefined: ...
    
class FunctionPrototype(NamedScopeChild):
    pass
    
    def getRtype(self) -> DataType: ...
    
    def parameters(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getParameters(self) -> List[FunctionParamDecl]: ...
    
class FunctionImportType(FunctionImport):
    pass
    
    def getType(self) -> TypeIdentifier: ...
    
class FunctionImportProto(FunctionImport):
    pass
    
    def getProto(self) -> FunctionPrototype: ...
    
class SymbolChildrenScope(SymbolChild):
    pass
    
    def getName(self) -> str: ...
    
    def setName(self, v : str): ...
    
    def children(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getChildren(self) -> List[ScopeChild]: ...
    
    def getTarget(self) -> ScopeChild: ...
    
class GlobalScope(Scope):
    pass
    
    def getFilename(self) -> str: ...
    
    def setFilename(self, v : str): ...
    
class NamedScope(Scope):
    pass
    
    def getName(self) -> ExprId: ...
    
class PackageScope(Scope):
    pass
    
    def id(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getId(self) -> List[ExprId]: ...
    
    def getSibling(self) -> PackageScope: ...
    
class ConstraintScope(ConstraintStmt):
    pass
    
    def constraints(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getConstraints(self) -> List[ConstraintStmt]: ...
    
class ConstraintStmtExpr(ConstraintStmt):
    pass
    
    def getExpr(self) -> Expr: ...
    
class ConstraintStmtField(ConstraintStmt):
    pass
    
    def getName(self) -> ExprId: ...
    
    def getType(self) -> DataType: ...
    
class ConstraintStmtIf(ConstraintStmt):
    pass
    
    def getCond(self) -> Expr: ...
    
    def getTrue_c(self) -> ConstraintScope: ...
    
    def getFalse_c(self) -> ConstraintScope: ...
    
class ConstraintStmtUnique(ConstraintStmt):
    pass
    
    def list(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getList(self) -> List[ExprHierarchicalId]: ...
    
class ConstraintStmtDefault(ConstraintStmt):
    pass
    
    def getHid(self) -> ExprHierarchicalId: ...
    
    def getExpr(self) -> Expr: ...
    
class ConstraintStmtDefaultDisable(ConstraintStmt):
    pass
    
    def getHid(self) -> ExprHierarchicalId: ...
    
class ExprAggrEmpty(ExprAggrLiteral):
    pass
    
class ExprAggrList(ExprAggrLiteral):
    pass
    
    def elems(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getElems(self) -> List[Expr]: ...
    
class ExprAggrMap(ExprAggrLiteral):
    pass
    
    def elems(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getElems(self) -> List[ExprAggrMapElem]: ...
    
class ExprAggrStruct(ExprAggrLiteral):
    pass
    
    def elems(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getElems(self) -> List[ExprAggrStructElem]: ...
    
class ExprRefPathId(ExprRefPath):
    pass
    
    def getId(self) -> ExprId: ...
    
    def getSlice(self) -> ExprBitSlice: ...
    
class ExprRefPathContext(ExprRefPath):
    pass
    
    def getHier_id(self) -> ExprHierarchicalId: ...
    
    def getSlice(self) -> ExprBitSlice: ...
    
class ExprRefPathStatic(ExprRefPath):
    pass
    
    def base(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getBase(self) -> List[TypeIdentifierElem]: ...
    
    def getSlice(self) -> ExprBitSlice: ...
    
class TemplateCategoryTypeParamDecl(TemplateParamDecl):
    pass
    
    def setCategory(self, v : TypeCategory): ...
    
    def getRestriction(self) -> TypeIdentifier: ...
    
    def getDflt(self) -> DataType: ...
    
class ExprRefPathStaticRooted(ExprRefPath):
    pass
    
    def getRoot(self) -> ExprRefPathStatic: ...
    
    def getLeaf(self) -> ExprHierarchicalId: ...
    
    def getSlice(self) -> ExprBitSlice: ...
    
class ExprSignedNumber(ExprNumber):
    pass
    
    def getImage(self) -> str: ...
    
    def setImage(self, v : str): ...
    
class TemplateValueParamDecl(TemplateParamDecl):
    pass
    
    def getType(self) -> DataType: ...
    
    def getDflt(self) -> Expr: ...
    
class ExprUnsignedNumber(ExprNumber):
    pass
    
    def getImage(self) -> str: ...
    
    def setImage(self, v : str): ...
    
class DataTypeBool(DataType):
    pass
    
class DataTypeChandle(DataType):
    pass
    
class DataTypeEnum(DataType):
    pass
    
    def getTid(self) -> DataTypeUserDefined: ...
    
    def getIn_rangelist(self) -> ExprOpenRangeList: ...
    
class EnumItem(NamedScopeChild):
    pass
    
    def getValue(self) -> Expr: ...
    
class EnumDecl(NamedScopeChild):
    pass
    
    def items(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getItems(self) -> List[EnumItem]: ...
    
class DataTypeInt(DataType):
    pass
    
    def getWidth(self) -> Expr: ...
    
    def getIn_range(self) -> ExprDomainOpenRangeList: ...
    
class DataTypePyObj(DataType):
    pass
    
class DataTypeRef(DataType):
    pass
    
    def getType(self) -> DataTypeUserDefined: ...
    
class DataTypeString(DataType):
    pass
    
    def in_range(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getIn_range(self) -> List[str]: ...
    
class DataTypeUserDefined(DataType):
    pass
    
    def getType_id(self) -> TypeIdentifier: ...
    
class ActivityBindStmt(ActivityStmt):
    pass
    
    def getLhs(self) -> ExprHierarchicalId: ...
    
    def rhs(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getRhs(self) -> List[ExprHierarchicalId]: ...
    
class ActivityConstraint(ActivityStmt):
    pass
    
    def getConstraint(self) -> ConstraintStmt: ...
    
class ActivityLabeledStmt(ActivityStmt):
    pass
    
    def getLabel(self) -> ExprId: ...
    
class ActivityRepeatCount(ActivityLabeledStmt):
    pass
    
    def getLoop_var(self) -> ExprId: ...
    
    def getCount(self) -> Expr: ...
    
    def getBody(self) -> ScopeChild: ...
    
class ActivityRepeatWhile(ActivityLabeledStmt):
    pass
    
    def getCond(self) -> Expr: ...
    
    def getBody(self) -> ScopeChild: ...
    
class ActivityForeach(ActivityLabeledStmt):
    pass
    
    def getIt_id(self) -> ExprId: ...
    
    def getIdx_id(self) -> ExprId: ...
    
    def getTarget(self) -> ExprRefPathContext: ...
    
    def getBody(self) -> ScopeChild: ...
    
class ActivitySelect(ActivityLabeledStmt):
    pass
    
    def branches(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getBranches(self) -> List[ActivitySelectBranch]: ...
    
class ActivityIfElse(ActivityLabeledStmt):
    pass
    
    def getCond(self) -> Expr: ...
    
    def getTrue_s(self) -> ActivityStmt: ...
    
    def getFalse_s(self) -> ActivityStmt: ...
    
class ActivityMatch(ActivityLabeledStmt):
    pass
    
    def getCond(self) -> Expr: ...
    
    def choices(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getChoices(self) -> List[ActivityMatchChoice]: ...
    
class ActivityReplicate(ActivityLabeledStmt):
    pass
    
    def getIdx_id(self) -> ExprId: ...
    
    def getIt_label(self) -> ExprId: ...
    
    def getBody(self) -> ScopeChild: ...
    
class ActivitySuper(ActivityLabeledStmt):
    pass
    
class ProceduralStmtRepeatWhile(ProceduralStmtBody):
    pass
    
    def getExpr(self) -> Expr: ...
    
class ProceduralStmtWhile(ProceduralStmtBody):
    pass
    
    def getExpr(self) -> Expr: ...
    
class TypeScope(NamedScope):
    pass
    
    def getSuper_t(self) -> TypeIdentifier: ...
    
    def getParams(self) -> TemplateParamDeclList: ...
    
class SymbolScope(SymbolChildrenScope):
    """
    Maps between local item identifier and item child index
    
    """
    pass
    
    def getImports(self) -> SymbolImportSpec: ...
    
class ConstraintBlock(ConstraintScope):
    pass
    
    def getName(self) -> str: ...
    
    def setName(self, v : str): ...
    
class ConstraintStmtForeach(ConstraintScope):
    pass
    
    def getIt(self) -> ConstraintStmtField: ...
    
    def getIdx(self) -> ConstraintStmtField: ...
    
    def getExpr(self) -> Expr: ...
    
    def getSymtab(self) -> ConstraintSymbolScope: ...
    
class ConstraintStmtForall(ConstraintScope):
    pass
    
    def getIterator_id(self) -> ExprId: ...
    
    def getType_id(self) -> DataTypeUserDefined: ...
    
    def getRef_path(self) -> ExprRefPath: ...
    
    def getSymtab(self) -> ConstraintSymbolScope: ...
    
class ConstraintStmtImplication(ConstraintScope):
    pass
    
    def getCond(self) -> Expr: ...
    
class ExprRefPathStaticFunc(ExprRefPathStatic):
    pass
    
    def getParams(self) -> MethodParameterList: ...
    
class ExprRefPathSuper(ExprRefPathContext):
    pass
    
class ActivityActionHandleTraversal(ActivityLabeledStmt):
    pass
    
    def getTarget(self) -> ExprRefPathContext: ...
    
    def getWith_c(self) -> ConstraintStmt: ...
    
class ActivityActionTypeTraversal(ActivityLabeledStmt):
    pass
    
    def getTarget(self) -> DataTypeUserDefined: ...
    
    def getWith_c(self) -> ConstraintStmt: ...
    
class ExecScope(SymbolScope):
    pass
    
class SymbolEnumScope(SymbolScope):
    pass
    
class RootSymbolScope(SymbolScope):
    """
    List of inbound refs to each unit
    
    """
    pass
    
    def units(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getUnits(self) -> List[GlobalScope]: ...
    
    def fileoutref(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getFileOutRef(self) -> List[List[int]]: ...
    
    def fileinref(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getFileInRef(self) -> List[List[int]]: ...
    
class SymbolExtendScope(SymbolScope):
    pass
    
class SymbolTypeScope(SymbolScope):
    pass
    
    def getPlist(self) -> SymbolScope: ...
    
    def spec_types(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getSpec_types(self) -> List[SymbolTypeScope]: ...
    
class SymbolFunctionScope(SymbolScope):
    pass
    
    def prototypes(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getPrototypes(self) -> List[FunctionPrototype]: ...
    
    def import_specs(self) -> ListUtil...
        """Returns an iterator over the items"""
    
    def getImport_specs(self) -> List[FunctionImport]: ...
    
    def getDefinition(self) -> FunctionDefinition: ...
    
    def getPlist(self) -> SymbolScope: ...
    
    def getBody(self) -> ExecScope: ...
    
class Action(TypeScope):
    pass
    
class Component(TypeScope):
    pass
    
class ConstraintSymbolScope(SymbolScope):
    pass
    
    def getConstraint(self) -> ConstraintStmt: ...
    
class ActivityDecl(SymbolScope):
    pass
    
class ProceduralStmtSymbolBodyScope(SymbolScope):
    pass
    
    def getBody(self) -> ScopeChild: ...
    
class ActivityLabeledScope(SymbolScope):
    pass
    
    def getLabel(self) -> ExprId: ...
    
class Struct(TypeScope):
    pass
    
    def setKind(self, v : StructKind): ...
    
class ActivitySchedule(ActivityLabeledScope):
    pass
    
    def getJoin_spec(self) -> ActivityJoinSpec: ...
    
class ExecBlock(ExecScope):
    pass
    
    def setKind(self, v : ExecKind): ...
    
class ProceduralStmtRepeat(ProceduralStmtSymbolBodyScope):
    pass
    
    def getIt_id(self) -> ExprId: ...
    
    def getCount(self) -> Expr: ...
    
class ProceduralStmtForeach(ProceduralStmtSymbolBodyScope):
    pass
    
    def getPath(self) -> ExprRefPath: ...
    
    def getIt_id(self) -> ExprId: ...
    
    def getIdx_id(self) -> ExprId: ...
    
class ActivitySequence(ActivityLabeledScope):
    pass
    
class ActivityParallel(ActivityLabeledScope):
    pass
    
    def getJoin_spec(self) -> ActivityJoinSpec: ...
    
