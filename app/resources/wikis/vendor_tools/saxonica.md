# What does Saxonica Software do?

[Saxonica Site](https://www.saxonica.com/welcome/welcome.xml)
[Licenses](https://www.saxonica.com/license/licenses.xml)
[Documentation](https://www.saxonica.com/documentation12/documentation.xml)

# How is Saxonica used in Checkpoint?

## From 2023 

Here is a general note about the Saxonica vendor and what they provide to us. Saxonica provides a software development library which processes Checkpoint’s content retrieved by the application from Novus. The library is contained within the Checkpoint application and does not make any calls to the supplier. 

## From 10/2024

Saxon is used whenever a document is viewed inside of Checkpoint. It is also used in the content pipeline for document rendering. It is a core piece of Checkpoint’s solution. 

 

It was introduced with the Broadside/Catalyst project because it is faster and uses less memory than any other XML parser in the world. Catalyst documents where making Checkpoint throw Out of Memory exceptions and crash servers. Not only did I help Scott Nygren write a whole new document rendering engine just for Catalyst documents, but I was also responsible for implementing Saxon into the document rendering portions of Checkpoint. The solution required a combination of both the new doc rendering and Saxon. I spent months with other developers testing that all the different content types and all the content within them were rendered exactly as they were before moving to Saxon. We had massive, automated tests that rendered 10s of thousands of documents in both the new and the old rendering and comparing them both structurally and visually. 
 
If were to stop paying for Saxon we must stop using it. The work to remove Saxon would amount to about 1 year effort for 1 dev. The testing effort would be astronomical. 

 

## Sensitive/confidential data management

- Will this supplier have access in any form to TR or TR Customer sensitive or confidential information? No 
- Will this supplier/vendor have a direct network connection To or From the TR Network? No 
- Does this supplier provide operational support of a strategic TR Product? No 


 

 