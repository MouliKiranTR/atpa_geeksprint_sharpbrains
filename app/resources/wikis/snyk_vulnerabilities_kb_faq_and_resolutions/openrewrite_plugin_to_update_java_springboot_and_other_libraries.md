**Introduction**
As part of resolving the critical and high issues resulting from Snyk scans of checkpoint microservices, we often need to upgrade Java version, springboot version, hibernate version and/or many other dependent libraries. In most of the cases, the critical or high vulnerabilities will not be resolved unless a springboot upgrade is done which often requires to upgrade the Java version upgrade as well. In this document, we are going explore the ways to handle this upgrade of libraries and identify how OpenRewrite plugin can help us achieve this with better turn around time.

**What is OpenRewrite plugin?**
OpenRewrite is an open source automatic code refactoring plugin that can be used by the developers to eliminate technical debts in the source code more efficiently.

**One example as mentioned in their website-**
_One customer of OpenRewrite mentioned that, it would take them 7, 500 hours of developer time equivalent to one developer working 40 hour weeks for over three years replicate with the automated migration accomplished only in minutes._
  
**How does OpenRewrite work?**
The tool features an auto-refactoring engine that executes prepackaged, open-source recipes for tasks such as framework migrations, security updates, and maintaining stylistic consistency. This significantly reduces the time spent coding from hours or days to mere minutes. Additionally, build tool plugins like the OpenRewrite Gradle and Maven plugins enable you to apply these recipes to individual repositories efficiently.

Although the initial emphasis was on the Java language, the OpenRewrite community is actively broadening its support to include more languages and frameworks. OpenRewrite operates by altering Lossless Semantic Trees (LSTs) that represent your source code and then converting the modified trees back into source code. This allows you to review the changes and commit them as needed. The modifications to the LSTs are executed by Visitors, which are grouped into Recipes. OpenRewrite recipes ensure that changes to your source code are minimally invasive and maintain the original formatting. More in-depth understanding of the LST's are outside of the score of this document; however you can visit [this page]([Lossless Semantic Trees (LST) | OpenRewrite Docs](https://docs.openrewrite.org/concepts-and-explanations/lossless-semantic-trees)) to know more.

**Steps to use OpenRewrite on a project**
1. Clone the project you want to migrate to use newer versions of libraries.
2. After checking out your project, the next step is to integrate the OpenRewrite plugin with Maven or Gradle. To do this, follow the instructions provided in the Maven or Gradle tab.
If you are working on  maven project add a new `<plugin>` in the `<plugins>` section of your `pom.xml` file as follows -

 ```
 <plugin>  
 <groupId>org.openrewrite.maven</groupId>  
 <artifactId>rewrite-maven-plugin</artifactId>  
 <version>5.46.1</version>  
 </plugin>
 ```
To view a list of all available recipes for execution, run `mvn rewrite:discover` or `gradle rewriteDiscover` from the command line. Initially, this will display only the recipes that are built into OpenRewrite.

3. To run any recipes, update the plugin configuration to designate the desired recipe(s) as "active". If you want to upgrade your microservice to springboot 3.3 you will first need to activate the recipe. To activate this recipe, update your `pom.xml` file so that the sections you modified earlier resemble the example below:

```
<plugin>
  <groupId>org.openrewrite.maven</groupId>
  <artifactId>rewrite-maven-plugin</artifactId>
  <version>5.46.1</version>
  <configuration>
    <activeRecipes>
      <recipe>org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_3</recipe>
    </activeRecipes>
  </configuration>
</plugin>
```
4. With the UpgradeSpringBoot_3_3 recipe activated, you can run it by executing the following command:
`mvn rewrite:run`

After running it you will be notified of all the files that have been changed. To review the changes in the code, use `git diff` or your preferred IDE's diff viewer.

5. Some recipes, like org.openrewrite.java.ChangePackage, are more complex than OrderImports and require configuration in a `rewrite.yml` file to run. This particular built-in recipe has three options that need to be configured.

|Type| Name | Description |
|--|--|--|
| `String` | oldPackageName | The package name to replace. |
| `String` | newPackageName | New package name to replace the old package name with. |
| `Boolean` | recursive | _Optional_. Whether or not to recursively change subpackage names. | 

For more information on this, please [look into this]([Quickstart: Setting up your project and running recipes | OpenRewrite Docs](https://docs.openrewrite.org/running-recipes/getting-started#step-3-activate-a-recipe)).


Please have a look at this [PR in cp_history-service]([Update cp_history-service to java to version 17 and springboot to 3.3.6 with other updates to remediate Snyk vlnerabilities by TauhidIslamTR · Pull Request #9 · tr/cp_history-service](https://github.com/tr/cp_history-service/pull/9)) for which spring-boot, java and hibernate was upgraded where OpenRewrite provided an initial skeleton to work with. The developer would still have to do many changes to be compatible with all the dependent libraries, however, it provides a good starting point to build up and proceed toward upgrading.

![video-icon-8039.png](/.attachments/video-icon-8039-6073c71f-a194-4cd8-91a4-65933d8dcc3e.png)
Please watch Knowledge sharing session on [ How to use OpenRewrite tool to upgrade Java, SpringBoot and other libraries](https://trten.sharepoint.com/:v:/r/sites/TRTAKSCheckpointAnswers/Shared%20Documents/Team%20House%20Mormont/Recordings/OpenRewrite%20tool%20to%20upgrade%20Java,%20SpringBoot%20and%20other%20libraries%20(Islam%20Mohammad)%20-%2020241211.mp4?csf=1&web=1&e=cZSP9R) 