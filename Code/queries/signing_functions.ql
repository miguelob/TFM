import javascript


from Expr e
where  e.getFile().getAbsolutePath() = "C:/Users/oleob/Downloads/test-dapp-main/src/index.js" 
and (e.mayHaveStringValue("eth_signTypedData")
or e.mayHaveStringValue("eth_signTypedData_v4")
or e.mayHaveStringValue("eth_signTypedData_v3")
or e.mayHaveStringValue("eth_sign")
or e.mayHaveStringValue("personal_sign")
)
select e as signing_methodes, e.getEnclosingFunction().getName() as function_name, e.getEnclosingFunction() as function, e.getEnclosingFunction().getLocation().getStartLine() as code_line




