**Objective**
The objective of this document is to find out if as checkpoint developers we need to make any changes on our side in the code base to reflect the “Payroll Calculators Update”. This document specifically addresses the release by Symmetry on October 27, 2023 ([User Story 151729: Payroll Calculators Update - Boards (azure.com)](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/151729/)).

**Checkpoint usage of Payroll Calculator**
After logging into checkpoint the user can click on “More” drop down list beside the list of practice areas to select ‘Tools’. Selecting ‘Tools’ will take the user to a page having two subsections under calculator. The second subsection is ‘Payroll’ which corresponds to ‘Symmetry Calculator’.
In appBase.properties file, two properties are defined related to providing access to the Symmetry calculator-


```
#symmetry payroll calculators url
symmetry.calc.url=https://calculators.symmetry.com/widget/js/
symmetry.calc.key=***************************************
```
****

The url and key are used in the ‘`getCalculatorUrl(String calcId)`’ of `CPSymmetryViewBean.java` class. Also, in `CPSymmetryViewBean.java` class depending on the option chosen from the Payroll Calculators as shown in the image below five different popup urls can be loaded-
 

This popup url selection is performed in `payrollCalc.jsp` which in turn calls `getCalculatorPopupUrl(String calcId)`. However, in the whole process the .js used in displaying the calculator is provided in the url set up in the appBase.properties and checkpoint codebase is just referring to the js provided in the url. 

According to the findings so far (without logging into Symmetry Software [here](https://auth0.symmetry.com/login?state=hKFo2SBrcWRCd0ZfbWRSc2djekZtOGJwVnI0c3Vfa1FrbkVTY6FupWxvZ2luo3RpZNkgVER1bjNsQzhEZDJGU3RsWUhrTzRwR011dnAyb3l0Z3qjY2lk2SB4N2ZwbmJvd2ZqalFRWWVmM0tiNUhuYzVGdmZjUnhDdg&client=x7fpnbowfjjQQYef3Kb5Hnc5FvfcRxCv&protocol=samlp&RelayState=https%3A%2F%2Fsupport.symmetry.com%2Fhc%2Fen-us%2Farticles%2F20123362359828%3F_hsenc%3Dp2ANqtz-_JB7tn1HAVj_ZyaqgltrKcaz4JtzTJQTL9yzaLdFCuGajRk-GJO3NCucL46vTBimP4AfWinkPsNkc82Ejo18QnV4mfHjRwRdLXUapNGTZy2ODmT9I%26_hsmi%3D280194616%26utm_content%3D280194616%26utm_medium%3Demail%26utm_source%3Dhs_email&brand_id=360006805071&SAMLRequest=hZHNTsMwEITvfQrLdyd2FGhiNamiVkiRCkLl58DNdTZqRGwXr1Nanh41UKkc%0AgOvufJrZ2dn8YHqyB4%2BdswUVEafzcjJDZfqdrIawtWt4GwADOZjeohwXBR28%0AlU5hh9IqAyiDlg%2FV7UomEZc774LTrqcXyN%2BEQgQfOmcpqZcFPQGe8ZRvYAM5%0Ay7KsZWkzBZZftQ3TmRA5z1qhr1NKasQBaotB2VDQhCcp4wlL%2BKNIpcglFy%2BU%0APJ%2BvSyJOSXU2WziLgwH%2FAH7faXharwq6DWGHMo7xaAwEfxTpNIs%2BwDaAr5F2%0AJlZaA2J8ikjLsSY5RvDlf%2BgsvlR%2FN3ynDNTLe9d3%2BkiqvnfvCw8qQEGDH4CS%0AG%2BeNCr%2B3JyIxTrqGtaNUglFdXzWNB0Qal1%2BuP19ZTj4B%0A)), we do not need to perform any code changes from our side to realize the changes to payroll calculators. However, a look into the release notes may reveal something more complex that we estimate at this point.
