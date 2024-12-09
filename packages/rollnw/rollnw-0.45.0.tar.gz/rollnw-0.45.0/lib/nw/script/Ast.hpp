#pragma once

#include "../kernel/Memory.hpp"
#include "../objects//ObjectBase.hpp"
#include "../objects/Location.hpp"
#include "../util/Variant.hpp"
#include "../util/string.hpp"
#include "Context.hpp"
#include "Token.hpp"

#include <fmt/format.h>
#include <glm/glm.hpp>
#include <immer/map.hpp>

#include <limits>
#include <memory>
#include <unordered_map>

namespace nw::script {

struct Nss;
struct Ast;
struct Context;
struct Export;

struct Declaration;
struct FunctionDecl;
struct FunctionDefinition;
struct StructDecl;
struct VarDecl;

struct AssignExpression;
struct BinaryExpression;
struct CallExpression;
struct ComparisonExpression;
struct ConditionalExpression;
struct DotExpression;
struct EmptyExpression;
struct GroupingExpression;
struct LiteralExpression;
struct LiteralVectorExpression;
struct LogicalExpression;
struct PostfixExpression;
struct UnaryExpression;
struct VariableExpression;

struct BlockStatement;
struct DeclList;
struct DoStatement;
struct EmptyStatement;
struct ExprStatement;
struct IfStatement;
struct ForStatement;
struct JumpStatement;
struct LabelStatement;
struct SwitchStatement;
struct WhileStatement;

struct BaseVisitor {
    virtual ~BaseVisitor() = default;

    virtual void visit(Ast* script) = 0;

    // Decls
    virtual void visit(FunctionDecl* decl) = 0;
    virtual void visit(FunctionDefinition* decl) = 0;
    virtual void visit(StructDecl* decl) = 0;
    virtual void visit(VarDecl* decl) = 0;

    // Expressions
    virtual void visit(AssignExpression* expr) = 0;
    virtual void visit(BinaryExpression* expr) = 0;
    virtual void visit(CallExpression* expr) = 0;
    virtual void visit(ComparisonExpression* expr) = 0;
    virtual void visit(ConditionalExpression* expr) = 0;
    virtual void visit(DotExpression* expr) = 0;
    virtual void visit(EmptyExpression* expr) = 0;
    virtual void visit(GroupingExpression* expr) = 0;
    virtual void visit(LiteralExpression* expr) = 0;
    virtual void visit(LiteralVectorExpression* expr) = 0;
    virtual void visit(LogicalExpression* expr) = 0;
    virtual void visit(PostfixExpression* expr) = 0;
    virtual void visit(UnaryExpression* expr) = 0;
    virtual void visit(VariableExpression* expr) = 0;

    // Statements
    virtual void visit(BlockStatement* stmt) = 0;
    virtual void visit(DeclList* stmt) = 0;
    virtual void visit(DoStatement* stmt) = 0;
    virtual void visit(EmptyStatement* stmt) = 0;
    virtual void visit(ExprStatement* stmt) = 0;
    virtual void visit(IfStatement* stmt) = 0;
    virtual void visit(ForStatement* stmt) = 0;
    virtual void visit(JumpStatement* stmt) = 0;
    virtual void visit(LabelStatement* stmt) = 0;
    virtual void visit(SwitchStatement* stmt) = 0;
    virtual void visit(WhileStatement* stmt) = 0;
};

constexpr size_t invalid_type_id = std::numeric_limits<size_t>::max();

struct AstNode {
    virtual ~AstNode() = default;
    virtual void accept(BaseVisitor* visitor) = 0;

    /// Find completions for this Ast Node
    /// @note This function does not traverse dependencies
    virtual void complete(const String& needle, Vector<const Declaration*>& out, bool no_filter = false) const;

    size_t type_id_ = invalid_type_id;
    bool is_const_ = false;
    immer::map<String, Export> env_;
    SourceRange range_;
};

#define DEFINE_ACCEPT_VISITOR                          \
    virtual void accept(BaseVisitor* visitor) override \
    {                                                  \
        visitor->visit(this);                          \
    }

// ---- Expression ------------------------------------------------------------

struct Expression : public AstNode {
    virtual ~Expression() = default;
};

struct AssignExpression : Expression {
    AssignExpression(Expression* lhs_, NssToken token, Expression* rhs_)
        : lhs{lhs_}
        , op{token}
        , rhs{rhs_}
    {
    }

