import javascript
import semmle.javascript.RestrictedLocations

from Stmt s
where
  // `s` is unreachable in the CFG
  s.getFirstControlFlowNode().isUnreachable() and
  // the CFG does not model all possible exceptional control flow, so be conservative about catch clauses
  not s instanceof CatchClause and
  // function declarations are special and always reachable
  not s instanceof FunctionDeclStmt and
  // allow a spurious 'break' statement at the end of a switch-case
  not exists(Case c, int i | i = c.getNumBodyStmt() | s.(BreakStmt) = c.getBodyStmt(i - 1)) and
  // ignore ambient statements
  not s.isAmbient() and
  // ignore empty statements
  not s instanceof EmptyStmt and
  // ignore unreachable throws
  not s instanceof ThrowStmt and
  // Sets the query only to run on the specified file
  s.getFile().getAbsolutePath() = "C:/Users/oleob/Downloads/test-dapp-main/src/index.js"
select s.(FirstLineOf), "This statement is unreachable."
