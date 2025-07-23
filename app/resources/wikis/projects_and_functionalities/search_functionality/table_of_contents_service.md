# Overview

Table of Contents consists of 1 DynamoDB table [a205159-cp-toc-dev-table-of-contents](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=a205159-cp-toc-dev-table-of-contents;tab=items) 

and 2 git repositories: 
- lambda for ingestion: https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-search-toc-ingestion-lambda
- lambdas for reading data: https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-search-toc-lambda

# DynamoDB table structure

- **Primary key** is made of **tocGuid** only.
- Index **ContentByParent** has a primary key of **tocGuid** of a parent node and a **tocGuid** - it's used for getting children of specific nodes.
- Index **ContentByEntryType** has a primary key of **tocEntryType** (**ROOT** or **CATEGORY_ROOT**) and **tocGuid** - it's used for retrieving nodes shown as roots on UI and could be used to retrieve the actual root node.

Exact table structure can be found in code: [TocEntryTableSchema](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-search-toc-ingestion-lambda?path=%2Fsrc%2Fmain%2Fjava%2Fcom%2Ftr%2Fcheckpoint%2Ftoc%2Frepository%2Fdynamodb%2FTocEntryTableSchema.java&version=GBmaster&line=39&lineEnd=40&lineStartColumn=1&lineEndColumn=1&lineStyle=plain)

# Environments

## Dev
- DynamoDB table: [a205159-cp-toc-dev-table-of-contents](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=a205159-cp-toc-dev-table-of-contents;tab=items)
- lambda handling ingestion from document metadata json file: [a205159-cp-search-toc-ingestion-lambda-test](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-search-toc-ingestion-lambda-test?tab=configuration)
- lambda returning root nodes: [a205159-cp-search-toc-get-roots-lambda-test](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-search-toc-get-roots-lambda-test?tab=configuration)
- lambda returning children of a specified node: [a205159-cp-search-toc-get-children-lambda-test](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-search-toc-get-children-lambda-test?tab=configuration)