    Expression* lhs = nullptr;
    NssToken op;
    Expression* rhs = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct BinaryExpression : Expression {
    BinaryExpression(
        Expression* lhs_,
        NssToken token,
        Expression* rhs_)
        : lhs{lhs_}
        , op{token}
        , rhs{rhs_}
    {
    }

    Expression* lhs = nullptr;
    NssToken op;
    Expression* rhs = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct ComparisonExpression : Expression {
    ComparisonExpression(
        Expression* lhs_,
        NssToken token,
        Expression* rhs_)
        : lhs{lhs_}
        , op{token}
        , rhs{rhs_}
    {
    }

    Expression* lhs = nullptr;
    NssToken op;
    Expression* rhs = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct ConditionalExpression : Expression {
    ConditionalExpression(
        Expression* expr_,
        Expression* true_branch_,
        Expression* false_branch_)
        : test{expr_}
        , true_branch{true_branch_}
        , false_branch{false_branch_}
    {
    }

    Expression* test = nullptr;
    Expression* true_branch = nullptr;
    Expression* false_branch = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct DotExpression : Expression {
    DotExpression(
        Expression* lhs_,
        NssToken token,
        Expression* rhs_)
        : lhs{lhs_}
        , dot{token}
        , rhs{rhs_}
    {
    }

    Expression* lhs = nullptr;
    NssToken dot;
    Expression* rhs = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct GroupingExpression : Expression {
    explicit GroupingExpression(Expression* expr_)
        : expr{expr_}
    {
    }

    Expression* expr = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct LiteralExpression : Expression {
    explicit LiteralExpression(NssToken token)
        : literal{token}
    {
    }

    NssToken literal;
    Variant<int32_t, float, PString, Location, ObjectID> data;

    DEFINE_ACCEPT_VISITOR
};

struct LiteralVectorExpression : Expression {
    explicit LiteralVectorExpression(NssToken x_, NssToken y_, NssToken z_)
        : x{x_}
        , y{y_}
        , z{z_}
    {
    }

    NssToken x, y, z;
    glm::vec3 data;

    DEFINE_ACCEPT_VISITOR
};

struct LogicalExpression : Expression {
    LogicalExpression(
        Expression* lhs_,
        NssToken token,
        Expression* rhs_)
        : lhs{lhs_}
        , op{token}
        , rhs{rhs_}
    {
    }

    Expression* lhs = nullptr;
    NssToken op;
    Expression* rhs = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct PostfixExpression : Expression {
    PostfixExpression(Expression* lhs_, NssToken token)
        : lhs{lhs_}
        , op{token}
    {
    }

    Expression* lhs = nullptr;
    NssToken op;

    DEFINE_ACCEPT_VISITOR
};

struct UnaryExpression : Expression {
    UnaryExpression(NssToken token, Expression* rhs_)
        : op{token}
        , rhs{rhs_}
    {
    }

    NssToken op;
    Expression* rhs = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct VariableExpression : Expression {
    explicit VariableExpression(NssToken token)
        : var{token}
    {
    }

    NssToken var;

    DEFINE_ACCEPT_VISITOR
};

struct CallExpression : Expression {
    explicit CallExpression(Expression* expr_, MemoryResource* allocator)
        : expr{expr_}
        , args{allocator}
        , comma_ranges{allocator}
    {
    }

    Expression* expr = nullptr;
    PVector<Expression*> args;
    SourceRange arg_range;
    PVector<SourceRange> comma_ranges; // This is probably stupid

    DEFINE_ACCEPT_VISITOR
};

struct EmptyExpression : Expression {
    DEFINE_ACCEPT_VISITOR
};

// ---- Statements ------------------------------------------------------------

struct Statement : public AstNode {
    virtual ~Statement() = default;
};

struct BlockStatement : public Statement {
    BlockStatement(MemoryResource* allocator)
        : nodes{allocator}
    {
    }

    BlockStatement(BlockStatement&) = delete;
    BlockStatement& operator=(const BlockStatement&) = delete;

    PVector<Statement*> nodes;

    DEFINE_ACCEPT_VISITOR
};

struct DoStatement : public Statement {
    Statement* block = nullptr;
    Expression* expr = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct EmptyStatement : public Statement {
    DEFINE_ACCEPT_VISITOR
};

struct ExprStatement : public Statement {
    Expression* expr = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct IfStatement : public Statement {
    Expression* expr = nullptr;
    Statement* if_branch = nullptr;
    Statement* else_branch = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct ForStatement : public Statement {
    AstNode* init = nullptr;
    Expression* check = nullptr;
    Expression* inc = nullptr;
    Statement* block = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct JumpStatement : public Statement {
    NssToken op;
    Expression* expr = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct LabelStatement : public Statement {
    NssToken type;
    Expression* expr = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct SwitchStatement : public Statement {
    Expression* target;
    Statement* block = nullptr;

    DEFINE_ACCEPT_VISITOR
};

struct WhileStatement : public Statement {
    Expression* check = nullptr;
    Statement* block = nullptr;

    DEFINE_ACCEPT_VISITOR
};

/// Contains type tokens
struct Type {
    NssToken type_qualifier; ///< `const`
    NssToken type_specifier; ///< `int`, `float`, `string`, etc
    NssToken struct_id;      // Only set if type_specifier if of type NssTokenType::STRUCT

    SourcePosition range_start() const noexcept
    {
        if (type_qualifier.type != NssTokenType::INVALID) {
            return type_qualifier.loc.range.start;
        } else {
            return type_specifier.loc.range.start;
        }
    }
};

struct Declaration : public Statement {
    Type type;
    SourceRange range_selection_;
    StringView view;

    virtual String identifier() const = 0;
    virtual SourceRange range() const noexcept;
    virtual SourceRange selection_range() const noexcept;
};

struct FunctionDecl : public Declaration {
    FunctionDecl(MemoryResource* allocator)
        : params{allocator}
    {
    }
    FunctionDecl(FunctionDecl&) = delete;
    FunctionDecl& operator=(const FunctionDecl&) = delete;

    NssToken identifier_;
    PVector<VarDecl*> params;

    virtual String identifier() const override { return String(identifier_.loc.view()); };

    DEFINE_ACCEPT_VISITOR
};

struct FunctionDefinition : public Declaration {
    FunctionDecl* decl_inline = nullptr;
    BlockStatement* block = nullptr;
    const FunctionDecl* decl_external = nullptr;

    virtual String identifier() const override { return String(decl_inline->identifier_.loc.view()); };

    DEFINE_ACCEPT_VISITOR
};

struct StructDecl : public Declaration {
    StructDecl(MemoryResource* allocator)
        : decls{allocator}
    {
    }

    PVector<Declaration*> decls;

    virtual String identifier() const override { return String(type.struct_id.loc.view()); };
    const VarDecl* locate_member_decl(StringView name) const;

    DEFINE_ACCEPT_VISITOR
};

struct VarDecl : public Declaration {
    NssToken identifier_;
    Expression* init = nullptr;

    virtual String identifier() const override { return String(identifier_.loc.view()); };

    DEFINE_ACCEPT_VISITOR
};

/// List of comma separated declarations
struct DeclList : public Declaration {
    DeclList(MemoryResource* allocator)
        : decls{allocator}
    {
    }

    PVector<VarDecl*> decls;

    virtual String identifier() const override
    {
        Vector<String> identifiers;
        for (const auto decl : decls) {
            identifiers.push_back(decl->identifier());
        }
        return string::join(identifiers);
    };

    const VarDecl* locate_decl(StringView name) const;

    DEFINE_ACCEPT_VISITOR
};

/// Abstracts an script include
struct Include {
    String resref;         ///< Resref of included script
    SourceRange location;  ///< Source location in script
    Nss* script = nullptr; ///< Loaded script
    int used = 0;          ///< Number of times include is used in script file
};

/// Abstracts a comment
struct Comment {

    void append(StringView comment, SourceLocation range)
    {
        if (comment_.empty()) {
            comment_ = String(comment);
            range_ = merge_source_location(range_, range);
        } else {
            comment_ = fmt::format("{}\n{}", comment_, comment);
            range_ = merge_source_location(range_, range);
        }
    }

    SourceLocation range_;
    String comment_;
};

struct Ast {
    Ast(Context* ctx);
    Ast(const Ast&) = delete;
    Ast(Ast&&) = default;
    Ast& operator=(const Ast&) = delete;
    Ast& operator=(Ast&&) = default;

    Context* ctx_;
    Vector<Statement*> decls;
    Vector<Include> includes;
    std::unordered_map<String, String> defines;
    Vector<Comment> comments;
    Vector<size_t> line_map;

    template <typename T, typename... Args>
    T* create_node(Args&&... args)
    {
        T* node = static_cast<T*>(ctx_->scope.alloc_obj<T>(std::forward<Args>(args)...));
        return node;
    }

    void accept(BaseVisitor* visitor)
    {
        visitor->visit(this);
    }

    /// Finds first comment that the source range of which ends on ``line`` or ``line`` - 1
    StringView find_comment(size_t line) const noexcept;
};

} // namespace nw::script
