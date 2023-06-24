/**
 * @name signing_functions.ql
 * @kind expresion has string value
 * @description Find all signing methods and their functions
 * @id javascript/signing_functions
 */
import javascript


from Expr e
where  e.getFile().getAbsolutePath() = "C:/Users/oleob/Downloads/test-dapp-main/src/index.js" // Replace with your path or delete to search in all dabatase
and (e.mayHaveStringValue("eth_signTypedData")
or e.mayHaveStringValue("eth_signTypedData_v3")
or e.mayHaveStringValue("eth_sign")
or e.mayHaveStringValue("personal_sign")
)
select e as signing_methodes, e.getEnclosingFunction().getName() as function_name, e.getEnclosingFunction() as function, e.getEnclosingFunction().getLocation().getStartLine() as code_line




